-- One row per campaign line: campaign + family + model year + component (grain of the gold fact).
-- 1. The model text of NHTSA is translated to our family by the macro model_to_family.
-- 2. Models we never sell (Sprinter, Metris, CLS...) have no family and are left out.
-- 3. NHTSA repeats one row per model text (GLE 350, GLE 450...): after translating to the family they
--    collapse into one line. units_affected is the campaign figure repeated on every row, so we take the
--    maximum instead of adding it up (adding would count the same vehicles many times, D-058).
with recalls as (
    select
        *,
        regexp_replace(model_text, '^((REDUNDANT|AMG|MAYBACH) )+', '') as model_clean
    from {{ ref('stg_recalls') }}
),

with_family as (
    select
        *,
        {{ model_to_family('model_clean') }} as family_name
    from recalls
)

select
    campaign_number,
    family_name,
    model_year,
    component_name,
    split_part(component_name, ':', 1) as component_type,
    min(campaign_date)                 as campaign_date,
    max(units_affected)                as units_affected,
    count(*)                           as source_rows
from with_family
where family_name is not null
group by campaign_number, family_name, model_year, component_name
