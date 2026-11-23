-- One row per car family (A-Class, C-Class, GLC...). Shared by fct_sales (D-059).
-- family_id is a hash of the cleaned name: the same family always gets the same key,
-- in every run and every environment (a row_number() would change if the order changed).
select distinct
    md5(upper(trim(model_family))) as family_id,
    trim(model_family)             as family_name
from {{ ref('model_catalog') }}
