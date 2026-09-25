"""
Lector de fuentes de datos para el pipeline de gobierno de datos.
Soporta extracción desde S3 y PostgreSQL con manejo de errores robusto
y registro de eventos para trazabilidad.
"""
import hashlib
import logging
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Optional

import boto3
import pandas as pd
import yaml
from botocore.exceptions import ClientError, BotoCoreError
from psycopg2 import OperationalError as Psycopg2OperationalError
from psycopg2.extras import RealDictCursor
from pydantic import BaseModel, Field, field_validator

logger = logging.getLogger(__name__)


class DataSourceConfig(BaseModel):
    """Configuración de una fuente de datos."""
    name: str = Field(..., description="Nombre único de la fuente de datos")
    type: str = Field(..., description="Tipo de fuente: s3, postgresql, mysql, etc.")
    connection_params: dict = Field(default_factory=dict, description="Parámetros de conexión")
    query_template: Optional[str] = Field(None, description="Template de consulta SQL")
    bucket: Optional[str] = Field(None, description="Bucket S3 para fuentes tipo s3")
    prefix: Optional[str] = Field(None, description="Prefijo en S3")
    file_format: str = Field("parquet", description="Formato de archivo: parquet, csv, json")
    partition_columns: list[str] = Field(default_factory=list, description="Columnas de partición")
    
    @field_validator('type')
    @classmethod
    def validate_type(cls, v: str) -> str:
        allowed = ['s3', 'postgresql', 'mysql', 'api', 'rest']
        if v not in allowed:
            raise ValueError(f"Tipo de fuente '{v}' no soportado. Usar: {allowed}")
        return v


class ExtractionEvent(BaseModel):
    """Evento de extracción registrado para trazabilidad."""
    source_name: str
    extraction_time: datetime
    record_count: int
    checksum: Optional[str]
    status: str
    error_message: Optional[str] = None
    execution_id: str


class DataSourceReader:
    """
    Lector de fuentes de datos con soporte para múltiples proveedores.
    Implementa patrón Strategy para diferentes tipos de fuentes.
    """
    
    def __init__(self, config_path: str = "conf/sources.yaml"):
        self.config_path = config_path
        self.sources: list[DataSourceConfig] = []
        self._load_config()
        self.execution_id = self._generate_execution_id()
        self.events: list[ExtractionEvent] = []
        
    def _load_config(self) -> None:
        """Carga configuración de fuentes desde archivo YAML."""
        try:
            with open(self.config_path, 'r') as f:
                config_data = yaml.safe_load(f)
                sources_data = config_data.get('sources', [])
                self.sources = [DataSourceConfig(**source) for source in sources_data]
                logger.info(f"Cargadas {len(self.sources)} fuentes de datos desde {self.config_path}")
        except FileNotFoundError:
            logger.warning(f"Archivo de configuración {self.config_path} no encontrado. Usando fuentes por defecto.")
            self._load_default_sources()
        except yaml.YAMLError as e:
            logger.error(f"Error parseando YAML: {e}")
            raise

    def _load_default_sources(self) -> None:
        """Carga fuentes por defecto si no existe configuración."""
        self.sources = [
            DataSourceConfig(
                name="customer_transactions",
                type="s3",
                bucket="datacorp-raw-data",
                prefix="transactions/",
                file_format="parquet",
                partition_columns=["year", "month"],
            ),
            DataSourceConfig(
                name="product_catalog",
                type="postgresql",
                connection_params={
                    "host": "datacorp-db.internal",
                    "database": "products",
                    "schema": "public",
                },
                query_template="SELECT * FROM product_catalog WHERE updated_at > '{{ last_run }}'",
            ),
        ]

    def _generate_execution_id(self) -> str:
        """Genera ID único para esta ejecución."""
        import uuid
        return str(uuid.uuid4())

    def discover_sources(self) -> list[dict]:
        """
        Descubre fuentes de datos disponibles.
        Returns:
            Lista de diccionarios con configuración de fuentes.
        """
        discovered = []
        for source in self.sources:
            discovered.append({
                'name': source.name,
                'type': source.type,
                'bucket': source.bucket,
                'prefix': source.prefix,
                'file_format': source.file_format,
                'partition_columns': source.partition_columns,
            })
            logger.info(f"Fuente descubierta: {source.name} ({source.type})")
        return discovered

    def read_source(self, source: dict, execution_date: datetime) -> Optional[pd.DataFrame]:
        """
        Lee datos de una fuente específica.
        
        Args:
            source: Diccionario con configuración de la fuente.
            execution_date: Fecha de ejecución del pipeline.
            
        Returns:
            DataFrame con los datos extraídos o None si hay error.
        """
        source_type = source.get('type')
        source_name = source.get('name')
        
        logger.info(f"Extrayendo datos de {source_name} (tipo: {source_type})")
        
        try:
            if source_type == 's3':
                data = self._read_from_s3(source, execution_date)
            elif source_type == 'postgresql':
                data = self._read_from_postgresql(source, execution_date)
            else:
                raise ValueError(f"Tipo de fuente no soportado: {source_type}")
            
            self._register_event(
                source_name=source_name,
                record_count=len(data) if data is not None else 0,
                status='SUCCESS',
            )
            
            return data
            
        except Exception as e:
            logger.error(f"Error extrayendo {source_name}: {str(e)}")
            self._register_event(
                source_name=source_name,
                record_count=0,
                status='FAILED',
                error_message=str(e),
            )
            raise

    def _read_from_s3(self, source: dict, execution_date: datetime) -> Optional[pd.DataFrame]:
        """Lee datos desde S3."""
        bucket = source.get('bucket')
        prefix = source.get('prefix', '')
        file_format = source.get('file_format', 'parquet')
        partition_cols = source.get('partition_columns', [])
        
        year = execution_date.year
        month = execution_date.month
        
        partition_prefix = f"year={year}/month={month:02d}/" if partition_cols else ""
        full_prefix = f"{prefix}{partition_prefix}"
        
        logger.info(f"Leyendo desde S3: bucket={bucket}, prefix={full_prefix}")
        
        try:
            s3_client = boto3.client('s3')
            response = s3_client.list_objects_v2(Bucket=bucket, Prefix=full_prefix)
            
            if 'Contents' not in response or len(response['Contents']) == 0:
                logger.warning(f"No se encontraron objetos en {bucket}/{full_prefix}")
                return pd.DataFrame()
            
            objects = response['Contents']
            logger.info(f"Encontrados {len(objects)} objetos en S3")
            
            dfs = []
            for obj in objects:
                key = obj['Key']
                if key.endswith('.parquet') or key.endswith('.snappy.parquet'):
                    try:
                        obj_url = f"s3://{bucket}/{key}"
                        df = pd.read_parquet(obj_url)
                        dfs.append(df)
                        logger.info(f"Leído {key}: {len(df)} registros")
                    except Exception as e:
                        logger.error(f"Error leyendo {key}: {e}")
                        continue
            
            if not dfs:
                return pd.DataFrame()
            
            result = pd.concat(dfs, ignore_index=True)
            logger.info(f"Total de registros extraídos de S3: {len(result)}")
            return result
            
        except (ClientError, BotoCoreError) as e:
            logger.error(f"Error de AWS al leer S3: {e}")
            raise

    def _read_from_postgresql(self, source: dict, execution_date: datetime) -> Optional[pd.DataFrame]:
        """Lee datos desde PostgreSQL."""
        connection_params = source.get('connection_params', {})
        query_template = source.get('query_template')
        
        host = connection_params.get('host', 'localhost')
        database = connection_params.get('database', 'postgres')
        schema = connection_params.get('schema', 'public')
        
        logger.info(f"Conectando a PostgreSQL: {host}/{database}.{schema}")
        
        try:
            import psycopg2
            conn = psycopg2.connect(
                host=connection_params.get('host'),
                port=connection_params.get('port', 5432),
                database=database,
                user=connection_params.get('user'),
                password=connection_params.get('password'),
            )
            
            query = query_template or f"SELECT * FROM {schema}.{source.get('name')} LIMIT 10000"
            query = query.replace('{{ last_run }}', (execution_date - timedelta(days=1)).isoformat())
            
            df = pd.read_sql(query, conn)
            conn.close()
            
            logger.info(f"Extraídos {len(df)} registros de PostgreSQL")
            return df
            
        except Psycopg2OperationalError as e:
            logger.error(f"Error de conexión a PostgreSQL: {e}")
            raise
        except Exception as e:
            logger.error(f"Error leyendo PostgreSQL: {e}")
            raise

    def calculate_checksum(self, data: Optional[pd.DataFrame]) -> Optional[str]:
        """
        Calcula checksum de los datos para verificar idempotencia.
        
        Args:
            data: DataFrame con los datos.
            
        Returns:
            Hash SHA-256 de los datos o None si no hay datos.
        """
        if data is None or data.empty:
            return None
        
        try:
            data_str = data.to_csv(index=False)
            checksum = hashlib.sha256(data_str.encode('utf-8')).hexdigest()
            logger.debug(f"Checksum calculado: {checksum[:16]}...")
            return checksum
        except Exception as e:
            logger.error(f"Error calculando checksum: {e}")
            return None

    def _register_event(
        self,
        source_name: str,
        record_count: int,
        status: str,
        error_message: Optional[str] = None,
    ) -> None:
        """
        Registra evento de extracción para trazabilidad.
        
        Args:
            source_name: Nombre de la fuente.
            record_count: Número de registros extraídos.
            status: Estado de la extracción (SUCCESS/FAILED).
            error_message: Mensaje de error si falló.
        """
        event = ExtractionEvent(
            source_name=source_name,
            extraction_time=datetime.utcnow(),
            record_count=record_count,
            checksum=None,
            status=status,
            error_message=error_message,
            execution_id=self.execution_id,
        )
        self.events.append(event)
        logger.info(f"Evento registrado: {source_name} - {status} - {record_count} registros")

    def get_extraction_summary(self) -> dict:
        """
        Obtiene resumen de la extracción actual.
        
        Returns:
            Diccionario con estadísticas de extracción.
        """
        total_records = sum(e.record_count for e in self.events)
        successful = sum(1 for e in self.events if e.status == 'SUCCESS')
        failed = sum(1 for e in self.events if e.status == 'FAILED')
        
        return {
            'execution_id': self.execution_id,
            'total_sources': len(self.events),
            'successful_extractions': successful,
            'failed_extractions': failed,
            'total_records': total_records,
        }