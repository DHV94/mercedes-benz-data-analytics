-- =============================================================================
-- 04 · Read access for Power BI (MB_REPORTING_ROLE) on the gold layer
-- =============================================================================
-- Power BI never connects with a transform role: it uses MB_REPORTING_ROLE, which can only READ gold.
-- "future" grants mean every table dbt creates later is readable with no extra step
-- (dbt recreates tables on every run, so one-off table grants would be lost).
--
-- HOW TO RUN: Snowsight -> new worksheet -> "Run all". Safe to run twice.
-- =============================================================================

use role securityadmin;

-- PRO gold: what Power BI reads in the final demo
grant usage on database PRO_MB_GOLD_DB to role MB_REPORTING_ROLE;
grant usage on all schemas in database PRO_MB_GOLD_DB to role MB_REPORTING_ROLE;
grant usage on future schemas in database PRO_MB_GOLD_DB to role MB_REPORTING_ROLE;
grant select on all tables in database PRO_MB_GOLD_DB to role MB_REPORTING_ROLE;
grant select on future tables in database PRO_MB_GOLD_DB to role MB_REPORTING_ROLE;

-- DEV gold: same, to test reports while building (optional, read-only)
grant usage on database DEV_MB_GOLD_DB to role MB_REPORTING_ROLE;
grant usage on all schemas in database DEV_MB_GOLD_DB to role MB_REPORTING_ROLE;
grant usage on future schemas in database DEV_MB_GOLD_DB to role MB_REPORTING_ROLE;
grant select on all tables in database DEV_MB_GOLD_DB to role MB_REPORTING_ROLE;
grant select on future tables in database DEV_MB_GOLD_DB to role MB_REPORTING_ROLE;

-- Check: the reporting role must now see the gold tables
show grants to role MB_REPORTING_ROLE;
