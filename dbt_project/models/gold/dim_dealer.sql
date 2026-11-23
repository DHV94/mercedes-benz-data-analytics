-- One row per dealer VERSION, read from the snapshot (D-052, D-058): a renamed dealer has two rows.
-- dealer_id mixes the code and the moment dbt detected the version, so each version has its own key.
-- postal_code and state are not in the dealer master, so they are left out of the model (v7 had them).
select
    md5(dealer_code || '|' || cast(dbt_valid_from as varchar)) as dealer_id,
    dealer_code,
    dealer_name,
    city,
    region                                                      as region_name,
    country_code,
    case country_code
        when 'DE' then 'Germany'
        when 'GB' then 'United Kingdom'
        when 'FR' then 'France'
        when 'IT' then 'Italy'
        when 'ES' then 'Spain'
        when 'CH' then 'Switzerland'
    end                                                         as country_name,
    case when is_active then 'ACTIVE' else 'CLOSED' end         as status,
    dbt_valid_from                                              as valid_from,
    dbt_valid_to                                                as valid_to,
    dbt_valid_to is null                                        as is_current
from {{ ref('snap_dealers') }}
