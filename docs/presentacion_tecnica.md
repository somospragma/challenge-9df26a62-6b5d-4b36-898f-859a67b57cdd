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