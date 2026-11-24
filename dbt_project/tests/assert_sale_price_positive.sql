{{ config(severity='warn', store_failures=true) }}

-- Alert: a sale price of zero or below is impossible. Warning, not error: the normal data already carry
-- this defect (D10, about 0.3 % of the rows), so the test counts them and keeps them for audit. The test returns the bad rows; a test passes when it returns none.
select sale_id, sale_price
from {{ ref('silver_sales') }}
where sale_price <= 0
