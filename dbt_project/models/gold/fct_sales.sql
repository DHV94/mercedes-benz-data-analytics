-- One row per sale (grain = sale_id), Europe only (D-056). Keys point to the gold dimensions.
-- Missing dates use the "unknown" date -1. A model, dealer or tax that cannot be matched stays null
-- on purpose: the relationships tests in _gold.yml report it instead of hiding it.
with sales as (
    select * from {{ ref('silver_sales') }}
),

models as (
    select model_id, family_id, model_variant_code from {{ ref('dim_model') }}
),

dealers as (
    -- the sale points to the current version of the dealer (D-058)
    select dealer_id, dealer_code from {{ ref('dim_dealer') }} where is_current
),

taxes as (
    select tax_id, country_code, tax_type_code, tax_rate, valid_from, valid_to from {{ ref('dim_tax') }}
)

select
    md5('EU|' || s.sale_id)                                              as sale_id,
    'EU'                                                                 as source_system,
    s.sale_id                                                            as source_sale_id,
    coalesce(to_number(to_char(s.sale_date, 'YYYYMMDD')), -1)            as sale_date_id,
    coalesce(to_number(to_char(s.delivery_date, 'YYYYMMDD')), -1)        as delivery_date_id,
    m.model_id,
    m.family_id,
    d.dealer_id,
    s.vin,
    s.sale_status                                                        as status,
    case when s.sale_status = 'SOLD' then 1 else 0 end                   as units_sold,
    s.sale_price                                                         as price_local,
    case when s.currency = '€' then 'EUR' else s.currency end            as local_currency,
    t.tax_rate,
    round(s.sale_price / (1 + t.tax_rate / 100), 2)                      as price_net_local,
    t.tax_id
from sales as s
left join models as m
    on s.model_variant_code = m.model_variant_code
left join dealers as d
    on s.dealer_code = d.dealer_code
left join taxes as t
    on s.country = t.country_code
   and s.tax_type_code = t.tax_type_code
   and s.sale_date between t.valid_from and coalesce(t.valid_to, to_date('9999-12-31'))
