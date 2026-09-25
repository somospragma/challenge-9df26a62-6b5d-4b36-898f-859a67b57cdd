# Diseño y Evaluación de un Marco de Gobierno de Datos

La empresa 'DataCorp' requiere un marco de gobierno de datos robusto para gestionar proyectos de mediana complejidad. El marco debe basarse en estándares reconocidos como DAMA, TOGAF y CMMI. El objetivo es diseñar, evaluar y comunicar un marco de gobierno de datos que garantice la calidad, la integridad y la disponibilidad de los datos en toda la organización.

## Informacion General

| Campo | Valor |
|-------|-------|
| **Tema** | implementación de gobierno de datos |
| **Nivel** | master-l3 |
| **Tipo** | practical |
| **Tiempo estimado** | 15 horas |

## Fases del Reto

### Fase 0: Configuración del Proyecto

**Objetivo:** Obtener el proyecto base funcional enviando el Código Base a un asistente de IA, que lo analizará, corregirá errores y generará un ZIP listo para usar.

**Tiempo estimado:** 15-30 minutos

**Instrucciones:**

- Asegúrate de tener instalado para ejecutar el proyecto: Un IDE o editor de código.
- Copia todo el contenido del campo **Código Base** de este reto — incluyendo el texto de instrucciones que aparece al inicio.
- Abre un asistente de IA (Claude en claude.ai, ChatGPT o Gemini — se recomienda Claude), pega el contenido copiado en el chat y envíalo.
- El asistente analizará los archivos, corregirá errores y generará un archivo ZIP descargable. Descárgalo y extráelo en la carpeta donde quieras trabajar.
- Verifica que el proyecto arranca sin errores.

**Entregable:** El proyecto compila/arranca sin errores.

<details>
<summary>Pistas de conocimiento</summary>

- Copia el Código Base completo incluyendo el texto de instrucciones al inicio — esas instrucciones le indican al asistente exactamente qué hacer con los archivos.
- Si el asistente no genera el ZIP automáticamente al terminar el análisis, escríbele: "genera el ZIP ahora".
- Si el proyecto tiene errores al arrancar, comparte el mensaje de error con el mismo asistente para que lo corrija.

</details>

### Fase 1: Exploración del Dominio

**Objetivo:** Identificar y documentar las necesidades y restricciones del dominio de gobierno de datos en DataCorp.

**Tiempo estimado:** 3 horas

**Instrucciones:**

- Investiga y documenta las necesidades específicas de DataCorp en términos de gobierno de datos.
- Identifica y enumera las restricciones y ambigüedades presentes en el dominio.
- Describe cómo distinguir entre restricciones relevantes y triviales.

**Entregable:** Documento que detalla las necesidades y restricciones del dominio de gobierno de datos en DataCorp.

<details>
<summary>Pistas de conocimiento</summary>

- Considera los estándares DAMA, TOGAF y CMMI.
- Analiza casos de uso y ejemplos de la industria.

</details>

### Fase 2: Evaluación de Decisiones de Diseño

**Objetivo:** Evaluar y documentar una decisión controversial en el diseño del marco de gobierno de datos.

**Tiempo estimado:** 5 horas

**Instrucciones:**

- Selecciona una decisión controversial en el diseño del marco de gobierno de datos.
- Documenta el contexto, las fuerzas en juego, las opciones disponibles, sus pros y contras, la decisión tomada y las consecuencias.
- Defiende tu decisión con argumentos sólidos.

**Entregable:** Registro de decisiones que detalla una decisión controversial en el diseño del marco de gobierno de datos.

<details>
<summary>Pistas de conocimiento</summary>

- Considera trade-offs entre calidad, integridad y disponibilidad de los datos.
- Analiza los impactos en diferentes partes interesadas.

</details>

### Fase 3: Comunicación a Diferentes Audiencias

**Objetivo:** Comunicar el marco de gobierno de datos a audiencias con diferentes niveles de abstracción.

**Tiempo estimado:** 4 horas

**Instrucciones:**

- Prepara una presentación técnica del marco de gobierno de datos para el equipo de ingeniería.
- Crea una presentación de alto nivel para la dirección ejecutiva que destaque los beneficios y la importancia del marco.
- Asegura que cada presentación sea clara y que la audiencia pueda tomar decisiones sin pedir aclaraciones.

**Entregable:** Dos presentaciones: una técnica para el equipo de ingeniería y una de alto nivel para la dirección ejecutiva.

<details>
<summary>Pistas de conocimiento</summary>

- Utiliza ejemplos concretos y casos de uso para ilustrar los conceptos.
- Considera el lenguaje y el nivel de detalle apropiado para cada audiencia.

</details>

### Fase 4: Revisión y Optimización

**Objetivo:** Revisar y optimizar el marco de gobierno de datos basado en retroalimentación y mejores prácticas.

**Tiempo estimado:** 3 horas

**Instrucciones:**

- Recopila retroalimentación de las presentaciones realizadas en la fase anterior.
- Identifica áreas de mejora y propone optimizaciones al marco de gobierno de datos.
- Documenta las mejoras y justifica tus decisiones.

**Entregable:** Documento que detalla las mejoras propuestas y las justificaciones para el marco de gobierno de datos.

<details>
<summary>Pistas de conocimiento</summary>

- Considera las mejores prácticas en gobierno de datos.
- Analiza la retroalimentación recibida y prioriza las áreas de mejora.

</details>

## Dimensiones Evaluadas

- **queEs**: ¿Qué es un marco de gobierno de datos y por qué es importante para DataCorp?
- **paraQueSirve**: ¿Para qué sirve el marco de gobierno de datos en el contexto de DataCorp?
- **comoSeUsa**: ¿Cómo se usa el marco de gobierno de datos en proyectos reales?
- **erroresComunes**: ¿Cuáles son los errores comunes al implementar un marco de gobierno de datos y cómo se pueden evitar?
- **queDecisionesImplica**: ¿Qué decisiones clave implica el diseño y la implementación de un marco de gobierno de datos?

## Criterios de Evaluacion

- Identificación y documentación de las necesidades y restricciones del dominio de gobierno de datos.
- Evaluación y documentación de una decisión controversial en el diseño del marco de gobierno de datos.
- Comunicación efectiva del marco de gobierno de datos a diferentes audiencias.
- Revisión y optimización del marco de gobierno de datos basada en retroalimentación y mejores prácticas.

## Como trabajar con un asistente de IA

Hay dos caminos, elegi uno:

- **AGENTS.md** (recomendado) — instrucciones nativas del repo. Abri esta carpeta con tu agente local (Claude Code, Cursor, Codex, Copilot, Gemini) y las carga solo. Sabe que archivos faltan y con que comando se verifica, y completa el scaffold escribiendo en disco.
- **PROMPT_MEJORA.md** — para copiar y pegar en un chat (claude.ai, ChatGPT). Devuelve un ZIP con el proyecto. Sirve si no tenes un agente en el IDE.

Ninguno de los dos resuelve las fases del reto: eso es tu trabajo.

## Verificacion

El proyecto esta listo para trabajar cuando este comando corre sin errores:

```bash
pip install -r requirements.txt && pytest -q
```

---

*Reto generado automaticamente por Challenge Generator - Pragma*
