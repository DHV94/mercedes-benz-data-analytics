-- One row per car family (A-Class, C-Class, GLC...). Shared by fct_sales and fct_campaign_line (D-059).
-- Families come from the model catalog AND from the recalls: CLS has recalls but is not in our simulated
-- sales catalog, so it appears here without sales (a family that nobody bought in our data).
-- family_id is a hash of the cleaned name: the same family always gets the same key,
-- in every run and every environment (a row_number() would change if the order changed).
with families as (
    select trim(model_family) as family_name from {{ ref('model_catalog') }}
    union
    select trim(family_name) as family_name from {{ ref('silver_campaign_lines') }}
)

select
    md5(upper(family_name)) as family_id,
    family_name
from families
