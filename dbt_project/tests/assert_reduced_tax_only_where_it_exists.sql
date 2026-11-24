-- Alert: a sale with the reduced tax regime in a country that has no reduced rate (DE, CH) cannot be taxed.
select s.sale_id, s.country, s.tax_type_code
from {{ ref('silver_sales') }} as s
left join {{ ref('taxes') }} as t
    on s.country = t.country_code
   and s.tax_type_code = t.tax_type_code
where s.tax_type_code = 'VAT_REDUCED'
  and t.country_code is null
