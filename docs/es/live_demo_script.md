# Guion de la demo en directo: cargar un delta (versión corta)

Se repite igual para cada delta. Sustituye `N` por el número del delta. Los números esperados están en la tabla del final.

## 0. Antes de empezar (10 segundos)
Mostrar los números de partida. Hoja de Snowsight con rol `MB_INGEST_ROLE`:

```sql
use role MB_INGEST_ROLE; use warehouse WH_MB; use database DEV_MB_BRONZE_DB;
select count(*) as filas_bronce from sales.raw_sales_eu;
select count(*) as filas_silver, count(distinct sale_id) as ventas_distintas
from DEV_MB_SILVER_DB.DBT_DHV994_CORE.SILVER_SALES;
```

## 1. Subir el archivo
Snowsight → Data → Databases → `DEV_MB_BRONZE_DB` → `SALES` → Stages → `STG_EU_SALES` → **+ Files**. Ruta: `delta_N` (sin barras). Archivo: `output/delta_N/sales_eu_2025_delta_N.csv`.

## 2. Cargar en bronce
```sql
copy into sales.raw_sales_eu
    (sale_id, vin, model_name, model_year, sale_date, delivery_date, dealer_code, country,
     sale_price, currency, sale_status, customer_type, tax_regime, _source_file, _file_row_number)
from (
    select $1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13,
           metadata$filename, metadata$file_row_number
    from @sales.stg_eu_sales/delta_N/
)
file_format = (format_name = 'sales.ff_eu_sales')
pattern = '.*sales_eu_.*[.]csv'
on_error = 'ABORT_STATEMENT';
```

## 3. Comprobar bronce
```sql
select _source_file, count(*) from sales.raw_sales_eu group by 1 order by 1;
```

## 4. Ejecutar dbt (IDE de dbt Cloud)
```
dbt run -s silver_sales
```
En el log: `SQL status: SUCCESS <filas>`. Es el número de filas que ha procesado el merge.

## 5. Comprobar silver y repetir
Repetir la consulta de silver del paso 0. Después ejecutar `dbt run -s silver_sales` **otra vez**: debe decir `0`.

## Qué decir en voz alta
1. «Antes: X filas en bronce y Y ventas en silver.»
2. «Cargo el delta: bronce sube a ...»
3. «dbt solo procesa lo nuevo: el log dice ...»
4. «Silver sube a ... Lo repito y procesa 0: es idempotente.»

## Números esperados
| Delta | Filas en el archivo (= merge) | Bronce (total) | Silver (ventas distintas) | Qué prueba |
|---|---|---|---|---|
| 1 | 156 | 44.889 | 44.228 | Carga normal incremental |
| 2 | 162 | 45.051 | 44.382 | 154 nuevas + 8 reenviadas idénticas: no hay duplicados |
| 3 | 160 | 45.211 | 44.532 | 150 nuevas + 10 correcciones (actualiza, no duplica) |
| 4 | 134 | 45.345 | 44.666 | + 3 concesionarios renombrados (snapshot) |
| 5 | 164 | 45.509 | 44.830 | + 2 cierres, otro renombrado y un concesionario nuevo |
| 6 | 180 | 45.689 | 45.000 | + 10 filas de alerta (deben fallar los tests) |

Para los deltas 4 y 5 hay que cargar también `dealer_master.csv` (stage `crm.stg_dealers`, ruta `delta_N`, `COPY` de concesionarios) y ejecutar `dbt snapshot`. Ver `demo_scenarios.md`.

## Plan B
Grabar la pantalla en el ensayo (en Windows: Win + Alt + R) y guardar el vídeo fuera del repositorio. Si el directo falla, se enseña el vídeo.
