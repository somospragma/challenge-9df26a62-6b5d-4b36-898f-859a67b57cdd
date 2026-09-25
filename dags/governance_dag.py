"""
DAG de Airflow para el pipeline de gobierno de datos de DataCorp.
Orquesta las etapas de extracción, transformación, carga y governance
con dependencias explícitas y ventanas de ejecución configurables.
"""
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.operators.empty import EmptyOperator
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.utils.trigger_rule import TriggerRule
from airflow.models import Variable
import logging
import json

logger = logging.getLogger(__name__)

DEFAULT_ARGS = {
    'owner': 'data-engineering',
    'depends_on_past': False,
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
    'execution_timeout': timedelta(hours=2),
}

ENVIRONMENT = Variable.get('environment', default_var='dev')
ENABLE_DATA_QUALITY = Variable.get('enable_data_quality', default_var='true').lower() == 'true'
ENABLE_SCHEMA_EVOLUTION = Variable.get('enable_schema_evolution', default_var='true').lower() == 'true'


def extract_data_sources(**context):
    """Extrae datos de fuentes configuradas (S3 y PostgreSQL)."""
    from src.extract.data_source_reader import DataSourceReader
    
    execution_date = context['execution_date']
    run_id = context['run_id']
    
    logger.info(f"Iniciando extracción para ejecución {execution_date}, run_id: {run_id}")
    
    reader = DataSourceReader()
    sources = reader.discover_sources()
    
    extracted_data = {}
    for source in sources:
        try:
            data = reader.read_source(source, execution_date)
            extracted_data[source['name']] = {
                'record_count': len(data) if data is not None else 0,
                'checksum': reader.calculate_checksum(data) if data is not None else None,
                'source_type': source['type'],
            }
            logger.info(f"Extraídos {extracted_data[source['name']]['record_count']} registros de {source['name']}")
        except Exception as e:
            logger.error(f"Error extrayendo {source['name']}: {str(e)}")
            extracted_data[source['name']] = {
                'record_count': 0,
                'error': str(e),
                'source_type': source['type'],
            }
    
    context['task_instance'].xcom_push(key='extracted_data', value=extracted_data)
    context['task_instance'].xcom_push(key='sources', value=sources)
    
    return extracted_data


def validate_data_quality(**context):
    """Aplica reglas de calidad de datos a los datos extraídos."""
    from src.transform.data_quality_rules import DataQualityEngine
    
    extracted_data = context['task_instance'].xcom_pull(key='extracted_data')
    sources = context['task_instance'].xcom_pull(key='sources')
    
    logger.info(f"Validando calidad de {len(extracted_data)} fuentes")
    
    engine = DataQualityEngine()
    quality_results = {}
    
    for source_name, metadata in extracted_data.items():
        if metadata.get('error'):
            quality_results[source_name] = {
                'status': 'FAILED',
                'error': metadata['error'],
                'failed_checks': ['EXTRACTION_FAILED'],
            }
            continue
        
        source_config = next((s for s in sources if s['name'] == source_name), None)
        result = engine.run_quality_checks(source_name, source_config)
        quality_results[source_name] = result
        
        if result['status'] == 'FAILED':
            logger.warning(f"Calidad fallida para {source_name}: {result.get('failed_checks')}")
    
    context['task_instance'].xcom_push(key='quality_results', value=quality_results)
    
    failed_sources = [k for k, v in quality_results.items() if v['status'] == 'FAILED']
    return 'stop_pipeline' if failed_sources and not ENABLE_DATA_QUALITY else 'transform_data'


def transform_data(**context):
    """Aplica transformaciones y evolución de esquema a los datos."""
    from src.transform.schema_evolution import SchemaEvolutionManager
    
    extracted_data = context['task_instance'].xcom_pull(key='extracted_data')
    quality_results = context['task_instance'].xcom_pull(key='quality_results')
    sources = context['task_instance'].xcom_pull(key='sources')
    
    logger.info("Iniciando transformación de datos")
    
    schema_manager = SchemaEvolutionManager()
    transformed_data = {}
    
    for source_name, metadata in extracted_data.items():
        if metadata.get('error'):
            logger.warning(f"Omitiendo transformación para {source_name} por error en extracción")
            continue
        
        if quality_results.get(source_name, {}).get('status') == 'FAILED':
            logger.warning(f"Omitiendo transformación para {source_name} por falla en calidad")
            continue
        
        source_config = next((s for s in sources if s['name'] == source_name), None)
        
        if ENABLE_SCHEMA_EVOLUTION:
            evolved_schema = schema_manager.evolve_schema(source_name, source_config)
            transformed_data[source_name] = {
                'schema_version': evolved_schema['version'],
                'transformations_applied': evolved_schema.get('transformations', []),
            }
        else:
            transformed_data[source_name] = {
                'schema_version': '1.0.0',
                'transformations_applied': [],
            }
    
    context['task_instance'].xcom_push(key='transformed_data', value=transformed_data)
    
    return transformed_data


def load_to_sinks(**context):
    """Carga datos transformados a los destinos configurados."""
    from src.load.data_sink_writer import DataSinkWriter
    
    transformed_data = context['task_instance'].xcom_pull(key='transformed_data')
    extracted_data = context['task_instance'].xcom_pull(key='extracted_data')
    sources = context['task_instance'].xcom_pull(key='sources')
    run_id = context['run_id']
    execution_date = context['execution_date']
    
    logger.info(f"Cargando {len(transformed_data)} fuentes a destinos")
    
    writer = DataSinkWriter()
    load_results = {}
    
    for source_name, metadata in transformed_data.items():
        source_config = next((s for s in sources if s['name'] == source_name), None)
        original_metadata = extracted_data.get(source_name, {})
        
        idempotency_key = f"{source_name}_{execution_date.strftime('%Y%m%d')}"
        
        result = writer.write(
            source_name=source_name,
            data=original_metadata,
            config=source_config,
            idempotency_key=idempotency_key,
            run_id=run_id,
        )
        
        load_results[source_name] = result
        logger.info(f"Cargado {source_name}: {result.get('status')}")
    
    context['task_instance'].xcom_push(key='load_results', value=load_results)
    
    return load_results


def track_data_lineage(**context):
    """Registra el linaje de datos para trazabilidad completa."""
    from src.governance.data_lineage_tracker import DataLineageTracker
    
    extracted_data = context['task_instance'].xcom_pull(key='extracted_data')
    transformed_data = context['task_instance'].xcom_pull(key='transformed_data')
    load_results = context['task_instance'].xcom_pull(key='load_results')
    sources = context['task_instance'].xcom_pull(key='sources')
    run_id = context['run_id']
    execution_date = context['execution_date']
    
    logger.info("Registrando linaje de datos")
    
    tracker = DataLineageTracker()
    execution_uuid = tracker.generate_execution_uuid()
    
    lineage_records = []
    for source_name in extracted_data.keys():
        source_config = next((s for s in sources if s['name'] == source_name), None)
        
        record = {
            'execution_uuid': execution_uuid,
            'run_id': run_id,
            'execution_date': execution_date.isoformat(),
            'source_name': source_name,
            'source_type': source_config.get('type') if source_config else 'unknown',
            'stage': 'COMPLETE',
            'record_count': extracted_data[source_name].get('record_count', 0),
            'checksum': extracted_data[source_name].get('checksum'),
            'schema_version': transformed_data.get(source_name, {}).get('schema_version'),
            'load_status': load_results.get(source_name, {}).get('status'),
        }
        lineage_records.append(record)
    
    tracker.record_lineage(lineage_records)
    context['task_instance'].xcom_push(key='lineage_execution_uuid', value=execution_uuid)
    
    return execution_uuid


def apply_governance_policies(**context):
    """Aplica políticas de gobierno de datos configuradas."""
    from src.governance.governance_framework import GovernanceFramework
    
    lineage_uuid = context['task_instance'].xcom_pull(key='lineage_execution_uuid')
    load_results = context['task_instance'].xcom_pull(key='load_results')
    
    logger.info(f"Aplicando políticas de gobierno para ejecución {lineage_uuid}")
    
    framework = GovernanceFramework()
    policy_results = framework.enforce_policies(load_results)
    
    return policy_results


def stop_pipeline(**context):
    """Detiene el pipeline cuando las validaciones fallan."""
    logger.warning("Pipeline detenido por falla en validación de calidad")
    return 'Pipeline stopped'


def generate_governance_report(**context):
    """Genera reporte consolidado de la ejecución del pipeline."""
    import boto3
    
    quality_results = context['task_instance'].xcom_pull(key='quality_results')
    load_results = context['task_instance'].xcom_pull(key='load_results')
    lineage_uuid = context['task_instance'].xcom_pull(key='lineage_execution_uuid')
    execution_date = context['execution_date']
    
    report = {
        'execution_date': execution_date.isoformat(),
        'lineage_uuid': lineage_uuid,
        'quality_summary': {
            'total_sources': len(quality_results),
            'passed': sum(1 for r in quality_results.values() if r.get('status') == 'PASSED'),
            'failed': sum(1 for r in quality_results.values() if r.get('status') == 'FAILED'),
        },
        'load_summary': {
            'total_sinks': len(load_results),
            'successful': sum(1 for r in load_results.values() if r.get('status') == 'SUCCESS'),
            'failed': sum(1 for r in load_results.values() if r.get('status') == 'FAILED'),
        },
    }
    
    s3_hook = S3Hook('aws_default')
    report_key = f"governance/reports/{execution_date.strftime('%Y/%m/%d')}/report_{lineage_uuid}.json"
    s3_hook.load_string(
        string_data=json.dumps(report, indent=2),
        key=report_key,
        bucket_name=Variable.get('governance_reports_bucket', default_var='datacorp-governance-reports'),
    )
    
    logger.info(f"Reporte generado: {report_key}")
    
    return report


with DAG(
    dag_id='data_governance_pipeline',
    default_args=DEFAULT_ARGS,
    description='Pipeline de gobierno de datos para DataCorp basado en estándares DAMA, TOGAF y CMMI',
    schedule_interval='0 2 * * *',
    start_date=datetime(2024, 1, 1),
    catchup=False,
    max_active_runs=1,
    tags=['governance', 'data-quality', 'lineage', 'etl'],
    params={
        'environment': ENVIRONMENT,
        'enable_data_quality': ENABLE_DATA_QUALITY,
        'enable_schema_evolution': ENABLE_SCHEMA_EVOLUTION,
    },
) as dag:
    
    start = EmptyOperator(task_id='start', trigger_rule=TriggerRule.ALL_SUCCESS)
    
    extract_task = PythonOperator(
        task_id='extract_data_sources',
        python_callable=extract_data_sources,
        provide_context=True,
    )
    
    branch_quality = BranchPythonOperator(
        task_id='branch_on_quality',
        python_callable=validate_data_quality,
        provide_context=True,
    )
    
    stop_task = PythonOperator(
        task_id='stop_pipeline',
        python_callable=stop_pipeline,
        provide_context=True,
        trigger_rule=TriggerRule.ALL_DONE,
    )
    
    transform_task = PythonOperator(
        task_id='transform_data',
        python_callable=transform_data,
        provide_context=True,
    )
    
    load_task = PythonOperator(
        task_id='load_to_sinks',
        python_callable=load_to_sinks,
        provide_context=True,
    )
    
    lineage_task = PythonOperator(
        task_id='track_data_lineage',
        python_callable=track_data_lineage,
        provide_context=True,
    )
    
    governance_task = PythonOperator(
        task_id='apply_governance_policies',
        python_callable=apply_governance_policies,
        provide_context=True,
    )
    
    report_task = PythonOperator(
        task_id='generate_governance_report',
        python_callable=generate_governance_report,
        provide_context=True,
        trigger_rule=TriggerRule.ALWAYS,
    )
    
    end = EmptyOperator(
        task_id='end',
        trigger_rule=TriggerRule.NONE_FAILED_MIN_ONE_SUCCESS,
    )
    
    start >> extract_task >> branch_quality
    branch_quality >> stop_task >> end
    branch_quality >> transform_task >> load_task >> lineage_task >> governance_task >> report_task >> end