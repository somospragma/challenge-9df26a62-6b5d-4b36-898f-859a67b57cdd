# AGENTS.md

Instrucciones para el agente de IA que abra este repositorio (Claude Code, Cursor, Codex, Copilot, Gemini). Se cargan solas: no hay que pegar nada en ningun chat.

## Que es este repositorio

Es el codigo base de un reto de aprendizaje de Pragma: **Diseño y Evaluación de un Marco de Gobierno de Datos**.

| | |
|---|---|
| Tema | implementación de gobierno de datos |
| Nivel | master-l3 |
| Chapter | Ciencia de Datos — Ingeniero de Datos |
| Especialidad | Ingeniero de datos |
| Stack | Python 3.13 / Apache Airflow 2.9 |
| Patron arquitectonico | ETL pipeline con orquestación Airflow y capas separadas (extract-transform-load) + governance layer |
| Tiempo estimado | 15 horas |

## Receta del stack

Esqueleto obligatorio:

- `pyproject.toml o requirements.txt en la raiz`
- `dags/ con el DAG de Airflow o el orquestador equivalente`
- `src/extract con los lectores de origen`
- `src/transform con las transformaciones y las reglas de calidad`
- `src/load con los escritores de destino`
- `tests/ con casos de validacion de resultados esperados`
- `conf/ con la configuracion por ambiente`

Dependencias:

- apache-airflow 2.9.0
- pydantic 2.7.1
- pandas 2.2.2
- pyspark 3.5.0
- boto3 1.34.80
- pytest 8.1.1
- pyyaml 6.0.1
- apache-airflow-providers-amazon 8.18.0

## Tu tarea

Dejar este proyecto en estado **verificable**: que el comando de verificacion corra sin errores. Escribi los archivos en disco, en este repositorio. No generes ZIPs ni archivos adjuntos.

En orden:

1. Corre `pip install -r requirements.txt && pytest -q` y mira que falla.
2. Completa lo que falte de la lista de abajo: manifiesto de dependencias, punto de entrada, capa de interfaz y las capas del patron declarado.
3. Arregla SOLO los errores que impiden compilar o arrancar.
4. Volve a correr `pip install -r requirements.txt && pytest -q` hasta que pase.
5. Pará ahí.

## Regla dura: las fases son trabajo del humano

**PROHIBIDO implementar los entregables de las fases.** El valor del reto esta en que la persona los resuelva. Tu trabajo es que tenga un proyecto que arranca; el hueco pedagogico se queda como esta.

No resuelvas nada de esto:

- **Fase 1 — Exploración del Dominio**: Documento que detalla las necesidades y restricciones del dominio de gobierno de datos en DataCorp.
- **Fase 2 — Evaluación de Decisiones de Diseño**: Registro de decisiones que detalla una decisión controversial en el diseño del marco de gobierno de datos.
- **Fase 3 — Comunicación a Diferentes Audiencias**: Dos presentaciones: una técnica para el equipo de ingeniería y una de alto nivel para la dirección ejecutiva.
- **Fase 4 — Revisión y Optimización**: Documento que detalla las mejoras propuestas y las justificaciones para el marco de gobierno de datos.

Distincion operativa:

- **Arreglar** (si): import faltante, tipo que no existe, dependencia sin declarar, error de sintaxis, archivo referenciado que no existe.
- **No tocar** (no): logica de negocio incompleta, validaciones ausentes, secretos hardcodeados, APIs deprecadas que funcionan, concurrencia insegura, patrones mejorables. Eso es lo que la persona tiene que encontrar.

## Lo que falta y tenes que completar

### 1. Archivos que la arquitectura declara (4 de 16)

La propuesta arquitectonica del reto los lista y no llegaron al repo. Crealos con implementacion real, respetando la capa en la que viven:

- [ ] `src/transform/data_quality_rules.py`
- [ ] `src/transform/schema_evolution.py`
- [ ] `src/load/data_sink_writer.py`
- [ ] `src/governance/governance_framework.py`

### 2. Referencias colgando (5)

Salieron de un analisis estatico del codigo que SI esta en el repo. Cada una rompe la compilacion:

- [ ] `dags/governance_dag.py` — `DataLineageTracker.items`
      Se invoca `items` sobre `DataLineageTracker`, pero esa clase no declara ese metodo. Agregalo con su implementacion real, o usa uno de los que si declara.
- [ ] `dags/governance_dag.py` — `DataLineageTracker.get`
      Se invoca `get` sobre `DataLineageTracker`, pero esa clase no declara ese metodo. Agregalo con su implementacion real, o usa uno de los que si declara.
- [ ] `dags/governance_dag.py` — `DataSourceReader.strftime`
      Se invoca `strftime` sobre `DataSourceReader`, pero esa clase no declara ese metodo. Agregalo con su implementacion real, o usa uno de los que si declara.
- [ ] `dags/governance_dag.py` — `DataLineageTracker.keys`
      Se invoca `keys` sobre `DataLineageTracker`, pero esa clase no declara ese metodo. Agregalo con su implementacion real, o usa uno de los que si declara.
- [ ] `dags/governance_dag.py` — `DataSourceReader.isoformat`
      Se invoca `isoformat` sobre `DataSourceReader`, pero esa clase no declara ese metodo. Agregalo con su implementacion real, o usa uno de los que si declara.

### Presentes (12)

- `pyproject.toml`
- `dags/governance_dag.py`
- `src/extract/data_source_reader.py`
- `src/governance/data_lineage_tracker.py`
- `tests/test_data_quality_rules.py`
- `tests/test_schema_evolution.py`
- `conf/dev.yaml`
- `docs/necesidades_restricciones.md`
- `docs/registro_decisiones.md`
- `docs/presentacion_tecnica.md`
- `docs/presentacion_ejecutiva.md`
- `docs/mejoras_propuestas.md`

### Capas del patron declarado

Cada una tiene que existir como directorio real con al menos un archivo. Codigo plano en la raiz no satisface el patron.

- `dags`
- `src/extract`
- `src/transform`
- `src/load`
- `src/governance`
- `tests`
- `conf`
- `docs`

## Verificacion

```bash
pip install -r requirements.txt && pytest -q
```

Ese comando pasando es la definicion de "terminado" para vos.

## Convenciones que tenes que respetar

- Un solo ecosistema: no declares librerias de otro lenguaje ni mezcles gestores de paquetes.
- Toda libreria que uses tiene que estar declarada en el manifiesto de dependencias.
- Todo import declarado tiene que usarse; todo tipo usado tiene que existir o venir de una dependencia declarada.
- El patron es **ETL pipeline con orquestación Airflow y capas separadas (extract-transform-load) + governance layer**: los contratos (interfaces, puertos) los define la capa interna y los implementa la externa, nunca al revés.
- Los archivos que crees llevan implementacion real, no stubs: sin `TODO`, sin cuerpos vacios, sin `// getters y setters`.

## Contexto del candidato

Sirve para calibrar el nivel del codigo, no para resolver las fases.

- Perfil: Chapter Ciencia de Datos, Especialidad Ingeniero de Datos, Tecnología Gobierno de Datos, Master
- Brecha que el reto ataca: Gestiona proyectos de mediana complejidad de Gobierno de Datos a través de marcos de trabajo como los propuestos en DAMA, TOGAF, CMMI
- Mision: Candidato con experiencia senior en ingeniería de datos

---

*Generado por Challenge Generator — Pragma. `README.md` tiene el enunciado completo del reto para la persona. `PROMPT_MEJORA.md` es la variante para pegar en un chat, si se prefiere ese flujo.*
