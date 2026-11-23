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

), 

tax_regimes as (

    select distinct
        upper(raw_regime) as raw_regime_upper,
        regime_code,
        tax_type_code
    from {{ ref('tax_regime_map') }}

)

select
    unique_sales.*,
    model_aliases.model_variant_code,
    tax_regimes.regime_code, 
    tax_regimes.tax_type_code
from unique_sales
left join model_aliases
    on upper(unique_sales.model_name) = model_aliases.raw_name_upper
left join tax_regimes
    on upper(unique_sales.tax_regime) = tax_regimes.raw_regime_upper