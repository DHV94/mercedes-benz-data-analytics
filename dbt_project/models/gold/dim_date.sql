-- Calendar from 2020-01-01 to 2027-12-31 (2,922 days) plus an "unknown" row with date_id = -1,
-- used when a sale has no valid date or has not been delivered yet.
-- date_id is the date as a number (20250131): readable and stable.
with days as (
    select dateadd(day, row_number() over (order by seq4()) - 1, to_date('2020-01-01')) as full_date
    from table(generator(rowcount => 2922))
)

select
    to_number(to_char(full_date, 'YYYYMMDD')) as date_id,
    full_date,
    year(full_date)                           as year,
    month(full_date)                          as month,
    to_char(full_date, 'MMMM')                as month_name,
    quarter(full_date)                        as quarter
from days

union all

select -1, null, null, null, 'Unknown', null
