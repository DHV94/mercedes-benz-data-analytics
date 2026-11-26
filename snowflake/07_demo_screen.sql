-- Demo en directo: carga incremental y snapshot de concesionarios (entorno DEV)

-- 1 · Antes de cargar
use role DEV_MB_TRANSFORM_ROLE; use warehouse WH_MB;
select count(*) as ventas_silver from DEV_MB_SILVER_DB.DBT_DHV994_CORE.SILVER_SALES;
select sale_id, sale_status, sale_price
from DEV_MB_SILVER_DB.DBT_DHV994_CORE.SILVER_SALES
where sale_id in ('EU-2024-000122', 'EU-2023-000546')
order by sale_id;


-- 2 · Carga en bronze (solo en directo)
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


-- 3 · dbt Cloud
--     dbt build -s silver_sales silver_dealers snap_dealers --exclude-resource-type test


-- 4 · Carga incremental
use role DEV_MB_TRANSFORM_ROLE; use warehouse WH_MB;
with lote as (
    select distinct sale_id from DEV_MB_BRONZE_DB.SALES.RAW_SALES_EU
    where _source_file ilike '%delta_3%'
),
anteriores as (
    select distinct sale_id from DEV_MB_BRONZE_DB.SALES.RAW_SALES_EU
    where _source_file not ilike '%delta_3%'
),
silver as (
    select count(*) as total from DEV_MB_SILVER_DB.DBT_DHV994_CORE.SILVER_SALES
)
select
    count(*)                            as filas_del_lote,
    count_if(a.sale_id is null)         as ventas_nuevas,
    count_if(a.sale_id is not null)     as actualizadas,
    max(silver.total)                   as ventas_silver
from lote as l
left join anteriores as a on l.sale_id = a.sale_id
cross join silver;

select sale_id, sale_status, sale_price
from DEV_MB_SILVER_DB.DBT_DHV994_CORE.SILVER_SALES
where sale_id in ('EU-2024-000122', 'EU-2023-000546')
order by sale_id;


-- 5 · Snapshot: historial de un concesionario
use role DEV_MB_TRANSFORM_ROLE; use warehouse WH_MB;
select dealer_code, dealer_name, dbt_valid_from, dbt_valid_to
from DEV_MB_SILVER_DB.DBT_DHV994_SNAPSHOTS.SNAP_DEALERS
where dealer_code = 'DE-0014'
order by dbt_valid_from;
