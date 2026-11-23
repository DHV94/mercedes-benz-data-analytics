with source as (

    select * from {{ source('bronze_sales', 'raw_sales_eu') }}

),

renamed as (

    select
        nullif(trim(sale_id), '')                   as sale_id,
        upper(nullif(trim(vin), ''))                as vin,
        nullif(trim(model_name), '')                as model_name,
        try_to_number(model_year)                   as model_year,
        coalesce(
            try_to_date(sale_date, 'DD/MM/YYYY'),
            try_to_date(sale_date, 'YYYY-MM-DD'),
            try_to_date(sale_date, 'DD.MM.YY')
        )                                           as sale_date,
        try_to_date(delivery_date, 'DD/MM/YYYY')    as delivery_date,
        upper(nullif(trim(dealer_code), ''))        as dealer_code,
        upper(nullif(trim(country), ''))            as country,
        upper(nullif(trim(currency), ''))           as currency,
        upper(nullif(trim(sale_status), ''))        as sale_status,
        upper(nullif(trim(customer_type), ''))      as customer_type,
        upper(nullif(trim(tax_regime), ''))         as tax_regime,
        try_to_number(
            replace(regexp_replace(sale_price, '[^0-9,-]', ''), ',', '.'), 12, 2
        )                                           as sale_price,
        _source_file,
        _file_row_number,
        _loaded_at
    from source

)

select * from renamed