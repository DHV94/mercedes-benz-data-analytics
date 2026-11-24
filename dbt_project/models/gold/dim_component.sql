-- One row per recalled component (e.g. SEAT BELTS: REAR/OTHER:BUCKLE ASSEMBLY) with its main system
-- (component_type: SEAT BELTS, ELECTRICAL SYSTEM, AIR BAGS...) and its category for use case UC5 (D-071):
--   ELECTRONICS_SOFTWARE  the component name says SOFTWARE, instrument cluster, ADAS or control module,
--                         or the whole system is electronic (communication, cameras and sensors, stability...)
--   ELECTRICAL            electrical hardware: wiring, fuses, batteries, starter, lighting
--   MECHANICAL            engine, brakes, steering, structure, seat belts...
--   MIXED_OTHER           systems with no single nature (air bags) and equipment
-- Rule: the keywords of the component name come first (NHTSA writes SOFTWARE in the name), and the seed
-- component_type_map decides by system for the rest. A system that is not in the seed gets UNCLASSIFIED
-- and a warning, so a new type never disappears silently.
with components as (
    select distinct component_name, component_type
    from {{ ref('silver_campaign_lines') }}
)

select
    md5(c.component_name) as component_id,
    c.component_name,
    c.component_type,
    case
        when c.component_name like '%SOFTWARE%'
          or c.component_name like '%INSTRUMENT CLUSTER%'
          or c.component_name like '%:ADAS%'
          or c.component_name like '%CONTROL MODULE%'
            then 'ELECTRONICS_SOFTWARE'
        else coalesce(m.component_category, 'UNCLASSIFIED')
    end                   as component_category
from components as c
left join {{ ref('component_type_map') }} as m
    on upper(trim(c.component_type)) = upper(trim(m.component_type))
