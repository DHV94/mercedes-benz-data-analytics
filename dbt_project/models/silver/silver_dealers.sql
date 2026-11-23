-- Author: Daniel Herrera
-- Version: 1.0

with dealers as (

    select * from {{ ref('stg_dealer_master') }}

)

select
    *
from dealers
qualify row_number() over (
    partition by dealer_code
    order by _loaded_at desc, _source_file desc
) = 1