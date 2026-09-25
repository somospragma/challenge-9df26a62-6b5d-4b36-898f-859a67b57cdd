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