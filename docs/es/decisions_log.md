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
| D-029 | 2026-11-20 | Flujo de ramas feature → develop → pre → main | ✅ (parcial, ver D-030) |
| D-030 | 2026-11-20 | Solo develop, pre puntual | ❌ (sustituida por D-038) |
| D-031 | 2026-11-20 | Demos en directo en la exposición | ✅ |
| D-032 | 2026-11-20 | Revisiones NHTSA de 2021 a 2025, filtradas por fecha del informe | ✅ |
| D-033 | 2026-11-20 | NHTSA: descarga del fichero plano en lugar de la API | ✅ |
| D-034 | 2026-11-20 | Todo lo de datos bajo `data/` | ✅ |
| D-035 | 2026-11-20 | NHTSA: bronze completo, filtrado en silver | ✅ |
| D-036 | 2026-11-20 | Revisiones NHTSA opcionales, con punto de control | ⏳ |
| D-037 | 2026-11-20 | Alcance: solo turismos Mercedes-Benz; camiones, furgonetas y Maybach como ampliación | ✅ |
| D-038 | 2026-11-20 | Flujo feature → develop → main, sin rama pre ni pro | ✅ |
| D-039 | 2026-11-20 | UC5 limitado a EE. UU. y mostrado junto a las ventas de EE. UU. | ✅ |

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
- **Aclaración (2026-11-20)**: el precio neto se mantiene **en moneda local** y se convierte a EUR aparte (D-011). Silver guarda `sale_price_gross_local` (tal como llega), `tax_rate`, `sale_price_net_local` y `currency`; gold usa solo `sale_price_net_local` y `sale_price_net_eur`. Se conserva el bruto porque el neto es derivado: así se puede auditar y recalcular si cambia el seed. En EE. UU. el precio no incluye impuestos, así que bruto = neto (`tax_rate` = 0).

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
- **Ajuste (2026-11-20)**: los avisos de Git (commit, rama, PR) solo cuando merezca la pena: tarea terminada o hito. Sin control excesivo, para no perder tiempo.

## D-029 · Flujo de ramas con tres entornos (parcialmente sustituida por D-030)
- **Opciones**: `feature` → `develop` → `main`; o añadir una rama `pre`.
- **Decisión**: `feature/*` → `develop` (DEV) → `pre` (PRE) → `main` (PRO).
- **Por qué**: replica los tres entornos DEV/PRE/PRO del curso y permite enseñar la promoción entre entornos. Coste: más merges, así que se usa `pre` solo cuando `develop` esté estable.

## D-030 · Solo develop, pre puntual (2026-11-20) (sustituida por D-038)
- **Contexto**: trabajo individual y pocos días; las ramas `feature/*` añaden merges y PRs sin aportar nada.
- **Opciones**: mantener `feature/*` → `develop` → `pre` → `main`; o trabajar directamente en `develop`.
- **Decisión**: se trabaja directamente en `develop`; `pre` solo en hitos puntuales (promoción DEV→PRE); `main` para la entrega final.
- **Por qué**: ahorrar tiempo. Se mantiene la promoción entre entornos para enseñarla en la exposición.
- **Consecuencia**: sustituye en parte a D-029 (`feature/*` deja de ser obligatorio).

## D-031 · Demos en directo en la exposición (2026-11-20)
- **Contexto**: indicación nueva del profesorado: plantear acciones en directo (ingestas, automatización, incrementalidad).
- **Decisión**: una demo corta (unos 3 minutos): lote 1 y lote 2 (con datos nuevos y modificados), ejecución incremental y recuentos SQL antes y después. Automatización con una Task de Snowflake o un job programado de dbt Cloud (por confirmar con los profesores).
- **Por qué**: es lo que cabe en 10-15 minutos y demuestra lo que piden los profesores (incrementalidad, sin duplicados).
- **Plan B**: capturas o vídeo grabado por si falla algo en directo.
- **Pendiente**: preguntar a los profesores en clase (canal de entrega, automatización válida, qué esperan de la demo).

## D-032 · Revisiones NHTSA de 2021 a 2025 (2026-11-20)
- **Contexto**: las ventas cubren 2021–2025 (D-026). Si las revisiones cubrieran solo 2025, UC5 («evolución por año») no tendría sentido.
- **Opciones**: solo 2025; 2021–2025 filtrando por fecha del informe; 2021–2025 filtrando por año modelo.
- **Decisión**: se cargan las campañas de 2021 a 2025 filtrando por la **fecha del informe** (cuándo se publica la campaña), igual que la ventana de ventas. El año modelo del vehículo afectado se conserva como atributo y puede ser anterior a 2021.
- **Por qué**: son dos fechas distintas (una campaña de 2023 puede afectar a modelos de 2018). Filtrar por fecha del informe da la misma línea temporal que las ventas.

## D-033 · NHTSA: fichero plano en lugar de la API (2026-11-20)
- **Contexto**: la NHTSA ofrece los datos de revisiones como ficheros planos descargables y como API.
- **Opciones**: (a) API de la NHTSA; (b) descarga del fichero plano `FLAT_RCL_POST_2010.zip` y su descripción de campos `RCL.txt`.
- **Decisión**: (b), descarga manual del fichero plano, filtrado de Mercedes-Benz y 2021–2025, y carga como carga batch en Snowflake.
- **Por qué**: **el tiempo disponible para el proyecto**. Una API obliga a construir y probar la extracción (paginación, errores, límites de uso) y añade una dependencia externa en directo el día de la exposición. El fichero es una sola descarga, encaja con el stage + file format que ya se ve en el curso y es reproducible sin conexión.
- **Dónde se guardan** (ajustado el mismo día): en `data/nhtsa/raw/` se suben a Git el **zip** (15 MB) y `RCL.txt`. El fichero descomprimido (314 MB) **no** se sube, porque GitHub rechaza ficheros de más de 100 MB; se vuelve a generar descomprimiendo el zip. Si más adelante se necesita un extracto pequeño, irá en `data/nhtsa/`.
- **Consecuencia**: no hay actualización automática de revisiones. Se documenta como limitación y como mejora futura (pasar a la API).

## D-034 · Carpeta `data/` (2026-11-20)
- **Decisión**: todo lo relativo a datos vive bajo `data/`: `data/data_generator/` (simulador de las fuentes) y `data/nhtsa/` (fichero real).
- **Por qué**: un solo sitio para lo que son datos de entrada, separado del código dbt y de Snowflake.

## D-035 · NHTSA: bronze completo, filtrado en silver (2026-11-20)
- **Opciones**: (a) filtrar Mercedes-Benz antes de cargar; (b) cargar el fichero completo en bronze y filtrar después.
- **Decisión**: (b). Bronze guarda el fichero tal como llega (todas las marcas, desde 2010); el filtro (turismos Mercedes-Benz, informes de 2021 a 2025) se hace al pasar a silver.
- **Por qué**: bronze es una copia fiel del origen, y así el filtro queda en código dbt versionado y se puede cambiar sin volver a descargar. Los datos de otras marcas son públicos de la NHTSA y no plantean problema; el coste de almacenamiento es insignificante.
- **Alternativa válida (descartada)**: filtrar antes de cargar, justificando que no queremos datos de la competencia. Se descarta porque rompe la regla de bronze y obliga a un paso fuera de dbt.
- **Ojo**: el filtro no es un simple `= 'MERCEDES-BENZ'`. La marca aparece como `MERCEDES-BENZ`, `MERCEDES BENZ` y `MERCEDES-MAYBACH`; además hay camiones y autobuses de Daimler (Freightliner, Western Star, Thomas Built, Setra) que no son turismos, y equipos sueltos (`RCLTYPECD` distinto de `V`).

## D-036 · Las revisiones NHTSA son opcionales: punto de control (2026-11-20)
- **Contexto**: el fichero real es sucio y de grano distinto al de las ventas (campaña × modelo × año × componente, con `POTAFF` repetido en cada fila; el modelo viene con nombres como `GLS450` y `GLS 450`; el componente es un texto jerárquico). Puede complicar el proyecto más de lo que aporta.
- **Decisión**: de momento se incluye en el modelado. **Se revisa en cada sesión**; si consume demasiado tiempo, se descarta UC5 y las revisiones, y el proyecto se queda con las ventas (UC1–UC4).
- **Criterio para descartar**: si el miércoles 25 o antes el flujo de ventas de extremo a extremo (bronze → gold) no está estable, las revisiones salen.

## D-037 · Alcance: solo turismos (2026-11-20)
- **Contexto**: el fichero de la NHTSA incluye también furgonetas (Sprinter, Daimler Vans), camiones, autobuses y Maybach, algo que no se había planteado.
- **Opciones**: (a) cubrir todo el grupo Daimler/Mercedes; (b) centrarse en turismos de la marca Mercedes-Benz y decir expresamente que el resto queda fuera.
- **Decisión**: (b). El proyecto trata **turismos Mercedes-Benz**; camiones, furgonetas y Maybach quedan fuera de alcance y se declaran así en la exposición.
- **Por qué**: menos casos y mejor hechos. Además, el diseño es escalable: añadir otro tipo de vehículo supone ampliar el catálogo de modelos y los mapeos, no rehacer el modelo.
- **Cómo se aplica**: en silver se filtra `MAKETXT` en `MERCEDES-BENZ` y `MERCEDES BENZ` y `RCLTYPECD = 'V'`. Las furgonetas Sprinter vienen bajo la marca Mercedes-Benz, así que se excluyen porque su modelo no está en el catálogo (alias → variante). Ajusta el filtro de D-035, que mencionaba `MERCEDES-MAYBACH`.

## D-038 · Flujo de ramas: feature → develop → main (2026-11-20)
- **Contexto**: D-030 proponía trabajar solo en `develop`. Se prefiere aislar cada tarea en su propia rama, pero sin la rama `pre`.
- **Opciones**: (a) solo `develop` (D-030); (b) `feature/*` → `develop` → `pre` → `main` (D-029); (c) `feature/*` → `develop` → `main`; (d) añadir una rama `pro` para dbt.
- **Decisión**: (c). Una rama `feature/<tema>` por tarea; cuando funciona, a `develop` (DEV); cuando se comprueba allí, a `main` (PRO). Sin `pre`.
- **Sobre una rama `pro`**: no hace falta. En dbt Cloud el entorno de producción se asocia a una rama (normalmente la principal), así que `main` cumple ese papel. Un entorno de despliegue sigue `develop` (DEV) y el de producción sigue `main` (PRO). Hay que confirmarlo al configurar dbt Cloud.
- **Por qué**: cada tarea queda aislada y revisable, y se mantiene la promoción entre dos entornos para enseñarla sin el coste de un tercero.
- **Consecuencia**: sustituye a D-030 y, en lo referente a `pre`, a D-029. `origin/pre` queda sin uso.

## D-039 · UC5 limitado a EE. UU., junto a las ventas de EE. UU. (2026-11-20)
- **Contexto**: la NHTSA solo cubre EE. UU., mientras que las ventas cubren varias regiones. Se quiere observar fallos de software frente a mecánicos con alguna referencia de ventas.
- **Opciones**: (a) UC5 con revisiones solas; (b) UC5 de EE. UU. mostrado junto a las ventas de EE. UU. (mismo selector de modelo, **sin ratio**); (c) además, desglosar por propulsión.
- **Decisión**: (b). El informe de revisiones se acota a EE. UU. y se muestra al lado de las ventas de EE. UU. de la misma familia y año. Sigue vigente D-020: no se dividen revisiones reales entre ventas simuladas.
- **Propulsión (opcional)**: las revisiones no traen propulsión, solo el texto del modelo (`C 300`), y un mismo modelo puede ser combustión o híbrido enchufable. A nivel de **familia** la unión es fiable; a nivel de propulsión es ambigua. Se deja como mejora opcional, solo si el mapeo sale limpio (ver D-036).
- **Advertencia para la exposición**: las ventas son simuladas, así que ninguna conclusión sobre qué propulsión falla más puede apoyarse en ellas; solo en las revisiones reales.
