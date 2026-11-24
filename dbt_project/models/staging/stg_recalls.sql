-- Same rows as bronze (14,603), with the right types and clean text. Nothing is removed here.
select
    try_to_number(nullif(trim(record_id), ''))          as record_id,
    upper(nullif(trim(campno), ''))                     as campaign_number,
    upper(nullif(trim(maketxt), ''))                    as make,
    upper(nullif(trim(modeltxt), ''))                   as model_text,
    try_to_number(nullif(trim(yeartxt), ''))            as model_year,
    upper(nullif(trim(compname), ''))                   as component_name,
    try_to_number(nullif(trim(potaff), ''))             as units_affected,
    try_to_date(nullif(trim(rcdate), ''), 'YYYYMMDD')   as campaign_date,
    _source_file,
    _file_row_number,
    _loaded_at
from {{ source('bronze_nhtsa', 'raw_recalls') }}
