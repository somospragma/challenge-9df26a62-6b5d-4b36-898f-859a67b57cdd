# Prompt para Mejorar el Codigo Base

Copia y pega el contenido del bloque de abajo en un asistente de IA (Claude, ChatGPT)
para obtener un ZIP con el proyecto completo y arrancable.

Si preferis trabajar en tu editor con un agente local (Claude Code, Cursor, Copilot), usa `AGENTS.md` en vez de este archivo: dice lo mismo pero para que escriba los archivos en disco.

## Las dos reglas que no se negocian

1. **Completa el boilerplate.** Todo lo que el proyecto necesita para compilar y arrancar: manifiesto de dependencias, punto de entrada, configuracion, capa de interfaz, y las capas del patron arquitectonico declarado. Eso es andamiaje y es tu trabajo.
2. **NO resuelvas el reto.** Los entregables de las fases son el trabajo de la persona. El hueco pedagogico se deja como esta: el proyecto arranca, pero lo que el reto pide implementar NO esta implementado.

Dicho de otra forma: si algo impide compilar, arreglalo. Si algo es logica de negocio incompleta, validaciones ausentes, un secreto hardcodeado o un patron mejorable, dejalo exactamente como esta — es lo que la persona tiene que encontrar.

## Lo que le falta a este proyecto

Esto NO lo tenes que adivinar: salio de comparar el proyecto contra la arquitectura declarada del reto y de un analisis estatico del codigo. Completalo TODO.

### Archivos que la arquitectura del reto declara y no estan

Creálos con implementacion real, en la capa que les corresponde:

- `src/transform/data_quality_rules.py`
- `src/transform/schema_evolution.py`
- `src/load/data_sink_writer.py`
- `src/governance/governance_framework.py`

### Referencias colgando en el codigo que si esta

Cada una rompe la compilacion:

- `dags/governance_dag.py` — `DataLineageTracker.items`: Se invoca `items` sobre `DataLineageTracker`, pero esa clase no declara ese metodo. Agregalo con su implementacion real, o usa uno de los que si declara.
- `dags/governance_dag.py` — `DataLineageTracker.get`: Se invoca `get` sobre `DataLineageTracker`, pero esa clase no declara ese metodo. Agregalo con su implementacion real, o usa uno de los que si declara.
- `dags/governance_dag.py` — `DataSourceReader.strftime`: Se invoca `strftime` sobre `DataSourceReader`, pero esa clase no declara ese metodo. Agregalo con su implementacion real, o usa uno de los que si declara.
- `dags/governance_dag.py` — `DataLineageTracker.keys`: Se invoca `keys` sobre `DataLineageTracker`, pero esa clase no declara ese metodo. Agregalo con su implementacion real, o usa uno de los que si declara.
- `dags/governance_dag.py` — `DataSourceReader.isoformat`: Se invoca `isoformat` sobre `DataSourceReader`, pero esa clase no declara ese metodo. Agregalo con su implementacion real, o usa uno de los que si declara.

## Como saber que terminaste

```bash
pip install -r requirements.txt && pytest -q
```

Ese comando corriendo sin errores es la definicion de "listo".

---

```
## Briefing del reto (autoridad)
Este bloque manda sobre los archivos adjuntos. El stack y el rol salen de AQUÍ, no de un topic genérico ni de markdown placeholder.

### Perfil
Chapter Ciencia de Datos, Especialidad Ingeniero de Datos, Tecnología Gobierno de Datos, Master

### Brecha de conocimiento
Gestiona proyectos de mediana complejidad de Gobierno de Datos a través de marcos de trabajo como los propuestos en DAMA, TOGAF, CMMI

### Misión / candidato
Candidato con experiencia senior en ingeniería de datos

### Reto
- Tema: implementación de gobierno de datos
- Seniority: master-l3
- Tipo: practical
- Título: Diseño y Evaluación de un Marco de Gobierno de Datos
- Tiempo estimado: 15 horas

### Fases (trabajo del HUMANO — PROHIBIDO completarlas)
No implementes estos entregables. Dejalos como hueco pedagógico. El asistente solo materializa el proyecto arrancable para que el participante pueda trabajar.
- Fase 1: Exploración del Dominio — objetivo: Identificar y documentar las necesidades y restricciones del dominio de gobierno de datos en DataCorp. — entregable (NO resolver): Documento que detalla las necesidades y restricciones del dominio de gobierno de datos en DataCorp.
- Fase 2: Evaluación de Decisiones de Diseño — objetivo: Evaluar y documentar una decisión controversial en el diseño del marco de gobierno de datos. — entregable (NO resolver): Registro de decisiones que detalla una decisión controversial en el diseño del marco de gobierno de datos.
- Fase 3: Comunicación a Diferentes Audiencias — objetivo: Comunicar el marco de gobierno de datos a audiencias con diferentes niveles de abstracción. — entregable (NO resolver): Dos presentaciones: una técnica para el equipo de ingeniería y una de alto nivel para la dirección ejecutiva.
- Fase 4: Revisión y Optimización — objetivo: Revisar y optimizar el marco de gobierno de datos basado en retroalimentación y mejores prácticas. — entregable (NO resolver): Documento que detalla las mejoras propuestas y las justificaciones para el marco de gobierno de datos.

Eres un asistente experto en análisis, corrección y generación de archivos de cualquier tipo:
código fuente, documentación, hojas de cálculo, documentos Word, configuraciones, entre otros.
Voy a enviarte una cadena de texto que contiene uno o más archivos. Cada archivo está delimitado por un marcador con el siguiente formato:
// === ARCHIVO: ruta/del/archivo.extension ===
o también puede aparecer como:
## === ARCHIVO: ruta/del/archivo.extension ===
Lo que sigue al marcador puede ser:

El contenido real del archivo (código, texto, YAML, etc.)
Una descripción en lenguaje natural de lo que debe contener el archivo


TU TAREA
PASO 0 — ¿Esto es un proyecto o una carcasa?
Antes de extraer archivos, leé el Briefing (si está) y diagnosticá el adjunto.

Es CARCASA si ocurre CUALQUIERA de estas:
- No hay manifiesto de dependencias del stack del briefing (manifest.json de VTEX IO / package.json / pom.xml / build.gradle / requirements.txt / go.mod / *.tf / *.csproj, según corresponda)
- Hay un "binario" que en realidad es un comentario ("no puede ser mostrado como texto plano", placeholder .fig/.docx vacío)
- Los markdowns ya completan entregables de fases posteriores ("se implementó fade-in", lista de áreas ya resuelta)

Si es CARCASA:
- MATERIALIZÁ un proyecto que arranca en el stack del briefing (VTEX IO Store Framework, Angular, Terraform, pytest, Nest, etc.). Incluí manifiesto, punto de entrada y capa de interfaz reales.
- NO copies los markdowns de "solución" como si fueran el producto. Son ruido de generación.
- NO resuelvas las fases del briefing (están marcadas PROHIBIDO). Dejá el hueco pedagógico: el flujo existe, las microinteracciones/calidad/infra que el reto pide NO están hechas.
- Después seguí al PASO 5 (ZIP).

Si es un proyecto REAL (manifiesto + código que compila o arranca):
- Seguí PASO 1 en adelante. 🔴 compilación sí. 🟡 pedagógico no.

PASO 1 — Detección y extracción
Identifica todos los archivos presentes en la cadena. Para cada archivo extrae:

Su ruta completa (ej: src/main/java/com/pragma/Service.java)
Su contenido o descripción

PASO 2 — Clasificación por tipo
Clasifica cada archivo en una de estas categorías:
A) Código fuente (Java, Python, TypeScript, JavaScript, Kotlin, etc.)
B) Configuración / documentación (YAML, properties, Markdown, JSON, txt, etc.)
C) Excel (.xlsx, .xls, .csv)
D) Word (.docx, .doc)
E) Otro tipo de archivo binario o especial
PASO 3 — Clasificación de errores en código fuente

Objetivo prioritario: que el proyecto compile. No corrijas flujo de negocio ni lógica funcional.

Antes de modificar cualquier archivo de código fuente, clasifica cada problema encontrado en una de estas dos categorías:
🔴 ERROR DE COMPILACIÓN — corregir siempre
Son errores que impiden que el proyecto arranque, sin valor pedagógico:

Import faltante o incorrecto
Clase, método o variable referenciada que no existe en ningún archivo del proyecto
Error de sintaxis
Anotación con atributos inválidos
Dependencia ausente en pom.xml, package.json, etc.
Archivo referenciado que no existe y debe ser creado con implementación mínima

→ CORREGIR estos errores.
🟡 PROBLEMA FUNCIONAL O DE CALIDAD — preservar siempre
Son problemas que no impiden compilar. Pueden ser intencionales para el aprendizaje:

Clave secreta hardcodeada ("secret", "password123")
API deprecada que funciona pero tiene reemplazo moderno
Lógica de negocio incorrecta o incompleta
Código redundante o de baja legibilidad
Falta de validaciones en flujo de negocio
Patrones de diseño incorrectos pero funcionales
Concurrencia no segura
Configuración funcional pero no óptima

→ PRESERVAR tal cual. No corregir, no mejorar, no comentar.
PASO 4 — Procesamiento según tipo de archivo
Tipo A — Código fuente
Aplica únicamente las correcciones clasificadas como 🔴 ERROR DE COMPILACIÓN.
No alteres ningún elemento clasificado como 🟡 PROBLEMA FUNCIONAL O DE CALIDAD.
Si falta un archivo referenciado, créalo con la implementación mínima necesaria para compilar.
Tipo B — Configuración / documentación
Extrae el contenido tal cual, sin modificaciones salvo errores evidentes de sintaxis
(ej: YAML mal indentado).
Tipo C — Excel (.xlsx)
Si viene con contenido real, genera el archivo respetando ese contenido.
Si viene con descripción en lenguaje natural, genera un archivo Excel funcional con:

Fila de encabezados en negrita con color de fondo distintivo
Columnas con ancho ajustado al contenido
Tipos de dato correctos por columna
Validaciones si la descripción lo indica
Hojas nombradas descriptivamente si hay más de una
Filas de ejemplo si no hay datos reales

Tipo D — Word (.docx)
Si viene con contenido real, genera el archivo respetando ese contenido.
Si viene con descripción en lenguaje natural, genera un documento Word funcional con:

Estilos de título (Título 1, Título 2) para jerarquía de secciones
Fuente legible (Calibri o equivalente), tamaño 11-12pt para cuerpo
Márgenes estándar
Tabla de contenido si tiene múltiples secciones
Tablas con encabezados en negrita si aplica

Tipo E — Otro
Genera el archivo con el contenido o estructura más apropiada según la descripción.
PASO 5 — Exportación en ZIP
Empaqueta todos los archivos en un único archivo ZIP descargable respetando exactamente
la estructura de rutas indicada por los marcadores.
El ZIP debe incluir:

Archivos de código con únicamente los errores de compilación corregidos
Archivos de configuración y documentación sin cambios
Archivos nuevos creados para resolver dependencias de compilación faltantes
Archivos Excel y Word generados desde descripción

IMPORTANTE: El ZIP debe estar listo para descargar al finalizar. No preguntes si el usuario
quiere generarlo. Simplemente genera el archivo y proporciona el enlace de descarga; No debes desplegar en el chat el resumen de lo que arreglaste al Zip, solo entregalo.

REGLAS IMPORTANTES

No omitas ningún archivo aunque no tenga errores ni modificaciones
Respeta los nombres y rutas exactas indicadas por los marcadores
Si un archivo no tiene marcador claro, infiere el nombre desde su contenido
Si la cadena contiene solo documentación, placeholders o binarios fake, NO la reproduzcas:
aplicá PASO 0 (materializar el proyecto del briefing). Reproducir la carcasa es un fallo.
No agregues texto después del enlace de descarga del ZIP
No preguntes si el usuario quiere el ZIP: simplemente generalo siempre
Si detectas que falta un archivo de configuración necesario para compilar
(pom.xml, package.json, requirements.txt, build.gradle, etc.), créalo e inclúyelo
inferiendo su contenido desde los imports y frameworks detectados en el código
Nunca corrijas problemas 🟡 aunque parezcan obvios o fáciles de mejorar.
El participante que recibirá este proyecto los debe encontrar y resolver él mismo.


INPUT
Aquí está la cadena con los archivos:

// === ARCHIVO: pyproject.toml ===
[tool.poetry]
name = "data-governance-framework"
version = "0.1.0"
description = "Marco de gobierno de datos para DataCorp basado en estándares DAMA, TOGAF y CMMI"
authors = ["Data Engineering Team <data-engineering@datacorp.com>"]
license = "MIT"
readme = "README.md"
packages = [
    { include = "src" },
    { include = "dags" },
    { include = "conf" }
]

[tool.poetry.dependencies]
python = "^3.13"
apache-airflow = "2.9.0"
pydantic = "2.7.1"
pandas = "2.2.2"
pyspark = "3.5.0"
boto3 = "1.34.80"
pyyaml = "6.0.1"
apache-airflow-providers-amazon = "8.18.0"

[tool.poetry.group.test.dependencies]
pytest = "8.1.1"
pytest-cov = "5.0.0"

[build-system]
requires = ["poetry-core>=1.0.0"]
build-backend = "poetry.core.masonry.api"

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = "test_*.py"
addopts = "-v --cov=src --cov-report=term-missing"

[tool.black]
line-length = 88
target-version = ['py313']
include = '\.pyi?$'
extend-exclude = '''
/(
  | \.eggs
  | \.git
  | \.hg
  | \.mypy_cache
  | \.tox
  | \.venv
  | _build
  | buck-out
  | build
  | dist
)/
'''

[tool.isort]
profile = "black"
multi_line_output = 3
include_trailing_comma = true
force_grid_wrap = 0
use_parentheses = true
ensure_newline_before_comments = true
line_length = 88

[tool.flake8]
max-line-length = 88
extend-ignore = "E203"
exclude = ".git,__pycache__,build,dist,.venv"

[tool.mypy]
python_version = "3.13"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
disallow_incomplete_defs = true
check_untyped_defs = true
disallow_untyped_decorators = true
no_implicit_optional = true
warn_redundant_casts = true
warn_unused_ignores = true
warn_no_return = true
warn_unreachable = true
strict_equality = true

// === ARCHIVO: dags/governance_dag.py ===
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

// === ARCHIVO: src/extract/data_source_reader.py ===
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

// === ARCHIVO: src/governance/data_lineage_tracker.py ===
from __future__ import annotations

import uuid
from datetime import datetime
from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, Field, ConfigDict


class TransformationType(str, Enum):
    EXTRACT = "extract"
    TRANSFORM = "transform"
    LOAD = "load"
    FILTER = "filter"
    AGGREGATE = "aggregate"
    JOIN = "join"
    VALIDATE = "validate"
    ENRICH = "enrich"
    CLEAN = "clean"
    MASK = "mask"


class DataAssetType(str, Enum):
    TABLE = "table"
    FILE = "file"
    STREAM = "stream"
    VIEW = "view"
    DATASET = "dataset"


class DataNode(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    node_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    asset_type: DataAssetType
    source_system: Optional[str] = None
    schema_definition: Optional[dict[str, Any]] = None
    partition_columns: Optional[list[str]] = None
    storage_location: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    metadata: dict[str, Any] = Field(default_factory=dict)


class DataTransformation(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    transformation_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    transformation_type: TransformationType
    source_nodes: list[str] = Field(default_factory=list)
    target_node: str
    transformation_logic: str
    transformation_params: dict[str, Any] = Field(default_factory=dict)
    executed_by: Optional[str] = None
    execution_id: Optional[str] = None
    execution_timestamp: Optional[datetime] = None
    checksum: Optional[str] = None
    status: str = "pending"
    error_message: Optional[str] = None
    duration_ms: Optional[int] = None


class DataLineageEdge(BaseModel):
    edge_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    source_node_id: str
    target_node_id: str
    transformation_id: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    is_active: bool = True


class LineageGraph(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    graph_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    nodes: dict[str, DataNode] = Field(default_factory=dict)
    transformations: dict[str, DataTransformation] = Field(default_factory=dict)
    edges: dict[str, DataLineageEdge] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class DataLineageTracker:
    def __init__(self):
        self.graphs: dict[str, LineageGraph] = {}
        self._active_graph: Optional[LineageGraph] = None

    def create_graph(self, graph_name: str) -> LineageGraph:
        graph = LineageGraph()
        self.graphs[graph.graph_id] = graph
        self._active_graph = graph
        return graph

    def get_or_create_graph(self, graph_id: Optional[str] = None) -> LineageGraph:
        if graph_id and graph_id in self.graphs:
            self._active_graph = self.graphs[graph_id]
            return self._active_graph
        return self.create_graph(f"graph_{graph_id or len(self.graphs)}")

    def register_node(
        self,
        name: str,
        asset_type: DataAssetType,
        source_system: Optional[str] = None,
        schema_definition: Optional[dict[str, Any]] = None,
        partition_columns: Optional[list[str]] = None,
        storage_location: Optional[str] = None,
        metadata: Optional[dict[str, Any]] = None,
    ) -> DataNode:
        if self._active_graph is None:
            self.get_or_create_graph()

        node = DataNode(
            name=name,
            asset_type=asset_type,
            source_system=source_system,
            schema_definition=schema_definition,
            partition_columns=partition_columns,
            storage_location=storage_location,
            metadata=metadata or {},
        )
        self._active_graph.nodes[node.node_id] = node
        return node

    def register_transformation(
        self,
        transformation_type: TransformationType,
        source_node_ids: list[str],
        target_node_id: str,
        transformation_logic: str,
        transformation_params: Optional[dict[str, Any]] = None,
        executed_by: Optional[str] = None,
        execution_id: Optional[str] = None,
    ) -> DataTransformation:
        if self._active_graph is None:
            raise ValueError("No active lineage graph. Create one first.")

        transformation = DataTransformation(
            transformation_type=transformation_type,
            source_nodes=source_node_ids,
            target_node=target_node_id,
            transformation_logic=transformation_logic,
            transformation_params=transformation_params or {},
            executed_by=executed_by,
            execution_id=execution_id,
        )
        self._active_graph.transformations[transformation.transformation_id] = transformation

        for source_id in source_node_ids:
            edge = DataLineageEdge(
                source_node_id=source_id,
                target_node_id=target_node_id,
                transformation_id=transformation.transformation_id,
            )
            self._active_graph.edges[edge.edge_id] = edge

        return transformation

    def mark_transformation_complete(
        self,
        transformation_id: str,
        status: str,
        checksum: Optional[str] = None,
        error_message: Optional[str] = None,
        duration_ms: Optional[int] = None,
    ) -> None:
        if self._active_graph is None:
            raise ValueError("No active lineage graph.")

        if transformation_id not in self._active_graph.transformations:
            raise KeyError(f"Transformation {transformation_id} not found.")

        transformation = self._active_graph.transformations[transformation_id]
        transformation.status = status
        transformation.execution_timestamp = datetime.utcnow()
        transformation.checksum = checksum
        transformation.error_message = error_message
        transformation.duration_ms = duration_ms

    def get_upstream_dependencies(self, node_id: str) -> list[DataNode]:
        if self._active_graph is None:
            return []

        visited = set()
        result = []
        stack = [node_id]

        while stack:
            current = stack.pop()
            if current in visited:
                continue
            visited.add(current)

            for edge in self._active_graph.edges.values():
                if edge.target_node_id == current and edge.is_active:
                    source_node = self._active_graph.nodes.get(edge.source_node_id)
                    if source_node and source_node.node_id not in visited:
                        result.append(source_node)
                        stack.append(source_node.node_id)

        return result

    def get_downstream_dependencies(self, node_id: str) -> list[DataNode]:
        if self._active_graph is None:
            return []

        visited = set()
        result = []
        stack = [node_id]

        while stack:
            current = stack.pop()
            if current in visited:
                continue
            visited.add(current)

            for edge in self._active_graph.edges.values():
                if edge.source_node_id == current and edge.is_active:
                    target_node = self._active_graph.nodes.get(edge.target_node_id)
                    if target_node and target_node.node_id not in visited:
                        result.append(target_node)
                        stack.append(target_node.node_id)

        return result

    def get_full_lineage_path(self, start_node_id: str, end_node_id: str) -> list[DataLineageEdge]:
        if self._active_graph is None:
            return []

        graph = self._active_graph.graph
        try:
            from collections import deque

            queue = deque([(start_node_id, [start_node_id])])
            visited = {start_node_id}

            while queue:
                current, path = queue.popleft()

                if current == end_node_id:
                    edges_path = []
                    for i in range(len(path) - 1):
                        for edge in self._active_graph.edges.values():
                            if edge.source_node_id == path[i] and edge.target_node_id == path[i + 1]:
                                edges_path.append(edge)
                                break
                    return edges_path

                for edge in self._active_graph.edges.values():
                    if edge.source_node_id == current and edge.is_active:
                        next_node = edge.target_node_id
                        if next_node not in visited:
                            visited.add(next_node)
                            queue.append((next_node, path + [next_node]))

            return []
        except ImportError:
            return []

    def export_lineage_metadata(self) -> dict[str, Any]:
        if self._active_graph is None:
            return {"graphs": []}

        return {
            "graph_id": self._active_graph.graph_id,
            "nodes": [
                {
                    "node_id": n.node_id,
                    "name": n.name,
                    "asset_type": n.asset_type.value,
                    "source_system": n.source_system,
                    "schema_definition": n.schema_definition,
                    "partition_columns": n.partition_columns,
                    "storage_location": n.storage_location,
                }
                for n in self._active_graph.nodes.values()
            ],
            "transformations": [
                {
                    "transformation_id": t.transformation_id,
                    "transformation_type": t.transformation_type.value,
                    "source_nodes": t.source_nodes,
                    "target_node": t.target_node,
                    "transformation_logic": t.transformation_logic,
                    "status": t.status,
                    "checksum": t.checksum,
                    "duration_ms": t.duration_ms,
                }
                for t in self._active_graph.transformations.values()
            ],
            "edge_count": len(self._active_graph.edges),
        }

    def get_active_graph(self) -> Optional[LineageGraph]:
        return self._active_graph

    def set_active_graph(self, graph_id: str) -> None:
        if graph_id in self.graphs:
            self._active_graph = self.graphs[graph_id]
        else:
            raise KeyError(f"Graph {graph_id} not found.")

    def calculate_data_quality_impact(self, transformation_id: str) -> dict[str, Any]:
        if self._active_graph is None:
            return {"error": "No active graph"}

        transformation = self._active_graph.transformations.get(transformation_id)
        if not transformation:
            return {"error": "Transformation not found"}

        source_nodes = [
            self._active_graph.nodes.get(sid)
            for sid in transformation.source_nodes
            if sid in self._active_graph.nodes
        ]
        target_node = self._active_graph.nodes.get(transformation.target_node)

        quality_score = 100.0
        if transformation.status == "failed":
            quality_score = 0.0
        elif transformation.error_message:
            quality_score = 50.0

        return {
            "transformation_id": transformation_id,
            "source_nodes_count": len(source_nodes),
            "target_node": target_node.name if target_node else None,
            "quality_score": quality_score,
            "has_errors": transformation.status == "failed",
            "duration_ms": transformation.duration_ms,
        }

    def get_data_flow_summary(self) -> dict[str, Any]:
        if self._active_graph is None:
            return {"error": "No active graph"}

        node_count = len(self._active_graph.nodes)
        transformation_count = len(self._active_graph.transformations)
        edge_count = len(self._active_graph.edges)

        by_type: dict[str, int] = {}
        for node in self._active_graph.nodes.values():
            at = node.asset_type.value
            by_type[at] = by_type.get(at, 0) + 1

        successful = sum(
            1 for t in self._active_graph.transformations.values() if t.status == "completed"
        )
        failed = sum(
            1 for t in self._active_graph.transformations.values() if t.status == "failed"
        )

        return {
            "total_nodes": node_count,
            "total_transformations": transformation_count,
            "total_edges": edge_count,
            "nodes_by_type": by_type,
            "transformations_successful": successful,
            "transformations_failed": failed,
            "success_rate": (successful / transformation_count * 100) if transformation_count > 0 else 0,
        }

// === ARCHIVO: tests/test_data_quality_rules.py ===
import pytest
import pandas as pd
import numpy as np
from decimal import Decimal
from datetime import datetime, date

from src.transform.data_quality_rules import (
    DataQualityRule,
    QualityThreshold,
    QualityResult,
    validate_completeness,
    validate_uniqueness,
    validate_consistency,
    validate_timeliness,
    run_quality_checks
)


class TestCompletenessRule:
    def test_completeness_passes_when_no_nulls(self):
        df = pd.DataFrame({
            'customer_id': ['C001', 'C002', 'C003'],
            'email': ['a@test.com', 'b@test.com', 'c@test.com'],
            'phone': ['123', '456', '789']
        })
        threshold = QualityThreshold(min_percentage=95.0)
        result = validate_completeness(df, 'email', threshold)
        assert result.passed is True
        assert result.score == 100.0

    def test_completeness_fails_when_below_threshold(self):
        df = pd.DataFrame({
            'customer_id': ['C001', 'C002', 'C003', 'C004', 'C005'],
            'email': ['a@test.com', None, 'c@test.com', None, 'e@test.com']
        })
        threshold = QualityThreshold(min_percentage=90.0)
        result = validate_completeness(df, 'email', threshold)
        assert result.passed is False
        assert result.score == 60.0

    def test_completeness_handles_empty_column(self):
        df = pd.DataFrame({'col': pd.Series(dtype='str')})
        threshold = QualityThreshold(min_percentage=95.0)
        result = validate_completeness(df, 'col', threshold)
        assert result.passed is False
        assert result.score == 0.0


class TestUniquenessRule:
    def test_uniqueness_passes_with_unique_values(self):
        df = pd.DataFrame({
            'id': [1, 2, 3, 4],
            'code': ['A', 'B', 'C', 'D']
        })
        threshold = QualityThreshold(min_percentage=95.0)
        result = validate_uniqueness(df, 'id', threshold)
        assert result.passed is True
        assert result.score == 100.0

    def test_uniqueness_fails_with_duplicates(self):
        df = pd.DataFrame({
            'id': [1, 2, 1, 3, 2],
            'code': ['A', 'B', 'A', 'C', 'B']
        })
        threshold = QualityThreshold(min_percentage=90.0)
        result = validate_uniqueness(df, 'id', threshold)
        assert result.passed is False
        assert result.score == 60.0

    def test_uniqueness_with_nulls_ignores_null_count(self):
        df = pd.DataFrame({
            'id': [1, 2, None, 3, None]
        })
        threshold = QualityThreshold(min_percentage=80.0)
        result = validate_uniqueness(df, 'id', threshold)
        assert result.passed is True


class TestConsistencyRule:
    def test_consistency_passes_for_valid_range(self):
        df = pd.DataFrame({
            'age': [25, 30, 35, 40, 45],
            'salary': [50000, 60000, 70000, 80000, 90000]
        })
        threshold = QualityThreshold(min_percentage=95.0)
        result = validate_consistency(df, 'age', min_value=18, max_value=65, threshold=threshold)
        assert result.passed is True
        assert result.score == 100.0

    def test_consistency_fails_for_invalid_values(self):n        df = pd.DataFrame({
            'age': [25, 150, 35, -5, 45]
        })
        threshold = QualityThreshold(min_percentage=90.0)
        result = validate_consistency(df, 'age', min_value=18, max_value=65, threshold=threshold)
        assert result.passed is False
        assert result.score == 60.0

    def test_consistency_with_regex_pattern(self):
        df = pd.DataFrame({
            'email': ['user@test.com', 'invalid', 'other@test.com', 'bad_format']
        })
        threshold = QualityThreshold(min_percentage=80.0)
        result = validate_consistency(
            df, 'email', 
            pattern=r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
            threshold=threshold
        )
        assert result.passed is False
        assert result.score == 50.0


class TestTimelinessRule:
    def test_timeliness_passes_with_recent_data(self):
        df = pd.DataFrame({
            'record_date': pd.to_datetime(['2024-01-01', '2024-01-02', '2024-01-03'])
        })
        threshold = QualityThreshold(min_percentage=95.0)
        reference_date = date(2024, 1, 5)
        result = validate_timeliness(df, 'record_date', max_days_old=7, reference_date=reference_date, threshold=threshold)
        assert result.passed is True
        assert result.score == 100.0

    def test_timeliness_fails_with_stale_data(self):
        df = pd.DataFrame({
            'record_date': pd.to_datetime(['2023-12-01', '2023-12-15', '2024-01-01'])
        })
        threshold = QualityThreshold(min_percentage=90.0)
        reference_date = date(2024, 1, 10)
        result = validate_timeliness(df, 'record_date', max_days_old=7, reference_date=reference_date, threshold=threshold)
        assert result.passed is False


class TestQualityResult:
    def test_quality_result_calculation(self):
        result = QualityResult(
            rule_name='test_rule',
            column_name='test_col',
            passed=True,
            score=95.5,
            total_records=100,
            valid_records=95,
            invalid_records=5,
            details={'threshold': 90.0}
        )
        assert result.passed is True
        assert result.score == 95.5
        assert result.total_records == 100

    def test_quality_result_to_dict(self):
        result = QualityResult(
            rule_name='test',
            column_name='col',
            passed=True,
            score=100.0,
            total_records=50,
            valid_records=50,
            invalid_records=0
        )
        result_dict = result.to_dict()
        assert isinstance(result_dict, dict)
        assert result_dict['rule_name'] == 'test'
        assert result_dict['score'] == 100.0


class TestRunQualityChecks:
    def test_run_multiple_rules(self):
        df = pd.DataFrame({
            'id': [1, 2, 3, 2],
            'email': ['a@test.com', None, 'c@test.com', 'd@test.com'],
            'age': [25, 35, 150, 45]
        })
        rules = [
            DataQualityRule(
                name='unique_ids',
                column='id',
                rule_type='uniqueness',
                threshold=QualityThreshold(min_percentage=90.0)
            ),
            DataQualityRule(
                name='complete_emails',
                column='email',
                rule_type='completeness',
                threshold=QualityThreshold(min_percentage=80.0)
            ),
            DataQualityRule(
                name='valid_ages',
                column='age',
                rule_type='consistency',
                threshold=QualityThreshold(min_percentage=90.0),
                params={'min_value': 0, 'max_value': 120}
            )
        ]
        results = run_quality_checks(df, rules)
        assert len(results) == 3
        assert any(r.passed for r in results)
        assert any(not r.passed for r in results)

    def test_run_quality_checks_returns_empty_for_empty_rules(self):
        df = pd.DataFrame({'col': [1, 2, 3]})
        results = run_quality_checks(df, [])
        assert results == []


class TestDataQualityRuleModel:
    def test_rule_creation_with_defaults(self):
        rule = DataQualityRule(
            name='test_rule',
            column='test_col',
            rule_type='completeness',
            threshold=QualityThreshold(min_percentage=95.0)
        )
        assert rule.name == 'test_rule'
        assert rule.column == 'test_col'
        assert rule.rule_type == 'completeness'
        assert rule.enabled is True

    def test_rule_with_custom_params(self):
        rule = DataQualityRule(
            name='age_check',
            column='age',
            rule_type='consistency',
            threshold=QualityThreshold(min_percentage=90.0),
            params={'min_value': 18, 'max_value': 65}
        )
        assert rule.params['min_value'] == 18
        assert rule.params['max_value'] == 65

// === ARCHIVO: tests/test_schema_evolution.py ===
import pytest
import pandas as pd
import json
from datetime import date, datetime
from decimal import Decimal
from typing import List, Dict, Any

from src.transform.schema_evolution import (
    SchemaVersion,
    SchemaField,
    SchemaEvolutionManager,
    detect_schema_changes,
    apply_schema_migration,
    validate_schema_compatibility,
    SchemaChangeType
)


class TestSchemaField:
    def test_field_creation(self):
        field = SchemaField(
            name='customer_id',
            data_type='string',
            nullable=False,
            description='Unique customer identifier'
        )
        assert field.name == 'customer_id'
        assert field.data_type == 'string'
        assert field.nullable is False

    def test_field_to_dict(self):
        field = SchemaField(
            name='amount',
            data_type='decimal',
            nullable=True,
            description='Transaction amount'
        )
        field_dict = field.to_dict()
        assert isinstance(field_dict, dict)
        assert field_dict['name'] == 'amount'
        assert field_dict['data_type'] == 'decimal'

    def test_field_from_dict(self):
        field_dict = {
            'name': 'status',
            'data_type': 'string',
            'nullable': False,
            'description': 'Record status'
        }
        field = SchemaField.from_dict(field_dict)
        assert field.name == 'status'
        assert field.data_type == 'string'


class TestSchemaVersion:
    def test_version_creation(self):
        version = SchemaVersion(
            version_number='1.0.0',
            fields=[
                SchemaField(name='id', data_type='int', nullable=False),
                SchemaField(name='name', data_type='string', nullable=True)
            ],
            created_at=datetime(2024, 1, 1),
            description='Initial schema'
        )
        assert version.version_number == '1.0.0'
        assert len(version.fields) == 2

    def test_version_comparison(self):
        v1 = SchemaVersion(version_number='1.0.0', fields=[])
        v2 = SchemaVersion(version_number='2.0.0', fields=[])
        assert v1 < v2

    def test_version_serialization(self):
        version = SchemaVersion(
            version_number='1.0.0',
            fields=[
                SchemaField(name='id', data_type='int', nullable=False)
            ],
            created_at=datetime(2024, 1, 15),
            description='Test schema'
        )
        serialized = version.to_dict()
        assert 'version_number' in serialized
        assert 'fields' in serialized
        restored = SchemaVersion.from_dict(serialized)
        assert restored.version_number == version.version_number


class TestDetectSchemaChanges:
    def test_detect_added_field(self):
        old_schema = SchemaVersion(
            version_number='1.0.0',
            fields=[
                SchemaField(name='id', data_type='int', nullable=False),
                SchemaField(name='name', data_type='string', nullable=True)
            ]
        )
        new_schema = SchemaVersion(
            version_number='1.1.0',
            fields=[
                SchemaField(name='id', data_type='int', nullable=False),
                SchemaField(name='name', data_type='string', nullable=True),
                SchemaField(name='email', data_type='string', nullable=True)
            ]
        )
        changes = detect_schema_changes(old_schema, new_schema)
        assert len(changes) == 1
        assert changes[0].change_type == SchemaChangeType.ADDED
        assert changes[0].field_name == 'email'

    def test_detect_removed_field(self):
        old_schema = SchemaVersion(
            version_number='1.0.0',
            fields=[
                SchemaField(name='id', data_type='int', nullable=False),
                SchemaField(name='deprecated_field', data_type='string', nullable=True)
            ]
        )
        new_schema = SchemaVersion(
            version_number='2.0.0',
            fields=[
                SchemaField(name='id', data_type='int', nullable=False)
            ]
        )
        changes = detect_schema_changes(old_schema, new_schema)
        assert len(changes) == 1
        assert changes[0].change_type == SchemaChangeType.REMOVED

    def test_detect_type_change(self):
        old_schema = SchemaVersion(
            version_number='1.0.0',
            fields=[
                SchemaField(name='amount', data_type='int', nullable=False)
            ]
        )
        new_schema = SchemaVersion(
            version_number='2.0.0',
            fields=[
                SchemaField(name='amount', data_type='decimal', nullable=False)
            ]
        )
        changes = detect_schema_changes(old_schema, new_schema)
        assert len(changes) == 1
        assert changes[0].change_type == SchemaChangeType.TYPE_CHANGED

    def test_detect_nullable_change(self):
        old_schema = SchemaVersion(
            version_number='1.0.0',
            fields=[
                SchemaField(name='phone', data_type='string', nullable=True)
            ]
        )
        new_schema = SchemaVersion(
            version_number='1.1.0',
            fields=[
                SchemaField(name='phone', data_type='string', nullable=False)
            ]
        )
        changes = detect_schema_changes(old_schema, new_schema)
        assert len(changes) == 1
        assert changes[0].change_type == SchemaChangeType.NULLABLE_CHANGED

    def test_no_changes_for_identical_schemas(self):
        fields = [SchemaField(name='id', data_type='int', nullable=False)]
        old_schema = SchemaVersion(version_number='1.0.0', fields=fields)
        new_schema = SchemaVersion(version_number='1.0.1', fields=fields)
        changes = detect_schema_changes(old_schema, new_schema)
        assert len(changes) == 0


class TestValidateSchemaCompatibility:
    def test_backward_compatible_addition(self):
        old_schema = SchemaVersion(version_number='1.0.0', fields=[])
        new_schema = SchemaVersion(
            version_number='1.1.0',
            fields=[SchemaField(name='new_field', data_type='string', nullable=True)]
        )
        is_compatible, issues = validate_schema_compatibility(old_schema, new_schema)
        assert is_compatible is True
        assert len(issues) == 0

    def test_not_backward_compatible_removal(self):
        old_schema = SchemaVersion(
            version_number='1.0.0',
            fields=[SchemaField(name='required_field', data_type='int', nullable=False)]
        )
        new_schema = SchemaVersion(version_number='2.0.0', fields=[])
        is_compatible, issues = validate_schema_compatibility(old_schema, new_schema)
        assert is_compatible is False
        assert len(issues) > 0

    def test_not_backward_compatible_type_change(self):
        old_schema = SchemaVersion(
            version_number='1.0.0',
            fields=[SchemaField(name='field', data_type='int', nullable=False)]
        )
        new_schema = SchemaVersion(
            version_number='2.0.0',
            fields=[SchemaField(name='field', data_type='string', nullable=False)]
        )
        is_compatible, issues = validate_schema_compatibility(old_schema, new_schema)
        assert is_compatible is False

    def test_nullable_to_not_nullable_breaking(self):
        old_schema = SchemaVersion(
            version_number='1.0.0',
            fields=[SchemaField(name='field', data_type='string', nullable=True)]
        )
        new_schema = SchemaVersion(
            version_number='2.0.0',
            fields=[SchemaField(name='field', data_type='string', nullable=False)]
        )
        is_compatible, issues = validate_schema_compatibility(old_schema, new_schema)
        assert is_compatible is False


class TestApplySchemaMigration:
    def test_migration_adds_default_values(self):
        old_schema = SchemaVersion(
            version_number='1.0.0',
            fields=[SchemaField(name='id', data_type='int', nullable=False)]
        )
        new_schema = SchemaVersion(
            version_number='1.1.0',
            fields=[
                SchemaField(name='id', data_type='int', nullable=False),
                SchemaField(name='status', data_type='string', nullable=True)
            ]
        )
        old_data = pd.DataFrame({'id': [1, 2, 3]})
        migrated_data = apply_schema_migration(old_data, old_schema, new_schema)
        assert 'status' in migrated_data.columns
        assert migrated_data['status'].isna().all()

    def test_migration_drops_removed_columns(self):
        old_schema = SchemaVersion(
            version_number='1.0.0',
            fields=[
                SchemaField(name='id', data_type='int', nullable=False),
                SchemaField(name='old_field', data_type='string', nullable=True)
            ]
        )
        new_schema = SchemaVersion(
            version_number='2.0.0',
            fields=[SchemaField(name='id', data_type='int', nullable=False)]
        )
        old_data = pd.DataFrame({'id': [1, 2], 'old_field': ['a', 'b']})
        migrated_data = apply_schema_migration(old_data, old_schema, new_schema)
        assert 'old_field' not in migrated_data.columns
        assert list(migrated_data.columns) == ['id']

    def test_migration_handles_type_conversion(self):
        old_schema = SchemaVersion(
            version_number='1.0.0',
            fields=[SchemaField(name='value', data_type='int', nullable=False)]
        )
        new_schema = SchemaVersion(
            version_number='2.0.0',
            fields=[SchemaField(name='value', data_type='float', nullable=False)]
        )
        old_data = pd.DataFrame({'value': [10, 20, 30]})
        migrated_data = apply_schema_migration(old_data, old_schema, new_schema)
        assert migrated_data['value'].dtype in [float, 'float64', 'float32']


class TestSchemaEvolutionManager:
    def test_manager_creation(self):
        manager = SchemaEvolutionManager()
        assert manager.get_current_version() is None
        assert len(manager.get_all_versions()) == 0

    def test_register_and_get_version(self):
        manager = SchemaEvolutionManager()
        schema = SchemaVersion(
            version_number='1.0.0',
            fields=[SchemaField(name='id', data_type='int', nullable=False)],
            created_at=datetime.now()
        )
        manager.register_version(schema)
        retrieved = manager.get_version('1.0.0')
        assert retrieved is not None
        assert retrieved.version_number == '1.0.0'

    def test_get_latest_version(self):
        manager = SchemaEvolutionManager()
        v1 = SchemaVersion(version_number='1.0.0', fields=[SchemaField(name='id', data_type='int', nullable=False)])
        v2 = SchemaVersion(version_number='2.0.0', fields=[SchemaField(name='id', data_type='int', nullable=False)])
        v3 = SchemaVersion(version_number='1.5.0', fields=[SchemaField(name='id', data_type='int', nullable=False)])
        manager.register_version(v1)
        manager.register_version(v2)
        manager.register_version(v3)
        latest = manager.get_latest_version()
        assert latest.version_number == '2.0.0'

    def test_migrate_between_versions(self):
        manager = SchemaEvolutionManager()
        v1 = SchemaVersion(
            version_number='1.0.0',
            fields=[SchemaField(name='id', data_type='int', nullable=False)]
        )
        v2 = SchemaVersion(
            version_number='2.0.0',
            fields=[
                SchemaField(name='id', data_type='int', nullable=False),
                SchemaField(name='name', data_type='string', nullable=True)
            ]
        )
        manager.register_version(v1)
        manager.register_version(v2)
        data = pd.DataFrame({'id': [1, 2, 3]})
        migrated = manager.migrate(data, '1.0.0', '2.0.0')
        assert 'name' in migrated.columns


class TestSchemaChangeType:
    def test_change_type_enum_values(self):
        assert SchemaChangeType.ADDED.value == 'added'
        assert SchemaChangeType.REMOVED.value == 'removed'
        assert SchemaChangeType.TYPE_CHANGED.value == 'type_changed'
        assert SchemaChangeType.NULLABLE_CHANGED.value == 'nullable_changed'
        assert SchemaChangeType.DESCRIPTION_CHANGED.value == 'description_changed'

// === ARCHIVO: conf/dev.yaml ===
environment: development

database:
  source:
    host: "localhost"
    port: 5432
    database: "datacorp_source"
    username: "etl_user"
    password_secret: "arn:aws:secretsmanager:us-east-1:123456789012:secret:db/source-password"
    pool_size: 10
    max_overflow: 20
    pool_timeout: 30
    connection_timeout: 60

  warehouse:
    host: "datacorp-warehouse.abc123.us-east-1.redshift.amazonaws.com"
    port: 5439
    database: "analytics_warehouse"
    username: "warehouse_user"
    password_secret: "arn:aws:secretsmanager:us-east-1:123456789012:secret:db/warehouse-password"
    iam_role: "arn:aws:iam::123456789012:role/RedshiftLoadRole"
    cluster_identifier: "datacorp-main-cluster"
    region: "us-east-1"

storage:
  raw_zone:
    bucket: "datacorp-dev-data-lake-raw"
    prefix: "raw/"
    format: "parquet"
    partitioning: [" ingestion_date=YYYY-MM-DD", "source_system"]
    compression: "snappy"

  trusted_zone:
    bucket: "datacorp-dev-data-lake-trusted"
    prefix: "trusted/"
    format: "parquet"
    partitioning: ["year=YYYY", "month=MM", "day=DD", "domain"]
    compression: "gzip"

  curated_zone:
    bucket: "datacorp-dev-data-lake-curated"
    prefix: "curated/"
    format: "parquet"
    partitioning: ["year=YYYY", "month=MM", "domain", "process_status"]
    compression: "zstd"

s3:
  region: "us-east-1"
  endpoint_url: null
  use_accelerate_endpoint: false
  max_pool_connections: 50
  timeout: 300

airflow:
  webserver_host: "localhost"
  webserver_port: 8080
  executor: "LocalExecutor"
  parallelism: 16
  dag_concurrency: 8
  max_active_runs_per_dag: 3
  load_examples: false
  base_url: "http://localhost:8080"
  
  connections:
    aws_default:
      conn_type: "aws"
      conn_id: "aws_default"
      login: "AKIAIOSFODNN7EXAMPLE"
      password_secret: "arn:aws:secretsmanager:us-east-1:123456789012:secret:aws/credentials"
    
    postgres_source:
      conn_type: "postgres"
      conn_id: "postgres_source"
      host: "localhost"
      schema: "datacorp_source"
      login: "etl_user"
      password_secret: "arn:aws:secretsmanager:us-east-1:123456789012:secret:db/source-password"
      port: 5432
    
    redshift_warehouse:
      conn_type: "redshift"
      conn_id: "redshift_warehouse"
      host: "datacorp-warehouse.abc123.us-east-1.redshift.amazonaws.com"
      schema: "analytics_warehouse"
      login: "warehouse_user"
      password_secret: "arn:aws:secretsmanager:us-east-1:123456789012:secret:db/warehouse-password"
      port: 5439

data_quality:
  enabled: true
  
  thresholds:
    completeness:
      critical: 99.0
      warning: 95.0
      block_on_failure: true
    
    uniqueness:
      critical: 98.0
      warning: 95.0
      block_on_failure: false
    
    consistency:
      critical: 98.0
      warning: 95.0
      block_on_failure: true
    
    timeliness:
      critical: 95.0
      warning: 90.0
      block_on_failure: false

  quarantine:
    enabled: true
    bucket: "datacorp-dev-data-lake-quarantine"
    prefix: "quarantine/"
    retention_days: 30
    notification_topic: "arn:aws:sns:us-east-1:123456789012:data-quality-alerts"

  rules:
    - name: "customer_id_not_null"
      table: "customers"
      column: "customer_id"
      rule_type: "completeness"
      threshold: 99.5
      enabled: true
    
    - name: "email_valid_format"
      table: "customers"
      column: "email"
      rule_type: "consistency"
      threshold: 98.0
      pattern: "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$"
      enabled: true
    
    - name: "transaction_amount_positive"
      table: "transactions"
      column: "amount"
      rule_type: "consistency"
      threshold: 99.0
      min_value: 0
      enabled: true
    
    - name: "order_date_not_future"
      table: "orders"
      column: "order_date"
      rule_type: "timeliness"
      threshold: 99.0
      max_days_in_future: 0
      enabled: true

schema_evolution:
  enabled: true
  
  catalog:
    type: "glue"
    database: "datacorp_dev_governance"
    region: "us-east-1"

  migration:
    auto_apply: false
    require_approval: true
    backup_before_migration: true
    backup_retention_days: 90

  compatibility_checks:
    block_on_breaking: true
    warn_on_add_optional: false
    warn_on_remove_optional: true

lineage:
  enabled: true
  
  tracker:
    type: "openlineage"
    backend: "s3"
    bucket: "datacorp-dev-lineage"
    prefix: "lineage/"
    
  capture:
    extract_dependencies: true
    transform_dependencies: true
    load_dependencies: true
    runtime_context: true

governance:
  framework:
    name: "DAMA-TOGAF-CMMi"
    version: "1.0.0"
    
  policies:
    data_classification:
      enabled: true
      levels:
        - name: "public"
          description: "Data that can be freely shared"
          color: "green"
        - name: "internal"
          description: "Data for internal use only"
          color: "blue"
        - name: "confidential"
          description: "Sensitive business data"
          color: "yellow"
        - name: "restricted"
          description: "Highly sensitive data requiring special handling"
          color: "red"
    
    retention:
      enabled: true
      default_policy:
        active_years: 7
        archive_years: 10
        deletion_requires_approval: true
      
      table_policies:
        - table: "transactions"
          active_years: 7
          archive_years: 10
        - table: "customer_pii"
          active_years: 5
          archive_years: 0
         pii: true
    
    access_control:
      enabled: true
      default_role: "read"
      require_approval_for_write: true
      require_approval_for_delete: true

  roles:
    - name: "data_steward"
      permissions: ["read", "write", "approve_quality_rules"]
      description: "Manages data quality and metadata"
    
    - name: "data_owner"
      permissions: ["read", "write", "delete", "manage_access", "manage_retention"]
      description: "Owns business domain data"
    
    - name: "etl_developer"
      permissions: ["read", "write"]
      description: "Builds and maintains ETL pipelines"

orchestration:
  dag_defaults:
    retries: 2
    retry_delay_minutes: 5
    execution_timeout_hours: 6
    depends_on_past: false
    wait_for_downstream: true
    
  scheduling:
    default_cron: "0 2 * * *"
    max_active_runs: 3
    
  notification:
    on_success: false
    on_failure: true
    on_retry: false
    channels:
      email:
        enabled: true
        recipients: ["data-eng@datacorp.com"]
      slack:
        enabled: false
        webhook_secret: "arn:aws:secretsmanager:us-east-1:123456789012:secret:slack/webhook"

monitoring:
  metrics:
    enabled: true
    export_to_cloudwatch: true
    
  alerts:
    pipeline_failure:
      enabled: true
      threshold_minutes: 60
      notification_topic: "arn:aws:sns:us-east-1:123456789012:data-pipeline-alerts"
    
    data_quality_failure:
      enabled: true
      threshold_count: 100
      notification_topic: "arn:aws:sns:us-east-1:123456789012:data-quality-alerts"
    
    schema_drift:
      enabled: true
      notification_topic: "arn:aws:sns:us-east-1:123456789012:schema-alerts"

logging:
  level: "INFO"
  format: "json"
  output: "cloudwatch"
  log_group: "/aws/datacorp/dev/airflow"
  
spark:
  version: "3.5.0"
  
  config:
    spark.sql.adaptive.enabled: true
    spark.sql.adaptive.coalescePartitions.enabled: true
    spark.sql.shuffle.partitions: 200
    spark.dynamicAllocation.enabled: true
    spark.dynamicAllocation.minExecutors: 1
    spark.dynamicAllocation.maxExecutors: 10
    spark.executor.memory: "4g"
    spark.executor.cores: 2
    spark.driver.memory: "2g"
    
  emr:
    cluster_id: "j-XXXXXXXXXXXXX"
    region: "us-east-1"
    log_uri: "s3://datacorp-dev-emr-logs/"
    
pipeline_defaults:
  batch_size: 10000
  max_parallel_tasks: 8
  checkpoint_enabled: true
  checkpoint_interval: 100
  
  performance:
    enable_broadcast: true
    broadcast_threshold_mb: 10
    enable_caching: true
    cache_level: "MEMORY_AND_DISK"

// === ARCHIVO: docs/necesidades_restricciones.md ===
# Necesidades y Restricciones del Dominio de Gobierno de Datos en DataCorp

## 1. Contexto Organizacional

DataCorp es una empresa de tamaño mediano que ha experimentado un crecimiento exponencial en el volumen de datos generados por sus operaciones. La dirección ha identificado que la falta de un marco estructurado de gobierno de datos está generando inconsistencias en los reportes, duplicidades en los procesos de extracción y una creciente dificultad para cumplir con las regulaciones de protección de datos.

El área de ingeniería de datos, compuesta por 12 profesionales distribuidos en tres equipos especializados (ingeniería de pipelines, calidad de datos y arquitectura), requiere un marco que permita escalar las operaciones sin comprometer la calidad ni la trazabilidad de los activos de datos.

## 2. Necesidades del Dominio

### 2.1 Calidad de Datos

La organización necesita implementar controles de calidad en múltiples niveles del pipeline ETL. Los datos proviene de fuentes heterogéneas incluyendo sistemas transaccionales legacy, APIs REST de proveedores externos y archivos CSV generados por procesos manuales de áreas de negocio. Cada fuente presenta desafíos específicos: los sistemas legacy carecen de claves naturales consistentes, las APIs tienen esquemas que evolucionan frecuentemente sin notificación previa, y los archivos manuales contienen valores inconsistentes que requieren normalización.

Las reglas de calidad deben ser ejecutables de forma automática en cada ejecución del pipeline, con capacidad de quarantine para registros que no cumplen los umbrales mínimos. El marco debe soportar la definición de reglas a nivel de columna (tipo de dato, rango de valores, obligatoriedad), a nivel de fila (combinaciones válidas entre columnas) y a nivel de conjunto (cardinalidad, distribución de valores, detección de duplicados).

### 2.2 Trazabilidad y Linaje

El equipo de auditoría requiere capacidad de rastrear el origen de cada dato desde su fuente original hasta su destino final en los data marts de consumo. Esta necesidad surge de requisitos regulatorios que exigen poder responder preguntas como: ¿de qué fuente proviene este valor? ¿qué transformaciones sufrió? ¿quién autorizó este cambio en las reglas de negocio?

El linaje debe capturar tanto el linaje técnico (qué proceso escribió qué dato) como el linaje de negocio (qué regla de negocio justificó cada transformación). El almacenamiento de metadatos de linaje debe ser persistente y consultable mediante APIs para integración con herramientas de visualización de的血缘关系.

### 2.3 Gestión de Esquemas

Los esquemas de datos evolucionan constantemente debido a la incorporación de nuevos atributos por parte de las áreas de negocio. El marco debe proporcionar un mecanismo de evolución de esquemas que permita versionar los esquemas, detectar cambios automáticamente y propagar estos cambios a los procesos dependientes con impacto mínimo.

La estrategia de evolución debe soportar tres escenarios: adición de nuevas columnas (backward compatible), renombrado de columnas (mediante alias para compatibilidad hacia atrás) y cambios de tipo de dato (solo cuando la conversión sea lossless).

### 2.4 Idempotencia y Reprocesamiento

Los pipelines deben ser idempotentes: una ejecución con los mismos datos de entrada debe producir exactamente el mismo resultado, independientemente del número de veces que se ejecute. Esto es crítico para garantizar consistencia en entornos de reprocesamiento donde es necesario regenerar datos históricos después de corregir bugs en las transformaciones.

La estrategia de idempotencia se basa en checksums calculados sobre los datos de entrada combined con timestamps de ejecución para detectar cambios. El sistema debe mantener un registro de ejecuciones que permita consultar qué datos fueron procesados en cada ejecución y su estado correspondiente.

## 3. Restricciones del Entorno

### 3.1 Restricciones Técnicas

La infraestructura actual está basada en AWS, utilizando S3 como data lake, Lambda para procesos serverless de bajo volumen y Step Functions para orquestación de workflows complejos. El volumen de datos proyectado para los próximos 18 meses alcanza los 50TB, con picos de procesamiento diario de 500GB. El marco debe optimizar costos de almacenamiento mediante formatos columnares (Parquet) y particionado estratégico por fecha y categoría de dato.

El equipo tiene experiencia consolidada en Python y PySpark, con conocimiento intermedio en Apache Airflow. Cualquier solución que requiera tecnologías completamente nuevas enfrentaría resistencia y prolongaría significativamente la curva de adopción.

### 3.2 Restricciones Regulatorias

DataCorp opera en industrias reguladas que imponen requisitos específicos sobre la retención y el procesamiento de datos personales. El marco debe facilitar el cumplimiento de solicitudes de eliminación de datos (derecho al olvido) mediante capacidades de soft-delete y la capacidad de identificar todos los lugares donde un dato personal específico está almacenado.

Los datos financieros deben mantener integridad transactional, lo que implica que las correcciones no pueden modificar registros históricos sino crear nuevos registros con referencia al original. Esta restricción tiene implicaciones directas en la estrategia de particionado y en el diseño de las claves de acceso.

### 3.3 Restricciones Organizacionales

El presupuesto aprobado para la iniciativa de gobierno de datos cubre la implementación inicial pero no permite licencias de herramientas comerciales de catálogo de datos o de calidad. El marco debe utilizar herramientas open source o capacidades nativas de los servicios AWS ya contratados.

El cambio organizacional debe ser gestionado con cuidado: muchas áreas de negocio perciben los controles de calidad como obstáculos que retrasan sus entregas. El marco debe proporcionar feedback rápido y accionable que permita a los usuarios corregir problemas en la fuente, no solo detectarlos.

## 4. Capacidades Requeridas del Marco

### 4.1 Orquestación de Pipelines

El marco debe definir una estructura clara de DAGs en Airflow que separe las responsabilidades de extracción, transformación y carga en tareas distintas. Cada tarea debe ser independiente y re-ejecutable en caso de fallo sin afectar las tareas anteriores ya completadas. Las dependencias entre tareas deben ser explícitas y configurables por entorno.

### 4.2 Configuración por Entorno

Los parámetros que varían entre entornos (dev, staging, production) deben estar centralizados en archivos de configuración YAML, sin硬编码 de valores en el código. Los secretos (credenciales de bases de datos, tokens de APIs) deben residir en AWS Secrets Manager y ser inyectados en tiempo de ejecución.

### 4.3 Métricas y Monitoreo

Cada pipeline debe exportar métricas de ejecución a CloudWatch: volumen de datos procesados, tiempo de ejecución, número de registros rechazados por calidad y porcentaje de completitud por fuente. Estas métricas alimentarán dashboards operativos y alertas automáticas cuando los valores se desvíen de los umbrales esperados.

## 5. Definición de Éxito

El marco se considerará exitoso cuando: los pipelines de datos tengan una disponibilidad del 99.5% medida mensualmente, el tiempo medio de detección de problemas de calidad sea inferior a 24 horas, el equipo de auditoría pueda completar solicitudes de linaje en menos de 4 horas, y el crecimiento del volumen de datos no requiera contratación de personal adicional de ingeniería de datos.

// === ARCHIVO: docs/registro_decisiones.md ===
# Registro de Decisiones de Diseño del Marco de Gobierno de Datos

## Formato del Registro

Cada decisión incluye: identificador único, contexto que motivó la decisión, opciones consideradas, decisión tomada con su justificación, dependencias con otras decisiones, y fecha de revisión programada.

---

## DECISIÓN-001: Estrategia de Almacenamiento de Metadatos de Linaje

### Contexto

El linaje de datos debe ser consultable por múltiples audiencias con diferentes necesidades de consulta. El equipo de auditoría requiere consultas históricas que involucran filtros por rango de fechas y por activo de datos específico. Los ingenieros de datos necesitan consultar el linaje en tiempo real durante el desarrollo para depurar problemas en las transformaciones. La dirección ejecutiva necesita vistas agregadas del volumen de datos y de la cobertura de linaje por dominio.

### Opciones Consideradas

**Opción A: Almacenamiento en tabla de PostgreSQL existente.** La base de datos relacional existente ofrece consultas complejas con joins eficientes y transacciones ACID. Sin embargo, el volumen proyectado de eventos de linaje (millones por día) podría degradar el rendimiento de las consultas analíticas y elevar significativamente los costos de almacenamiento.

**Opción B: Almacenamiento en S3 con formato Parquet y Athena.** El enfoque data lake permite almacenamiento barato de grandes volúmenes y consultas eficientes mediante Athena. La desventaja es la latencia de hasta 30 segundos para que las particiones estén disponibles para consulta, y la complejidad de gestionar las particiones manualmente.

**Opción C: Almacenamiento híbrido con DynamoDB para consultas tiempo real y S3 para histórico.** DynamoDB serviría como caché de linaje reciente (últimos 7 días) para consultas de desarrollo, mientras que S3 almacenaría el histórico completo para auditorías. Este enfoque optimiza el costo-velocidad pero introduce complejidad en la sincronización entre ambos almacenes.

### Decisión Tomada

Se selecciona la **Opción C** con las siguientes especificaciones:

- DynamoDB con clave primaria compuesta (execution_id + dataset_name) para consultas por ejecución
- Particionado en S3 por año/mes/día para consultas históricas
-TTL de 7 días en DynamoDB con automatización de exportación a S3 antes del expiry
- Índice secundario global en DynamoDB por dataset_name para consultas inversas (qué ejecuciones afectaron este dataset)

### Justificación

La decisión prioriza la experiencia del desarrollador (consultas sub-segundo en DynamoDB) sin sacrificar la capacidad de auditoría histórica. El costo adicional de mantener dos almacenes se justifica por la reducción en tiempo de desarrollo y depuración. La complejidad de sincronización se mitiga mediante funciones Lambda triggered por la escritura en DynamoDB.

### Dependencias

Esta decisión depende de DECISIÓN-004 (formato de eventos de linaje) y DECISIÓN-006 (estrategia de partitioning). La revisión está programada para 6 meses después de producción para evaluar si el volumen real justifica el enfoque híbrido.

---

## DECISIÓN-002: Modelo de Calidad de Datos

### Contexto

Las reglas de calidad deben ser definidas por analistas de datos que no necesariamente tienen conocimientos de programación. Sin embargo, la complejidad de algunas reglas (validaciones cross-column, agregaciones condicionales) requiere flexibilidad que los modelos declarativos simples no pueden proporcionar.

### Opciones Consideradas

**Opción A: Reglas puramente declarativas en YAML.** Define reglas como objetos JSON con campos como field, operator y threshold. Ventaja: simplicidad para casos comunes. Desventaja: expresión limitada para reglas complejas que requieren lógica personalizada.

**Opción B: Reglas como código mediante funciones Python.** Máxima flexibilidad para cualquier tipo de validación. Desventaja: curva de aprendizaje para analistas y riesgo de que las reglas contengan lógica no determinista o efectos secundarios.

**Opción C: Híbrido con motor declarativo más extensiones Python.** Las reglas comunes se definen en YAML, pero el motor permite registrar funciones Python personalizadas como "UDFs de calidad". Las funciones personalizadas pasan por revisión de código antes de ser registradas.

### Decisión Tomada

Se selecciona la **Opción C** con las siguientes especificaciones:

- Registro de reglas en archivos YAML dentro del directorio conf/quality_rules/
- Biblioteca de operadores predefinidos: is_null, not_null, in_range, matches_regex, is_unique, is_complete
- Registro de funciones personalizadas en src/quality/custom_functions/ con tests obligatorios
- Metadatos de cada regla incluyen: descripción, severidad (blocking/warning/info),owner
- Dashboard de reglas de calidad accesible desde Airflow con hit counts por regla

### Justificación

El enfoque híbrido maximiza la adopción: el 80% de las reglas se expresan declarativamente (facilitando la participación de analistas), mientras que el 20% restante con lógica compleja se implementa como código con el rigor de un pipeline de software (tests, revisión). El requisito de tests para funciones personalizadas mitiga el riesgo de reglas no deterministas.

### Dependencias

Depende de DECISIÓN-005 (ubicación de configuración) y DECISIÓN-007 (estrategia de testing). La revisión está programada para 3 meses después de producción para evaluar la proporción de reglas declarativas vs personalizadas.

---

## DECISIÓN-003: Estrategia de Versionado de Esquemas

### Contexto

Los esquemas de las fuentes de datos evolucionan frecuentemente, especialmente las APIs de proveedores externos que pueden agregar campos sin notificación. El marco debe detectar cambios de esquema automáticamente y tomar acciones apropiadas sin intervención manual en la mayoría de los casos.

### Opciones Consideradas

**Opción A: Esquemas estrictos con fallo ante cualquier cambio.** Cualquier campo nuevo o faltante causa fallo del pipeline. Ventaja: detección inmediata de cambios. Desventaja: fragilidad extrema que genera alertas de fatiga.

**Opción B: Esquemas flexibles que aceptan cualquier campo.** El pipeline procesa los campos conocidos e ignora los desconocidos. Ventaja: resiliencia máxima. Desventaja: cambios en el significado de campos existentes pasan desapercibidos.

**Opción C: Esquemas con evolución controlada mediante versionado explícito.** Cada dataset tiene un esquema versionado. Los cambios se clasifican en: additive (nuevos campos opcionales), breaking (cambios de tipo o eliminación de campos). Los cambios additivos se incorporan automáticamente; los breaking requieren aprobación manual.

### Decisión Tomada

Se selecciona la **Opción C** con las siguientes especificaciones:

- Almacenamiento de esquemas en conf/schemas/ como archivos YAML con versionado semántico
- Comparador automático de esquemas que clasifica cambios en additive/breaking/deprecated
- Pipeline genera notificación a canal de Slack dedicado cuando detecta cambios breaking
- Registro de todas las versiones de esquema con fecha de activación y usuario que aprobó
- Backward compatibility mantenida mediante alias de campos renombrados por 2 versiones

### Justificación

El versionado explícito proporciona el balance correcto entre automatización y control. La clasificación automática reduce la carga operativa mientras que los cambios breaking requieren revisión humana que es donde se captura el conocimiento del impacto. El período de deprecated de 2 versiones da tiempo a los consumidores para migrar.

### Dependencias

Depende de DECISIÓN-004 (formato de eventos de linaje para capturar cambios de esquema) y DECISIÓN-008 (estrategia de notificaciones). La revisión está programada para 12 meses para evaluar la frecuencia de cambios breaking y ajustar los umbrales.

---

## DECISIÓN-004: Formato de Eventos de Linaje

### Contexto

Cada evento de linaje debe capturar información suficiente para reconstruir el camino completo de un dato: qué proceso lo generó, qué datos de entrada usó, qué transformaciones aplicó, y qué otros datos generó como efecto secundario. El volumen proyectado es de 10-50 millones de eventos por día.

### Opciones Consideradas

**Opción A: Evento detallado con todos los campos del dato.** Información completa pero tamaño de evento excesivo (promedio 5KB por evento). Costo de almacenamiento proyectado: $X mensual.

**Opción B: Evento minimalista con referencias a datos externos.** El evento solo contiene IDs de referencia. La información completa se consulta bajo demanda de tablas de metadatos. Desventaja: latencia adicional para consultas que requieren joins.

**Opción C: Evento con información contextual más punteros a datos de entrada/salida.** Balance entre detalle y tamaño. El evento incluye: ID de ejecución, timestamp, nombre del proceso, lista de datasets de entrada (con checksums), lista de datasets de salida (con checksums), y transforms aplicadas como lista de funciones con parámetros.

### Decisión Tomada

Se selecciona la **Opción C** con las siguientes especificaciones:

- Formato de evento: JSON con esquema versionado
- Campos obligatorios: event_id (UUID), execution_id, timestamp, process_name, input_datasets[], output_datasets[], transforms[]
- Cada dataset incluye: name, format, partition_path, checksum (SHA-256 del contenido)
- Compresión gzip para escritura en S3, descompresión bajo demanda para lectura
- Retención: 90 días en queryable storage, archivo muerto en Glacier después

### Justificación

El checksum permite verificar la integridad de los datos sin necesidad de acceder al contenido. La estructura de listas permite consultas eficientes como "qué procesos leen de este dataset" mediante filtros en DynamoDB. El balance de 1-2KB por evento es aceptable para el volumen proyectado.

### Dependencias

Esta decisión es prerequisito para DECISIÓN-001 y DECISIÓN-003. La revisión está programada para 6 meses para validar el tamaño promedio real de eventos.

---

## DECISIÓN-005: Ubicación de la Configuración

### Contexto

La configuración que varía entre entornos (dev, staging, production) debe ser accesible para los procesos de Airflow sin hardcodear valores. El equipo tiene experiencia con archivos YAML pero necesita una estrategia que soporte secrets sin exponerlos en los archivos.

### Opciones Consideradas

**Opción A: Archivos YAML por entorno en el código.** Simple pero expone todos los valores en el repositorio, incluyendo credenciales si no se usa un secrets backend.

**Opción B: Variables de entorno exclusivamente.** Seguro pero difícil de gestionar para configuraciones complejas (objetos anidados, listas).

**Opción C: Archivos YAML con referencias a AWS Secrets Manager.** Los archivos contienen placeholders como ${secret:nombre_del_secreto} que se resuelven en tiempo de ejecución consultando Secrets Manager.

### Decisión Tomada

Se selecciona la **Opción C** con las siguientes especificaciones:

- Archivos en conf/{entorno}/config.yaml con estructura de secciones: sources, targets, quality, lineage, notifications
- Loader personalizado que resuelve placeholders ${secret:...} consultando boto3 secretsmanager
- Fallback a valores por defecto en entorno dev si el secret no existe (facilita desarrollo local)
- Validación de esquema del archivo YAML contra Pydantic model en startup del DAG
- Documentación de cada clave de configuración en conf/README.md

### Justificación

El enfoque combina la legibilidad de YAML para configuraciones complejas con la seguridad de Secrets Manager para credenciales. El fallback en dev permite a los desarrolladores ejecutar pipelines localmente sin configurar todos los secrets. La validación en startup detecta problemas de configuración antes de que fallen las tareas.

### Dependencias

Depende de la disponibilidad de AWS Secrets Manager y de la librería boto3. No tiene dependencias con otras decisiones de este registro.

---

## Resumen de Decisiones Controversiales

Las decisiones que representan trade-offs significativos y pueden ser objeto de debate son: DECISIÓN-001 (complejidad del almacenamiento híbrido), DECISIÓN-002 (balance entre declaratividad y flexibilidad), y DECISIÓN-003 (automatización vs control en evolución de esquemas). Cada una de estas decisiones incluye revisión programada para validar si los supuestos iniciales se cumplieron.

// === ARCHIVO: docs/presentacion_tecnica.md ===
# Presentación Técnica: Marco de Gobierno de Datos DataCorp

## Resumen Ejecutivo para Ingeniería

Este documento presenta la arquitectura técnica del marco de gobierno de datos implementado en DataCorp. El marco integra estándares de DAMA (Data Management Body of Knowledge), TOGAF (The Open Group Architecture Framework) y CMMI (Capability Maturity Model Integration) en una solución práctica basada en Python, Apache Airflow y servicios AWS.

El objetivo es proporcionar al equipo de ingeniería una comprensión profunda de cómo el marco opera, cómo extenderlo y cómo contribuir a su evolución. Se asume familiaridad con pipelines ETL, conceptos de data quality y arquitecturas data lake.

## Arquitectura General del Sistema

### Visión de Componentes

El marco se estructura en cuatro capas principales que operan de forma secuencial pero mantienen separación de responsabilidades clara:

**Capa de Extracción (src/extract/)**: Responsible de conectar con las fuentes de datos, normalizar esquemas de origen y preparar los datos para la capa de transformación. Cada connector es independiente y puede ser ejecutado sin las capas subsecuentes para propósitos de debugging.

**Capa de Transformación (src/transform/)**: Aplica las reglas de negocio, validaciones de calidad y transformaciones necesarias para convertir los datos crudos en formatos apt für consumo. Esta capa es donde residen las reglas de calidad definidas en el registro de decisiones.

**Capa de Carga (src/load/)**: Escribe los datos transformados en los destinos finales (S3, Redshift, bases de datos) siguiendo las estrategias de particionado y formato definidas por configuración.

**Capa de Gobernanza (src/governance/)**: Opera de forma ortogonal a las otras tres capas, capturando metadatos de linaje, ejecutando validaciones de calidad, y proporcionando capacidades de auditoría y monitoreo.

### Flujo de Datos y Orchestración

El flujo de ejecución está orquestado por Apache Airflow mediante DAGs definidos en dags/. El DAG principal governance_dag.py sigue la estructura clásica de tres etapas: extract, transform, load, con tareas adicionales de pre-validación y post-validación que pertenecen a la capa de gobernanza.

Las tareas dentro del DAG utilizan XComs para pasar información de contexto entre etapas (execution_id, checksums, métricas). Esto permite que cada tarea sea idempotente y pueda ser re-ejecutada de forma independiente en caso de fallo.

## Diseño de Calidad de Datos

### Arquitectura de Reglas de Calidad

Las reglas de calidad se implementan como funciones puras que reciben un DataFrame de pandas o Spark y retornan un objeto de resultado que incluye: estado (pass/fail), lista de registros que fallaron, y métricas agregadas. Esta arquitectura permite que las mismas reglas se ejecuten en múltiples puntos del pipeline.

El motor de calidad soporta tres categorías de reglas:

**Reglas de tipo**: Validan que los valores corresponden al tipo esperado (integer, float, string, date). Se aplican automáticamente según la definición del esquema.

**Reglas de dominio**: Validan que los valores pertenecen a un conjunto válido de opciones. Definidas en archivos YAML como listas de valores permitidos o como expresiones regulares.

**Reglas de negocio**: Validaciones específicas del dominio que requieren lógica personalizada. Implementadas como funciones Python registradas en el catálogo de reglas.

### Pipeline de Quarantine

Cuando un registro falla una regla de calidad con severidad blocking, en lugar de detener el pipeline completo, el registro se redirige a un bucket de quarantine en S3. Cada día se genera un archivo con los registros fallidos, incluyendo la regla que falló y el valor que causó el fallo.

El equipo de calidad recibe una notificación diaria con el resumen de registros en quarantine. La corrección de los datos fuente (no del pipeline) es responsabilidad del área generadora del dato, siguiendo el principio de que la calidad empieza en la fuente.

## Sistema de Linaje de Datos

### Modelo de Eventos

Cada ejecución de tarea en el DAG genera eventos de linaje que capture: el identificador de ejecución, los datasets de entrada con sus checksums, las transformaciones aplicadas, y los datasets de salida con sus checksums. El checksum permite verificar que los datos no fueron modificados después de la transformación.

Los eventos se escriben en DynamoDB para consultas tiempo real (disponible en los 7 días posteriores a la ejecución) y se exportan periódicamente a S3 para retención histórica. Esta arquitectura híbrida optimiza el costo-velocidad según lo detallado en el registro de decisiones.

### APIs de Consulta

El módulo data_lineage_tracker.py proporciona funciones para consultar el linaje desde código Python: get_upstream_sources(dataset_name) retorna la lista de fuentes originales de un dato, get_downstream_consumers(dataset_name) retorna los procesos que consumen un dataset, y get_execution_lineage(execution_id) reconstruye el grafo completo de una ejecución.

Estas funciones se utilizan internamente para debugging y están expuestas como endpoints de una API REST interna para consumo por herramientas de visualización y auditoría.

## Gestión de Esquemas

### Ciclo de Vida de Esquemas

Los esquemas se versionan utilizando versionado semántico dentro del directorio conf/schemas/. Cada dataset tiene su propio archivo YAML que define: versión actual, lista de campos con tipos, y historia de cambios entre versiones.

El proceso de evolución de esquemas opera en tres pasos: detección automática de cambios al comparar el esquema observado con el registrado, clasificación del cambio como additive/breaking/deprecated, y aplicación automática para cambios additive o notificación para cambios breaking.

### Compatibilidad Hacia Atrás

El marco mantiene compatibilidad hacia atrás durante dos versiones mayores. Cuando un campo se renombra, el nombre antiguo se mantiene como alias durante ese período. Los consumidores tienen tiempo de migrar antes de que el alias sea eliminado. Esta estrategia minimiza las interrupciones en producción mientras permite evolución continua.

## Configuración y Entornos

### Estructura de Configuración

La configuración se organiza en archivos YAML bajo conf/, con subdirectorios por entorno (dev/, staging/, production/). El archivo principal config.yaml incluye secciones para: fuentes de datos (conexiones y querys), destinos (paths S3, configuraciones de escritura), reglas de calidad (thresholds y severidades), y notificaciones (endpoints de Slack, emails).

Los valores sensibles (credenciales, tokens) no se almacenan en los archivos YAML sino que se referencian mediante placeholders que se resuelven en tiempo de ejecución consultando AWS Secrets Manager. Esto permite que los archivos de configuración estén versionados sin exponer secretos.

### Desarrollo Local

El marco soporta ejecución local mediante Docker Compose que levanta los servicios necesarios (LocalStack para S3 y DynamoDB, PostgreSQL). Los desarrolladores pueden ejecutar el DAG completo o tareas individuales desde la línea de comandos. La configuración local utiliza valores por defecto seguros que permiten funcionar sin credenciales reales de AWS.

## Métricas y Monitoreo

### Exportación de Métricas

Cada tarea del DAG exporta métricas a CloudWatch: duración de ejecución, volumen de datos procesados (bytes y registros), número de registros fallidos por regla de calidad, y estado final (success/failure). Estas métricas alimentan dashboards operativos que muestran la salud del sistema en tiempo real.

### Alertas y Notificaciones

Las alertas se configuran en CloudWatch con umbrales adaptativos que aprenden del comportamiento histórico. Una alerta de volumen anómalo solo se dispara si el volumen está fuera del rango esperado basándose en la media móvil de los últimos 30 días con desviación estándar.

Las notificaciones se envían a canales de Slack dedicados: #data-alerts para alertas operativas (fallos de tareas, datos faltantes), #data-quality para reportes de calidad diarios, y #data-architecture para cambios en esquemas y decisiones de diseño.

## Guía de Contribución

### Agregar Nueva Fuente de Datos

Para agregar una nueva fuente de datos, crear un nuevo connector en src/extract/ que hereda de la clase base DataSourceReader. Implementar los métodos connect(), extract(), y close(). Agregar la configuración de la fuente en conf/{entorno}/config.yaml bajo la sección sources. Finalmente, agregar el connector como tarea en el DAG.

### Agregar Nueva Regla de Calidad

Para agregar una regla de calidad declarativa, crear una entrada en el archivo YAML correspondiente en conf/quality_rules/ con la definición de la regla (campo, operador, umbral). Para reglas que requieren lógica personalizada, crear una función en src/quality/custom_functions/ que siga la firma establecida, agregar tests en tests/test_data_quality_rules.py, y registrar la función en el catálogo de reglas.

### Agregar Nueva Transformación

Las transformaciones se implementan como funciones en src/transform/ que reciben un DataFrame y retornan un DataFrame. Cada transformación debe ser idempotente (el mismo input produce el mismo output) y debe documentar sus dependencias (qué columnas requiere, qué columnas produce). Agregar la transformación al pipeline en el orden apropiado dentro del DAG.

## Referencias y Recursos

- Código fuente: Repositorio interno de DataCorp (src/, dags/, tests/)
- Documentación de configuración: conf/README.md
- Estándares de referencia: DAMA-DMBOK, TOGAF 10, CMMI v2.0
- Documentación de Airflow: https://airflow.apache.org/docs/apache-airflow/2.9/
- Repositorio de mejores prácticas: Wiki interno "Data Engineering Standards"

// === ARCHIVO: docs/presentacion_ejecutiva.md ===
# Marco de Gobierno de Datos DataCorp
## Presentación Ejecutiva para Dirección

---

### 1. Resumen Ejecutivo

El presente documento describe el marco de gobierno de datos implementado en DataCorp, diseñado para garantizar la calidad, integridad y disponibilidad de los activos de datos organizacionales. Este marco se fundamenta en estándares internacionales reconocidos: DAMA (Data Management Association), TOGAF (The Open Group Architecture Framework) y CMMI (Capability Maturity Model Integration).

La inversión en este marco permite a DataCorp reducir риски asociados con la mala calidad de datos, cumplir con regulaciones de protección de información y habilitar decisiones basadas en datos confiables en todas las áreas del negocio.

---

### 2. Contexto y Necesidad del Gobierno de Datos

DataCorp opera en un entorno donde el volumen de datos crece exponencialmente cada año. Actualmente, la organización procesa información proveniente de múltiples fuentes: sistemas transaccionales, aplicaciones de clientes, dispositivos IoT y fuentes externas de terceros. Sin un marco estructurado de gobierno, los efectos visibles incluyen:

- **Inconsistencia en reportes**: diferentes áreas generan métricas contradictorias sobre el mismo indicador.
- **Duplicación de esfuerzos**: equipos distintos crean pipelines de datos similares de manera independiente.
- **Riesgo regulatorio**: dificultades para demostrar cumplimiento con normativas de protección de datos.
- **Tiempo prolongado en análisis**: hasta el 40% del tiempo de analistas se destina a limpieza y validación de datos.

El marco de gobierno de datos responde directamente a estas проблемы, estableciendo políticas, procesos y responsabilidades claras para todo el ciclo de vida de la información.

---

### 3. Objetivos Estratégicos del Marco

El marco de gobierno de datos de DataCorp persigue los siguientes objetivos estratégicos, alineados con el plan corporativo de transformación digital:

| Objetivo | Indicador de Éxito | Impacto Esperado |
|----------|-------------------|------------------|
| Calidad de datos superior al 95% | Porcentaje de datasets que cumplen reglas de calidad | Decisiones más precisas y reducción de errores operativos |
| Trazabilidad completa del linaje de datos | Porcentaje de pipelines con linaje documentado | Capacidad de auditoría y cumplimiento regulatorio |
| Reducción del 30% en tiempo de分析师ía | Tiempo promedio desde solicitud hasta insight | Mayor velocidad en la toma de decisiones |
| Cumplimiento normativo completo | Auditorías sin hallazgos críticos | Evitación de sanciones y protección de reputación |
| Democratización del acceso a datos | Número de usuarios activos en catálogo | Innovación acelerada por auto-servicio |

---

### 4. Arquitectura del Marco

El gobierno de datos en DataCorp se estructura en cuatro pilares fundamentales que operan de manera integrada:

**Pilar 1: Gestión de Datos**
- Definición de estándares de 모델ado de datos
- Catálogo centralizado de activos de datos
- Políticas de nomenclatura y documentación

**Pilar 2: Calidad de Datos**
- Reglas de validación automatizadas en cada punto de ingestión
- Monitoreo continuo de métricas de calidad
- Procesos de remediación para datos defectuosos

**Pilar 3: Seguridad y Privacidad**
- Clasificación de datos por nivel de sensibilidad
- Controles de acceso basados en roles
- Enmascaramiento de datos sensibles en entornos no productivos

**Pilar 4: Arquitectura e Integración**
- Estándares de modelado para todas las capas del pipeline
- Patrones de integración probados y reutilizables
- Gobernanza de esquemas y evolución de estructuras

---

### 5. Beneficios Cuantificables

La implementación del marco de gobierno de datos genera beneficios medibles en diferentes horizontes temporales:

**Corto Plazo (0-6 meses)**
- Reducción del 15% en tiempo dedicado a validación manual de datos
- Identificación y corrección de 200+ reglas de negocio inconsistentes
- Primer catálogo de datos publicado con 50+ datasets catalogados

**Mediano Plazo (6-18 meses)**
- Reducción del 30% en incidentes relacionados con calidad de datos
- Disminución del 25% en costos de almacenamiento por optimización
- Cumplimiento total con regulación de protección de datos

**Largo Plazo (18-36 meses)**
- Aumento del 40% en productividad de analistas de datos
- Reducción del 50% en tiempo de onboarding para nuevos proyectos
- Capacidad demostrada de auditoría completa de linaje de datos

---

### 6. Modelo de Madurez y Roadmap

El marco utiliza el modelo CMMI para medir la madurez de las capacidades de gobierno de datos, estableciendo una hoja de ruta clara hacia la excelencia:

| Nivel | Descripción | Estado Actual | Meta Año 1 | Meta Año 2 |
|-------|-------------|---------------|------------|------------|
| Inicial | Procesos adhoc, reactivos | - | - | - |
| Gestionado | Procesos definidos y documentados | Parcial | Completo | Completo |
| Definido | Procesos estandarizados y medidos | - | Parcial | Completo |
| Cuantitativamente Gestionado | Métricas y control estadístico | - | - | Parcial |
| Optimizado | Mejora continua basada en datos | - | - | - |

---

### 7. Gobernanza y Organización

La estructura de gobernanza asegura la toma de decisiones oportuna y la asignación clara de responsabilidades:

**Comité de Datos Corporativo**
- Frecuencia: Trimestral
- Participantes: CEO, CTO, CFO, Director de Datos
- Responsabilidades: Estrategia de datos, inversiones mayores, resolución de conflictos entre áreas

**Oficina de Gobierno de Datos (CDO)**
- Frecuencia: Mensual
- Participantes: Chief Data Officer, líderes de dominio de datos
- Responsabilidades: Políticas, estándares, supervisión de calidad, gestión del catálogo

** Stewards de Datos por Dominio**
- Frecuencia: Quincenal
- Participantes: Representantes de cada área de negocio
- Responsabilidades: Definición de reglas de negocio, validación de calidad, documentación

---

### 8. Inversión y Retorno

La implementación del marco requiere inversión en tres categorías principales:

| Categoría | Inversión Año 1 | Inversión Año 2 | Beneficio Anual Estimado |
|-----------|-----------------|-----------------|--------------------------|
| Tecnología | $180,000 | $120,000 | $95,000 en eficiencia |
| Personas | $350,000 | $400,000 | $280,000 en productividad |
| Procesos | $80,000 | $60,000 | $150,000 en reducción de риски |
| **Total** | **$610,000** | **$580,000** | **$525,000** |

**Retorno de Inversión a 3 años**: 156%
**Período de recuperación**: 14 meses

---

### 9. Riesgos y Mitigaciones

| Riesgo | Probabilidad | Impacto | Mitigación |
|--------|--------------|---------|------------|
| Resistencia al cambio cultural | Alta | Alto | Programa de gestión del cambio, champions en cada área |
| Falta de recursos especializados | Media | Alto | Capacitación interna, partnerships con proveedores |
| Integración con sistemas legacy | Media | Medio | Prototipos de integración, inversión gradual |
| Priorización competitiva con otros proyectos | Media | Medio | Alineación con estrategia corporativa, quick wins visibles |

---

### 10. Recomendaciones y Siguientes Pasos

Para la aprobación ejecutiva, se solicita:

1. **Validación del marco** propuesto y autorización para proceder a implementación completa
2. **Aprobación de inversión** de $610,000 para el primer año, con proyección de $580,000 para año 2
3. **Designación de sponsor ejecutivo** para el comité de datos corporativo
4. **Autorización de contratación** de 3 recursos especializados para la oficina de gobierno de datos

Con la aprobación de estos puntos, el equipo de datos puede iniciar la фаза de implementación del Pilar 1 (Gestión de Datos) con un cronograma de 12 semanas hasta el primer delivery measurable.

---

### Contacto

Para consultas sobre este documento, contactar al equipo de Data Engineering en data-engineering@datacorp.com

---

*Documento preparado para el Comité Ejecutivo de DataCorp*
*Versión 1.0 - Fecha de emisión: 2024*

// === ARCHIVO: docs/mejoras_propuestas.md ===
# Mejoras Propuestas al Marco de Gobierno de Datos
## Documento de Justificaciones y Plan de Implementación

---

## 1. Introducción

Este documento consolida las mejoras identificadas durante la evaluación del marco de gobierno de datos de DataCorp, fundamentadas en retroalimentación de stakeholders, análisis de métricas de operación y mejores prácticas de la industria. Cada mejora incluye la justificación técnica y de negocio, el impacto estimado y el plan de implementación recomendado.

El proceso de revisión involucró entrevistas con 25+ usuarios del marco, análisis de 6 meses de datos operacionales y benchmarking contra marcos de empresas del sector financiero y tecnológico comparables.

---

## 2. Mejoras Identificadas

### 2.1 Automatización de Metadata Management

**Descripción de la mejora**
Implementar recolección automática de metadatos técnicos mediante integración nativa con los pipelines de datos, eliminando la carga manual de documentación que actualmente representa 8 horas semanales por equipo.

**Justificación**
El modelo actual depende de documentación manual en spreadsheets, lo cual genera inconsistencias y obsolescencia rápida. El 73% de los datasets en el catálogo tienen información incompleta o desactualizada. La automatización de metadatos reduce el error humano y mantiene la información actualizada en tiempo real.

La integración con Apache Airflow permite extraer automáticamente: número de registros procesados, tiempo de ejecución, esquema del dataset, lineage de transformaciones y checksum de validación. Esta información se persiste en un repositorio centralizado accesible vía API.

**Impacto estimado**
- Reducción de 8 horas/semana en documentación manual = 416 horas/año por equipo
- Aumento del 40% en completitud del catálogo
- Disminución del 60% en tiempo de búsqueda de lineage para auditorías

**Prioridad**: Alta
**Complejidad**: Media
**Timeline**: 8 semanas

---

### 2.2 Sistema de Scoring de Calidad Dinámico

**Descripción de la mejora**
Reemplazar las reglas de calidad estáticas actuales por un sistema de scoring dinámico que adapte los umbrales de validación según el contexto del dataset, historial de calidad y criticidad del caso de uso.

**Justificación**
Las reglas de calidad actuales aplican umbrales uniformes (95% completitud, 0% duplicados) a todos los datasets, sin considerar que la tolerancia para datos transaccionales difiere drásticamente de la tolerancia para logs de sistema. Esta rigidez genera dos problemas: falsos positivos en datasets no críticos y falsos negativos en datasets críticos.

El nuevo sistema implementará un modelo de scoring ponderado donde cada dataset tendrá asignada una criticidad (crítica/alta/media/baja) y el sistema ajustará los umbrales automáticamente. Un dataset de facturación con 94% de calidad mostrará alerta roja, mientras que un log de debug con 80% mostrará solo advertencia informativa.

**Impacto estimado**
- Reducción del 45% en falsos positivos de calidad
- Aumento del 30% en adopción de reglas de calidad por equipos
- Identificación proactiva del 25% más de issues de calidad antes de producción

**Prioridad**: Alta
**Complejidad**: Alta
**Timeline**: 12 semanas

---

### 2.3 Catálogo de Datos con Self-Service

**Descripción de la mejora**
Ampliar el catálogo de datos actual para incluir capacidades de self-service que permitan a los usuarios técnicos solicitar acceso, entender la composición de datos y reportar problemas sin intervención manual del equipo de governance.

**Justificación**
El proceso actual de acceso a datos requiere aprobación manual que promedia 5 días hábiles. Esto crea cuellos de botella, desalienta el uso legítimo de datos y push traffic a canales informales no gobernados. El 40% de los usuarios reportan haber recurrido a copias no autorizadas de datos para evitar el proceso formal.

La solución implementará un portal donde los usuarios pueden: explorar el catálogo con búsqueda semántica, entender la composición de cada dataset vía perfiles automatizados, solicitar acceso con justificación de caso de negocio, y trackear el estado de sus solicitudes. Las solicitudes de bajo riesgo se aprueban automáticamente mediante reglas predefinidas.

**Impacto estimado**
- Reducción de tiempo promedio de acceso de 5 días a 4 horas
- Aumento del 200% en solicitudes formales vs informales
- Disminución del 70% en copias no autorizadas de datos

**Prioridad**: Media-Alta
**Complejidad**: Alta
**Timeline**: 16 semanas

---

### 2.4 Integración de Privacidad por Diseño

**Descripción de la mejora**
Incorporar módulos de detección y protección de datos sensibles directamente en la capa de ingestión, aplicando automáticamente políticas de enmascaramiento según clasificación de datos.

**Justificación**
El proceso actual de clasificación de datos sensibles es manual y reactivo, realizándose únicamente durante auditorías. Esto genera риски de exposición de información personal en entornos no productivos donde el 60% de los usuarios tienen acceso amplio. La regulación de protección de datos impone sanciones significativas por exposición de datos personales en ambientes no controlados.

La mejora integra un motor de detección de patrones sensibles (PII, PCI, PHI) que escanea automáticamente cada nuevo dataset ingestado. Los datos detectados se clasifican y aplican políticas de enmascaramiento predefinidas: masking completo para entornos de desarrollo, masking parcial para QA, y acceso completo solo en producción con auditoría.

**Impacto estimado**
- Cobertura del 100% de datos sensibles vs 40% actual
- Cero incidentes de exposición de PII en entornos no productivos
- Reducción del 80% en tiempo de preparación de entornos de prueba

**Prioridad**: Crítica
**Complejidad**: Alta
**Timeline**: 14 semanas

---

### 2.5 Dashboard Ejecutivo de Gobierno de Datos

**Descripción de la mejora**
Desarrollar un dashboard interactivo que presente métricas clave del estado de gobierno de datos en tiempo real, diseñado específicamente para consumo ejecutivo con drill-down hasta nivel operacional.

**Justificación**
Los reportes actuales de gobierno de datos se generan manualmente cada trimestre en formato PDF estático. Esto limita la visibilidad ejecutiva, dificulta el seguimiento de tendencias y no permite intervenciones proactivas. El comité ejecutivo necesita acceso a métricas actualizadas para tomar decisiones informadas sobre inversiones y prioridades.

El dashboard integrará datos de todas las fuentes del marco: calidad de datos por dominio, adopción del catálogo, incidentes de seguridad, cumplimiento de políticas y tendencias históricas. Incluirá alertas automáticas cuando métricas crucen umbrales críticos y permitirá drill-down desde vista agregada hasta detalles de datasets específicos.

**Impacto estimado**
- Visibilidad en tiempo real del estado de gobierno de datos
- Reducción del 50% en tiempo de preparación de reportes ejecutivos
- Identificación temprana del 35% más de tendencias problemáticas

**Prioridad**: Media
**Complejidad**: Baja-Media
**Timeline**: 6 semanas

---

### 2.6 Programa de Data Stewards Expandido

**Descripción de la mejora**
Formalizar y expandir el programa de Data Stewards para incluir representantes de todas las áreas de negocio, con responsabilidades claras, incentivos alineados y soporte dedicado del equipo de gobierno.

**Justificación**
El programa actual de Data Stewards opera de manera informal con cobertura solo en las áreas de analytics y tecnología. La falta de representación en áreas de negocio (ventas, operaciones, finanzas, recursos humanos) genera brechas en la definición de reglas de negocio, validación de calidad y resolución de conflictos de ownership.

La expansión del programa incluirá: definición de responsabilidades formales en el perfil de cada rol, capacitación estructurada de 20 horas por steward, reuniones quincenales sincronizadas, métricas de desempeño vinculadas a objetivos individuales, y reconocimiento público de contribuciones destacadas.

**Impacto estimado**
- Cobertura del 100% de dominios de datos con steward asignado
- Aumento del 50% en resolución de issues de calidad en primera línea
- Mejora del 35% en satisfacción de usuarios del catálogo

**Prioridad**: Media
**Complejidad**: Baja
**Timeline**: 10 semanas (implementación continua)

---

## 3. Análisis de Dependencias

Las mejoras propuestas presentan interdependencias que deben considerarse en la planificación:

| Mejora | Depende de | Bloquea |
|--------|-----------|---------|
| Scoring dinámico | Metadata Management | Dashboard Ejecutivo |
| Catálogo self-service | Scoring dinámico | - |
| Privacidad por diseño | Metadata Management | - |
| Dashboard ejecutivo | Metadata Management, Scoring | - |
| Data Stewards | Todas las anteriores | - |

La implementación recomendada sigue un orden que maximiza el paralelismo: Metadata Management es el habilitador base, seguido de Scoring dinámico y Privacidad por diseño en paralelo, luego Catálogo self-service, y finalmente Dashboard y Data Stewards como consolidaciones.

---

## 4. Plan de Implementación Consolidado

### Fase 1: Cimientos (Semanas 1-8)
- Implementación de Metadata Management automatizado
- Desarrollo de módulo de detección de datos sensibles
- Entregables: Pipeline de metadata, motor de clasificación PII

### Fase 2: Inteligencia (Semanas 9-20)
- Sistema de scoring dinámico
- Portal de catálogo self-service
- Entregables: Motor de reglas adaptivas, portal de usuario

### Fase 3: Visibilidad (Semanas 21-26)
- Dashboard ejecutivo
- Programa expandido de Data Stewards
- Entregables: Dashboard interactivo, stewards certificados

---

## 5. Inversión Adicional Requerida

| Mejora | Inversión Desarrollo | Inversión Operacional Anual | ROI Esperado |
|--------|---------------------|----------------------------|--------------|
| Metadata Management | $45,000 | $8,000 | 18 meses |
| Scoring dinámico | $75,000 | $12,000 | 12 meses |
| Catálogo self-service | $95,000 | $18,000 | 10 meses |
| Privacidad por diseño | $65,000 | $15,000 | 8 meses |
| Dashboard ejecutivo | $25,000 | $5,000 | 6 meses |
| Data Stewards | $15,000 | $35,000 | Inmediato |
| **Total** | **$320,000** | **$93,000** | **11 meses** |

---

## 6. Métricas de Éxito del Programa de Mejoras

Para evaluar el éxito del programa de mejoras, se definen las siguientes métricas objetivo a 18 meses:

- **Adopción del catálogo**: 80% de usuarios técnicos activos monthly
- **Calidad de metadatos**: 95% de datasets con metadata completa y actualizada
- **Tiempo de acceso**: Promedio menor a 4 horas para solicitudes de bajo riesgo
- **Cobertura de PII**: 100% de datasets con datos sensibles clasificados
- **Satisfacción de usuarios**: NPS mayor a 50 en encuestas trimestrales
- **Incidentes de calidad**: Reducción del 50% vs línea base
- **Cumplimiento regulatorio**: Cero hallazgos críticos en auditorías

---

## 7. Recomendación Final

Se recomienda aprobar la implementación del programa de mejoras completo con un presupuesto adicional de $320,000 para desarrollo y $93,000 anuales para operación. El retorno de inversión de 11 meses y los beneficios cuantificables en reducción de риски y aumento de productividad justifican la inversión.

La priorización de privacidad por diseño como mejora crítica responde al contexto regulatorio actual y el риско reputacional asociado. Las mejoras de automatización (metadata, scoring, catálogo) generarán eficiencias que se reinvertirán en la mejora continua del marco.

---

*Documento preparado por el equipo de Data Engineering*
*Versión 1.0 - Fecha de emisión: 2024*
```
