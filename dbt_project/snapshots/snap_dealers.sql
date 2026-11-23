{% snapshot snap_dealers %}

-- Author: Daniel Herrera
-- Version: 1.0

{{
    config(
        unique_key='dealer_code',
        strategy='check',
        check_cols=['dealer_name', 'city', 'region', 'closing_date', 'is_active']
    )
}}

-- Si alguna de las columnas de check_cols cambia, se entiende que el estado del concesionario ha cambiado. 
-- No se hacen comprobaciones en los metadatos, porque serán distintos en cada carga (fecha, fichero...)

select
    dealer_code,
    dealer_name,
    country_code,
    city,
    region,
    opening_date,
    closing_date,
    is_active
from {{ ref('silver_dealers') }}

{% endsnapshot %}