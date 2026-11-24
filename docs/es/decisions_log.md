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

## D-040 · Modelado: sin modelo físico y normalización flexible (2026-11-20)
- **Contexto**: el ejercicio de modelado pedía conceptual, lógico y físico para silver, con comprobación hasta 3FN, y después el dimensional para gold.
- **Opciones**: (a) hacer las tres fases y llegar a 3FN; (b) conceptual, lógico y dimensional, sin modelo físico, sin exigir 3FN completa.
- **Decisión**: (b). El modelo físico se descarta; el `CREATE TABLE` real saldrá de dbt. En el lógico se busca una normalización razonable y se justifica cada simplificación (por ejemplo, moneda e impuesto como atributos de país).
- **Por qué**: tiempo limitado y el físico en dbt se define por los propios modelos. Lo importante es entender y poder defender el grano, las claves y las relaciones.
- **Revisión del conceptual (2026-11-20)**: el diagrama está en `docs/diagrams/mercedes-benz-data-analytics_modelado_conceptual.png`. Cardinalidades de familia, carrocería y propulsión por corregir; moneda e impuesto pasan a país; el tipo de cambio es una tabla aparte. Pendiente: nivel al que se unen revisiones y modelo (familia o variante) y si el impuesto varía con el tiempo.

## D-041 · Conceptual v2: revisiones unidas a la familia, impuesto aparte y historial (2026-11-20)
- **Revisiones ↔ modelo**: en la v2 las campañas se unen a **familia**, no a variante (coherente con D-039: la unión a variante es ambigua).
- **Campaña ↔ componente**: relación de **muchos a muchos**, comprobada con el fichero real (turismos Mercedes-Benz, informes 2021–2025): 216 campañas; 162 con un componente, 45 con dos, 8 con tres y 1 con cuatro; y un mismo componente aparece en varias campañas (por ejemplo, `ELECTRICAL SYSTEM:SOFTWARE` en 12). Además, el componente depende de la combinación campaña + modelo + año (en `21V058000`, un modelo tiene componente de software y otro, de notificación de accidente), así que el lógico necesita ese grano.
- **Grano real del fichero**: 43.484 filas se reducen a 2.973 combinaciones distintas de campaña, modelo, año y componente; el fichero repite la fila por cada referencia de pieza (`MFR_COMP_PTNO`). Hay 237 textos de modelo distintos. Silver debe deduplicar y mapear a familia.
- **Impuesto**: tabla aparte (no atributo de país), porque puede cambiar con el tiempo.
- **Historial (snapshot)**: confirmado para **concesionarios** (cambios de nombre y estado). Para impuestos queda **por decidir**; recomendación: tabla con fechas de vigencia (`valid_from`/`valid_to`), porque la ley fija la fecha de efecto y un snapshot solo registra cuándo detectamos el cambio.

## D-042 · Concesionarios con historial de versiones (2026-11-21)
- **Contexto**: los concesionarios cambian de nombre y de estado (abierto o cerrado), y los profesores piden un snapshot SCD2 demostrable (D-023).
- **Opciones**: (a) solo el estado actual; (b) una tabla con columnas de vigencia (`valid_from`, `valid_to`, `is_current`), que es lo que produce el snapshot de dbt; (c) dos tablas, concesionario e historial.
- **Decisión**: (b). La clave primaria identifica cada **versión** y `dealer_code` es la clave de negocio común a todas sus versiones. La venta referencia el `dealer_code`, y los informes usan la versión vigente.
- **Mejora futura (para mencionar en la exposición)**: unir cada venta con la versión del concesionario **vigente en la fecha de la venta** (*point-in-time join*). Es más preciso pero más trabajo; en gold se haría en la dimensión de concesionario.
- **Matiz**: las fechas del snapshot son cuándo dbt **detectó** el cambio, no cuándo ocurrió; si el origen trae la fecha de cierre real, se guarda además como atributo.

## D-043 · Clave de la venta (2026-11-21)
- **Opciones**: el VIN como clave primaria, o un identificador propio.
- **Decisión**: `sale_id` propio, **generado con un hash determinista** de `source_system` y `source_sale_id` (no un contador). El VIN queda como atributo con test de calidad.
- **Por qué**: un VIN puede repetirse (venta, devolución, nueva venta), puede venir vacío o mal formado, y un contador cambiaría en cada ejecución e impediría demostrar que ejecutar dos veces no duplica.

## D-044 · Generador de datos: diseño (2026-11-21)
- **Contexto**: hace falta un origen reproducible para la demo de incrementalidad (D-022, D-031) y poco tiempo. El generador lo escribe el asistente (excepción prevista en las normas de trabajo) y se explica después al usuario.
- **Decisión**: se empieza solo por **Europa** (D-021). `data/data_generator/generate_europe.py`, con una semilla fija (mismos ficheros en cada ejecución, comprobado con huellas SHA-256).
- **Dos lotes**: el lote 1 es el histórico hasta el 31-10-2025 (un fichero por año, unas 44.000 filas con duplicados); el lote 2 trae ventas nuevas (nov–dic 2025), **correcciones** de ventas ya enviadas (mismo `sale_id` con estado o precio cambiado) y filas **reenviadas idénticas**. El maestro de concesionarios del lote 2 incluye nombres cambiados y cierres, para el snapshot.
- **Catálogo**: 49 variantes, 3 propulsiones (ICE, PHEV, BEV; sin híbrido ligero para simplificar) y 7 carrocerías. Precios y disponibilidad ficticios. Una tendencia anual hace que los datos «cuenten algo»: el eléctrico pasa de ~2 % (2021) a ~22 % (2025), y el SUV de ~42 % a ~51 %.
- **Suciedad**: 13 defectos con porcentaje configurable (duplicados, VIN vacío o inválido, nombres de modelo, fechas malas, entrega anterior a la venta, precios con separador de miles o símbolo, precios 0 o negativos, moneda, espacios y mayúsculas, tipo de cliente vacío, concesionario desconocido). Es una reducción respecto a los 24 del diseño inicial.
- **Alias**: el generador crea `model_alias.csv` con todas las grafías de cada modelo (300 filas), que será el seed de equivalencias en dbt. Así todo nombre sucio se puede resolver a una variante.
- **Por qué**: control total de la suciedad y de las demostraciones, a coste mínimo de tiempo del usuario.

## D-045 · Revisiones: campaña y líneas de campaña (2026-11-21)
- **Contexto**: el lógico v4 plantea una campaña con una sola familia, un estado y líneas con campaña y componente.
- **Comprobación con el fichero real**: unas 76 de las 216 campañas (≈35 %, cálculo aproximado por el prefijo del modelo) afectan a **más de una familia**; por ejemplo, `21V058000` toca más de diez. Y el fichero **no trae estado** de la campaña.
- **Decisión**: `campaigns` (id, fecha del informe, unidades potenciales) 1—M `campaign_lines` (id, `campaign_id`, `family_id`, `model_year`, `component_id`). La familia y el año van en la línea, no en la campaña. Sin columna de estado.
- **Por qué**: el componente depende de la combinación familia + año dentro de la campaña, y UC5 lo pide por modelo y año.

## D-046 · Impuesto solo en el país (2026-11-21) (SUSTITUIDA por D-050)
- **Opciones**: (a) `countries.tax_id` y `taxes.country_id` a la vez; (b) solo `taxes.country_id` con fechas de vigencia; (c) solo `countries.tax_id`.
- **Decisión**: (c), a petición del usuario.
- **Consecuencia (limitación)**: cada país apunta a un solo impuesto, el vigente; no hay historial de cambios de tasa por país. Es válido mientras la tasa no cambie en 2021–2025 en los países incluidos (hay que comprobar Suiza, si se incluye) y debe decirse como limitación. Las fechas `valid_from`/`valid_to` de `taxes` se quitan y **no hay snapshot de impuestos** (2026-11-21): el snapshot se reserva para los concesionarios, donde el historial es el objetivo; en una tabla de referencia con una tasa por país no aporta.

## D-047 · Jerarquía geográfica y recogida de datos (2026-11-21)
- **Decisión**: la jerarquía es venta → concesionario → país → región (el nivel «global» es el total, no una tabla). Sirve para el desglose en Power BI (región → país → concesionario).
- **Recogida**: no sigue esa jerarquía. Cada **sistema regional envía su propio fichero** (Europa, EE. UU., China), que contiene varios países. La jerarquía se reconstruye en silver con el concesionario de cada venta.

## D-048 · Años del modelo (2026-11-21)
- **Decisión**: la tabla de modelos guarda `first_model_year` y `last_model_year` (vacío si sigue en producción); cada venta y cada línea de campaña guarda su propio `model_year`.
- **Por qué**: son dos cosas distintas: cuándo se fabrica una variante y el año modelo de un vehículo concreto. El rango permite validar datos (una venta de una variante antes de que existiera es un error) y describir el ciclo de vida del modelo.

## D-049 · Importes: medida secundaria (2026-11-21) ⏳
- **Contexto**: los cinco casos de uso **cuentan ventas o revisiones**; ninguno pide importes. Los impuestos y los tipos de cambio solo sirven para el ingreso neto en euros.
- **Opciones**: (a) solo unidades, sin tablas de impuestos ni tipos de cambio; (b) unidades como medida principal e ingreso neto en EUR como medida secundaria, que se construye al final y solo si hay tiempo.
- **Recomendación**: (b). Las tablas son pequeñas, aparecen en el modelo y muestran limpieza de precios, conversión de moneda y cálculo del neto. Si falta tiempo, se recorta sin afectar a UC1–UC5.
- **Pendiente**: confirmación del usuario.

## D-050 · Impuestos con vigencia y aplicados en la venta (2026-11-21)
- **Contexto**: el usuario quiere que el cálculo del precio neto sea correcto aunque la tasa cambie con el tiempo, y se plantea si los datos podrían llegar ya con el impuesto.
- **Opciones**: (a) que el origen envíe el impuesto o el precio neto; (b) un solo impuesto por país, el vigente (D-046); (c) tabla de impuestos con vigencia por país y guardar en cada venta el impuesto aplicado.
- **Decisión**: (c). `taxes` (id, `country_id`, tasa, `valid_from`, `valid_to`) y en `sales` una clave foránea al impuesto aplicado, calculada en silver uniendo por país y por la fecha de la venta. Se quita `tax_id` de `countries`.
- **Por qué no (a)**: en la simulación los orígenes envían un único precio (con IVA en Europa, China y Japón; sin impuestos en EE. UU.) y no indican la tasa, que es lo habitual cuando el sistema de ventas no calcula impuestos. Mantenerlo así hace útil la tabla y muestra una transformación real. Se podría cambiar el generador para que envíe el neto, pero perdería sentido la tabla.
- **Detalles**: para EE. UU., cuyo precio ya excluye impuestos, la fila lleva tasa 0, de modo que la fórmula neto = bruto ÷ (1 + tasa) sirve para todos. Tests: que los periodos de un país no se solapen y que cubran todas las fechas de venta; que el país del impuesto coincida con el del concesionario.
- **Sin snapshot**: la vigencia ya guarda el historial; el snapshot sigue reservado a los concesionarios.
- **Relación con D-049**: solo se aprovecha si se construye el ingreso neto (medida secundaria).

## D-051 · Monedas en dos tablas en el modelo lógico (2026-11-21)
- **Opciones**: (a) una sola tabla `exchange_rates` con código de moneda, mes y tasa, y `countries.currency_code` apuntando al código (simplificación defendible, comentada con un profesor); (b) `currencies` (una fila por moneda) y `exchange_rates` (una fila por moneda y mes).
- **Decisión**: (b) en el lógico, por coherencia con el conceptual. En dbt bastará un seed de tipos de cambio y los países con su código de moneda.
- **Por qué**: lo que cambia con el tiempo (la tasa) se separa de lo que no cambia (la moneda), y `countries` apunta a una moneda y no a una fila con fecha. El coste es una tabla pequeña.
- **Justificación de (a), por si se pregunta**: la moneda solo tiene código y nombre, y el código ISO es una clave natural estable; normalizar más no aporta datos nuevos.

## D-052 · Historial de concesionarios solo en el snapshot, no en el lógico (2026-11-21)
- **Contexto**: en el lógico v10 `dealers` llevaba `valid_from` y `valid_to` y `dealer_id` como PK. Si cada versión fuera una fila, `dealer_id` se repetiría y dejaría de ser clave.
- **Decisión**: `dealers` en silver guarda **una fila por concesionario (estado actual)**; las versiones las crea el snapshot de dbt (SCD2) con sus propias columnas `dbt_valid_from` / `dbt_valid_to`. Se quitan `valid_from`/`valid_to` del lógico.
- **Por qué**: separa el estado actual (silver) del historial (snapshot) y mantiene la PK única. Sustituye a la parte de tabla con vigencia de D-042; el punto de mejora futuro (unir por fecha de la venta) sigue igual.
- **Recordatorio**: las fechas del snapshot significan «detectado el», no «ocurrió el».

## D-053 · Generador calibrado con cuotas públicas de mercado, año a año (2026-11-21; implementado 2026-11-22)
- **Contexto**: el usuario quiere que los datos simulados de Europa se parezcan a datos públicos (propulsión y carrocería), año a año, con un pequeño ajuste para Mercedes.
- **Decisión**: `data/data_generator/config/market_mix.csv` guarda, para 2021-2025, la cuota europea por propulsión (ACEA, UE) y la cuota SUV (JATO, Europa-28), con fuente y estado (`verified`, `derived`, `estimated`, `to_check`). El generador reajusta los pesos de cada variante del catálogo (ajuste proporcional iterativo) para que cada año salgan esas cuotas. Al final escribe `reference/calibration_report.csv` (cuota de mercado, objetivo Mercedes y cuota generada).
- **Cinco tipos de propulsión** (a petición del usuario): `BEV` (eléctrico), `PHEV` (híbrido enchufable), `HEV` (híbridos de otro tipo, incluidos los suaves), `PETROL` (gasolina) y `DIESEL`. El catálogo pasa de 3 a 5 valores: 11 variantes de gasolina pasan a HEV (las de tecnología EQ Boost) y las 10 variantes «d» pasan a DIESEL. ACEA publica gasolina y diésel por separado; el pequeño resto (GLP, GNC, ~3 %) se reparte entre gasolina y diésel en proporción.
- **Ajuste Mercedes**: Mercedes-Benz Cars tuvo un 40 % de electrificados (BEV + PHEV) en Europa en 2025 frente al 26,8 % del mercado (ACEA): factor ×1,49 sobre BEV y PHEV en todos los años (hipótesis; no hay dato de Mercedes para 2021-2023). El resto se reparte entre HEV e ICE con la proporción del mercado. Carrocería: sin dato de Mercedes, se usa la cuota SUV del mercado.
- **Descartado**: cuotas por país (KBA solo existe para Alemania y no hay dato gratuito equivalente en los otros países); inventar tendencias (lo que hacía la primera versión).
- **Límites a decir en la presentación**: son cuotas del mercado europeo, ajustadas a Mercedes con un solo dato; SUV 2022 y 2025 estimados; PHEV 2024 por comprobar; «HEV» de ACEA mezcla híbridos completos y suaves y el catálogo usa HEV para los suaves. Los datos siguen siendo simulados, pero calibrados: el informe de calibración muestra que se desvían menos de un punto, salvo ruido del muestreo.

## D-054 · Criterio para guardar fechas y tipo de cambio mensual (2026-11-21)
- **Decisión**: se guardan fechas solo en hechos (ventas, campañas) y en valores que cambian con el tiempo (impuestos con intervalo, tipo de cambio mensual, concesionarios con snapshot). Las tablas de referencia guardan solo el estado actual.
- **Tipo de cambio mensual** en lugar de diario: análisis comercial, menos ruido, unas 180 filas en vez de ~5.500, fácil de cargar como seed. Mejora futura: tasa diaria.
- **Detalle y respuestas preparadas**: `docs/es/defense_justifications.md`.

## D-055 · El ciclo de vida se guarda en el modelo y se deriva a la familia (2026-11-21)
- **Contexto**: el usuario se plantea poner fechas de primer y último año también en las familias (ejemplo: EQA dejaría de fabricarse).
- **Opciones**: (a) fechas también en `families`; (b) solo en `models` y derivar la vigencia de la familia.
- **Decisión**: (b). Una familia está vigente mientras tenga algún modelo vigente; se calcula en gold si hace falta.
- **Por qué**: evita un dato redundante que podría contradecirse con el de sus modelos. Respuesta preparada en `docs/es/defense_justifications.md` §5.

## D-056 · Construcción por cortes verticales: primero ventas de Europa (2026-11-22)
- **Contexto**: queda poco tiempo y hay riesgo de que Snowflake o dbt Cloud den problemas; el usuario prefiere tener algo funcional antes que algo amplio.
- **Opciones**: (a) construir todo por bloques (todas las capas de todas las fuentes y los dos hechos a la vez); (b) corte vertical: ventas de Europa de extremo a extremo y, si hay tiempo, revisiones después.
- **Decisión**: (b). Fase 1: ventas de Europa (Snowflake, bronze, staging, silver, gold, tests, snapshot de concesionarios, demo de doble ejecución y segundo lote). Fase 2, si hay tiempo: revisiones, que reutilizan `dim_model` y `dim_date`. Fase 3, extra: más regiones o Power BI ampliado.
- **Por qué**: un trabajo completo y demostrable pesa más que uno amplio e incompleto; la fase 2 es más barata porque ya se conoce el método. Refuerza D-021 y D-036.
- **Modelado**: el dimensional recoge ambos hechos (estructura compartida), pero solo se construye el de ventas en la fase 1.

## D-057 · Claves del dimensional: `id_` como en el curso y claves candidatas marcadas (2026-11-22)
- **Contexto**: en el dimensional propuse nombres `_key` para las claves sustitutas. El usuario prefiere la convención del curso: PK llamada `..._id` y columnas marcadas como clave candidata (CC) en cada tabla.
- **Decisión**: PK `..._id` (sustituta, generada por nuestro modelo) y CC para la clave natural del origen. Ejemplo: `dim_dealer.dealer_id` (PK) y `dealer_code` (CC).
- **Por qué**: el nombre es solo una convención; lo importante es que la PK de la dimensión no dependa del origen y que la clave natural quede identificada como CC y con un test de unicidad. En el snapshot, un mismo concesionario tiene varias versiones: cada versión necesita su propia PK, y la CC (`dealer_code`) se repite.

## D-058 · Vigencia del concesionario como atributos y `units_affected` (2026-11-22)
- **Contexto**: duda sobre si `dim_dealer` debe enlazar con `dim_date` por las fechas del snapshot, y sobre el nombre de `potential_units`.
- **Decisión**: `dim_dealer` lleva `valid_from`, `valid_to` e `is_current` como **atributos** (vienen del snapshot), sin clave foránea a `dim_date`. La CC es `dealer_code` + `valid_from`. La venta apunta a una versión (la vigente, D-042). `potential_units` pasa a `units_affected` en el dimensional.
- **Por qué no enlazar a `dim_date`**: las fechas describen el periodo de validez de la fila, no un hecho; un intervalo no es un punto del calendario, y una dimensión que enlaza con otra es un copo de nieve. Del mismo modo, `dim_model` no enlaza con `dim_date`: `first_model_year`/`last_model_year` son números atributo.
- **Aviso**: `units_affected` es el dato que informa el fabricante (potencial) y no se suma por líneas de la misma campaña; se decide cómo tratarlo en la fase 2.

## D-059 · `dim_family` como dimensión compartida enlazada directamente a los dos hechos (2026-11-22)
- **Contexto**: las campañas se publican por familia y año modelo, y las ventas por variante. `dim_model` ya contiene la familia, pero una familia no es única por fila de `dim_model`, así que no se puede unir una campaña a `dim_model` sin duplicar.
- **Opciones**: (a) `dim_family` 1—M `dim_model` (copo de nieve, defendible pero rompe la estrella); (b) `dim_family` enlazada directamente a `fct_sales` (con `family_id` en el hecho) y a `fct_campaign_line`; (c) una sola dimensión de modelo con la familia y unir campañas por texto.
- **Decisión**: (b). `fct_sales` lleva `family_id` (derivable de `model_id`), y `dim_model` conserva `family_id` y `family_name` como atributos, sin enlace a `dim_family`. Un selector de familia filtra ventas y campañas.
- **Por qué**: estrella pura (ninguna dimensión enlaza con otra) y dimensión conforme. El coste es un dato repetido en el hecho; se protege con un test (el `family_id` del hecho coincide con el de su modelo). Descartado (c) por frágil.

## D-060 · Tipos de impuesto: varias tasas por país y tipo explícito (2026-11-22)
- **Contexto**: el usuario detecta que `taxes` no indica de qué impuesto se trata y que un país puede tener **varias tasas a la vez** (ejemplo: IVA general del 21 % y reducido del 4 % para familias con hijos con discapacidad). Con solo país y fecha, silver no puede saber qué tasa aplicar: el dato tiene que venir en la venta.
- **Opciones**: (A) mantener D-050 (una tasa por país y fecha); (B) añadir el catálogo `tax_types`, relacionarlo con `taxes` y que el origen envíe el régimen (`tax_regime`); (C) además, acumular **varios impuestos en una misma venta** (IVA + impuesto de matriculación, por ejemplo) con una tabla puente `sale_taxes`.
- **Decisión**: (B), con el mayor detalle posible. (C) se descarta por tiempo y queda como mejora futura documentada (una venta con un único impuesto aplicado).
- **Modelo lógico (v14)**:
  - Tabla nueva `Tax_types`: `tax_type_id` (PK), `tax_type_code` (ej. `VAT_STANDARD`, `VAT_REDUCED`), `tax_type_name`, `description`.
  - `Taxes`: se añade `tax_type_id` (FK a `Tax_types`). Columnas: `tax_id` (PK), `country_id` (FK), `tax_type_id` (FK), `tax_value`, `valid_from`, `valid_to`. En el lógico no se dibujan claves candidatas (v14, decisión del usuario: ninguna tabla las lleva); se declaran en el dimensional (`dim_tax`) y como test único en dbt: país + tipo + `valid_from`.
  - `Sales` no cambia: `tax_id` sigue siendo el **impuesto aplicado** (D-050); el tipo se obtiene por `tax_id` → `Taxes` → `Tax_types`, así no se duplica ni se pierde nada.
  - Relaciones: `Tax_types` 1—M `Taxes`; `Countries` 1—M `Taxes`; `Taxes` 1—M `Sales`.
- **Origen**: el CSV europeo gana la columna `tax_regime` (`STD` estándar, `RED` reducido) y una parte de las ventas llega con el régimen reducido. Silver une por país + régimen (traducido a tipo) + fecha de venta y guarda el `tax_id`.
- **Seed `taxes` (unas 11 filas)**: estándar DE 19 %, GB 20 %, FR 20 %, IT 22 %, ES 21 %, CH 7,7 % hasta 2023-12-31 y 8,1 % desde 2024-01-01 (ejemplo de cambio con vigencia). Reducido **simulado**, inspirado en regímenes reales: ES 4 %, IT 4 %, GB 0 %, FR 5,5 %. DE y CH no tienen reducido. **Verificar las tasas reales antes de afirmarlas en la presentación.**
- **Tests**: cada venta casa con **exactamente un** impuesto; los periodos de un mismo país y tipo no se solapan y cubren todas las fechas de venta; el país del impuesto coincide con el del concesionario; `tax_regime` solo admite valores del seed de equivalencias.
- **Por qué no deducirlo en silver**: ningún dato de la venta indica el régimen; inventarlo sería arbitrario. En la vida real lo sabe el sistema de ventas.
- **Por qué no una columna de régimen en `Sales` silver**: ya se obtiene por `tax_id`; guardarlo dos veces permitiría contradicciones.
- **Límites a decir**: un solo impuesto por venta; EE. UU. (sin impuestos en el precio) queda para la fase de más regiones; el reducido es simulado.
- **Documentos afectados**: lógico v14, dimensional v7 (D-061), `source_design.md` (columna y defecto D24), generador.

## D-061 · `dim_tax` en gold (2026-11-22; propuesta a confirmar al dibujar el dimensional v7)
- **Opciones**: (a) atributo degenerado `tax_type` en `fct_sales`, sin dimensión nueva; (b) dimensión `dim_tax` y clave `tax_id` en `fct_sales`.
- **Recomendación**: (b). Conserva el impuesto aplicado completo (país, tipo, tasa, vigencia) y permite filtrar ventas por tipo de impuesto, sin perder datos. Sigue siendo **estrella pura**: `dim_tax` lleva el país desnormalizado y no enlaza con ninguna otra dimensión (D-059). Son unas 11 filas.
- **Columnas**: `tax_id` (PK); CC: `country_code`, `tax_type_code`, `valid_from`; `tax_type_name`, `tax_rate`, `valid_to`.
- **`fct_sales`**: añade `tax_id` (FK) y mantiene `tax_rate` para calcular el neto sin unir, como valor aplicado en el momento del cálculo.
- **Si el usuario prefiere (a)**: se cambia por una columna `tax_type_code` en `fct_sales` y se elimina `dim_tax`.

## D-062 · Seis deltas pequeños de diciembre de 2025 y escenario de concesionarios guionizado (2026-11-22)
- **Contexto**: el usuario tiene que probar la carga incremental en casa, en clase y en directo, y quiere saber exactamente cuántas filas tiene cada prueba. El lote 2 anterior tenía 2.477 filas y un escenario de concesionarios aleatorio.
- **Opciones**: (a) un solo lote 2 grande y aleatorio; (b) 6 deltas pequeños, cada uno con un propósito, y un escenario de concesionarios fijo.
- **Decisión**: (b). El histórico (`batch_1`) llega hasta el 30-11-2025 y diciembre de 2025 se reparte en 6 deltas de unos 5 días (134-180 filas): ventas nuevas; reenvío de filas idénticas; correcciones por `sale_id`; renombrado de 3 concesionarios; 2 cierres + un segundo renombrado + un concesionario nuevo; filas de alerta (10 que deben hacer fallar tests).
- **Por qué diciembre y no una muestra**: así no queda un hueco al final de la serie en Power BI (diciembre de 2025 tiene su volumen real, repartido en 6 cargas).
- **Escenario de concesionarios fijo** (no aleatorio) para que el resultado sea igual en cada ejecución; DE-0014 acaba con 3 versiones en el snapshot.
- **Documentación**: `docs/es/demo_scenarios.md` (guion con recuentos exactos de bronze y de silver) y `reference/delta_plan.csv` generado por el script.
- **Límite**: los recuentos de silver suponen que las filas con defectos se marcan pero no se descartan; si se descartan, el guion se ajusta.

## D-063 · Carga a bronze: stage interno y subida manual desde Snowsight (2026-11-22)
- **Contexto**: hay que llevar los CSV de Europe a bronze, repetirlo en 4 ensayos y poder mostrarlo.
- **Opciones**: (a) subida manual desde Snowsight a un stage interno + `COPY INTO`; (b) Snowflake CLI (`snow stage copy`) con clave privada, automatizable; (c) `PUT` desde SnowSQL (no funciona en hojas de Snowsight).
- **Decisión**: (a) ahora, porque se ve bien en pantalla y no necesita la clave privada. (b) queda como **propuesta de mejora** y se configura solo si sobra tiempo. El `COPY INTO` es el mismo en ambos casos.
- **Diseño de bronze**: todas las columnas del origen como `varchar` (no se convierte ni se rechaza nada) + `_source_file`, `_file_row_number` y `_loaded_at` (convención del curso). Solo se añaden filas. Un stage por fuente y subcarpetas (`batch_1`, `delta_1`…) para que dos ficheros con el mismo nombre (`dealer_master.csv`) no choquen.
- **Idempotencia en dos niveles**: `COPY INTO` recuerda qué ficheros ya cargó y no repite el mismo fichero; si llegan filas repetidas dentro de ficheros distintos (reenvíos), las elimina silver por `sale_id`.
- **Detalles**: formato con `error_on_column_count_mismatch` para notar un cambio de columnas del origen; `on_error = ABORT_STATEMENT` (un fichero mal estructurado no se carga a medias). Script: `snowflake/02_bronze_europe.sql`.
- **Pendiente de comprobar**: que `truncate table` borra también el historial de ficheros cargados (si no, `force = true`), para el reset entre ensayos.

## D-064 · Conexión de dbt Cloud a Snowflake: clave en lugar de contraseña (2026-11-22)
- **Contexto**: Snowflake exige doble factor (MFA); con contraseña habría que reautenticarse y los jobs programados no funcionarían.
- **Opciones**: (a) contraseña (descartada: MFA); (b) par de claves reutilizando el del curso del usuario `dhv994` (su clave pública ya está registrada); (c) usuario de servicio con clave propia (lo correcto en un proyecto real).
- **Decisión**: (b) ahora, por rapidez y porque es una cuenta de prueba; (c) queda como **propuesta de mejora**. La clave privada y la passphrase viven **fuera de este repositorio** (en el otro repositorio de apuntes) y se pegan solo en dbt Cloud.
- **Conexión de desarrollo**: base de datos `DEV_MB_SILVER_DB`, warehouse `WH_MB`, rol `DEV_MB_TRANSFORM_ROLE` (mínimo privilegio: lee bronze, crea esquemas solo en silver y gold de DEV). Esquema personal `dbt_dhv994`.
- **Versión de dbt**: se mantiene D-004, **v1 «Latest»** (no v2/Fusion): menos riesgo con paquetes; comprobar en el entorno que la pista de versión sea «Latest».
- **Limitación a decir**: reutilizar la clave de un usuario personal no sería aceptable en producción.
- **Actualización D-064 (2026-11-22) · IMPORTANTE**: la conexión de dbt Cloud con clave **solo funcionó cuando en `Username` se puso el correo de la cuenta de Snowflake (su `LOGIN_NAME`), no el nombre de objeto `dhv994`**. Antes daba `JWT token is invalid`. Comprobación: `desc user "dhv994";` muestra `NAME` (`dhv994`) y `LOGIN_NAME` (el correo). En dbt Cloud el usuario de las credenciales de desarrollo = `LOGIN_NAME`. En las sentencias SQL (`grant ... to user`, `alter user`) sigue usándose `"dhv994"`. El correo real no se escribe en el repositorio.

## D-065 · Repositorio de dbt Cloud conectado por «Git clone» (deploy key) (2026-11-22)
- **Contexto**: el enlace con GitHub por la app de dbt Cloud dio «Account in use»: una cuenta de GitHub solo puede estar asociada a **un** usuario de dbt, y ya lo estaba a la cuenta del curso.
- **Opciones**: (a) desenlazar GitHub de la cuenta antigua y usar la app de GitHub; (b) «Git clone» por SSH con una clave de despliegue (*deploy key*) con permiso de escritura, sin tocar la otra cuenta; (c) repositorio gestionado por dbt (descartado: perdería el historial y el flujo de ramas).
- **Decisión**: (b). Es reversible y no arriesga el proyecto del curso. GitHub avisa de que recomienda GitHub Apps (control fino y más seguridad): se cita como mejora si la otra cuenta deja de usarse.
- **Límite**: sin la integración nativa no se lanza CI automáticamente al abrir un PR (no se necesita para la demo).

## D-066 · Fechas de venta rotas: recuperar el formato, avisar de las imposibles (2026-11-23)
- **Contexto**: en bronce, 258 `sale_date` no se entendían con `DD/MM/YYYY`. Al mirarlas aparecen tres casos del defecto `bad_date` (D06): `31/02/AAAA` (fecha imposible, 79 filas), `AAAA-MM-DD` y `DD.MM.AA` (fechas válidas en otro formato).
- **Decisión**:
  1. **Staging** prueba los tres formatos con `coalesce(try_to_date(...), ...)`. Recupera las 179 fechas válidas y deja en **nulo** las 79 imposibles. Solo es limpieza de formato: no se inventa ningún día.
  2. **Silver** conserva esas filas con la fecha nula y un test `not_null` de la fecha de venta con severidad `warn` y `store_failures` (una tabla en Snowflake lista las ventas afectadas = **alerta**).
  3. **Gold** no incluye las ventas sin fecha hasta que se corrijan: no se pueden colocar en una serie temporal y la fila `date_id = -1` ensuciaría los totales por año.
  4. **La corrección real se hace en el origen**: el sistema de ventas reenvía la venta con el mismo `sale_id` y la fecha buena, y el incremental actualiza la fila (mismo mecanismo que las correcciones del delta 3).
- **Por qué**: un test **avisa, no cambia el dato**; corregir un dato sin conocer el valor real sería inventarlo. Descartado: mandarlas a `date_id = -1` (contamina las gráficas por año) y borrarlas (se pierde información).
- **Evidencias**: 21 (formatos en bronce) y 22 (conteos tras la corrección: 44.654 fechas de 44.733).

## D-067 · Tres entornos (DEV / PRE / PRO) y variables de entorno de dbt Cloud (2026-11-23)
- **Contexto**: D-038 había descartado `pre` por tiempo. Se decide recuperarlo: un amigo que hizo el curso y trabaja en el sector lo considera la práctica habitual, y las variables de entorno se han visto en el curso.
- **Opciones**: (a) mantener DEV y PRO; (b) añadir PRE con **una rama más** (`pre`); (c) añadir PRE **sin rama nueva**: el entorno PRE ejecuta la rama `develop` y el entorno PRO ejecuta `main`.
- **Decisión**: (c). Flujo: `feature-*` → PR → `develop` (se prueba en PRE) → PR → `main` (se ejecuta en PRO). DEV es el IDE de dbt Cloud sobre la rama de trabajo. Snowflake: `PRE_MB_SILVER_DB`, `PRE_MB_GOLD_DB` y `PRE_MB_TRANSFORM_ROLE` (script `snowflake/03_pre_environment.sql`); el bronce sigue siendo uno solo en DEV.
- **Variables de entorno** (dbt Cloud): `DBT_ENV_NAME` (`DEV` por defecto, `PRE`, `PRO`) elige la base de silver y gold en el macro `generate_database_name`; `DBT_BRONZE_DB` indica la base del bronce en `_sources.yml`. Las dos tienen valor por defecto, así que el IDE sigue funcionando sin configurar nada.
- **Por qué**: el mismo código se despliega en los tres entornos y solo cambia la configuración, como en una empresa; no cambia el incremental ni el snapshot, que es lo que se muestra en la demo. Sustituye a la idea previa de usar `target.name`.
- **Coste y riesgo**: unos 45–60 min (Snowflake, dos entornos de despliegue con sus credenciales, un job por entorno). Se hace **después** de tener silver y gold, para no retrasar lo esencial. Si el martes por la tarde no cabe, se recorta PRE y se queda DEV/PRO.
- **Actualiza**: D-038 (flujo de ramas y entornos).

- **Actualización D-067 (2026-11-23, decisión del autor)**: el entorno PRE usará la **rama `pre`** (opción b) en lugar de ejecutar `develop`. Flujo final: `feature-*` → PR → `develop` → PR → `pre` (entorno PRE, job de pruebas) → PR → `main` (entorno PRO). El desarrollo en el IDE (DEV) trabaja sobre la rama de la tarea. **Por qué**: separa «código integrado» (`develop`) de «candidato a producción» (`pre`), como en el patrón visto en el curso, y la promoción se ve en cada PR. **Coste**: un PR más por promoción. La rama `pre` ya existía en el remoto y está sin divergir de `develop` (0 commits propios, 54 por detrás), así que el primer PR `develop` → `pre` es limpio. Esto sustituye al punto «PRE ejecuta `develop`» de la decisión original.
- **Macro nueva (2026-11-23)**: `generate_schema_name` — en DEV el esquema lleva el prefijo personal (`DBT_DHV994_CORE`); en PRE y PRO se usa el nombre limpio (`CORE`, `SNAPSHOTS`, `SALES`...). Es lo habitual (documentación de dbt) y hace que Power BI lea `PRO_MB_GOLD_DB.SALES`.
- **Ejecución verificada (2026-11-23)**: creados los entornos PRE (rama `pre`) y PRO (rama `main`) en dbt Cloud, cada uno con su rol, su base de datos y `DBT_ENV_NAME` propio, y un job `dbt build` por entorno (manual, con generación de docs, sin *source freshness*). Ambos terminan en Success con 78 filas de aviso en `not_null` de `sale_date` (D-066) y el aviso esperado de `gold` sin modelos. Evidencias 29-36.
- **Source freshness desactivado (decisión del autor)**: las fuentes no declaran `loaded_at_field` ni umbral y la carga es manual por deltas, así que no aporta. En producción real con ingesta automática se activaría sobre `_loaded_at`.
- **Seguridad: claves en dbt Cloud**: la clave privada key-pair solo va en el campo de credenciales (cifrado en reposo); dbt Cloud avisa de que *Extended attributes* se ve en texto plano, así que **no se usa para claves** (evidencia 33). Mejora posible: rotar la clave si se expone.
- **Incidente del macro de esquemas (2026-11-24)**: el archivo `generate_schema_name` llegó a `develop`, `pre` y `main` **vacío y sin extensión `.sql`**, así que dbt lo ignoró en PRE y PRO y creó esquemas como `CORE_CORE` y `CORE_STAGING`. Detectado al revisar la rama; corregido con `generate_schema_name.sql` y reejecutados los jobs: ahora aparecen los esquemas limpios (evidencias 37-38). **Lecciones**: (1) comprobar que un archivo nuevo tiene extensión y contenido antes de comitear; (2) una captura puede parecer prueba sin serlo (el esquema `core_dbt_test__audit` era el comportamiento por defecto); (3) los esquemas equivocados se borran a mano.
- **Mejoras de orquestación a mencionar (no implementadas)**: job de CI en cada PR con `dbt build --select state:modified+` (CI ligera), job programado diario en PRO y *source freshness* si la ingesta fuera automática.

## D-068 · Campañas de defectos con datos reales de NHTSA (2026-11-24)
- **Contexto**: el usuario quiere cargar datos reales y tener algo que enseñar de la parte de defectos. El fichero público de NHTSA trae todas las marcas desde 2010 (248.544 filas).
- **Decisión**: un script (`data/nhtsa/prepare_recalls.py`) filtra Mercedes-Benz y Mercedes-Maybach, solo **vehículos** y modelos **2021-2025** (14.603 filas, 181 campañas) y escribe un CSV pequeño. Va a bronce como texto (`nhtsa.raw_recalls`), con el mismo patrón que ventas. En dbt: `stg_recalls` (tipos) → `silver_campaign_lines` → `dim_component` y `fct_campaign_line`, que comparte `dim_family` con `fct_sales` (D-059).
- **Traducción modelo → familia**: el macro `model_to_family` (expresiones regulares, de las más largas a las más cortas: `EQS SUV` antes que `EQS`). Se quitan los prefijos `AMG`, `MAYBACH` y `REDUNDANT`. **Quedan fuera** los modelos que no vendemos (CLS, Sprinter, Metris, Tourrider): 1.009 filas. Resultado esperado: 499 líneas de campaña, 100 componentes y 141 campañas.
- **`units_affected` no se suma**: NHTSA repite la cifra de la campaña en cada fila, y al juntar modelos de una misma familia se toma el máximo (D-058).
- **Por qué un script en Python y no cargar el fichero entero**: 15 MB comprimidos con 248.000 filas de otras marcas no aportan nada; filtrar antes de bronce simplifica y deja un fichero que se sube a mano en un minuto.
- **Límite a decir**: datos reales de EE. UU. aplicados a un catálogo europeo ficticio; sirven como ejemplo de una segunda fuente conectada por la familia, no como análisis real de defectos.
