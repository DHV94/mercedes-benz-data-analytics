{#
  Maps the layer written in dbt_project.yml (+database: silver / gold) to the real database.
  The same code runs in DEV and in PRO; only the target name changes (D-038):
    target.name = 'prod'  -> PRO_MB_SILVER_DB / PRO_MB_GOLD_DB
    anything else (dev)   -> DEV_MB_SILVER_DB / DEV_MB_GOLD_DB
  Bronze is never built by dbt (it is a source), so it is not mapped here.
#}
{% macro generate_database_name(custom_database_name, node) -%}
    {%- if custom_database_name is none -%}
        {{ target.database }}
    {%- else -%}
        {%- set env = 'PRO' if target.name == 'prod' else 'DEV' -%}
        {{ env ~ '_MB_' ~ custom_database_name | upper ~ '_DB' }}
    {%- endif -%}
{%- endmacro %}
