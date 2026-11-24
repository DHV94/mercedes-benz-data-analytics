-- One row per recalled component (e.g. SEAT BELTS: REAR/OTHER:BUCKLE ASSEMBLY) with its main system
-- (component_type: SEAT BELTS, ELECTRICAL SYSTEM, AIR BAGS...). Used by fct_campaign_line.
select distinct
    md5(component_name)  as component_id,
    component_name,
    component_type
from {{ ref('silver_campaign_lines') }}
