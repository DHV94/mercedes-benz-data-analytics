# Diseño de fuentes (BORRADOR v0.1)

> Estado: borrador para revisar. Nada de esto está implementado todavía.
> **Alcance revisado el 2026-11-20 (ver D-021):** fuentes principales Europa, EE. UU. y China; Japón y Corea son opcionales y solo se harán si hay una fuente completa de extremo a extremo. El catálogo de defectos (§5) se recortará al alcance final.
> Objetivo: decidir **qué datos llegan, cómo llegan y qué suciedad traen** antes de escribir el generador.

## 1. Inventario de fuentes

| # | Fuente | Simula | Formato | Destino bronze |
|---|---|---|---|---|
| S1 | `sales_eu` | ERP de Europa | CSV `;` UTF-8 | `BRONZE.sales_eu` |
| S2 | `sales_us` | Sistema de EE. UU. | CSV `,` UTF-8 | `BRONZE.sales_us` |
| S3 | `sales_cn` | Plataforma de China | JSON anidado | `BRONZE.sales_cn` (VARIANT) |
| S4 | `sales_jp` | Sistema de Japón | CSV `,` Shift-JIS (CP932) | `BRONZE.sales_jp` |
| S4b | `sales_kr` | Sistema de Corea del Sur | CSV tabulador, CP949 | `BRONZE.sales_kr` |
| S5 | `dealer_master` | Maestro de concesionarios (CRM) | CSV | `BRONZE.dealer_master` |
| S6 | `nhtsa_recalls` | Datos públicos NHTSA (reales) | Fichero plano | `BRONZE.nhtsa_recalls` |

**Seeds de dbt** (los mantenemos nosotros, van al repo): `model_catalog`, `region_country`, `nhtsa_component_map`, `fx_rates`, `tax_rates`, `status_map`.

> **Por qué así:** cada región es un "equipo" distinto con su propio sistema. Es lo que pasa en una multinacional y obliga a unificar en staging/silver, que es donde dbt aporta valor.

## 2. Campos lógicos (lo que acabará en `fct_sales`)

| Campo lógico | Descripción |
|---|---|
| `sale_id` | Id de la transacción en el sistema origen |
| `vin` | Número de bastidor (17 caracteres) |
| `model_name` | Variante del modelo (ej. `C 300 e`) |
| `model_year` | Año modelo |
| `sale_date` | Fecha de venta |
| `delivery_date` | Fecha de entrega (siempre ≥ `sale_date`) |
| `dealer_code` | Concesionario |
| `country_code` | País (ISO-2) |
| `sale_price` | Precio en **moneda local** |
| `currency` | EUR, GBP, USD, CNY, JPY |
| `sale_status` | vendida / devuelta / cancelada |
| `customer_type` | particular / flota / empresa |
| `gross_price` / `tax_rate` / `net_price` | Se **calculan en silver** a partir de `sale_price` y del seed `tax_rates` |

Cada región nombra y formatea estos campos a su manera (siguiente sección).

## 3. Formato por región

### S1 · Europa (`sales_eu`)
- Países: DE, FR, IT, ES (EUR), GB (GBP) y CH (CHF). Así hay tres monedas en la misma región. Más países no aportan nada nuevo y solo alargan el generador.
- CSV con `;`, UTF-8, cabecera en inglés, **decimal con coma** (`54321,50`), **fecha `dd/mm/yyyy`**.
- Columnas: `sale_id; vin; model_name; model_year; sale_date; delivery_date; dealer_code; country; sale_price; currency; sale_status; customer_type`
- Estados: `sold`, `returned`, `cancelled`.
- Particularidad: el precio **incluye IVA**.

### S2 · EE. UU. (`sales_us`)
- CSV con `,`, UTF-8, columnas con otros nombres, **fecha `mm/dd/yyyy`**.
- Columnas: `transaction_id, vin, model, year, sold_on, delivered_on, dealer_number, state, price_paid, status_cd, buyer_type`
- **Sin columna de moneda** (se da por supuesto USD) y **sin país** (solo `state`, 2 letras). Hay que inferir `country_code = 'US'` y `currency = 'USD'`.
- `price_paid` viene como texto: `"$54,321.00"` (símbolo y miles con coma, entre comillas).
- Estados: `S`, `R`, `C`. Tipo de comprador: `P`, `F`, `B`.
- Particularidad: el precio **no incluye** el impuesto local.

### S3 · China (`sales_cn`)
- Un fichero JSON por lote (array de objetos), **anidado**. Ejemplo:
  ```json
  {"order": {"id": "CN-2024-000123", "ts": "2024-03-15T14:22:10+08:00", "status": "completed"},
   "vehicle": {"vin": "WDD...", "model": "GLC 300 L", "model_year": 2024},
   "dealer": {"id": "SH021", "name": "上海星徽"},
   "price_cny": 398000, "customer": {"type": "private"}}
  ```
- Fecha como **timestamp ISO con zona horaria +08:00** (hay que decidir en qué zona se calcula `sale_date`).
- Precio entero en yuanes, a veces como **string** (`"398000"`).
- Nombres de concesionario en caracteres chinos. Estados: `completed`, `refunded`, `cancelled`.
- En Snowflake se carga en una columna `VARIANT` y se aplana con `FLATTEN` / notación `:` en staging (se vio en el bloque de semiestructurados).

### S4 · Japón (`sales_jp`)
- CSV `,`, codificación **Shift-JIS (CP932)**: en Snowflake hay que declararlo en el `FILE FORMAT` (`ENCODING = 'SHIFT_JIS'`), o los kanjis salen rotos.
- Nombres de columna en **romaji, mayúsculas**: `HANBAI_ID, SHADAI_NO, SHASHU, NENSHIKI, HANBAI_BI, NOUSHA_BI, TENPO_CD, TODOUFUKEN, HANBAI_KAKAKU, JOTAI, KOKYAKU_KUBUN`.
- Fecha **`yyyymmdd`** sin separadores (`20240315`); una pequeña parte en **era Reiwa** (`R6.03.15`) como suciedad extra.
- Precio en JPY sin decimales; algunos con `¥` y coma de miles. Particularidad: el precio **incluye impuesto al consumo** (10 %).
- Estados numéricos: `1` vendida, `2` devuelta, `9` cancelada.
- Prefecturas en lugar de país (`TODOUFUKEN`), a veces en kanji.

### S4b · Corea del Sur (`sales_kr`) — añadido 2026-11-18
- Mercado relevante: en 2025 Mercedes fue la segunda marca importada en Corea (unos 68.000 coches, ~22 % de las importaciones, según KAIDA, el organismo de importadores coreanos).
- CSV con **tabulador**, codificación **CP949 / EUC-KR** (otra codificación distinta de Shift-JIS), fecha `yyyy-mm-dd`.
- Columnas en inglés abreviado: `sale_no, vin, model, model_yr, sale_dt, deliver_dt, dealer_cd, city, price_krw_10k, status, cust_type`.
- **El precio viene en unidades de 10.000 KRW** (`6850` = 68.500.000 KRW), una trampa real y buen defecto de unidades (D23).
- Moneda KRW. El precio incluye IVA (10 %).

### S5 · Maestro de concesionarios (`dealer_master`)
Campos: `dealer_code, dealer_name, country_code, city, region, opening_date, closing_date, is_active`.
Sirve para `dim_dealer`. Incluye concesionarios **cerrados**, otros con **nombre cambiado** (candidato a snapshot SCD2), y códigos que **no existen en las ventas** (y al revés).

### S6 · NHTSA (`nhtsa_recalls`, datos reales)
Descarga de los ficheros planos públicos de la NHTSA filtrando por fabricante Mercedes-Benz. Campos que nos interesan: nº de campaña, fabricante, modelo, año modelo, componente, fecha del informe, unidades afectadas, descripción del defecto. **Revisar los nombres exactos de campos al descargar** (no los doy por definitivos).

## 4. Carga en bronze

- **Todo como texto (`VARCHAR`)** en bronze para CSV: no se pierde nada si el formato viene roto. Los tipos se aplican en staging.
- Columnas técnicas añadidas por la carga: `_source_file` (`METADATA$FILENAME`), `_row_number` (`METADATA$FILE_ROW_NUMBER`), `_loaded_at`.
- Un `STAGE` interno y un `FILE FORMAT` por región (cuatro: EU, US, JP y JSON).
- **Lotes**: 2021–2024, un fichero por región y año; 2025, un fichero por región y mes. Así probamos carga histórica y carga incremental (`COPY INTO` ignora ficheros ya cargados; en dbt, modelo incremental sobre `_loaded_at`).

## 5. Catálogo de suciedad

Porcentajes orientativos sobre las filas de cada región. Cada defecto debe tener su sitio de arreglo y su test.

| ID | Defecto | Dónde | % | Se arregla en | Test dbt |
|---|---|---|---|---|---|
| D01 | Filas duplicadas exactas | Todas | ~1,5 | silver (dedup) | `unique` sobre `sale_id` |
| D02 | Misma venta reenviada en otro lote (`sale_id` repetido, distinta fecha de carga) | Todas | ~0,8 | silver (`qualify row_number`) | `unique` |
| D03 | `vin` nulo o vacío | EU, US | ~0,5 | silver (descarte + registro) | `not_null` con `severity: warn` |
| D04 | `vin` con longitud ≠ 17 o con `I`, `O`, `Q` (no válidos) | Todas | ~0,4 | staging (flag `is_valid_vin`) | test singular |
| D05 | Nombre de modelo inconsistente (`C 300`, `c300`, `C-Class 300`, `C300 `) | Todas | ~12 | silver (macro de normalización + seed) | `relationships` a `dim_model` |
| D06 | Fecha mal formada o imposible (`31/02/2023`) | EU, US, JP | ~0,6 | staging (`try_to_date`) | `not_null` |
| D07 | Fecha de entrega anterior a la de venta | Todas | ~0,4 | silver (flag) | test singular |
| D08 | Venta en fecha futura | EU, US | ~0,2 | silver | test singular |
| D09 | Precio con símbolo, texto o miles (`$54,321.00`, `¥5,200,000`, `398000` como string) | US, JP, CN | 100 en US; ~15 en JP/CN | staging (macro de limpieza de precio) | `accepted_range` (dbt_utils) |
| D10 | Precio negativo o cero | Todas | ~0,3 | silver | test singular |
| D11 | Precio atípico (×10, error de decimales) | EU, US | ~0,2 | silver (flag `is_price_outlier`) | warn |
| D12 | Moneda inconsistente (`EUR`, `eur`, `€`, vacío) | EU | ~2 | staging | `accepted_values` |
| D13 | Estados con códigos distintos por región | Todas | 100 | silver (seed `status_map`) | `accepted_values` |
| D14 | Espacios sobrantes y mayúsculas/minúsculas mezcladas | Todas | ~3 | staging (`trim`, `upper`) | – |
| D15 | Concesionario inexistente en el maestro | Todas | ~0,7 | gold (miembro "desconocido") | `relationships` |
| D16 | Nombre de concesionario escrito de varias formas | Todas | ~5 | silver (por `dealer_code`) | – |
| D17 | Año modelo imposible (año modelo > año de venta + 1) | Todas | ~0,3 | silver (flag) | test singular |
| D18 | Fechas en era Reiwa (`R6.03.15`) | JP | ~2 | staging (macro) | `not_null` |
| D19 | Codificación Shift-JIS mal declarada (kanjis rotos) | JP | demostración | `FILE FORMAT` | – |
| D20 | `customer_type` nulo o con valores nuevos | Todas | ~4 | silver (`unknown`) | `accepted_values` |
| D21 | Columna nueva que aparece en un lote (cambio de esquema) | EU 2025 | 1 lote | bronze/staging | – |
| D22 | Zona horaria: el timestamp chino cruza medianoche al convertir a UTC | CN | ~2 | staging (decisión documentada) | – |

| D23 | Precio en unidades de 10.000 KRW en vez de KRW | KR | 100 | staging (×10.000) | `accepted_range` |

> D09–D13 son las que más "lucen": limpieza de precios y unificación de estados y monedas.
> D21 es opcional y la dejo para el final si da tiempo: es un buen ejemplo de *schema drift*.

## 6. Reglas de negocio a documentar

1. **Moneda**: se conserva `sale_price_local` y `currency`; en gold se calcula `sale_price_eur` con `fx_rates` (tipo mensual) y, si hay tiempo, `sale_price_usd`, etc.
2. **Impuestos (decidido)**: los orígenes envían el precio tal cual (con IVA en EU, JP y CN; sin impuestos en US). En silver se guardan `gross_price`, `tax_rate` y `net_price` usando el seed `tax_rates` (país, tasa, `valid_from`, `valid_to`; las tasas cambian con el tiempo). Los informes usan `net_price` (el IVA no es ingreso de la compañía). **Verificar las tasas reales al crear el seed.**
5. **Consumo semanal (decidido)**: los directivos consultan los datos los **martes por la mañana**. Los ficheros llegan como tarde el lunes; un job de dbt Cloud programado el martes de madrugada reconstruye gold, y se vigila con `dbt source freshness` (aviso si el último `_loaded_at` tiene más de 8 días).
3. **Ventas válidas** para ingresos: `sold`; `returned` y `cancelled` se cuentan aparte.
4. **Fecha de venta**: hora local de cada región.

## 7. Decisiones tomadas (2026-11-18)

1. **Reiwa (D18) y schema drift (D21)**: incluidos.
2. **Europa**: EUR + GBP + CHF.
3. **Impuestos**: precio sin impuestos en los informes, conservando también el bruto (ver regla 2).
4. **Lotes**: histórico anual 2021–2024 y mensual en 2025. Consumo semanal los martes (regla 5).
5. **Renting/leasing/sustitución**: ~~añadido como `acquisition_type`~~ **descartado el 2026-11-20** (D-018) para simplificar: el proyecto solo registra ventas.
6. **Mercados**: Europa (DE, FR, IT, ES, GB, CH), EE. UU., China, Japón y Corea del Sur. India (tercer mercado mundial, pero pequeño para Mercedes), Canadá, México y Australia quedan como ampliación futura.
7. **Peso de cada mercado en la muestra de ~100k** (orientativo, según cifras públicas de 2025: China ~31 % de Mercedes-Benz Cars, Europa ~35 %, EE. UU. ~16 %): Europa 35 %, China 30 %, EE. UU. 18 %, Corea 8 %, Japón 5 % y el resto ajustable. Reparto por países europeos pendiente (Alemania ~213.000 unidades en 2025).

## 8. Pendiente

- Seeds por crear: `tax_rates`, `fx_rates`, `status_map` (cada región nombra los estados distinto).
