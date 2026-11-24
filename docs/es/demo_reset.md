# Procedimiento de reinicio de la demo

**Para qué:** después de ensayar (cargar `delta_3`, `delta_5`, `delta_6`), la base queda en otro estado. Este procedimiento la devuelve al **estado de partida**: ventas hasta el delta 2 y concesionarios con el delta 4 (snapshot 131/128).

> **NO ejecutar todavía.** Se prueba el miércoles con calma, grabando. Hasta entonces el estado actual ya es el de partida.

## Por qué un `delete` no basta
`COPY INTO` recuerda qué archivos cargó (durante 64 días). Borrar filas con `delete` **no** borra ese recuerdo, y el archivo no se volvería a cargar. `TRUNCATE TABLE` **sí** borra la memoria de carga. Por eso el reinicio vacía las tablas de bronce con `truncate` y vuelve a cargar los archivos que ya están en el stage (no hace falta subirlos otra vez).

## Estado de partida (objetivo)
| Dato | Valor |
|---|---|
| Bronce de ventas | 45.051 filas (44.382 distintas) |
| Silver de ventas | 44.382 |
| Bronce de concesionarios | 256 filas |
| Snapshot | 131 versiones, 128 vigentes |

## Pasos
**1. Ventas: bronce** (rol **`MB_INGEST_ROLE`**). Antes de empezar, comprueba que los archivos siguen en el stage: `list @sales.stg_eu_sales;` (deben verse `batch_1`, `delta_1` y `delta_2`).
```sql
use role MB_INGEST_ROLE; use warehouse WH_MB; use database DEV_MB_BRONZE_DB;
truncate table sales.raw_sales_eu;

copy into sales.raw_sales_eu
    (sale_id, vin, model_name, model_year, sale_date, delivery_date, dealer_code, country,
     sale_price, currency, sale_status, customer_type, tax_regime, _source_file, _file_row_number)
from (
    select $1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13,
           metadata$filename, metadata$file_row_number
    from @sales.stg_eu_sales/
)
file_format = (format_name = 'sales.ff_eu_sales')
pattern = '.*(batch_1|delta_1|delta_2)/sales_eu_.*[.]csv'
on_error = 'ABORT_STATEMENT';
```
Comprueba (rol `DEV_MB_TRANSFORM_ROLE`): 45.051 filas y 44.382 distintas.

**2. Ventas: silver** (IDE de dbt Cloud): `dbt run --full-refresh -s silver_sales`. Comprueba 44.382.

**3. Concesionarios: bronce, solo el lote 1** (rol **`MB_INGEST_ROLE`**):
```sql
use role MB_INGEST_ROLE; use warehouse WH_MB; use database DEV_MB_BRONZE_DB;
truncate table crm.raw_dealer_master;

copy into crm.raw_dealer_master
    (dealer_code, dealer_name, country_code, city, region, opening_date, closing_date, is_active,
     _source_file, _file_row_number)
from (
    select $1, $2, $3, $4, $5, $6, $7, $8, metadata$filename, metadata$file_row_number
    from @crm.stg_dealers/batch_1/
)
file_format = (format_name = 'crm.ff_dealers')
pattern = '.*dealer_master[.]csv'
on_error = 'ABORT_STATEMENT';
```
Comprueba 128 filas.

**4. Snapshot desde cero.** El snapshot guarda el historial en su propia tabla y no se puede "deshacer": se borra y se reconstruye repitiendo la secuencia real.
- Rol **`DEV_MB_TRANSFORM_ROLE`**: `drop table DEV_MB_SILVER_DB.DBT_DHV994_SNAPSHOTS.SNAP_DEALERS;`
- IDE: `dbt run -s silver_dealers` y `dbt snapshot` → **128 y 128**.

**5. Concesionarios: delta 4** (rol **`MB_INGEST_ROLE`**): el mismo `copy` del paso 3, cambiando `batch_1/` por `delta_4/`. Comprueba 256 filas.
- IDE: `dbt run -s silver_dealers` y `dbt snapshot` → **131 y 128**.

**6. (Opcional) gold de DEV:** `dbt build -s gold`.

## Comprobación final
| Consulta (rol `DEV_MB_TRANSFORM_ROLE`) | Esperado |
|---|---|
| Bronce de ventas, filas y distintas | 45.051 / 44.382 |
| Silver de ventas | 44.382 |
| Bronce de concesionarios | 256 |
| Snapshot, versiones y vigentes | 131 / 128 |

## Qué afecta a PRE y PRO
El bronce es único: PRE y PRO leen lo mismo. Tras el reinicio sus tablas se rehacen con el siguiente job (`PRO · build` o el programado del lunes). El snapshot de PRE y PRO no se toca.

## Riesgos y cómo se comprueban
- **El stage no conserva los archivos:** `list @sales.stg_eu_sales;` y `list @crm.stg_dealers;` antes de empezar. Si faltan, hay que subirlos de nuevo.
- **El `delete` por error:** si se borró con `delete` en vez de `truncate`, el `copy` dirá «0 files processed». Solución: `truncate` y repetir.
