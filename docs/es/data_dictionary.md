# Diccionario de datos

Qué es cada columna, de dónde viene y qué se le hace. Borrador de Claude para que el autor lo revise y cambie lo que quiera. **Gold se añade cuando esté construido** (`dim_*` y `fct_sales`, según el modelo dimensional v7).

Convenciones: las columnas que empiezan por `_` son **metadatos de carga** (de qué archivo y cuándo llegó cada fila); no son datos de negocio.

---

## 1. Bronce · `DEV_MB_BRONZE_DB.sales.raw_sales_eu`
Texto tal como llega del sistema de ventas de Europa. **Todas las columnas son `VARCHAR`** salvo los metadatos. No se limpia nada.

| Columna | Qué es | Ejemplo / notas |
|---|---|---|
| `sale_id` | Identificador de la venta (`EU-AAAA-NNNNNN`) | `EU-2025-000123`. Puede repetirse (duplicados y reenvíos) |
| `vin` | Número de bastidor del vehículo | 17 caracteres; puede venir vacío o inválido (D03, D04) |
| `model_name` | Nombre del modelo, escrito de formas distintas | `C 300 e`, `c300e`, `Mercedes-Benz C 300 E` (D05, D14) |
| `model_year` | Año modelo del vehículo | `2024` |
| `sale_date` | Fecha de la venta | `DD/MM/AAAA`; puede venir en otros formatos o imposible (`31/02/2024`, D06) |
| `delivery_date` | Fecha de entrega | Vacía si aún no se ha entregado |
| `dealer_code` | Código del concesionario | `DE-0014`; puede no existir en el maestro (D15) |
| `country` | País de la venta | `DE`, `GB`, `FR`, `IT`, `ES`, `CH` |
| `sale_price` | Precio con impuestos, en moneda local | Coma decimal; puede traer símbolo o separador de miles (D09) |
| `currency` | Moneda | `EUR`, `GBP`, `CHF`; con variantes (`eur`, `€`, D12) |
| `sale_status` | Estado de la venta | `sold`, `returned`, `cancelled` |
| `customer_type` | Tipo de cliente | `private`, `company`, `fleet`; a veces vacío (D20) |
| `tax_regime` | Régimen de impuesto aplicado | `STD` (estándar) o `RED` (reducido); con otras grafías (D24) |
| `_source_file` | Archivo del que viene la fila | `batch_1/sales_eu_2023.csv`, `delta_2/...` |
| `_file_row_number` | Línea dentro de ese archivo | Distingue duplicados exactos |
| `_loaded_at` | Momento de la carga en Snowflake | Base del filtro del incremental |

## 2. Bronce · `DEV_MB_BRONZE_DB.crm.raw_dealer_master`
Una fila por concesionario **y por entrega**. Texto, salvo los metadatos.

| Columna | Qué es | Notas |
|---|---|---|
| `dealer_code` | Código del concesionario | Clave natural. `PAÍS-NNNN` |
| `dealer_name` | Nombre comercial | Cambia con los renombrados (deltas 4 y 5) |
| `country_code` | País | `DE`, `GB`, `FR`, `IT`, `ES`, `CH` |
| `city`, `region` | Ciudad y región | |
| `opening_date`, `closing_date` | Fechas de apertura y cierre | ISO `AAAA-MM-DD`; cierre vacío si sigue abierto |
| `is_active` | ¿Está abierto? | `true` / `false` |
| `_source_file`, `_file_row_number`, `_loaded_at` | Metadatos de carga | Igual que en ventas |

---

## 3. Staging · `stg_sales_eu` (vista)
Misma tabla que bronce, con **tipos correctos y texto limpio**. No quita filas (44.733 → 44.733).

| Columna | Tipo | Qué se hace |
|---|---|---|
| `sale_id` | texto | `trim`; vacío → nulo |
| `vin` | texto | `trim`, mayúsculas; vacío → nulo |
| `model_name` | texto | `trim` (la equivalencia se hace en silver) |
| `model_year` | número | `try_to_number` |
| `sale_date` | fecha | Prueba tres formatos (`DD/MM/AAAA`, `AAAA-MM-DD`, `DD.MM.AA`); imposible → nulo (D-066) |
| `delivery_date` | fecha | `DD/MM/AAAA`; vacío → nulo |
| `dealer_code`, `country`, `currency`, `sale_status`, `customer_type`, `tax_regime` | texto | `trim`, mayúsculas; vacío → nulo |
| `sale_price` | número (12,2) | Quita símbolos y miles, coma decimal → punto |
| `_source_file`, `_file_row_number`, `_loaded_at` | — | Sin cambios |

## 4. Staging · `stg_dealer_master` (vista)
| Columna | Tipo | Qué se hace |
|---|---|---|
| `dealer_code`, `country_code` | texto | `trim`, mayúsculas; vacío → nulo |
| `dealer_name`, `city`, `region` | texto | `trim`; vacío → nulo |
| `opening_date`, `closing_date` | fecha | `try_to_date` con `AAAA-MM-DD`; vacío → nulo |
| `is_active` | booleano | `try_to_boolean` |
| metadatos | — | Sin cambios |

---

## 5. Silver · `silver_sales` (tabla incremental, `merge` por `sale_id`)
Una fila por venta (la versión más reciente). Todas las columnas de `stg_sales_eu` más:

| Columna | Qué es | Cómo se obtiene |
|---|---|---|
| `model_variant_code` | Clave estable del modelo (`C300E`) | Cruce con el seed `model_alias`, sin distinguir mayúsculas. Nulo = modelo desconocido |
| `regime_code` | `STD` o `RED` | Cruce con el seed `tax_regime_map`. Nulo = régimen desconocido (alerta) |
| `tax_type_code` | `VAT_STANDARD` o `VAT_REDUCED` | Mismo cruce. La **tasa** se resuelve en gold con país y fecha |

## 6. Silver · `silver_dealers` (tabla)
Una fila por concesionario: la **entrega más reciente** (`_loaded_at`, `_source_file` descendentes). Mismas columnas que `stg_dealer_master`.

## 7. Snapshot · `snap_dealers` (historial SCD2)
Una fila por **versión** de cada concesionario. Vigila `dealer_name`, `city`, `region`, `closing_date`, `is_active`.

| Columna | Qué es |
|---|---|
| `dealer_code` … `is_active` | Valores del concesionario en esa versión |
| `dbt_valid_from` | Cuándo detectó dbt esa versión |
| `dbt_valid_to` | Cuándo dejó de valer. **Nulo = versión vigente** |
| `dbt_scd_id`, `dbt_updated_at` | Identificador técnico de la versión y fecha de actualización |

---

## 8. Seeds (`DEV_MB_SILVER_DB.<esquema>_REFERENCE`)
| Seed | Columnas | Para qué |
|---|---|---|
| `model_alias` | `raw_name`, `model_variant_code` | Todas las grafías de cada modelo → clave estable (300 filas) |
| `model_catalog` | `model_variant_code`, `model_family`, `variant_name`, `body_type`, `powertrain`, `available_from`, `available_to`, `base_price_eur`, `popularity` | Catálogo de 51 variantes (7 carrocerías, 5 motorizaciones) |
| `tax_types` | `tax_type_code`, `tax_type_name`, `description` | Tipos de impuesto (2) |
| `taxes` | `country_code`, `tax_type_code`, `tax_value`, `valid_from`, `valid_to` | Tasa por país, tipo y vigencia (11) |
| `tax_regime_map` | `raw_regime`, `regime_code`, `tax_type_code` | Grafías del régimen → código y tipo (8) |
