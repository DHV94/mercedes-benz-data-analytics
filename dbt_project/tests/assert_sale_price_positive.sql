-- Alert: a sale price of zero or below is impossible. The test returns the bad rows; a test passes when it returns none.
select sale_id, sale_price
from {{ ref('silver_sales') }}
where sale_price <= 0
