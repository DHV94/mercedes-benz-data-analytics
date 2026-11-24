# Preguntas para llevar a clase (martes 24/11)

Objetivo: preguntar cosas **concretas**, que demuestran que has pensado el modelo y que el proyecto avanza. Cada una lleva, entre paréntesis, la respuesta que defiendo yo, para que puedas contrastarla con la del profesor.

Estado que puedes contar en una frase: *«Bronce, staging, silver (incremental y snapshot), gold con dos hechos y seis dimensiones, entornos DEV/PRE/PRO con variables de entorno, jobs y macros funcionando. Ahora preparo Power BI.»*

## Las dos principales (las que querías llevar)
**1. Dimensión de concesionario con vigencia y la dimensión de fecha**
> «`dim_dealer` guarda una fila por versión del concesionario, con `valid_from` y `valid_to` como atributos, y no enlaza con `dim_date`, porque un intervalo no es un punto del calendario y enlazar dimensiones con dimensiones rompería la estrella. ¿Os parece correcto, o preferís otro diseño?»

(Mi respuesta: está bien. Es estrella pura. La venta apunta a la versión vigente del concesionario, y como mejora futura se uniría por la fecha de la venta. Las fechas del snapshot significan «detectado el», no la fecha real del cambio.)

**2. Dos fechas contra una sola tabla de fechas**
> «En `fct_sales` tengo dos fechas, la de venta y la de entrega, y las dos apuntan a la misma `dim_date`. Es como un billete con aeropuerto de salida y de llegada contra una sola tabla de aeropuertos. ¿Está bien con una única tabla de fechas, o es mejor duplicarla?»

(Mi respuesta: una sola. Se llama *role-playing dimension*. En Power BI una relación queda activa y la otra inactiva, y se usa con `USERELATIONSHIP`. La fila `-1` cubre las ventas sin fecha válida o sin entregar.)

## Para enseñar que el proyecto avanza
**3. Dimensión compartida entre dos hechos**
> «`dim_family` la comparten `fct_sales` y `fct_campaign_line`, de modo que un selector de familia filtra ventas y defectos. El CLS aparece en los defectos reales de NHTSA pero no en el catálogo de ventas simulado, así que tiene campañas y ninguna venta. ¿Es aceptable que una dimensión tenga miembros que solo existen en uno de los hechos?»

(Mi respuesta: sí, es normal en una dimensión conforme. Lo importante es contarlo como una limitación del catálogo simulado.)

**4. Claves sustitutas con hash**
> «Genero las claves sustitutas con un hash (`md5`) del dato de negocio, en vez de un contador, para que no cambien entre ejecuciones ni entre entornos. ¿Veis algún inconveniente?»

(Mi respuesta: coste de almacenamiento y teórico riesgo de colisión, despreciable aquí. La ventaja es que se pueden reconstruir y reejecutar sin romper los enlaces del hecho.)

**5. Un solo bronce para tres entornos**
> «Mis tres entornos (DEV, PRE y PRO) leen el mismo bronce, porque la ingesta es manual y los datos son los mismos. En un caso real, ¿cada entorno tendría su bronce, o se haría una copia sin coste, como un `clone`?»

(Mi respuesta: en producción real se suele separar o clonar para no probar sobre datos vivos. Aquí es una simplificación consciente: la capa que cambia es silver y gold, y el rol de PRO solo lee de bronce.)

## Si hay tiempo y ánimo
**6. Incremental en gold**
> «Silver es incremental con `merge`. Mi `fct_sales` en gold se reconstruye entera en cada ejecución, porque son 44.000 filas. ¿A partir de qué volumen merece la pena hacerla incremental también?»

**7. Qué esperáis ver en la demo**
> «Para la demo he previsto una carga incremental en directo y un cambio de concesionario que se vea en el snapshot. ¿Falta algo que os gustaría ver?»

## Después de preguntar
Anota las respuestas aquí abajo y se las llevas a Claude para decidir si cambia algo del modelo antes del miércoles.

## Respuestas de los profesores (martes 24/11)
Las tres preguntas que se llevaron finalmente (versión corta de las anteriores).

1. **Dos claves de fecha en `fct_sales` contra una sola `dim_date`.** Sin problema. En el modelado se queda con una única `dim_date`. Solo en Power BI se duplica (una copia para cada fecha) si hace falta aplicar filtros a ambas a la vez.
2. **Fechas en `dim_dealer` y `dim_model` sin enlazar a `dim_date`.** Sin problema: es justificable (estrella, no copo de nieve). Aviso: en `dim_dealer` una de las fechas forma parte de la clave candidata (`dealer_code` + `valid_from`), y eso puede dar problemas al hacer **agregados**, porque un mismo concesionario tiene varias filas (una por versión). Hay que contar por `dealer_code` distinto y no por filas.
3. **Gold de ventas: ¿reconstruir o incremental?** Debe ser **incremental también en gold**. No tiene sentido que lo sea en silver y no en gold. Solo se justificaría no hacerlo en pocos casos en los que los agregados dieran problemas, y aquí no es el caso. → decisión D-072 y rama de feature para hacerlo.

Pendiente de Claude: ninguno.
