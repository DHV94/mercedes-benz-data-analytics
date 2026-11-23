-- =============================================================================
-- 02 · Bronze for Europe: file formats, stages and raw tables
-- =============================================================================
-- Bronze = the raw copy of what the source sends. Rules (D-008, medallion):
--   * every source column is VARCHAR: nothing is converted or rejected here (dates, prices and
--     model names arrive dirty on purpose and are cleaned in staging/silver with dbt)
--   * three metadata columns say where each row came from:
--       _source_file      file path inside the stage (e.g. delta_1/sales_eu_2025_delta_1.csv)
--       _file_row_number  line of the row inside that file
--       _loaded_at        when it was loaded (same convention as the course: default current_timestamp)
--   * rows are only appended; history is never overwritten
--
-- HOW TO RUN (Snowsight, one step at a time):
--   Part A (this section down to the tables): run once.
--   Part B: upload the CSV files to the stage by hand (Snowsight -> Data -> Add Data ->
--           "Load files into a Stage"; choose role MB_INGEST_ROLE). PUT does not work in worksheets.
--   Part C: COPY INTO. Run it again for every delta (change the folder in the FROM clause).
-- =============================================================================

use role MB_INGEST_ROLE;
use warehouse WH_MB;
use database DEV_MB_BRONZE_DB;

-- ---------- Part A. File formats ------------------------------------------------
-- Europe sales: ';' separator, UTF-8, header line. A row with a different number of columns
-- makes the load fail (this is how a schema change in the source would be noticed).
create file format if not exists sales.ff_eu_sales
    type = csv
    field_delimiter = ';'
    skip_header = 1
    encoding = 'UTF8'
    field_optionally_enclosed_by = '"'
    error_on_column_count_mismatch = true;

-- Dealer master: ',' separator, ISO dates.
create file format if not exists crm.ff_dealers
    type = csv
    field_delimiter = ','
    skip_header = 1
    encoding = 'UTF8'
    field_optionally_enclosed_by = '"'
    error_on_column_count_mismatch = true;

-- ---------- Part A. Stages (internal, one per source) ---------------------------
-- Files are uploaded in sub-folders (batch_1, delta_1 ... delta_6) so two files with the
-- same name (dealer_master.csv) never clash.
create stage if not exists sales.stg_eu_sales
    directory = (enable = true)
    encryption = (type = 'SNOWFLAKE_SSE')
    comment = 'Landing area for Europe sales files';

create stage if not exists crm.stg_dealers
    directory = (enable = true)
    encryption = (type = 'SNOWFLAKE_SSE')
    comment = 'Landing area for dealer master files';

-- ---------- Part A. Raw tables ---------------------------------------------------
create table if not exists sales.raw_sales_eu (
      sale_id           varchar
    , vin               varchar
    , model_name        varchar
    , model_year        varchar
    , sale_date         varchar
    , delivery_date     varchar
    , dealer_code       varchar
    , country           varchar
    , sale_price        varchar
    , currency          varchar
    , sale_status       varchar
    , customer_type     varchar
    , tax_regime        varchar
    , _source_file      varchar
    , _file_row_number  number
    , _loaded_at        timestamp_ltz default current_timestamp()
);

create table if not exists crm.raw_dealer_master (
      dealer_code       varchar
    , dealer_name       varchar
    , country_code      varchar
    , city              varchar
    , region            varchar
    , opening_date      varchar
    , closing_date      varchar
    , is_active         varchar
    , _source_file      varchar
    , _file_row_number  number
    , _loaded_at        timestamp_ltz default current_timestamp()
);

-- ---------- Part B. After uploading the files, check what the stage holds -------
-- list @sales.stg_eu_sales;
-- list @crm.stg_dealers;

-- ---------- Part C. Load batch 1 (history) --------------------------------------
-- COPY remembers which files it has already loaded (per stage path): running it twice
-- does NOT load the same file twice. That is the first line of defence against duplicates.
-- The column list leaves out _loaded_at so it takes its DEFAULT.
copy into sales.raw_sales_eu
    (sale_id, vin, model_name, model_year, sale_date, delivery_date, dealer_code, country,
     sale_price, currency, sale_status, customer_type, tax_regime, _source_file, _file_row_number)
from (
    select $1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13,
           metadata$filename, metadata$file_row_number
    from @sales.stg_eu_sales/batch_1/
)
file_format = (format_name = 'sales.ff_eu_sales')
pattern = '.*sales_eu_.*[.]csv'
on_error = 'ABORT_STATEMENT';

copy into crm.raw_dealer_master
    (dealer_code, dealer_name, country_code, city, region, opening_date, closing_date, is_active,
     _source_file, _file_row_number)
from (
    select $1, $2, $3, $4, $5, $6, $7, $8,
           metadata$filename, metadata$file_row_number
    from @crm.stg_dealers/batch_1/
)
file_format = (format_name = 'crm.ff_dealers')
pattern = '.*dealer_master[.]csv'
on_error = 'ABORT_STATEMENT';

-- ---------- Part C. Checks after batch 1 ----------------------------------------
-- Expected (seed 42): 44,733 rows, 44,072 distinct sale_id (661 exact duplicates), 128 dealers.
-- select count(*) as rows_loaded, count(distinct sale_id) as distinct_sales from sales.raw_sales_eu;
-- select _source_file, count(*) as rows_in_file from sales.raw_sales_eu group by 1 order by 1;
-- select count(*) as dealers from crm.raw_dealer_master;

-- ---------- Part C. Later: load a delta (change the folder; one delta at a time) --
-- Same COPY statements with  from @sales.stg_eu_sales/delta_1/  and  from @crm.stg_dealers/delta_1/
-- Expected rows after every delta: see docs/es/demo_scenarios.md
