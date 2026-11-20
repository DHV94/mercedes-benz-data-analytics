# Ejercicio de modelado: Mercedes-Benz Data Analytics

> Enunciado para ti, con el mismo formato que los ejercicios del curso (Papelería Lápiz, Gimnasio Pulso…). **No incluye la solución**: la diseñas tú y después la revisamos juntos.
> Todos los datos de ejemplo son **ficticios** (VIN, concesionarios, campañas). Sirven para razonar, no son reales.

## 1. El caso

El departamento de Data Analytics de Mercedes-Benz recibe cada semana datos de ventas desde los sistemas de cada región (Europa, EE. UU. y China). Cada sistema usa **sus propios nombres de columna, formatos de fecha, monedas y códigos**. Además, la compañía quiere cruzar la información con las **campañas de revisión** (*recalls*) que publica la agencia de seguridad vial de EE. UU. (NHTSA).

Dirección explica cómo trabajan:

1. Cada **venta** es un vehículo entregado a un cliente, identificado por su **VIN** (número de bastidor). Se registra con fecha de venta, fecha de entrega, concesionario, precio en moneda local y estado (vendida, devuelta o cancelada).
2. Cada vehículo es de una **variante de modelo** (por ejemplo, *GLC 300 e 4MATIC*). Varias variantes forman una **familia** (*GLC*). La **carrocería** (SUV, berlina, coupé…) y la **propulsión** (combustión, híbrido enchufable, eléctrico…) dependen de la variante.
3. Los **concesionarios** pertenecen a un país y una región. Pueden **cerrar** o **cambiar de nombre** con el tiempo.
4. Cada región cobra en **su moneda**, y los precios incluyen o no impuestos según el país.
5. Una **campaña de revisión** afecta a uno o varios modelos y años modelo, y señala uno o varios componentes defectuosos. Los componentes se clasifican en **software/electrónica**, **mecánica** u **otros**.

## 2. Las tablas de partida

Tamaños orientativos del proyecto final (muestra de demostración).

| Tabla | Qué es | Filas aprox. | Columnas |
|---|---|---|---|
| `sales_eu` | Ventas de Europa | ~45.000 | 12 |
| `sales_us` | Ventas de EE. UU. | ~20.000 | 11 |
| `sales_cn` | Ventas de China (JSON anidado) | ~35.000 | 9 (anidadas) |
| `dealer_master` | Maestro de concesionarios | ~250 | 8 |
| `model_catalog` | Catálogo de variantes | ~50 | 7 |
| `model_alias` | Nombres escritos de varias formas → variante | ~300 | 2 |
| `region_country` | País → región y moneda | ~8 | 4 |
| `fx_rates` | Tipo de cambio mensual a EUR | ~300 | 3 |
| `tax_rates` | Impuesto por país con fechas de validez | ~12 | 4 |
| `status_map` | Estados de cada origen → estado único | ~12 | 3 |
| `nhtsa_recalls` | Campañas de revisión (reales, turismos Mercedes-Benz, informes 2021–2025) | ~45.000 (≈ 220 campañas) | 29 (ver 2.6) |
| `nhtsa_component_map` | Componente NHTSA → grupo | ~100 | 2 |

### 2.1 `sales_eu` (CSV con `;`, decimal con coma, fecha `dd/mm/yyyy`)

| sale_id | vin | model_name | model_year | sale_date | delivery_date | dealer_code | country | sale_price | currency | sale_status | customer_type |
|---|---|---|---|---|---|---|---|---|---|---|---|
| EU-24-000101 | WDD00000000EU0001 | C 300 e | 2024 | 15/03/2024 | 02/04/2024 | DE-0042 | DE | 61250,50 | EUR | sold | private |
| EU-24-000102 | WDD00000000EU0002 | C-Class 300 | 2024 | 18/03/2024 | 05/04/2024 | FR-0107 | FR | 58900,00 | EUR | sold | fleet |
| EU-24-000103 | W1K0000000000EU03 | glc 220 d | 2024 | 20/03/2024 | 05/04/2024 | GB-0011 | GB | 52300,00 | GBP | sold | fleet |
| EU-24-000101 | WDD00000000EU0001 | C 300 e | 2024 | 15/03/2024 | 02/04/2024 | DE-0042 | DE | 61250,50 | EUR | sold | private |

### 2.2 `sales_us` (CSV con `,`, fecha `mm/dd/yyyy`, sin país ni moneda)

| transaction_id | vin | model | year | sold_on | delivered_on | dealer_number | state | price_paid | status_cd | buyer_type |
|---|---|---|---|---|---|---|---|---|---|---|
| US-24-770001 | W1N00000000US0001 | GLC 300 4MATIC | 2024 | 03/22/2024 | 04/01/2024 | 3105 | TX | "$54,321.00" | S | P |
| US-24-770002 | W1N00000000US0002 | EQB 350 | 2024 | 04/02/2024 | 04/20/2024 | 2210 | CA | "$61,800.00" | S | B |
| US-24-770003 | W1N00000000US0003 | G 550 | 2023 | 02/10/2024 | 02/28/2024 | 3105 | TX | "$142,900.00" | R | P |

### 2.3 `sales_cn` (JSON anidado; una fila = un objeto)

```json
{"order": {"id": "CN-2024-000123", "ts": "2024-03-15T14:22:10+08:00", "status": "completed"},
 "vehicle": {"vin": "LE400000000CN0001", "model": "GLC 300 L", "model_year": 2024},
 "dealer": {"id": "SH021", "name": "上海星徽"},
 "price_cny": 398000, "customer": {"type": "private"}}
```

### 2.4 `dealer_master`

| dealer_code | dealer_name | country_code | city | region | opening_date | closing_date | is_active |
|---|---|---|---|---|---|---|---|
| DE-0042 | Autohaus Stern München | DE | München | Bayern | 2005-03-01 | | true |
| FR-0107 | Étoile Paris Nord | FR | Paris | Île-de-France | 2011-09-15 | | true |
| GB-0011 | Three Pointed Star Leeds | GB | Leeds | West Yorkshire | 2008-01-10 | 2024-06-30 | false |
| US-3105 | Lone Star Mercedes Austin | US | Austin | TX | 2015-05-20 | | true |

> Fíjate en que en `sales_us` el concesionario viene como `3105` y aquí como `US-3105`.

### 2.5 Tablas de referencia (seeds)

`model_catalog`

| model_variant_code | model_family | variant_name | body_type | powertrain | first_model_year | last_model_year |
|---|---|---|---|---|---|---|
| C300E | C-Class | C 300 e | Sedan | PHEV | 2022 | |
| C200 | C-Class | C 200 | Sedan | ICE | 2022 | |
| GLC300E | GLC | GLC 300 e 4MATIC | SUV | PHEV | 2023 | |
| GLC220D | GLC | GLC 220 d 4MATIC | SUV | ICE | 2023 | |
| EQB350 | EQB | EQB 350 4MATIC | SUV | BEV | 2022 | |
| G550 | G-Class | G 550 | SUV | ICE | 2019 | |

`model_alias`

| raw_name | model_variant_code |
|---|---|
| C 300 e | C300E |
| C-Class 300 | C300E |
| c300e | C300E |
| glc 220 d | GLC220D |

`region_country`

| country_code | country_name | region | currency |
|---|---|---|---|
| DE | Germany | Europe | EUR |
| GB | United Kingdom | Europe | GBP |
| US | United States | North America | USD |
| CN | China | China | CNY |

`fx_rates`

| rate_month | currency | eur_per_unit |
|---|---|---|
| 2024-03-01 | USD | 0,92 |
| 2024-03-01 | GBP | 1,17 |
| 2024-03-01 | CNY | 0,13 |

`tax_rates`

| country_code | tax_rate | valid_from | valid_to |
|---|---|---|---|
| DE | 0.19 | 2021-01-01 | |
| FR | 0.20 | 2019-01-01 | |
| GB | 0.20 | 2019-01-01 | |
| CN | 0.13 | 2019-04-01 | |

`status_map`

| source_system | source_status | standard_status |
|---|---|---|
| eu | sold | sold |
| us | S | sold |
| us | R | returned |
| cn | completed | sold |

### 2.6 Revisiones (NHTSA)

Datos **reales** del fichero plano de la NHTSA (`data/nhtsa/raw/`, descripción de campos en `RCL.txt`). Es un fichero separado por tabuladores, **sin cabecera**, con 29 campos y fechas `yyyymmdd`. Aquí ves solo los campos que nos interesan. Una misma campaña aparece en **varias filas**.

`nhtsa_recalls` (campos reales; se muestran 4 filas de la campaña `21V232000`)

| RECORD_ID | CAMPNO | MAKETXT | MODELTXT | YEARTXT | COMPNAME | MFGNAME | POTAFF | RCDATE |
|---|---|---|---|---|---|---|---|---|
| 197388 | 21V232000 | MERCEDES-BENZ | GLB 250 | 2020 | STRUCTURE:BODY | Mercedes-Benz USA, LLC | 2362 | 20210401 |
| 197389 | 21V232000 | MERCEDES-BENZ | GLB 250 | 2020 | STRUCTURE:BODY | Mercedes-Benz USA, LLC | 2362 | 20210401 |
| 197390 | 21V232000 | MERCEDES-BENZ | GLB 250 | 2021 | STRUCTURE:BODY | Mercedes-Benz USA, LLC | 2362 | 20210401 |
| 197391 | 21V232000 | MERCEDES-BENZ | GLB 250 | 2021 | STRUCTURE:BODY | Mercedes-Benz USA, LLC | 2362 | 20210401 |

Observaciones del fichero real:
- `POTAFF` = unidades potencialmente afectadas. `RCDATE` = fecha en que se recibe el informe. `YEARTXT` = año modelo (`9999` si se desconoce).
- `COMPNAME` es un texto **jerárquico** separado por `:` (por ejemplo `ELECTRICAL SYSTEM:SOFTWARE`). Hay unos 130 valores distintos solo en el periodo 2021–2025.
- `MODELTXT` viene como cada fabricante lo escribe, con variantes tipo `GLS450` y `GLS 450`, o `AMG C43`. No coincide con nuestro catálogo de variantes.
- `MAKETXT` aparece como `MERCEDES-BENZ`, `MERCEDES BENZ` y `MERCEDES-MAYBACH`. El fichero completo incluye otras marcas (incluidos camiones y autobuses de Daimler), que no son de nuestro alcance. No hay VIN.
- Hay campañas con una sola fila y otras con cientos.

`nhtsa_component_map` (lo mantenemos nosotros; el mapeo completo se hace sobre los componentes reales)

| component_pattern | component_group |
|---|---|
| ELECTRICAL SYSTEM:SOFTWARE | software_electronics |
| POWER TRAIN | mechanical |
| BACK OVER PREVENTION | other |

## 3. Preguntas de negocio

- **UC1** · ¿Cómo han evolucionado las ventas por **familia de modelo** entre 2021 y 2025?
- **UC2** · ¿Y por **carrocería**, entre 2021 y 2025?
- **UC3** · ¿Y por **propulsión**, entre 2021 y 2025?
- **UC4** · ¿Cuáles son las **3 familias más vendidas** por región en 2025?
- **UC5** · ¿Cómo han evolucionado las campañas de revisión por **software/electrónica frente a mecánicas**, por modelo y año?

Todas las ventas se analizan por **región y país**, con importes **sin impuestos y en EUR**.

## 4. Primera parte: la capa silver

1. **Modelo conceptual.** Entidades, relaciones con un verbo y su cardinalidad (1:1, 1:N o N:M). Sin atributos ni tipos.
2. **Modelo lógico.** Atributos de cada entidad, clave primaria, claves foráneas y claves candidatas. Resuelve las relaciones N:M y comprueba 1FN, 2FN y 3FN.
3. **Modelo físico.** Los `CREATE TABLE` de Snowflake, con tipos exactos y `NOT NULL` donde toque.
4. **Prueba.** Con tu modelo, ¿se responden UC1 a UC5?

**Pistas:**
- Tres sistemas de ventas con columnas distintas: ¿qué tabla única de ventas **limpia** salen de ellos? ¿Qué columnas faltan en un origen y hay que deducir?
- Hay filas repetidas y datos escritos de varias formas. ¿Dónde se corrigen y con qué tabla de apoyo?
- ¿La **variante** y la **familia** son dos entidades o una? ¿De cuál depende la carrocería?
- ¿Cuál es la clave natural de una venta? ¿Es suficiente el VIN?
- ¿Qué ocurre con un concesionario que cambia de nombre? ¿Y con uno que cierra?

## 5. Segunda parte: la capa gold

La capa gold se diseña a partir de las preguntas de negocio. Resuélvelas **en orden**: cada una puede invalidar lo anterior.

### Pregunta 1 · «¿Cuántas unidades vendemos cada año por carrocería y por región?»
1. ¿Cuál es el hecho que se mide? Completa: «una fila de esta tabla de hechos es…». ¿Cuál es su clave primaria?
2. ¿Qué medidas guardas? ¿Se pueden sumar? ¿Y el precio en moneda local?
3. ¿Qué dimensiones necesitas? ¿Dónde pones la carrocería, la propulsión y la familia?
4. Dibuja el esquema en estrella y rellena la tabla de hechos con las filas de ejemplo.
5. ¿Cuántas unidades se venden en marzo de 2024 con los datos de ejemplo?

### Pregunta 2 · «¿Cuáles son las 3 familias más vendidas por región en 2025?»
1. ¿Puede responder la tabla de la pregunta 1? ¿Hace falta cambiar algo?
2. ¿La clave de la dimensión de modelo debe ser la variante o la familia? ¿Qué pasa si eliges la equivocada?
3. ¿Qué dimensiones de la pregunta 1 reutilizas?

### Pregunta 3 · «¿Cómo evolucionan las revisiones por software frente a mecánicas?»
1. ¿Puede responderla la tabla de ventas? ¿Por qué?
2. Mira la campaña `21V232000` de la tabla 2.6: ¿cuántas filas tiene y cuántas unidades afectadas hay realmente? Si sumas `POTAFF` fila a fila, ¿cuánto suma? ¿Cuánto debería sumar? ¿Qué ha pasado? ¿Y qué ocurre con la campaña si afecta a dos modelos distintos?
3. Propón una solución: ¿qué tabla de hechos necesitas, qué representa cada fila y qué medidas guarda?
4. ¿Qué dimensiones comparte con la de ventas? ¿Cuál es nueva?

### Pregunta 4 · «¿Podemos mostrar ventas y revisiones en un mismo informe?»
1. ¿Qué dimensión permite filtrar los dos hechos con el mismo selector de modelo? ¿Cómo se llama esa propiedad en un esquema en estrella? Pista: las ventas se registran por **variante** y las revisiones por el **texto de modelo** de la NHTSA (`GLB 250`, `GLS450`…). ¿A qué nivel puedes unirlas y con qué tabla de apoyo?
2. Las ventas son simuladas y las revisiones reales. ¿Es correcto dividir unas entre otras? ¿Qué mostrarías en su lugar?

## 6. Entrega

Puedes responder en un documento, una foto de papel o un diagrama (dbdiagram.io, draw.io o a mano). Incluye siempre:
- el **grano** de cada tabla, escrito como «una fila es…»,
- las **claves** (primarias y foráneas),
- el **diagrama**,
- tus **dudas**: es lo que más me sirve para ayudarte.

Después lo revisamos juntos, sin que yo te dé la solución antes.
