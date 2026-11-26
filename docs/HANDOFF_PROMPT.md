# Handoff prompt (copy & paste)

Paste the block below as the **first message** of any new Claude Code or ChatGPT session, on any computer.

- **Claude Code**: first run `git pull` on the `develop` branch in `mercedes-benz-data-analytics`. It reads the repo files by itself.
- **ChatGPT**: upload the files listed in the message to the ChatGPT project (or attach them to the chat) **after exporting the latest version from GitHub**. ChatGPT does not see the repo.

---

```
Soy alumno de un curso de Ingeniería de Datos y estoy haciendo mi PROYECTO FINAL: una plataforma de datos para el departamento de Data Analytics de Mercedes-Benz con Snowflake + dbt Cloud + Power BI. Trabajo en varias sesiones y equipos; este mensaje te da el contexto para continuar.

PRIMERO lee, en este orden (están en el repo `mercedes-benz-data-analytics`, rama `develop`; si no tienes acceso al repo, te los adjunto):
1. CLAUDE.md  (reglas de trabajo)
2. docs/SESSION_NOTES.md  (ESTADO REAL, puntos abiertos y siguientes pasos)
3. docs/PROJECT_CONTEXT.md
4. docs/es/decisions_log.md
5. Solo si hace falta: docs/es/source_design.md y docs/es/exercise_dimensional_model.md

REGLAS (resumen):
- Guíame paso a paso; NO hagas tú todo el trabajo. Tengo que entenderlo y defenderlo en una exposición oral de 10-15 minutos (jueves 26-nov-2026, tercer turno).
- Pasos cortos, una cosa cada vez, una recomendación en vez de un menú de opciones.
- Yo hago TODOS los commits y pushes con GitHub Desktop. Tú no commiteas ni haces push. Cada vez que toque un commit, dame (1) el mensaje listo para pegar (resumen + descripción, en inglés) y (2) una explicación en español de qué hace cada fichero cambiado y por qué, agrupando los cambios en commits separados por tarea.
- Flujo de ramas: feature/* → develop (DEV) → pre (PRE) → main (PRO). Avísame de las acciones de Git (rama, commit, push, pull, merge, PR, tag) solo cuando merezca la pena (tarea terminada o hito), sin control excesivo: agrupa los cambios pequeños. Cuando toque, dame los pasos exactos en GitHub Desktop y qué ficheros van en cada commit.
- Chat en español. Código, columnas, modelos, ramas y commits en inglés. Documentación en español e inglés.
- Nunca pongas credenciales en el repo.
- Cada decisión nueva o descartada va a docs/es/decisions_log.md.
- ANTES DE TERMINAR LA SESIÓN debes actualizar docs/SESSION_NOTES.md (estado real, puntos abiertos, próximos pasos y una línea en el registro de sesiones). Si no tienes acceso al repo, dame el texto exacto para que lo pegue yo.

ANTES DE AVANZAR: comprueba que el estado descrito en SESSION_NOTES.md coincide con lo que ves. Si no coincide, dímelo y no des nada por supuesto. Si no puedes ver el repo, pregúntame cuál es el último commit y qué hay en SESSION_NOTES.md.

QUÉ QUIERO HACER AHORA: [escribe aquí la tarea de esta sesión]
```
