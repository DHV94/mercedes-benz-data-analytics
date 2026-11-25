# Justificaciones para la defensa (preguntas del tribunal)

> Archivo vivo. Cada respuesta debe poder decirse en 20-30 segundos. Si una cifra o un dato externo aparece aquí, se comprueba antes de usarlo.

## 1. Regla general: ¿cuándo guardo fechas y cuándo no?

**Regla:** una tabla lleva fechas solo si (a) describe un **hecho que ocurre** en un momento, o (b) describe un valor que **cambia con el tiempo** y necesito saber cuál valía en cada momento. Si no, guarda solo el estado actual.

| Tabla | ¿Fechas? | Por qué |
|---|---|---|
| `sales` | `date_of_sale`, `delivery_date` | Es un **hecho**: ocurre un día concreto. Sin fecha no se puede analizar por año. Dos fechas porque venta y entrega no son el mismo día (puede haber cancelaciones entre medias) |
| `campaigns` | `date_of_campaign` | También un hecho: el día en que se registra la campaña |
| `exchange_rates` | fecha de vigencia (mensual) | El valor **cambia continuamente** (ver §2) |
| `taxes` | `valid_from` / `valid_to` | El valor **cambia pocas veces y en fechas arbitrarias** (ver §3) |
| `dealers` | ninguna en silver; `dbt_valid_from/to` en el snapshot | El origen solo da el estado actual; el historial lo **detecta** el snapshot (ver §4) |
| `models` | `first_model_year`, `last_model_year` | No es historial: es el **ciclo de vida** del modelo. Último año vacío = sigue en producción |
| `families`, `bodyworks`, `type_of_propulsions`, `components`, `type_of_components`, `regions`, `countries`, `currencies`, `campaign_lines` | ninguna | **Datos de referencia** que casi no cambian. Se guardan en su estado actual (en terminología de dimensiones, tipo 1: se sobrescribe). Limitación asumida: si una familia cambiara de nombre, perderíamos el nombre antiguo |

## 2. ¿Por qué el tipo de cambio es mensual?

- **Qué pregunta responde:** convertir el precio de cada venta a euros para comparar regiones. Es análisis comercial, no contabilidad.
- **Menos ruido:** la cotización cambia cada día. Un valor mensual (media o fin de mes, a decidir y documentar) evita que una venta parezca más cara que otra por la fluctuación de un día.
- **Menos filas y más fácil de mantener:** 3 monedas distintas del euro × 60 meses = unas 180 filas, frente a unas 5.500 con tasa diaria. Se carga como seed de dbt.
- **Coherencia con la fuente real:** los bancos centrales publican tasas medias mensuales. *(Comprobar con la fuente exacta que se use antes de afirmarlo en la presentación.)*
- **Limitación y mejora:** para auditoría o contabilidad se usaría la tasa del día. Cambiar a diaria solo cambia el grano de `exchange_rates` y el join (por fecha en lugar de por mes).
- **Cómo se une:** `date_of_sale` truncada al mes = mes de la tasa. Test: ninguna venta sin tasa.
- **Dato simulado:** los valores de nuestro seed son aproximaciones; lo importante aquí es el diseño.

## 3. ¿Por qué impuestos con intervalo y cambio con punto mensual?

Es la pregunta que enlaza los dos casos:
- El **IVA** cambia **pocas veces** y un día concreto (por ley). Un intervalo (`valid_from`–`valid_to`) lo describe con una fila por periodo.
- El **tipo de cambio** cambia **siempre**; un intervalo sería una fila por cada día o mes igualmente. Un valor por mes es más simple.
- El impuesto aplicado se **guarda en la venta** (`tax_id`) para que el cálculo no cambie si la tabla se actualiza y para poder auditarlo.
- EE. UU.: el precio ya excluye impuestos; la fila tiene tasa 0 para que la fórmula `neto = bruto ÷ (1 + tasa)` valga para todos.
- Tests: periodos de un país sin solaparse y que cubran todas las fechas de venta.

## 4. ¿Por qué un snapshot para concesionarios y no para otras tablas?

- Los concesionarios **cambian de nombre, se cierran o se traspasan**, y el origen solo envía el estado actual. Para conservar el pasado hay que **detectar el cambio** → snapshot SCD2 de dbt (estrategia `check` sobre nombre y estado).
- Los impuestos y tipos de cambio ya traen su vigencia, así que no necesitan snapshot (D-050).
- Las tablas de referencia casi no cambian, y no merece la pena.
- Limitación a decir: las fechas del snapshot significan **«detectado el»**, no «ocurrió el». Un cambio se ve con el retraso de la carga.
- Mejora futura (D-042): unir las ventas con la versión del concesionario que estaba vigente en la fecha de venta.

## 5. Otras preguntas probables

- **¿Por qué tablas separadas para familia, carrocería y propulsión?** Porque son atributos del modelo que se repiten muchas veces; separarlos evita duplicar texto y permite agrupar (carrocería y propulsión son los ejes de las preguntas de negocio).
- **¿Por qué el VIN no es la clave?** Se repite (venta, devolución, nueva venta), llega vacío o con errores. La clave es `sale_id`, creada con `source_system` + `source_sale_id` (D-043).
- **¿Por qué los datos de revisiones no se dividen entre ventas?** Mezcla datos reales con simulados; la cifra sería engañosa (D-020).
- **¿Por qué `campaign_lines`?** Una campaña afecta a varias familias, años y componentes: es una relación N:M que se resuelve con una tabla intermedia (D-041, D-045).
- **¿Por qué el precio va en moneda local?** Es lo que envía el origen; se conserva y se convierte después, así no se pierde el dato original (D-011, D-012).
- **¿Por qué `families` no tiene fechas de primer y último año, como `models`?** El ciclo de vida se guarda donde nace el dato, en el modelo (`first_model_year`, `last_model_year`), y se **deriva hacia arriba**: una familia está vigente mientras tenga algún modelo vigente (`min`/`max` de sus modelos). Guardarlo también en la familia sería un dato redundante que podría contradecirse. Ejemplo: EQA es una familia; cuando dejen de fabricarse sus modelos (EQA 250, EQA 300…), la familia lo refleja sin cambiar nada. Se puede exponer como columna calculada en gold (`dim_family`).
- **¿Por qué `family_id` está también en `fct_sales` si ya se puede sacar de `dim_model`?** Para mantener una **estrella pura**. Si `dim_family` colgara de `dim_model` sería un copo de nieve (dimensión que cuelga de otra), con más joins y consultas más lentas. Preferimos repetir una clave en el hecho (barato: unas decenas de miles de filas) y protegerla con un test de coherencia. A cambio, `dim_family` es una **dimensión compartida** por ventas y campañas: un selector de familia filtra los dos hechos (D-059). Frase: «hice lo posible por evitar el copo de nieve y dejarlo como estrella».
- **¿Qué pasa con `delivery_date_id` si la venta no se ha entregado?** Va a una fila «desconocida» de `dim_date` (`date_id = -1`), para no perder la venta ni romper el join.

## 6. Impuestos con tipo (D-060, D-061)

- **¿Por qué hay una tabla de tipos de impuesto?** Porque un país puede aplicar **varias tasas a la vez** (general y reducida). Antes solo había una por país y fecha. Ahora `taxes` indica el tipo y la venta guarda el impuesto aplicado.
- **¿Cómo sabe el sistema cuál aplicar?** El origen envía el régimen (`tax_regime`), igual que en la vida real. Con país y fecha no basta; deducirlo en silver sería inventarlo. Silver une país + régimen + fecha y comprueba que salga **exactamente un** impuesto.
- **¿Qué pasa si el régimen llega vacío o mal escrito?** Un seed de equivalencias normaliza las grafías; si sigue sin casar, el test falla y salta la alerta (no se asume en silencio).
- **¿Y si cambia una tasa?** Se añade una fila con su vigencia y se cierra la anterior. Ejemplo (verificar): IVA de Suiza 7,7 % hasta 2023 y 8,1 % desde 2024. Las ventas antiguas conservan el impuesto que se les aplicó.
- **¿Por qué `dim_tax` y no una columna en la venta?** Conserva país, tipo, tasa y vigencia del impuesto aplicado sin perder datos, permite filtrar por tipo y mantiene la estrella (sin enlaces entre dimensiones).
- **¿Por qué no varios impuestos en la misma venta?** Exigiría una tabla puente y medidas por impuesto. Se descarta por tiempo y se cita como mejora (por ejemplo, impuesto de matriculación según emisiones). Los informes usan el IVA, que es lo que no es ingreso de la compañía.
- **Límite que decir**: el régimen reducido es **simulado**, inspirado en regímenes reales.

## 7. Seguridad y conexión (D-063, D-064)

- **¿Por qué dbt entra con una clave y no con contraseña?** Snowflake obliga a doble factor; un par de claves permite que dbt y los jobs programados entren sin reautenticarse, y la clave privada nunca se guarda en el repositorio.
- **¿Dónde está la clave privada?** Fuera del repo (en un repositorio aparte de apuntes) y solo se pega en dbt Cloud. El repo ignora `profiles.yml` y `.env`.
- **¿Es seguro reutilizar tu usuario?** En una cuenta de prueba sí; en un proyecto real se crearía un **usuario de servicio** con su propia clave y el rol mínimo. Se deja como mejora.
- **¿Por qué un rol distinto para cargar y para transformar?** Mínimo privilegio: `MB_INGEST_ROLE` es el único que escribe en bronze; `DEV_MB_TRANSFORM_ROLE` solo lee bronze y crea objetos en silver y gold de su entorno; reporting solo lee gold.
- **¿Por qué subida manual a un stage?** Se ve en pantalla y no necesita la clave; `COPY INTO` recuerda los ficheros ya cargados (primera defensa contra duplicados). La subida con la CLI queda como mejora.
- **¿Por qué dbt v1 «Latest» y no v2?** Menos riesgo con paquetes y menos cambios; la v2 (Fusion) se menciona como evolución.

## 8. Silver de ventas (`silver_sales`): lecciones para defender

- **¿Por qué una fila por `sale_id` y cómo se elige?** `row_number() over (partition by sale_id order by _loaded_at desc, _source_file desc, _file_row_number desc) = 1`. `row_number` y no `rank`: con un empate `rank` deja dos filas con el 1 y reaparece el duplicado. El tercer criterio existe porque los duplicados exactos comparten fecha de carga y archivo; solo los distingue la línea del archivo.
- **Bronce 44.733 → silver 44.072**: 661 duplicados exactos (defecto D01). Es la cuenta que se enseña.
- **Nombre del modelo (D05)**: se casa con el seed `model_alias` comparando en **mayúsculas por los dos lados** y con `distinct` en el seed. Sin `distinct`, `GLC 200` y `glc 200` coinciden en mayúsculas y la venta se **duplica sin error** (el conteo sube en silencio). Se guarda el nombre original; en gold se muestra el `variant_name` limpio del catálogo.
- **`left join` y no `join`**: las ventas mandan; si un nombre o régimen no casa, la venta se queda con el campo vacío y un test avisa, en vez de desaparecer.
- **Régimen de impuesto**: se traduce a `tax_type_code` y **no se asume el estándar en silencio**. La tasa se resuelve en gold (depende de país y fecha).
- **Incremental (`merge` por `sale_id`)**: filtra bronce por `_loaded_at` mayor que el máximo ya cargado. El merge inserta las ventas nuevas y actualiza las existentes (correcciones). El resto de la lógica no cambia porque se aplica solo al lote nuevo. `--full-refresh` reconstruye todo (reset de la demo).
- **Dónde investigar si algo falla**: el log de `dbt run` (varias sentencias SQL: tabla temporal, `merge`, limpieza; el `0` es el merge sin filas nuevas), los conteos en bronce (`count(*)` y `count(distinct sale_id)`) y silver, y `_source_file` para saber de qué lote viene una fila.

## 9. Cómo se decidió la clasificación de los defectos (UC5, D-071)
**Historia para contar (es un buen ejemplo de criterio propio):** «La primera clasificación era por sistema y metía todo el sistema eléctrico en electrónica y software. Al revisarla vi que **eléctrico no es lo mismo que electrónico**, y que el airbag no es ni mecánico ni electrónico. Miré los datos y descubrí que NHTSA da un segundo nivel de detalle: de las 5.845 filas del sistema eléctrico, 4.129 dicen literalmente "software" y el resto son baterías y cableado. Así que la regla usa primero el nombre del componente y después una tabla por sistema. Lo que no se puede clasificar con honestidad va a una categoría aparte.»

**Mensaje:** una clasificación de negocio no se adivina, se revisa con los datos; y es mejor una categoría «mixta» honesta que forzar cada defecto a un lado.

**Preguntas probables:**
- *¿Por qué no separas software de electrónica?* NHTSA no indica si un defecto se corrige con una actualización; la etiqueta SOFTWARE solo aparece en una parte de los componentes. Separarlos obligaría a inventar.
- *¿Por qué un seed y no un `case when` en el modelo?* Porque es una decisión de negocio: se ve, se revisa y se cambia sin tocar el código.
- *¿Y si aparece un sistema nuevo?* Cae en `UNCLASSIFIED` y un test avisa.

## 10. Un entorno de trabajo internacional simulado (por qué hay cosas en inglés)
**Qué decir:** «He trabajado como en un equipo internacional: el código (modelos, columnas, ramas), los mensajes de commit y los títulos de los pull requests están en inglés, con el formato de *Conventional Commits* (`feat:`, `fix:`, `docs:`, `test:`), y la documentación va en español e inglés. Así cualquier persona de otro país podría leer y revisar el repositorio.»

**Qué se ve en el repositorio:**
- Mensajes de commit como `feat(dbt): add gold star schema for Europe sales` o `fix(dbt): restore generate_schema_name macro`.
- Pull requests con título y comentario descriptivo, y un flujo con revisión de entornos: `feature` → `develop` → `pre` → `main`.
- Un `CONTRIBUTING.md` con las convenciones, y un registro de decisiones numerado (`D-001` en adelante).

**Por qué es un plus:** en una empresa real el código lo leen y lo mantienen otras personas; un estilo común y un historial legible valen tanto como el código.

## 11. Qué aporta el autor frente a una IA (conocimiento de negocio)
**Qué decir:** «Una IA puede escribir mucho código, pero no sabe qué decisión de negocio es la correcta. Esas decisiones las he tomado yo, con conocimiento de coches y del entorno de trabajo, y están escritas con fecha en el registro de decisiones.»

**Ejemplos concretos, todos en el repositorio (D-xxx):**
- **Vocabulario del automóvil:** que una *familia* (Clase C) no es un *modelo* (C 300 e), y que el año modelo no es el de la venta. De ahí sale el grano de las tablas y que `dim_family` se comparta entre ventas y campañas (D-059).
- **Propulsión y carrocería** como ejes del análisis por el cambio de motores (combustión, híbrido, eléctrico).
- **El CLS es un turismo** y debía estar en los defectos, aunque no estuviera en el catálogo de ventas; las furgonetas y autobuses no.
- **Airbags e iluminación no son ni mecánicos ni electrónicos**, y **eléctrico no es electrónico** (D-071): la clasificación de los defectos salió de esas dos objeciones.
- **Reglas de negocio:** impuestos con régimen estándar y reducido según el país (D-060), concesionarios que se renombran o cierran (D-052), precio sin impuestos y en euros con el tipo de cambio del mes de la venta (D-069).
- **Qué se avisa y qué se corrige:** no corregir en silencio un dato dudoso (D-066, D-070).
- **Alcance:** qué se deja fuera (predicción de ventas, más regiones) para terminar bien lo esencial.

**Mensaje:** la IA aceleró la escritura; el criterio, el alcance y la comprobación de que los números tienen sentido fueron míos. Un proyecto de datos sin conocimiento del negocio da números correctos que no significan nada.

## 12. Por qué `dim_date` no usa un paquete (D-073)
- **Pregunta probable:** «¿No hay un paquete de dbt para generar la dimensión de fechas?»
- **Respuesta:** sí: `dbt_utils.date_spine` (genera la secuencia de días) y `dbt_date` (con atributos de calendario). Yo la generé con el `generator()` nativo de Snowflake: son pocas líneas, se entienden enteras y no añaden dependencias. Cubre 2020–2027 (2.922 días) con una fila `-1` «Unknown» para ventas sin fecha válida.
- **Límite que reconozco:** el rango y los atributos son manuales (no hay día de la semana ni semana del año). Si hiciera falta más, pasaría a `date_spine` o `dbt_date`.
- **Mensaje:** conozco la alternativa estándar y elegí la opción más simple para el tamaño del proyecto, sabiendo lo que se pierde.

## 13. Dos fechas en `fct_sales` y una sola `dim_date` (Power BI)
- **Pregunta probable:** «Tienes fecha de venta y fecha de entrega. ¿No hay que duplicar la dimensión de fecha?»
- **Respuesta (confirmada por los profesores):** en el modelado se queda **una sola** `dim_date`, con dos claves en el hecho. En Power BI solo una relación puede estar activa entre dos tablas (la de la fecha de venta); la de entrega queda **inactiva** y se usa dentro de una medida con `USERELATIONSHIP` (`Unidades entregadas`).
- **Cuándo sí se duplicaría (solo en Power BI):** si hiciera falta que **ambas fechas filtraran a la vez** (por ejemplo, un segmentador de año de venta y otro de año de entrega). No hace falta para UC1–UC4, que se analizan por fecha de venta.
- **Por qué no se duplica en el modelo:** una copia más de la dimensión no aporta nada al dato y añade otra tabla y otra relación que mantener.
- **Mensaje:** una dimensión puede jugar varios papeles (*role-playing*); se resuelve con una relación inactiva y una medida, no copiando tablas.

## 14. «Rutas de acceso ambiguas» en Power BI: por qué `dim_family` va directa a los hechos (D-059)
- **Qué pasó:** al cargar el modelo, Power BI creó solo una relación `dim_family` → `dim_model` (por tener ambas la columna `family_id`). Eso dejó **dos caminos** entre `fct_sales` y `dim_family` (`fct_sales → dim_model → dim_family` y `fct_sales → dim_family`), y Power BI **desactivó** una relación para evitar la ambigüedad (la de `dim_model → fct_sales`), con el error «Hay rutas de acceso ambiguas».
- **Cómo se resolvió:** se eliminó la relación automática `dim_family` → `dim_model`, que no forma parte del diseño, y se reactivó `dim_model` → `fct_sales`. Las 9 relaciones del modelo quedan, todas de uno a varios con filtro único de dimensión a hecho.
- **Por qué es así (D-059):** `dim_family` se enlaza **directamente** con los dos hechos, porque es la dimensión compartida: un mismo selector de familia filtra ventas y defectos. Si pasara por `dim_model`, los defectos (que solo conocen la familia, no la variante) no podrían usarla. Por eso en los informes se usa siempre `family_name` de `dim_family`, no la copia que trae `dim_model` como atributo.
- **Mensaje:** una estrella limpia no tiene dos caminos entre dos tablas. Power BI lo detecta y lo avisa; el diseño ya lo evitaba y solo hubo que quitar una relación que la herramienta había añadido por su cuenta.

## 15. ¿Por qué las campañas llegan ya filtradas a bronce? (D-074)
«El fichero de NHTSA trae 248.000 filas de todas las marcas. Hice una **extracción filtrada**, como pedir a la fuente solo Mercedes: el texto llega a bronce tal cual, y la limpieza y la traducción de modelos están en dbt. Lo más fiel sería cargar el fichero entero y filtrar en silver; sé cómo hacerlo (un `.gz` de 14 MB, las 29 columnas y los filtros en `silver_campaign_lines`) y lo dejo como mejora.»
