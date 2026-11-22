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
