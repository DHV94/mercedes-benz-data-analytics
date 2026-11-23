-- Author: Daniel Herrera
-- Version: 1.0

with sales as (

    select * from {{ ref('stg_sales_eu') }}

),

unique_sales as(

    select
    *
    from sales
    qualify row_number() over (
        partition by sale_id
        order by _loaded_at desc, _source_file desc, _file_row_number desc
    ) = 1

),

model_aliases as (

    select 
           distinct upper(raw_name) as raw_name_upper, 
           model_variant_code
    from {{ ref('model_alias') }}

)

select
    unique_sales.*,
    model_aliases.model_variant_code
from unique_sales
left join model_aliases
    on upper(unique_sales.model_name) = model_aliases.raw_name_upper