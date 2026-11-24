-- Alert: a sale after the last day of the data (variable max_sale_date in dbt_project.yml) cannot exist yet.
select sale_id, sale_date
from {{ ref('silver_sales') }}
where sale_date > to_date('{{ var("max_sale_date") }}')
