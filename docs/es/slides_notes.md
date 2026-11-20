# Notas para las diapositivas

> Archivo vivo. Cada día se añade lo que se haya terminado y las capturas que haya que guardar.
> Las secciones **«Mis notas»** son para ti: lo que quieras decir con tus palabras.

## 1. Datos de la presentación

| Dato | Valor |
|---|---|
| Fecha y turno | **Jueves 26 de noviembre de 2026, tercer turno** |
| Duración | 10 minutos objetivo, 15 máximo |
| Entrega | Repositorio y diapositivas **antes** de presentar. Canal sin confirmar: **preguntar al profesorado** |
| Demo | Sí, si es posible. Alternativa: capturas y un vídeo corto de respaldo |
| Extras | Meme con un perro (solo si encaja de forma natural) · coche Mercedes en miniatura · pizarra de clase si ayuda |

## 2. Guion por diapositiva (≈ 12 min)

| # | Diapositiva | Min | Mensaje clave |
|---|---|---|---|
| 1 | Portada | 0:20 | Título, nombre, formación |
| 2 | Motivación | 1:00 | Por qué Mercedes-Benz y por qué este proyecto |
| 3 | Contexto de negocio y casos de uso | 1:30 | El problema y las 5 preguntas (UC1–UC5) |
| 4 | Cómo llegamos a la solución | 1:30 | Decisiones tomadas y descartadas (ver §3) |
| 5 | Datos y arquitectura | 1:30 | Fuentes simuladas + reales, bronze → silver → gold |
| 6 | Grano y modelo dimensional | 2:00 | Esquema estrella, hechos y dimensiones, por qué no se duplica |
| 7 | Demo técnica | 2:30 | Incremental (2 ejecuciones sin duplicados, 2º lote), snapshot SCD2, tests y alertas |
| 8 | Resultados en Power BI | 1:30 | Mapa interactivo (UC1–UC4) y sección de revisiones (UC5) |
| 9 | Aprendizajes, limitaciones y futuro | 1:00 | Qué haría distinto y qué se puede ampliar |
| 10 | Cierre y preguntas | 0:20 | Agradecimiento |

### Mis notas por diapositiva
- **2 · Motivación:**
- **3 · Contexto:**
- **4 · Decisiones:**
- **5 · Arquitectura:**
- **6 · Modelo:** (aquí explicaré el grano de cada tabla con mis palabras)
- **7 · Demo:**
- **8 · Resultados:**
- **9 · Aprendizajes:**

## 3. Decisiones destacadas para la diapositiva 4

Elige 4 o 5; el detalle está en `docs/es/decisions_log.md`.

| Decisión | Alternativa descartada | Por qué |
|---|---|---|
| Datos híbridos: ventas simuladas + revisiones reales (D-001) | Dataset de segunda mano de Kaggle | No son ventas de la marca ni tienen carrocería ni región |
| No dividir revisiones reales entre ventas simuladas (D-020) | Ratio de revisiones por cada 1.000 ventas | Mezclar real con simulado da una cifra engañosa |
| Una fuente de extremo a extremo antes de ampliar (D-021) | Construir las cinco regiones a la vez | Pocas funcionalidades bien hechas |
| Precio sin impuestos y en EUR, conservando el bruto (D-011, D-012) | Guardar todo ya en EUR | Los orígenes no son comparables entre sí |
| Predicción de ventas fuera de alcance (D-002) | Modelo predictivo | Es ciencia de datos, no ingeniería de datos |
| Flujo `feature` → `develop` → `pre` → `main` (D-029) | Solo `develop` y `main` | Replica los tres entornos DEV/PRE/PRO |

## 4. Evidencias que hay que guardar (capturas)

Guarda cada captura el día que funcione; es lo más difícil de recuperar al final.

- [ ] Script de Snowflake ejecutado (las 7 bases de datos)
- [ ] Carga en bronze con `COPY INTO` (y recuento de filas)
- [ ] Linaje de dbt (el grafo de modelos)
- [ ] Tests de dbt en verde y uno fallando a propósito (aviso)
- [ ] Recuento antes y después: primera ejecución, segunda ejecución sin cambios, segundo lote
- [ ] Snapshot SCD2 de concesionarios con dos versiones de un mismo concesionario
- [ ] Job programado de dbt Cloud (martes por la mañana)
- [ ] Diagrama del modelo dimensional
- [ ] Informe de Power BI (mapa y sección de revisiones)
- [ ] Historial de ramas y pull requests en GitHub

## 5. Ideas sueltas
-

## 6. Preguntas para el profesorado
- ¿Por qué canal se envían el repositorio y las diapositivas, y hasta cuándo?
- ¿Se puede usar la pizarra de clase durante la exposición?
- ¿Hay que hacer demo en directo o basta con capturas?
