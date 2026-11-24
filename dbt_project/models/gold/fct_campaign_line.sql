-- One row per campaign line: campaign + family + model year + component. It links to the same dim_family
-- as fct_sales, so one family selector filters sales and recalls together (D-059).
-- units_affected is the figure reported for the campaign: do not add it up across lines (D-058).
select
    md5(l.campaign_number || '|' || l.family_name || '|' || l.model_year || '|' || l.component_name) as campaign_line_id,
    l.campaign_number                                                                               as campaign_id,
    f.family_id,
    l.model_year,
    c.component_id,
    coalesce(to_number(to_char(l.campaign_date, 'YYYYMMDD')), -1)                                   as campaign_date_id,
    l.units_affected
from {{ ref('silver_campaign_lines') }} as l
left join {{ ref('dim_family') }} as f
    on upper(l.family_name) = upper(f.family_name)
left join {{ ref('dim_component') }} as c
    on l.component_name = c.component_name
