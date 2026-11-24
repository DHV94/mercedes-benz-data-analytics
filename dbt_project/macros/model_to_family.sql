{#
  Translates the model text of a NHTSA recall (GLE 450, S 580 4MATIC, EQS SUV 450+...) to one of the
  22 families of our catalog (A-Class, C-Class, GLE, EQS SUV...). Returns NULL when the model is not in our
  catalog (Sprinter, Metris, CLS...): those vehicles are never sold in our data.

  Pass a column that is already cleaned (upper case, without the prefixes AMG / MAYBACH / REDUNDANT).
  Order matters: the longer names (EQS SUV) must be tested before the shorter ones (EQS).
  Usage:  {{ model_to_family('model_clean') }}
#}
{% macro model_to_family(column) -%}
    case
        when regexp_like({{ column }}, '^EQS SUV.*') then 'EQS SUV'
        when regexp_like({{ column }}, '^EQS.*')     then 'EQS'
        when regexp_like({{ column }}, '^EQE SUV.*') then 'EQE SUV'
        when regexp_like({{ column }}, '^EQE.*')     then 'EQE'
        when regexp_like({{ column }}, '^EQA.*')     then 'EQA'
        when regexp_like({{ column }}, '^EQB.*')     then 'EQB'
        when regexp_like({{ column }}, '^EQC.*')     then 'EQC'
        when regexp_like({{ column }}, '^GLA.*')     then 'GLA'
        when regexp_like({{ column }}, '^GLB.*')     then 'GLB'
        when regexp_like({{ column }}, '^GLC.*')     then 'GLC'
        when regexp_like({{ column }}, '^GLE.*')     then 'GLE'
        when regexp_like({{ column }}, '^GLS.*')     then 'GLS'
        when regexp_like({{ column }}, '^CLA.*')     then 'CLA'
        when regexp_like({{ column }}, '^CLE.*')     then 'CLE'
        when regexp_like({{ column }}, '^GT.*')      then 'AMG GT'
        when regexp_like({{ column }}, '^SL ?[0-9].*') then 'SL'
        when regexp_like({{ column }}, '^S ?[0-9].*')  then 'S-Class'
        when regexp_like({{ column }}, '^C ?[0-9].*')  then 'C-Class'
        when regexp_like({{ column }}, '^E ?[0-9].*')  then 'E-Class'
        when regexp_like({{ column }}, '^A ?[0-9].*')  then 'A-Class'
        when regexp_like({{ column }}, '^B ?[0-9].*')  then 'B-Class'
        when regexp_like({{ column }}, '^G ?[0-9].*')  then 'G-Class'
    end
{%- endmacro %}
