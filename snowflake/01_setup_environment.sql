-- =============================================================================
-- 01 · Snowflake environment for the Mercedes-Benz data platform
-- =============================================================================
-- Based on the course convention (01_crear_entorno.sql), with the MB prefix so
-- it never clashes with the practice objects (DEV_BRONZE_DB, WH_CURSO...).
--
--   Databases : {ENV}_MB_BRONZE_DB / {ENV}_MB_SILVER_DB / {ENV}_MB_GOLD_DB
--   Roles     : {ENV}_MB_TRANSFORM_ROLE (dbt), MB_INGEST_ROLE (loads bronze),
--               MB_REPORTING_ROLE (Power BI, read-only on DEV gold for now)
--   Warehouse : WH_MB (XSMALL, auto-suspend 60 s)
--
-- HOW TO RUN: Snowsight -> new worksheet -> replace <YOUR_USER> (run
-- `select current_user();` first) -> "Run all".
-- Principle: least privilege. Each role gets only what it needs.
-- =============================================================================

-- 0. Cost guard: the trial has limited credits. The monitor suspends the
--    warehouse when the quota is reached. Needs ACCOUNTADMIN (only place we use it).
use role accountadmin;
create resource monitor if not exists RM_MB
    with credit_quota = 40
    triggers on 80 percent do notify
             on 100 percent do suspend;

-- 1. Warehouse
use role sysadmin;
create warehouse if not exists WH_MB
    warehouse_size = 'XSMALL'
    auto_suspend = 60
    auto_resume = true
    initially_suspended = true;

use role accountadmin;
alter warehouse WH_MB set resource_monitor = RM_MB;

-- 2. Databases. Bronze exists only in DEV (PRE/PRO will be clones, like in the course).
use role sysadmin;
create database if not exists DEV_MB_BRONZE_DB;
create schema if not exists DEV_MB_BRONZE_DB.sales;   -- regional sales feeds (EU, US, CN, JP, KR)
create schema if not exists DEV_MB_BRONZE_DB.crm;     -- dealer master
create schema if not exists DEV_MB_BRONZE_DB.nhtsa;   -- public recall data

create database if not exists DEV_MB_SILVER_DB;
create database if not exists DEV_MB_GOLD_DB;
create database if not exists PRE_MB_SILVER_DB;
create database if not exists PRE_MB_GOLD_DB;
create database if not exists PRO_MB_SILVER_DB;
create database if not exists PRO_MB_GOLD_DB;

-- 3. Roles
use role securityadmin;
create role if not exists DEV_MB_TRANSFORM_ROLE;
create role if not exists PRE_MB_TRANSFORM_ROLE;
create role if not exists PRO_MB_TRANSFORM_ROLE;
create role if not exists MB_INGEST_ROLE;
create role if not exists MB_REPORTING_ROLE;

-- SYSADMIN inherits the functional roles (Snowflake best practice)
grant role DEV_MB_TRANSFORM_ROLE to role sysadmin;
grant role PRE_MB_TRANSFORM_ROLE to role sysadmin;
grant role PRO_MB_TRANSFORM_ROLE to role sysadmin;
grant role MB_INGEST_ROLE to role sysadmin;
grant role MB_REPORTING_ROLE to role sysadmin;

-- In the trial your user plays every role. In a real project jobs use a
-- service user with key-pair authentication (see docs, security section).
grant role DEV_MB_TRANSFORM_ROLE to user <YOUR_USER>;
grant role PRE_MB_TRANSFORM_ROLE to user <YOUR_USER>;
grant role PRO_MB_TRANSFORM_ROLE to user <YOUR_USER>;
grant role MB_INGEST_ROLE to user <YOUR_USER>;
grant role MB_REPORTING_ROLE to user <YOUR_USER>;

-- 4. Warehouse usage
grant usage on warehouse WH_MB to role DEV_MB_TRANSFORM_ROLE;
grant usage on warehouse WH_MB to role PRE_MB_TRANSFORM_ROLE;
grant usage on warehouse WH_MB to role PRO_MB_TRANSFORM_ROLE;
grant usage on warehouse WH_MB to role MB_INGEST_ROLE;
grant usage on warehouse WH_MB to role MB_REPORTING_ROLE;

-- 5. Ingest role: the only one allowed to WRITE in bronze (stages, file formats, tables, COPY INTO)
grant usage on database DEV_MB_BRONZE_DB to role MB_INGEST_ROLE;
grant usage on all schemas in database DEV_MB_BRONZE_DB to role MB_INGEST_ROLE;
grant create table, create stage, create file format
    on all schemas in database DEV_MB_BRONZE_DB to role MB_INGEST_ROLE;

-- 6. Transform roles: READ bronze, create schemas in their own silver/gold.
--    (Bronze tables are created later by MB_INGEST_ROLE, so we use FUTURE grants.)
grant usage on database DEV_MB_BRONZE_DB to role DEV_MB_TRANSFORM_ROLE;
grant usage on all schemas in database DEV_MB_BRONZE_DB to role DEV_MB_TRANSFORM_ROLE;
grant select on all tables in database DEV_MB_BRONZE_DB to role DEV_MB_TRANSFORM_ROLE;
grant select on future tables in database DEV_MB_BRONZE_DB to role DEV_MB_TRANSFORM_ROLE;

grant usage, create schema on database DEV_MB_SILVER_DB to role DEV_MB_TRANSFORM_ROLE;
grant usage, create schema on database DEV_MB_GOLD_DB   to role DEV_MB_TRANSFORM_ROLE;
grant usage, create schema on database PRE_MB_SILVER_DB to role PRE_MB_TRANSFORM_ROLE;
grant usage, create schema on database PRE_MB_GOLD_DB   to role PRE_MB_TRANSFORM_ROLE;
grant usage, create schema on database PRO_MB_SILVER_DB to role PRO_MB_TRANSFORM_ROLE;
grant usage, create schema on database PRO_MB_GOLD_DB   to role PRO_MB_TRANSFORM_ROLE;

-- 7. Reporting role: nothing yet. Read grants on gold are added later (see day 7 of
--    the course: grant_select_on_gold macro) once gold models exist.

-- 8. Check: you should see 7 databases with the MB prefix
use role sysadmin;
show databases like '%_MB_%';
