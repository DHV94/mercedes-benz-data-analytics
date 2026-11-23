-- =============================================================================
-- 03 · PRE environment (D-067: three environments DEV / PRE / PRO)
-- =============================================================================
-- Adds PRE_MB_SILVER_DB, PRE_MB_GOLD_DB and PRE_MB_TRANSFORM_ROLE, copying exactly
-- what 01_setup_environment.sql did for PRO. Bronze stays single and lives in DEV
-- (PRE and PRO read it, they never write in it).
--
-- HOW TO RUN: Snowsight -> new worksheet -> "Run all". Safe to run twice (if not exists).
-- The user is "dhv994" in double quotes: it is lower case (see the uppercase error of 2026-11-22).
-- =============================================================================

-- 1. Databases
use role sysadmin;
create database if not exists PRE_MB_SILVER_DB;
create database if not exists PRE_MB_GOLD_DB;

-- 2. Role
use role securityadmin;
create role if not exists PRE_MB_TRANSFORM_ROLE;
grant role PRE_MB_TRANSFORM_ROLE to role sysadmin;
grant role PRE_MB_TRANSFORM_ROLE to user "dhv994";

-- 3. Warehouse usage
grant usage on warehouse WH_MB to role PRE_MB_TRANSFORM_ROLE;

-- 4. Read the single bronze copy (same grants as PRO)
grant usage on database DEV_MB_BRONZE_DB to role PRE_MB_TRANSFORM_ROLE;
grant usage on all schemas in database DEV_MB_BRONZE_DB to role PRE_MB_TRANSFORM_ROLE;
grant select on all tables in database DEV_MB_BRONZE_DB to role PRE_MB_TRANSFORM_ROLE;
grant select on future tables in database DEV_MB_BRONZE_DB to role PRE_MB_TRANSFORM_ROLE;

-- 5. Write only in PRE silver and gold
grant usage, create schema on database PRE_MB_SILVER_DB to role PRE_MB_TRANSFORM_ROLE;
grant usage, create schema on database PRE_MB_GOLD_DB   to role PRE_MB_TRANSFORM_ROLE;

-- 6. Check: 4 transform roles in total (DEV, PRE, PRO + ingest/reporting = 5 with MB_)
show roles like '%MB_%';
show databases like '%_MB_%';
