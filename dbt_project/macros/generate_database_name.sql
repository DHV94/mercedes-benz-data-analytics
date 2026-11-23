{#
  Maps the layer written in dbt_project.yml (+database: silver / gold) to the real database.
  The environment comes from the dbt Cloud environment variable DBT_ENV_NAME (D-067):
    DBT_ENV_NAME = DEV -> DEV_MB_SILVER_DB / DEV_MB_GOLD_DB   (default, development IDE)
    DBT_ENV_NAME = PRE -> PRE_MB_SILVER_DB / PRE_MB_GOLD_DB   (deployment environment PRE)
    DBT_ENV_NAME = PRO -> PRO_MB_SILVER_DB / PRO_MB_GOLD_DB   (deployment environment PRO)
  The same code runs everywhere; only the variable changes. Without the variable it falls back to DEV,
  so the IDE keeps working with nothing configured. Bronze is a source (never built by dbt).
#}
{% macro generate_database_name(custom_database_name, node) -%}
    {%- if custom_database_name is none -%}
        {{ target.database }}
    {%- else -%}
        {%- set env = env_var('DBT_ENV_NAME', 'DEV') | upper -%}
        {{ env ~ '_MB_' ~ custom_database_name | upper ~ '_DB' }}
    {%- endif -%}
{%- endmacro %}
