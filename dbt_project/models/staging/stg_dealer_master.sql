-- Author: Daniel Herrera
-- Version: 1.0

with source as (

    select * from {{ source('bronze_crm', 'raw_dealer_master') }}

),

renamed as(
    
    select
        upper(nullif(trim(dealer_code), ''))                        as dealer_code,
        nullif(trim(dealer_name), '')                               as dealer_name,
        upper(nullif(trim(country_code), ''))                       as country_code,
        nullif(trim(city), '')                                      as city,
        nullif(trim(region), '')                                    as region,
        try_to_date(nullif(trim(opening_date), ''), 'YYYY-MM-DD')   as opening_date,
        try_to_date(nullif(trim(closing_date), ''), 'YYYY-MM-DD')   as closing_date,
        try_to_boolean(trim(is_active))                             as is_active,
        _source_file,
        _file_row_number,
        _loaded_at,
    from source
)

select * from renamed

-- Las columnas con _ son metadatos, no se tocan.