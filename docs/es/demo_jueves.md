# Guion de la demo del jueves (definitivo)

> **ANTES DE EMPEZAR cualquier ensayo: iniciar la grabación de pantalla (Win + Alt + R).** Es el plan B si el directo falla.

Sustituye a `live_demo_script.md` (que queda como referencia de los pasos sueltos). Aquí está **solo** lo que se hace el jueves, en orden, con los números exactos.

## Qué se enseña (10-15 minutos de presentación, 3-4 de demo)
1. **Incremental en directo:** cargar el `delta_3` de ventas y ver que dbt solo procesa lo nuevo (160 filas) y que repetirlo da 0.
2. **Snapshot en directo:** cargar el `delta_5` de concesionarios y ver el historial de DE-0014 con tres versiones.
3. **Alertas (grabadas, miércoles):** el delta 6 hace saltar los tests. Se enseña el vídeo.
4. **Gold y Power BI:** el modelo en estrella y el informe, ya hechos.

## Archivos que hay que tener a mano (en tu Drive, carpeta `data`)
| Qué | Archivo | Se sube a |
|---|---|---|
| Ventas del delta 3 | `output/delta_3/sales_eu_2025_delta_3.csv` | `DEV_MB_BRONZE_DB` → `SALES` → stage `STG_EU_SALES`, ruta **`delta_3`** |
| Concesionarios del delta 5 | `output/delta_5/dealer_master.csv` | `DEV_MB_BRONZE_DB` → `CRM` → stage `STG_DEALERS`, ruta **`delta_5`** |

Del delta 3 **no se carga** el `dealer_master.csv` y del delta 5 **no se cargan** las ventas. Cada demo usa un solo archivo.

## Estado de partida (comprobar antes de empezar)
Hoja de Snowsight, rol **`DEV_MB_TRANSFORM_ROLE`**:
```sql
use role DEV_MB_TRANSFORM_ROLE; use warehouse WH_MB;
select count(*), count(distinct sale_id) from DEV_MB_BRONZE_DB.SALES.RAW_SALES_EU;       -- 45.051 y 44.382
select count(*) from DEV_MB_BRONZE_DB.CRM.RAW_DEALER_MASTER;                              -- 256
select count(*), count_if(dbt_valid_to is null) from DEV_MB_SILVER_DB.DBT_DHV994_SNAPSHOTS.SNAP_DEALERS;  -- 131 y 128
```
Si no salen esos números, **no empieces**: sigue el procedimiento de reinicio de `demo_reset.md`.

---

## A) Incremental: delta 3 de ventas
**Qué dices:** «La tabla de ventas de silver es incremental: solo procesa lo que llegó después de la última carga y actualiza por `sale_id`, así que ni se duplican las ventas reenviadas ni las corregidas.»

1. **Subir** el archivo `sales_eu_2025_delta_3.csv` a `STG_EU_SALES`, ruta `delta_3` (sin barras).
2. **Cargar** (rol **`MB_INGEST_ROLE`**):
```sql
use role MB_INGEST_ROLE; use warehouse WH_MB; use database DEV_MB_BRONZE_DB;
copy into sales.raw_sales_eu
    (sale_id, vin, model_name, model_year, sale_date, delivery_date, dealer_code, country,
     sale_price, currency, sale_status, customer_type, tax_regime, _source_file, _file_row_number)
from (
    select $1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13,
           metadata$filename, metadata$file_row_number
    from @sales.stg_eu_sales/delta_3/
)
file_format = (format_name = 'sales.ff_eu_sales')
pattern = '.*sales_eu_.*[.]csv'
on_error = 'ABORT_STATEMENT';
```
3. **Comprobar bronce** (rol `DEV_MB_TRANSFORM_ROLE`): `select count(*) from DEV_MB_BRONZE_DB.SALES.RAW_SALES_EU;` → **45.211** (45.051 + 160).
4. **IDE de dbt Cloud**, rama `develop` o la rama de trabajo: `dbt run -s silver_sales`. En el log, el `merge` procesa **160**.
5. **Comprobar silver** (rol `DEV_MB_TRANSFORM_ROLE`):
```sql
select count(*), count(distinct sale_id) from DEV_MB_SILVER_DB.DBT_DHV994_CORE.SILVER_SALES;   -- 44.532 y 44.532
```
Son 44.382 + 150 nuevas. Las otras 10 filas son **correcciones** de ventas antiguas (6 pasan a `RETURNED` y 4 cambian de precio): se actualizan, no se suman.
6. **Repetir** `dbt run -s silver_sales`: el merge procesa **0** (idempotencia).
7. (Opcional, 30 s) llevarlo a gold: `dbt build -s fct_sales`. Gold también es incremental (D-072): el `merge` procesa **160** y la tabla queda en **44.532** filas.

**Números:** bronce 45.211 · silver 44.532 · merge 160 y luego 0.

---

## B) Snapshot: delta 5 de concesionarios
**Qué dices:** «Cada entrega del maestro trae el estado actual de los 128 concesionarios. El snapshot compara con lo que guardó, cierra la versión antigua y abre una nueva, así que no se pierde el nombre anterior.»

1. **Estado de partida** (rol `DEV_MB_TRANSFORM_ROLE`): 131 versiones y 128 vigentes (arriba).
2. **Subir** `dealer_master.csv` del delta 5 a `STG_DEALERS`, ruta `delta_5`.
3. **Cargar** (rol **`MB_INGEST_ROLE`**):
```sql
use role MB_INGEST_ROLE; use warehouse WH_MB; use database DEV_MB_BRONZE_DB;
copy into crm.raw_dealer_master
    (dealer_code, dealer_name, country_code, city, region, opening_date, closing_date, is_active,
     _source_file, _file_row_number)
from (
    select $1, $2, $3, $4, $5, $6, $7, $8, metadata$filename, metadata$file_row_number
    from @crm.stg_dealers/delta_5/
)
file_format = (format_name = 'crm.ff_dealers')
pattern = '.*dealer_master[.]csv'
on_error = 'ABORT_STATEMENT';
```
4. **Comprobar bronce** (rol `DEV_MB_TRANSFORM_ROLE`): `select count(*) from DEV_MB_BRONZE_DB.CRM.RAW_DEALER_MASTER;` → **385** (256 + 129: el delta 5 añade un concesionario).
5. **IDE de dbt Cloud, dos comandos y por este orden:** `dbt run -s silver_dealers` y después `dbt snapshot`. La rama debe contener `snapshots/snap_dealers.sql` (si no, «Success» sin hacer nada: comprueba que el log dice `1 of 1`, no `0 of 0`).
6. **Captura estrella** (rol `DEV_MB_TRANSFORM_ROLE`):
```sql
select dealer_code, dealer_name, dbt_valid_from, dbt_valid_to
from DEV_MB_SILVER_DB.DBT_DHV994_SNAPSHOTS.SNAP_DEALERS
where dealer_code = 'DE-0014' order by dbt_valid_from;
```
Tres filas: «Autohaus München», «… Partner» y «… Partner Group». Las dos primeras tienen `dbt_valid_to` y la última no.
7. **Totales:** `select count(*), count_if(dbt_valid_to is null) from DEV_MB_SILVER_DB.DBT_DHV994_SNAPSHOTS.SNAP_DEALERS;` → **135** y **129**.
8. **Repetir** `dbt snapshot` sin cargar nada: los números no cambian.

**Qué cambió en el delta 5:** dos cierres (GB-0112 e IT-0278), DE-0014 se renombra otra vez («Group») y se abre CH-0999.
**Nota para decir:** las fechas de `dbt_valid_from` son «cuándo lo detectó dbt», no el día real del cambio (`defense_justifications.md`, apartado 4).

---

## C) Alertas (vídeo del miércoles)
El delta 6 trae 10 filas defectuosas a propósito. Lo que se ve al ejecutar `dbt test -s silver_sales`:
| Test | Resultado esperado |
|---|---|
| `assert_sale_price_positive` | **aviso** 126 (124 previos + 2 nuevas) |
| `accepted_values` de `sale_status` | **error** (1 fila, estado `UNKNOWN`) |
| `not_null` de `regime_code` | **error** (2 filas) |
| `assert_sale_date_not_in_future` | **error** (2 filas, fechas de 2026) |
| `assert_reduced_tax_only_where_it_exists` | **error** (1 fila, reducido en CH) |
Y en gold, el aviso de `dealer_id` sube de 212 a 214 (dos concesionarios inexistentes).

## Después de las demos
Por orden: parar la grabación; guardar el vídeo fuera del repositorio; **reiniciar** si hay otra demo (`demo_reset.md`).

## Si algo falla (plan B)
1. Enseñar el vídeo grabado en el ensayo.
2. Si falla la carga: comprobar que el rol es `MB_INGEST_ROLE` y la ruta del stage (`delta_3` o `delta_5`, sin barras).
3. Si dbt no ve la tabla: comprobar la rama del IDE y hacer `Refresh`.
4. Si falla Snowflake por completo: capturas de evidencias (`docs/evidence/`, números 23-25 y 26-28 y 72-74) cuentan la misma historia.

## Qué ve Power BI
Power BI lee de **PRO**. La demo del jueves actualiza **DEV** (el bronce es único, pero silver y gold se calculan por entorno). PRO se pone al día con su job: se puede mostrar una ejecución anterior de `PRO · build` o lanzarlo (1,5 minutos).
