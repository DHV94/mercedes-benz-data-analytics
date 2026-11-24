-- One row per sale (grain = sale_id), Europe only (D-056). Keys point to the gold dimensions.
-- Missing dates use the "unknown" date -1. A model, dealer or tax that cannot be matched stays null
-- on purpose: the relationships tests in _gold.yml report it instead of hiding it.
with sales as (
    select
        *,
        -- currency variants (eur, €, £) are normalised to the code of the three currencies
        case
            when currency in ('EUR', '€') then 'EUR'
            when currency in ('GBP', '£') then 'GBP'
            else currency
        end as currency_code
    from {{ ref('silver_sales') }}
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
),

fx as (
    -- monthly rate to euros (D-054): the sale uses the rate of its own month, so history never changes
    select month_start, currency, rate_to_eur from {{ ref('fx_rates') }}
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
    s.currency_code                                                      as local_currency,
    t.tax_rate,
    round(s.sale_price / (1 + t.tax_rate / 100), 2)                      as price_net_local,
    fx.rate_to_eur                                                       as exchange_rate,
    round(s.sale_price / (1 + t.tax_rate / 100) * fx.rate_to_eur, 2)     as price_net_eur,
    t.tax_id
from sales as s
left join models as m
    on s.model_variant_code = m.model_variant_code
left join dealers as d
    on s.dealer_code = d.dealer_code
left join fx
    on s.currency_code = fx.currency
   and date_trunc('month', s.sale_date) = fx.month_start
left join taxes as t
    on s.country = t.country_code
   and s.tax_type_code = t.tax_type_code
   and s.sale_date between t.valid_from and coalesce(t.valid_to, to_date('9999-12-31'))
