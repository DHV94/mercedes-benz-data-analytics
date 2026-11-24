-- One row per tax rate with its validity period (11 rows): country + tax type + start date (D-060, D-061).
-- A null valid_to means "still in force". The sale picks its row by country, tax type and sale date.
select
    md5(t.country_code || '|' || t.tax_type_code || '|' || to_char(t.valid_from)) as tax_id,
    t.country_code,
    t.tax_type_code,
    ty.tax_type_name,
    t.tax_value                                                                   as tax_rate,
    t.valid_from,
    t.valid_to
from {{ ref('taxes') }} as t
left join {{ ref('tax_types') }} as ty
    on t.tax_type_code = ty.tax_type_code
