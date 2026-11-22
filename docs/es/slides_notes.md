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

## 2. Bloques de contenido (≈ 12 min)

> No es una diapositiva por bloque ni por minuto: el diseño es libre. Un bloque puede ocupar varias diapositivas o varios bloques compartir una. Los minutos son solo orientativos. El diseño final lo haces tú a mano cuando el contenido esté cerrado.

| # | Bloque | Min | Mensaje clave |
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

### Mis notas por bloque
- **2 · Motivación:**
- **3 · Contexto:**
- **4 · Decisiones:**
- **5 · Arquitectura:**
- **6 · Modelo:** (aquí explicaré el grano de cada tabla con mis palabras)
- **7 · Demo:**
- **8 · Resultados:**
- **9 · Aprendizajes:**

## 2b. Apertura (borrador, 2026-11-21)

Idea del usuario, con ajustes sugeridos. Duración objetivo: **1,5–2 minutos** de los 10–15.

1. **Gancho (10 segundos)**: un comentario de broma corto y seguro. Posible apoyo visual: el **coche Mercedes en miniatura** sobre la mesa.
2. **Motivación personal**: «desde pequeño me gustan los coches». Conecta de forma natural con el coche en miniatura.
3. **Modelo de negocio**: cuántos coches vende Mercedes-Benz y **por qué importa este trabajo ahora**: el cambio de motores (combustión, híbridos, eléctricos).
4. **La pregunta inicial**: de ahí salen los casos de uso. La **carrocería** se explica porque era la pregunta original (qué se vende mejor y dónde); la propulsión, por el cambio de motores.

Datos de contexto ya encontrados (de la web de Mercedes-Benz Group y prensa, ventas de 2025; **comprobar antes de usarlos**): unos 2,16 millones de turismos y furgonetas en total, unos 1,8 millones de turismos; China fue el mayor mercado (~552.000 unidades, ~31 % de los turismos). Fuente: `group.mercedes-benz.com/company/news/sales-2025.html`.
Para el cambio de motores, busca una cifra o una norma europea concreta y compruébala; no la doy por buena de memoria.

Sugerencias:
- No ocupes más de 2 minutos: el tribunal espera ver la parte técnica.
- El **meme del perro** puede encajar mejor más adelante, en el bloque de limpieza de datos («cuando el fichero llega con el VIN vacío»), que al inicio.
- Cierra la apertura con una frase puente: «con esta pregunta, construí esto».

### Mis notas de la apertura
- Broma:
- Frase personal:

## 2c. Explicar modelo, familia, carrocería y propulsión (obligatorio en la presentación)

Una diapositiva corta con un ejemplo, porque el tribunal no conoce el vocabulario del automóvil:

| Concepto | Qué es | Ejemplo |
|---|---|---|
| **Familia** | Gama comercial de coches parecidos | Clase C, Clase A, GLA |
| **Modelo** (variante) | Versión concreta que se vende: familia + motor | C 220 d, C 200, GLA 250 e |
| **Carrocería** | Forma del coche | Sedán, compacto, SUV, todoterreno |
| **Propulsión** | Cómo se mueve | Combustión (gasolina/diésel), híbrido enchufable, eléctrico |
| **Año modelo** | Año de la edición del coche (no el de la venta) | Un 2024 puede venderse en 2023 |

Frase clave: «una familia tiene muchos modelos; un modelo tiene una carrocería y una propulsión; una venta es de un modelo». Las revisiones (recalls) se publican por familia y año modelo, no por VIN: por eso la tabla de líneas de campaña apunta a la familia.
Dibujo sugerido: Clase C → C 220 d (sedán, diésel) y C 300 e (sedán, híbrido enchufable).

## 2d. Diseño de las diapositivas
- Google Slides, con tonos de Mercedes-Benz: negro, plata/grises y blanco, con un acento frío. Buscar una paleta pública; si no, que la proponga ChatGPT. No usar el logotipo como decoración excesiva.

## 3. Decisiones destacadas para la diapositiva 4

Elige 4 o 5; el detalle está en `docs/es/decisions_log.md`.

| Decisión | Alternativa descartada | Por qué |
|---|---|---|
| Datos híbridos: ventas simuladas + revisiones reales (D-001) | Dataset de segunda mano de Kaggle | No son ventas de la marca ni tienen carrocería ni región |
| No dividir revisiones reales entre ventas simuladas (D-020) | Ratio de revisiones por cada 1.000 ventas | Mezclar real con simulado da una cifra engañosa |
| Una fuente de extremo a extremo antes de ampliar (D-021) | Construir las cinco regiones a la vez | Pocas funcionalidades bien hechas |
| Precio sin impuestos y en EUR, conservando el bruto (D-011, D-012) | Guardar todo ya en EUR | Los orígenes no son comparables entre sí |
| Predicción de ventas fuera de alcance (D-002) | Modelo predictivo | Es ciencia de datos, no ingeniería de datos |
| Estrella pura: `family_id` también en el hecho, sin copo de nieve (D-059) | `dim_family` colgando de `dim_model` | Menos joins y una dimensión compartida entre ventas y campañas |
| Flujo `feature/*` → `develop` → `main`, sin rama `pre` (D-038) | `feature/*` → `develop` → `pre` → `main` | Cada tarea aislada, con dos entornos (DEV y PRO); un tercero cuesta más de lo que aporta |
| Revisiones NHTSA desde fichero plano, no desde la API (D-033) | API de la NHTSA | Tiempo del proyecto: una descarga reproducible en lugar de construir y probar una extracción; sin dependencia externa en la demo |

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

## 7. Explicar el VIN (número de bastidor)

**Qué es.** *Vehicle Identification Number*: código de **17 caracteres** que identifica a un vehículo de forma única, como su huella dactilar (norma ISO 3779). No usa las letras `I`, `O` ni `Q`, para no confundirlas con `1` y `0`.

**Cómo se trocea.**

| Posiciones | Parte | Qué dice |
|---|---|---|
| 1–3 | WMI | Fabricante y país (en Mercedes, por ejemplo, `WDD`, `W1K` o `W1N`) |
| 4–9 | VDS | Características: modelo, carrocería, motor. La posición 9 es un dígito de control en Norteamérica |
| 10 | Año modelo | Una letra: 2021 = `M`, 2022 = `N`, 2023 = `P`, 2024 = `R`, 2025 = `S` |
| 11 | Planta | Dónde se fabricó |
| 12–17 | Nº de serie | Identifica la unidad |

**Por qué importa en el proyecto.**
- Es la **clave natural** de una venta. Ojo: un mismo VIN puede aparecer más de una vez (venta, devolución y nueva venta), así que hay que pensar si `vin` es único en la tabla de hechos. Tema del ejercicio de modelado.
- Es un **defecto de calidad** típico (D04): longitud distinta de 17, vacío o con `I`, `O`, `Q`. Se puede validar en staging.
- **No sirve para cruzar ventas con las revisiones de la NHTSA**: las campañas se publican por modelo y año, no por VIN.
- Puede ser un **dato sensible**: si se puede vincular a un propietario, se trata como dato personal. Encaja con el apartado de ciberseguridad (por ejemplo, una *masking policy* en Snowflake).
- Nuestros VIN de ejemplo son **ficticios** y no siguen la estructura real. Decidir si el generador crea VIN con estructura válida (más realista, algo más de trabajo).

**Idea de diapositiva:** un VIN troceado en colores con una flecha a cada parte.

> Antes de poner estos datos en una diapositiva, compruébalos con una fuente fiable.

## Anécdotas reales para la presentación (con capturas numeradas en `docs/evidence/README.md`)
1. **Usuario en mayúsculas (capturas 01-02)**: Snowflake convierte a mayúsculas los nombres sin comillas; el usuario `dhv994` hay que escribirlo entre comillas. Diagnóstico con `current_user()`.
2. **Subida sin carpeta (capturas 05-08)**: el `COPY INTO` decía «0 files processed»; el `list` del stage mostró los ficheros en la raíz en vez de en `batch_1/`. Se diagnosticó con capturas y se corrigió (09-12). Mensaje: leer el estado antes de tocar nada.
3. **Cifras que cuadran (capturas 11-14)**: 44.733 filas cargadas, 44.072 ventas distintas (661 duplicados puestos a propósito) y 128 concesionarios.
