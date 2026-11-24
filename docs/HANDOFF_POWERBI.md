# Traspaso para la sesión de Power BI (PC de trabajo)

Copia el texto de la sección «Prompt» en una sesión nueva de Claude abierta **dentro de este repositorio**. Esa sesión no tiene la conversación de casa, así que esto le da el contexto mínimo. Antes, haz `git pull` de `main` (o de `develop`) para tener todo.

## Prompt (copiar y pegar)

```
Lee primero CLAUDE.md y docs/SESSION_NOTES.md (estado real del proyecto). Hoy trabajamos SOLO en Power BI.

Contexto: proyecto final de Data Engineering (plataforma de datos simulada de Mercedes-Benz: Snowflake + dbt Cloud + Power BI). Está terminado el gold en PRO: base PRO_MB_GOLD_DB, esquema SALES, con fct_sales, fct_campaign_line, dim_date, dim_model, dim_family, dim_dealer, dim_tax y dim_component (estrella; dim_family compartida por los dos hechos). La guía completa de conexión, relaciones, medidas DAX y páginas del informe está en docs/es/powerbi_guide.md: síguela.

Cómo quiero que trabajes (acuerdo del repositorio, CLAUDE.md):
- Guíame paso a paso y explícame el porqué de cada cosa; yo tengo que poder defender cada pieza en una presentación oral. Pasos cortos, una cosa a la vez, sin menús largos. Al terminar un bloque importante hazme una pregunta de comprobación.
- Idioma del chat: español.
- No pongas secretos en el repositorio (cuentas, usuarios, claves, .pbix con credenciales).
- Tú NO haces push, PR ni merge. Puedes crear commits locales solo después de explicarme en español qué contienen. Nunca añadas coautoría ni atribución de Claude en los commits.
- Las capturas que te pase son evidencias: guárdalas en docs/evidence/ con número correlativo (la siguiente es la 61; mira docs/evidence/README.md) y un nombre descriptivo en español, y añade su fila al índice.

Qué hacer hoy, en orden:
1. Comprobar la conexión a Snowflake desde Power BI (rol MB_REPORTING_ROLE, almacén WH_MB, PRO_MB_GOLD_DB.SALES). Si falla, usar el Plan B con CSV de la guía.
2. Importar las 8 tablas y crear las relaciones (la relación de delivery_date_id es inactiva a propósito).
3. Crear las medidas DAX de la guía. Aviso: NO sumar importes de países distintos (hay EUR, GBP y CHF sin tipo de cambio) y NO sumar units_affected.
4. Montar las páginas: Ventas, Defectos (campañas NHTSA) y, si hay tiempo, Calidad del dato.
5. Hacer capturas de cada página para las diapositivas y guardar el .pbix en mi Drive.

Cifras de control (deben coincidir): fct_sales 44.382 filas (tras el delta 2), 78 con sale_date_id = -1, 212 sin dealer_id, 78 sin tax_id; fct_campaign_line 525 líneas y 141 campañas; dim_component 100; dim_family 23.
```

## Preguntas para clase
Están preparadas en `docs/es/class_questions.md` (dos principales y cinco de apoyo, con la respuesta que defiendo). Anota ahí lo que te contesten.

## Después de la sesión de Power BI
- Sube las capturas y el índice de evidencias (git: tú haces push/PR).
- Anota en `docs/SESSION_NOTES.md` qué se hizo y qué falta.
