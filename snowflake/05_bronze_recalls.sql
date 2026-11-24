-- =============================================================================
-- 05 · Bronze for NHTSA recalls (real public data): file format, stage, raw table, load
-- =============================================================================
-- Same pattern as 02_bronze_europe.sql, for the schema DEV_MB_BRONZE_DB.nhtsa.
-- The file comes from `python data/nhtsa/prepare_recalls.py` (14,603 rows, text only).
--
--   Part A: run once (creates objects).
--   Part B: upload data/nhtsa/prepared/mb_recalls_2021_2025.csv by hand to the stage
--           (Snowsight -> Data -> Add Data -> "Load files into a Stage", role MB_INGEST_ROLE,
--            database DEV_MB_BRONZE_DB, schema NHTSA, stage STG_RECALLS, path `batch_1`).
--   Part C: COPY INTO and check.
-- =============================================================================

use role MB_INGEST_ROLE;
use warehouse WH_MB;
use database DEV_MB_BRONZE_DB;

-- ---------- Part A ---------------------------------------------------------------
create file format if not exists nhtsa.ff_recalls
    type = csv
    field_delimiter = ','
    skip_header = 1
    encoding = 'UTF8'
    field_optionally_enclosed_by = '"'
    error_on_column_count_mismatch = true;

create stage if not exists nhtsa.stg_recalls
    directory = (enable = true)
    encryption = (type = 'SNOWFLAKE_SSE')
    comment = 'Landing area for the prepared NHTSA recall file';

create table if not exists nhtsa.raw_recalls (
      record_id         varchar
    , campno            varchar
    , maketxt           varchar
    , modeltxt          varchar
    , yeartxt           varchar
    , compname          varchar
    , potaff            varchar
    , rcdate            varchar
    , _source_file      varchar
    , _file_row_number  number
    , _loaded_at        timestamp_ltz default current_timestamp()
);

-- ---------- Part B: check the file is in the stage ---------------------------------
-- list @nhtsa.stg_recalls;

-- ---------- Part C: load -------------------------------------------------------------
copy into nhtsa.raw_recalls
    (record_id, campno, maketxt, modeltxt, yeartxt, compname, potaff, rcdate,
     _source_file, _file_row_number)
from (
    select $1, $2, $3, $4, $5, $6, $7, $8,
           metadata$filename, metadata$file_row_number
    from @nhtsa.stg_recalls/batch_1/
)
file_format = (format_name = 'nhtsa.ff_recalls')
pattern = '.*mb_recalls.*[.]csv'
on_error = 'ABORT_STATEMENT';

-- Check: expected 14,603 rows and 181 distinct campaign numbers.
-- select count(*) as rows_loaded, count(distinct campno) as campaigns from nhtsa.raw_recalls;
