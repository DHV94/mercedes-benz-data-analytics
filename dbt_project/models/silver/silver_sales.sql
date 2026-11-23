-- Author: Daniel Herrera
-- Version: 1.0

with sales as (

    select * from {{ ref('stg_sales_eu') }}

)

select
    *
from sales
qualify row_number() over (
    partition by sale_id
    order by _loaded_at desc, _source_file desc, _file_row_number desc
) = 1