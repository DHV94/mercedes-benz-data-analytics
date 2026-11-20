# Registro de decisiones / Decision log

> Cada decisión relevante, con las **alternativas que se descartaron y por qué**. Es material directo para la diapositiva de "toma de decisiones" de la exposición.
> Formato: ADR simplificado (contexto → opciones → decisión → consecuencias). Estados: ✅ tomada · ⏳ pendiente · ❌ descartada.
> Se mantiene en el repositorio (versionado). Para pasarlo a Google Drive o Word, basta copiarlo o pedir su exportación.

---

## Índice

| ID | Fecha | Decisión | Estado |
|---|---|---|---|
| D-001 | 2026-11-17 | Enfoque de datos híbrido (ventas simuladas + NHTSA real) | ✅ |
| D-002 | 2026-11-17 | Descartar la predicción de ventas por región | ❌ |
| D-003 | 2026-11-17 | Reformular la pregunta de ciberseguridad | ✅ |
| D-004 | 2026-11-17 | dbt Cloud "Latest" (v1.x) y cuenta nueva | ✅ |
| D-005 | 2026-11-17 | Repositorio aparte, sin el material del curso | ✅ |
| D-006 | 2026-11-17 | Flujo de ramas y commits (Conventional Commits, sin fecha) | ✅ |
| D-007 | 2026-11-17 | Idioma: código en inglés, documentación bilingüe | ✅ |
| D-008 | 2026-11-17 | Arquitectura medallion y prefijo `MB` en Snowflake | ✅ |
| D-009 | 2026-11-17 | Cada región entrega en un formato distinto | ✅ |
| D-010 | 2026-11-18 | Volumen: muestra de ~100.000 ventas | ✅ |
| D-011 | 2026-11-18 | Precio en moneda local, conversión a EUR | ✅ |
| D-012 | 2026-11-18 | Impuestos: guardar bruto y neto, informar en neto | ✅ |
| D-013 | 2026-11-18 | Mercados: añadir Corea, dejar fuera India y otros | ✅ |
| D-014 | 2026-11-18 | Consumo semanal los martes por la mañana | ✅ |
| D-015 | 2026-11-17 | Registro automático de tokens con un hook | ✅ |
| D-016 | 2026-11-17 | Cambio de Opus 5.5 a Sonnet 5.5 | ✅ |
| D-017 | 2026-11-19 | Reducir a 5 casos de uso, sencillos y visuales | ✅ |
| D-018 | 2026-11-18 | Coche de sustitución, leasing y renting como forma de adquisición | ❌ (descartada 2026-11-20) |
| D-019 | 2026-11-20 | Casos de uso definitivos (UC1–UC5), sustituye a D-017 | ✅ |
| D-020 | 2026-11-20 | No calcular ratios de revisiones reales sobre ventas simuladas | ✅ |
| D-021 | 2026-11-20 | Una fuente de extremo a extremo primero; Europa, EE. UU. y China como núcleo | ✅ |
| D-022 | 2026-11-20 | Incremental de la ingesta a Gold solo donde tenga sentido, con pruebas de idempotencia | ✅ |
| D-023 | 2026-11-20 | Snapshot SCD2 sobre concesionarios | ✅ |
| D-024 | 2026-11-20 | Nuevo calendario: exposición el jueves 26, tercer turno | ✅ |
| D-025 | 2026-11-20 | Trabajo en dos sesiones (Claude y ChatGPT) con un fichero de relevo | ✅ |
| D-026 | 2026-11-20 | Ventana de análisis 2021–2025 para UC1–UC3 | ✅ (justificación ⏳) |
| D-027 | 2026-11-20 | El modelo dimensional lo diseña el usuario primero, con un ejercicio | ✅ |
| D-028 | 2026-11-20 | Cada commit se entrega con mensaje y explicación | ✅ |
| D-029 | 2026-11-20 | Flujo de ramas feature → develop → pre → main | ✅ |

---

## D-001 · Enfoque de datos híbrido
- **Contexto**: no existen datos públicos de ventas de Mercedes-Benz a nivel de transacción con carrocería, propulsión y región.
- **Opciones**: (a) usar un dataset de Kaggle de coches de segunda mano; (b) solo cifras agregadas de notas de prensa; (c) ventas simuladas calibradas con cifras públicas, más datos reales de revisiones.
- **Decisión**: (c).
- **Por qué**: (a) no son ventas de la marca y no tienen carrocería ni región; (b) no permite construir un modelo dimensional ni limpiar nada. (c) da control sobre la suciedad y las fuentes, como un proyecto real.
- **Consecuencias**: hay que decir claramente en la exposición que las ventas son simuladas.

## D-002 · Descartar la predicción de ventas por región
- **Contexto**: idea inicial del usuario: qué modelos se venderían mejor por región.
- **Decisión**: descartada; queda como trabajo futuro.
- **Por qué**: es trabajo de ciencia de datos, no de ingeniería de datos, y no se ha visto en el curso. Con 7 días, mejor un proyecto cerrado y sólido.

## D-003 · Reformular la pregunta de ciberseguridad
- **Contexto**: "¿los pentesting y certificaciones nos hacen coches más seguros?".
- **Decisión**: reformulada como evolución de las revisiones por fallos de software/electrónica frente a mecánicos.
- **Por qué**: la pregunta original es de causa y efecto y no hay datos que la respalden. La versión reformulada es honesta y se responde con datos públicos.

## D-004 · dbt Cloud "Latest" (v1.x) y cuenta nueva
- **Opciones**: v1 Latest o v2 (motor Fusion); cuenta antigua o nueva; dbt Core local.
- **Decisión**: v1 Latest, cuenta nueva (alias de Gmail `+dbt`).
- **Por qué**: la v2 cambia cosas y algunos paquetes pueden dar problemas; el plan gratuito solo admite un proyecto, que ocupa el de prácticas; el trial da CI y jobs. Core local obliga a aprender un entorno nuevo.

## D-005 · Repositorio aparte, sin el material del curso
- **Por qué**: lo verán evaluadores y posibles empleadores; las diapositivas son material del curso y publicarlas podría no estar permitido. El repo del curso se usa solo como referencia de convenciones.

## D-006 · Ramas y commits
- **Opciones**: fecha delante del mensaje (idea del usuario) o Conventional Commits.
- **Decisión**: Conventional Commits en inglés (`feat(scope): ...`), **sin fecha**; ramas `main`/`develop`/`feature/*` con pull requests; versiones con tags SemVer (`alpha`, `beta`).
- **Por qué**: Git ya guarda la fecha de cada commit; repetirla no aporta información.

## D-007 · Idioma
- **Decisión**: código, columnas, modelos, ramas y commits en inglés; documentación en español e inglés. Simula un equipo internacional.

## D-008 · Arquitectura medallion y prefijo `MB`
- **Decisión**: bronze → silver → gold con una base de datos por capa y entorno (DEV/PRE/PRO), igual que el curso, con prefijo `MB` para no mezclarse con los objetos de las prácticas en la misma cuenta.

## D-009 · Cada región entrega en un formato distinto
- **Decisión**: Europa (CSV `;`), EE. UU. (CSV `,`), China (JSON), Japón (CSV Shift-JIS), Corea (CSV tabulador CP949).
- **Por qué**: es lo que ocurre en una multinacional y justifica la limpieza y unificación en staging/silver.

## D-010 · Volumen
- **Decisión**: unas 100.000 ventas de 2021 a 2025 (inicialmente 2019–2025, ver D-026), presentadas como muestra de demostración.
- **Por qué**: más filas no aportan nada y ralentizan Power BI.

## D-011 · Moneda
- **Decisión**: se conserva el precio en moneda local y se convierte con un seed de tipos de cambio (EUR como moneda principal; EUR, GBP, CHF, USD, CNY, JPY, KRW).
- **Alternativa descartada**: guardar todo ya en EUR (pierde realismo y trabajo de modelado).

## D-012 · Impuestos
- **Propuesta inicial (descartada)**: no normalizar y solo documentarlo como limitación.
- **Decisión**: guardar `gross_price`, `tax_rate` y `net_price` con un seed `tax_rates` con fechas de validez; los informes usan neto.
- **Por qué**: el IVA no es ingreso de la compañía y los orígenes no son comparables entre sí.

## D-013 · Mercados
- **Decisión**: Europa (DE, FR, IT, ES, GB, CH), EE. UU., China, Japón y Corea. Fuera: India, Canadá, México, Australia.
- **Por qué**: China, Europa y EE. UU. concentran la mayor parte de las ventas de Mercedes y Corea fue en 2025 la segunda marca importada. India es el tercer mercado mundial pero pequeño para Mercedes. Corea se añadió a petición del usuario tras revisar las cifras públicas.

## D-014 · Consumo semanal
- **Decisión**: los directivos consultan los datos los martes por la mañana: carga el lunes, job programado de dbt Cloud de madrugada y vigilancia con `dbt source freshness`.

## D-015 · Registro de tokens
- **Decisión**: hook `Stop` de Claude Code que añade una línea a `logs/token_log.csv` tras cada respuesta. Documentado en `scripts/log_tokens.py`.

## D-016 · Modelo de IA
- **Decisión**: Sonnet 5.5 en esfuerzo medio, con Opus solo para decisiones de diseño difíciles. Consume menos límite de uso con calidad suficiente.

## D-017 · Cinco casos de uso (SUSTITUIDA por D-019)
- **Contexto**: la lista creció a 9 casos, algunos más técnicos que de negocio.
- **Opciones**: mantener los 9; reducir a pocos, sencillos y visuales.
- **Decisión**: 5 casos (ver `PROJECT_CONTEXT.md`, sección 3b). Los demás (forma de adquisición, ventas por país en EUR, calidad de datos) pasan a ser atributos, filtros o trabajo técnico, no casos de uso.
- **Por qué**: mejor pocos casos bien hechos y que se vean bien en un mapa de Power BI que muchos a medias; escalable en el futuro.

## D-018 · Coche de sustitución, leasing y renting ❌ (descartada el 2026-11-20)
- **Propuesta**: valor `replacement` en `acquisition_type` (unidad entregada sin ingreso, por garantía o campaña de revisión).
- **Decisión final (2026-11-20)**: descartada, junto con leasing, renting, `monthly_payment` y `contract_months`. El proyecto solo registra **ventas**.
- **Por qué**: simplificar. Estas formas de adquisición obligan a decidir qué cuenta como venta, añaden campos y reglas (precio 0, cuotas) y no aportan a los cinco casos de uso. Se menciona como ampliación futura.

## D-019 · Casos de uso definitivos (2026-11-20)
- **Contexto**: tras revisar casos de uso, alcance y las indicaciones de los profesores con ChatGPT.
- **Decisión**: UC1 evolución por familia de modelo (2021–2025); UC2 por carrocería; UC3 por propulsión; UC4 top 3 de familias por región en 2025; UC5 campañas de revisión por software/electrónica frente a mecánicas, por modelo y año. UC1–UC4 en una sección comercial con mapa interactivo; UC5 en una sección aparte, sin mapa.
- **Descartado por ahora**: top de modelos menos vendidos (el caso 4 de D-017) y predicciones de ventas.
- **Por qué**: menos casos, mejor hechos. UC5 no lleva mapa porque la NHTSA solo cubre EE. UU.
- **Consecuencia**: hay que distinguir **familia** de modelo y **variante**, y definir el grano de cada tabla.

## D-020 · Sin ratios de revisiones reales sobre ventas simuladas
- **Contexto**: la idea de "revisiones por cada 1.000 unidades vendidas" por modelo.
- **Decisión**: descartada.
- **Por qué**: dividir datos reales entre datos simulados da una cifra que parece real y no lo es. Es engañoso y indefendible en una exposición.

## D-021 · Una fuente de extremo a extremo primero
- **Opciones**: construir las cinco regiones a la vez, o una fuente completa y luego ampliar.
- **Decisión**: núcleo Europa, EE. UU. y China; Japón y Corea (solo diseñados en papel) se evalúan después, sin rehacer trabajo.
- **Por qué**: pocas funcionalidades bien hechas valen más que muchas a medias, y queda poco tiempo.
- **Consecuencia**: revisa D-013 (mercados); el diseño de Corea y Japón queda como ampliación.

## D-022 · Estrategia incremental
- **Decisión**: incremental desde la ingesta hasta Gold, sin full-refresh rutinario de Gold. No se impone materialización incremental a todas las tablas: solo donde tenga sentido (por ejemplo, tablas de hechos grandes; las dimensiones pequeñas pueden ser tablas normales).
- **Demostración exigida**: lotes reproducibles; ejecutar el proceso dos veces sin duplicados; un segundo lote con datos nuevos o modificados; recuentos SQL antes y después.

## D-023 · Snapshot SCD2 sobre concesionarios
- **Decisión**: snapshot del maestro de concesionarios (cambios de nombre, cierres).
- **Por qué**: es una de las pruebas de lo aprendido que piden los profesores y el maestro ya contempla cambios a propósito.

## D-024 · Calendario
- **Cambio**: la exposición pasa al **jueves 26**, en tercer lugar (antes: miércoles 25, primer día).
- **Decisión**: se mantiene el objetivo interno de código estable el martes 24 hacia las 20:00; el miércoles es para documentación, entrega y ensayo.
- **Pendiente**: canal de envío del repositorio y las diapositivas (preguntar al profesorado).

## D-025 · Dos sesiones de trabajo (Claude y ChatGPT)
- **Decisión**: `docs/SESSION_NOTES.md` es el fichero de relevo. Toda sesión debe leerlo al empezar y actualizarlo antes del último commit. El orden de lectura está en el propio fichero.
- **Por qué**: evita depender de la memoria de una conversación y permite retomar el trabajo desde cualquiera de las dos herramientas.
- **Complemento**: `docs/HANDOFF_PROMPT.md` contiene el mensaje para pegar al empezar una sesión nueva.

## D-026 · Ventana de análisis 2021–2025
- **Decisión**: UC1, UC2 y UC3 cubren 2021–2025 (UC4 solo 2025). En Power BI se valorará si cada vista es de un año o de toda la ventana, con un selector de año.
- **Justificación narrativa (pendiente de cerrar)**: cinco años de histórico como base para planificar los cinco siguientes, por ejemplo en una revisión estratégica a finales de 2026, o en una reunión celebrada en el primer cuatrimestre de 2026.
- **Decidido (2026-11-20)**: se generan datos solo de **2021 a 2025**, sin 2020.
- **Por qué**: no se hacen comparaciones con años anteriores al ciclo; menos filas y un calendario más pequeño. Contrapartida aceptada: no hay variación interanual de 2021 (sí desde 2022).

## D-027 · El usuario diseña el modelo dimensional primero
- **Opciones**: que Claude proponga el modelo y el usuario lo revise; o que el usuario lo diseñe con un enunciado y Claude lo corrija.
- **Decisión**: la segunda, con `docs/es/exercise_dimensional_model.md`, en el formato de los ejercicios del curso (silver conceptual/lógico/físico y gold por preguntas).
- **Por qué**: el usuario debe poder explicar y defender el esquema estrella; diseñarlo es la mejor forma de entenderlo.

## D-028 · Commits explicados
- **Decisión**: cada vez que toque un commit, el asistente entrega el mensaje listo para pegar (Conventional Commits, en inglés) y una explicación en español de qué hace cada fichero y por qué. El usuario hace los commits a mano y puede copiar la explicación a la descripción.
- **Por qué**: entender en todo momento qué contiene cada commit, para poder defender el historial.

## D-029 · Flujo de ramas con tres entornos
- **Opciones**: `feature` → `develop` → `main`; o añadir una rama `pre`.
- **Decisión**: `feature/*` → `develop` (DEV) → `pre` (PRE) → `main` (PRO).
- **Por qué**: replica los tres entornos DEV/PRE/PRO del curso y permite enseñar la promoción entre entornos. Coste: más merges, así que se usa `pre` solo cuando `develop` esté estable.
