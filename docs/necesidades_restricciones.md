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