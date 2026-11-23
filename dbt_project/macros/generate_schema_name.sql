{# Decides the SCHEMA of every model, seed and snapshot (D-067).
   DEV: <personal schema>_<layer>, so each developer has their own tables and nobody overwrites another.
   PRE / PRO: the clean layer name only (core, staging, ...): one shared version. #}
{% macro generate_schema_name(custom_schema_name, node) -%}

    {%- set default_schema = target.schema -%}
    {%- set env = env_var('DBT_ENV_NAME', 'DEV') | upper -%}

    {%- if custom_schema_name is none -%}
        {{ default_schema }}
    {%- elif env == 'DEV' -%}
        {{ default_schema }}_{{ custom_schema_name | trim }}
    {%- else -%}
        {{ custom_schema_name | trim }}
    {%- endif -%}

{%- endmacro %}
