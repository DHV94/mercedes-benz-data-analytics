-- One row per model variant (51). The family comes from dim_family, so its key is defined in one place.
-- Silver joins on model_variant_code (the stable key); model_name is the clean name shown in reports.
select
    md5(upper(c.model_variant_code)) as model_id,
    c.model_variant_code,
    c.variant_name                   as model_name,
    f.family_id,
    f.family_name,
    c.body_type                      as bodywork,
    c.powertrain                     as propulsion,
    c.available_from                 as first_model_year,
    c.available_to                   as last_model_year
from {{ ref('model_catalog') }} as c
left join {{ ref('dim_family') }} as f
    on upper(trim(c.model_family)) = upper(f.family_name)
