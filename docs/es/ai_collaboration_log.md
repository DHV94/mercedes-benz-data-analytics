# Registro de colaboración con IA (material opcional para la presentación)

> Archivo vivo. Lo pidió el usuario el 2026-11-22: cada vez que la conversación con Claude se compacta (resume) se avisa y se anota aquí. Prioridad baja, pero sirve para mencionar el uso de IA en la presentación. Los tokens consumidos están en `logs/token_log.csv`.

## Cómo se ha trabajado con la IA
- Claude **guía y explica**; el usuario construye y decide. Las decisiones de proyecto son del usuario y se registran en `docs/es/decisions_log.md`.
- Claude escribe plantillas y el generador de datos (con explicación). Los commits locales los puede crear Claude tras explicarlos; push, PR y merge son siempre del usuario.
- Las preguntas de defensa y las decisiones descartadas se documentan para poder justificarlas en voz alta.

## Compactaciones de contexto
Una compactación ocurre cuando la conversación es demasiado larga: el contexto se resume y se continúa con el resumen. Se pierde detalle fino, por eso los acuerdos importantes viven en archivos del repositorio (`CLAUDE.md`, `SESSION_NOTES.md`, `decisions_log.md`).

| Fecha | Sesión | Qué ocurrió | Cómo se recuperó el contexto |
|---|---|---|---|
| 2026-11-22 | Modelado, Snowflake y generador | Primera compactación anotada en este registro (al menos una antes de empezar el registro) | Resumen + lectura de `SESSION_NOTES.md`, `decisions_log.md` y `defense_justifications.md` |

## Ideas para mencionar en la presentación
- La IA como asistente que explica y revisa, no como sustituto: el usuario defiende cada pieza.
- Trazabilidad: decisiones y alternativas descartadas por escrito (D-001 en adelante).
- Control de calidad humano: se comprobaron cifras externas y se corrigió a la IA cuando se equivocó (por ejemplo, el filtro de roles `'%_MB_%'`).
