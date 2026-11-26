-- ============================================================================
-- DEMO EN DIRECTO: carga incremental + snapshot
-- Mientras dbt trabaja (paso 3) se cuentan las diapositivas 9 y 10.
-- Hoja de Snowsight. Ejecutar bloque a bloque (seleccionar el bloque y Ctrl+Enter).
-- "DIGO:" es lo que se dice en voz alta. "SALE:" es el resultado esperado.
-- Entorno DEV. Los dos ficheros deben estar ya subidos al stage (bloque P1).
-- ============================================================================


-- ############################################################################
-- PREPARACION (antes de presentar, no se enseña)
-- ############################################################################

-- P1. Los dos ficheros estan en el stage (se suben una sola vez desde Snowsight:
--     SALES.STG_EU_SALES, ruta delta_3  <- sales_eu_2025_delta_3.csv
--     CRM.STG_DEALERS,    ruta delta_5  <- dealer_master.csv del delta 5)
use role MB_INGEST_ROLE; use warehouse WH_MB; use database DEV_MB_BRONZE_DB;
list @sales.stg_eu_sales/delta_3/;
list @crm.stg_dealers/delta_5/;
-- SALE: una fila en cada consulta.

-- P2. Estado de partida
use role DEV_MB_TRANSFORM_ROLE; use warehouse WH_MB;
select
    (select count(*) from DEV_MB_BRONZE_DB.SALES.RAW_SALES_EU)                     as filas_bronze,
    (select count(*) from DEV_MB_BRONZE_DB.CRM.RAW_DEALER_MASTER)                  as filas_bronze_dealers,
    (select count(*) from DEV_MB_SILVER_DB.DBT_DHV994_CORE.SILVER_SALES)           as ventas_silver,
    (select count(*) from DEV_MB_SILVER_DB.DBT_DHV994_SNAPSHOTS.SNAP_DEALERS)      as versiones_dealers;
-- SALE: 45051 | 256 | 44382 | 131
-- Si sale otra cosa: NO cargar nada y avisar.

-- P3. Justo antes de presentar, en dbt Cloud (IDE, rama develop): ejecutar el comando UNA vez
--     para que el entorno este despierto (sin cargar nada no cambia datos) y dejarlo escrito:
--     dbt build -s silver_sales silver_dealers snap_dealers --exclude-resource-type test
--     Solo ANTES del paso 2. Dejar abiertas: diapositivas, esta hoja y el IDE.


-- ############################################################################
-- EN DIRECTO
-- ############################################################################

-- ----------------------------------------------------------------------------
-- PASO 1 (20 s) · Antes de cargar
-- DIGO: "En silver hay 44.382 ventas. Me fijo en dos: una esta vendida y la otra
--        tiene este precio. Y el concesionario DE-0014 tiene dos versiones."
-- ----------------------------------------------------------------------------
use role DEV_MB_TRANSFORM_ROLE; use warehouse WH_MB;
select count(*) as ventas_silver from DEV_MB_SILVER_DB.DBT_DHV994_CORE.SILVER_SALES;
select sale_id, sale_status, sale_price
from DEV_MB_SILVER_DB.DBT_DHV994_CORE.SILVER_SALES
where sale_id in ('EU-2024-000122', 'EU-2023-000546')
order by sale_id;
-- SALE: 44382
--       EU-2023-000546 | (estado) | 51627.28
--       EU-2024-000122 | SOLD     | (precio)


-- ----------------------------------------------------------------------------
-- PASO 2 (20 s) · Llegan los ficheros a bronze        *** NO EJECUTAR AL ENSAYAR ***
-- DIGO: "Llega un lote de ventas y un maestro de concesionarios. Los cargo en
--        bronze con un rol que solo sirve para ingesta, tal como llegan."
-- ----------------------------------------------------------------------------
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
-- SALE: 160 filas cargadas y 129 filas cargadas


-- ----------------------------------------------------------------------------
-- PASO 3 (15 s) · Pasar a dbt Cloud, ejecutar (Enter) y VOLVER A LAS DIAPOSITIVAS
--     dbt build -s silver_sales silver_dealers snap_dealers --exclude-resource-type test
-- DIGO mientras corre: "silver_sales es incremental: solo procesa lo que llego
--        despues de la ultima carga y hace merge por sale_id: las ventas nuevas se
--        insertan y las que ya existian se actualizan. El snapshot compara los
--        concesionarios con lo guardado y, si algo cambio, cierra la version
--        antigua y abre una nueva."
-- DIGO al irme: "Mientras dbt trabaja, os enseno el linaje y la calidad."
--
-- >>> DIAPOSITIVAS 9 (linaje) y 10 (calidad): 1:15 <<<
--
-- Al volver, comprobar en el log: silver_sales 160 filas; silver_dealers y snap_dealers correctos.
-- ----------------------------------------------------------------------------


-- ----------------------------------------------------------------------------
-- PASO 4 (25 s) · La incremental
-- DIGO: "Han llegado 160 filas, pero la tabla solo crece en 150: 150 son ventas
--        nuevas y 10 son cambios sobre ventas que ya tenia. Una pasa a devuelta y
--        la otra cambia de precio. No se duplican."
-- ----------------------------------------------------------------------------
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
-- SALE: 160 | 150 | 10 | 44532
--       EU-2023-000546 | (estado) | 49434.82
--       EU-2024-000122 | RETURNED | (precio)


-- ----------------------------------------------------------------------------
-- PASO 5 (15 s) · El snapshot
-- DIGO: "Este concesionario ha cambiado de nombre dos veces. Tengo las tres
--        versiones, con desde cuando y hasta cuando; la vigente no tiene fin.
--        La fecha es cuando dbt detecto el cambio."
-- ----------------------------------------------------------------------------
use role DEV_MB_TRANSFORM_ROLE; use warehouse WH_MB;
select dealer_code, dealer_name, dbt_valid_from, dbt_valid_to
from DEV_MB_SILVER_DB.DBT_DHV994_SNAPSHOTS.SNAP_DEALERS
where dealer_code = 'DE-0014'
order by dbt_valid_from;
-- SALE: 3 filas: "Autohaus München", "... Partner" y "... Partner Group"
--       (la ultima con dbt_valid_to vacio)


-- ############################################################################
-- SI ALGO FALLA
-- ############################################################################
-- COPY dice "0 files processed": ese fichero ya estaba cargado. Seguir en el paso 3.
-- dbt rechaza --exclude-resource-type: ejecutar estos dos comandos, en este orden:
--     dbt run -s silver_sales silver_dealers
--     dbt snapshot
-- Falla Snowflake o dbt: contar la demo con las capturas de docs/evidence 23-28 y 72-74.
