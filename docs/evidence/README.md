# Evidencias (capturas) · Evidence index

> Las capturas llevan un número para citarlas en orden en la presentación y en la memoria. Solo se guardan capturas del proyecto (nada de ejercicios del curso).

| Nº | Carpeta / fichero | Qué muestra | Cuándo se hizo |
|---|---|---|---|
| 01 | `snowflake/01_snowflake_error_user_uppercase.png` | Error al dar permisos: el usuario en minúsculas se convierte en mayúsculas si no va entre comillas | 2026-11-22 |
| 02 | `snowflake/02_snowflake_current_user.png` | `current_user()` devuelve `dhv994` (minúsculas) | 2026-11-22 |
| 03 | `snowflake/03_snowflake_databases_created.png` | Las 5 bases de datos creadas (1 bronze, DEV/PRO silver y gold), propiedad de `SYSADMIN` | 2026-11-22 |
| 04 | `snowflake/04_snowflake_roles_created.png` | Los 4 roles creados (2 de transformación, ingesta y reporting) | 2026-11-22 |

| 05 | `snowflake/05_snowflake_upload_sales_dialog_no_path.png` | Subida de los ficheros de ventas al stage **sin indicar carpeta** (campo de ruta vacío) | 2026-11-22 |
| 06 | `snowflake/06_snowflake_list_stage_sales_files_at_root.png` | `list` del stage: los ficheros están en la raíz, no en `batch_1/` | 2026-11-22 |
| 07 | `snowflake/07_snowflake_copy_sales_0_files_processed.png` | `COPY INTO` de ventas: «0 files processed» (busca en `batch_1/`) | 2026-11-22 |
| 08 | `snowflake/08_snowflake_bronze_counts_zero.png` | Recuentos a 0: confirma que no se cargó nada | 2026-11-22 |
| 09 | `snowflake/09_snowflake_list_stage_sales_batch_1.png` | Ventas bien subidas: `stg_eu_sales/batch_1/…` (corregido) | 2026-11-22 |
| 10 | `snowflake/10_snowflake_list_stage_dealers_batch_1.png` | Concesionarios bien subidos: `stg_dealers/batch_1/…` | 2026-11-22 |
| 11 | `snowflake/11_snowflake_copy_sales_batch_1_loaded.png` | `COPY INTO` de ventas: 5 ficheros `LOADED`, 44.733 filas, 0 errores | 2026-11-22 |
| 12 | `snowflake/12_snowflake_copy_dealers_batch_1_loaded.png` | `COPY INTO` de concesionarios: 128 filas, 0 errores | 2026-11-22 |
| 13 | `snowflake/13_snowflake_bronze_sales_counts.png` | Bronce de ventas: 44.733 filas y 44.072 ventas distintas | 2026-11-22 |
| 14 | `snowflake/14_snowflake_bronze_dealers_count.png` | Bronce de concesionarios: 128 filas | 2026-11-22 |
| 15 | `dbt/15_dbt_cloud_connection_form.png` | Formulario de conexión de dbt Cloud a Snowflake (cuenta tapada): base de datos `DEV_MB_SILVER_DB`, warehouse `WH_MB` | 2026-11-22 |
| 16 | `dbt/16_dbt_cloud_connection_test_complete.png` | Test de conexión de dbt Cloud completado: clave y passphrase tapadas, estado «COMPLETE» | 2026-11-22 |
| 17 | `dbt/17_github_recommends_apps_over_deploy_key.png` | Aviso de GitHub: recomienda GitHub Apps en lugar de deploy keys (decisión D-065) | 2026-11-22 |
| 18 | `dbt/18_dbt_cloud_project_ready.png` | dbt Cloud: «Your project is ready!» con la conexión y el repositorio configurados | 2026-11-22 |
| 19 | `dbt/19_snowflake_seed_tables_in_silver.png` | Snowflake: las 5 tablas de referencia creadas por `dbt seed` en `DEV_MB_SILVER_DB` (esquema personal de desarrollo): 300, 51, 11, 8 y 2 filas | 2026-11-22 |
| 20 | `dbt/20_dbt_seed_success.png` | dbt Cloud IDE: `dbt seed` en verde, rama `feature-dbt-setup`, versión v1 Latest, estado Parsed | 2026-11-22 |
| 21 | `dbt/21_bronze_bad_sale_date_formats.png` | Bronce: fechas de venta que `DD/MM/YYYY` no entiende. Tres tipos: `31/02/AAAA` (imposible), `AAAA-MM-DD` y `DD.MM.AA` (válidas en otro formato) | 2026-11-23 |
| 22 | `dbt/22_stg_sales_eu_counts_after_date_fix.png` | `stg_sales_eu` tras probar tres formatos de fecha: 44.733 filas, 44.654 fechas de venta (solo quedan nulas las 79 imposibles), 43.412 entregas, 44.733 precios | 2026-11-23 |
| 23 | `dbt/23_dbt_delta1_merge_156_rows.png` | Log de dbt tras cargar el delta 1: el `merge` de `silver_sales` procesa **156** filas (solo las nuevas) | 2026-11-23 |
| 24 | `dbt/24_dbt_delta1_rerun_0_rows.png` | Segunda ejecución sin datos nuevos: el `merge` procesa **0** filas (idempotencia) | 2026-11-23 |
| 25 | `dbt/25_silver_sales_44228_after_delta1.png` | Silver tras el delta 1: 44.228 filas y 44.228 `sale_id` distintos (44.072 + 156, sin duplicados) | 2026-11-23 |
| 26 | `dbt/26_bronze_dealers_256_after_delta4.png` | Bronce de concesionarios tras cargar el `dealer_master.csv` del delta 4: 256 filas (128 + 128) | 2026-11-23 |
| 27 | `snowflake/27_snowflake_pre_roles.png` | Los 5 roles `MB_` tras ejecutar `03_pre_environment.sql`, con `PRE_MB_TRANSFORM_ROLE` (D-067) | 2026-11-23 |
| 28 | `snowflake/28_snowflake_pre_databases.png` | Las 7 bases `_MB_`: bronce, y silver y gold de DEV, PRE y PRO (D-067) | 2026-11-23 |
| 29 | `dbt/29_dbt_cloud_environment_variables.png` | dbt Cloud: variables de entorno `DBT_ENV_NAME` (DEV por defecto, PRE en PRE, PRO en PRO) y `DBT_BRONZE_DB` (D-067) | 2026-11-23 |
| 30 | `dbt/30_dbt_pre_test_warn_78_sale_date.png` | Job de PRE (antes de arreglar el macro de esquemas; el esquema de auditoría aún era `core_dbt_test__audit`): el test `not_null` de `sale_date` avisa con 78 filas y las guarda en `PRE_MB_SILVER_DB.core_dbt_test__audit` (D-066) | 2026-11-23 |
| 31 | `dbt/31_dbt_pre_job_success.png` | Job `PRE · build` en Success tras arreglar el macro de esquemas: clone, deps, `dbt build` (con aviso) y generación de docs | 2026-11-23 |
| 32 | `dbt/32_dbt_pre_docs_unused_gold_warning.png` | Generación de docs en PRE: 4 modelos, 1 snapshot, 5 seeds, 5 tests; aviso esperado de que `gold` aún no tiene modelos | 2026-11-23 |
| 33 | `dbt/33_dbt_cloud_extended_attributes_warning.png` | Aviso de dbt Cloud en las credenciales: no poner claves sensibles en *Extended attributes* (se ven en texto plano) | 2026-11-23 |
| 34 | `dbt/34_dbt_pro_job_success.png` | Job `PRO · build` en Success sobre el entorno PRO (rama `main`) tras arreglar el macro de esquemas | 2026-11-23 |
| 35 | `dbt/35_dbt_pro_test_warn_78_sale_date.png` | Job de PRO (antes de arreglar el macro de esquemas, esquema antiguo `core_dbt_test__audit`): mismo aviso de 78 filas, guardadas en `PRO_MB_SILVER_DB.core_dbt_test__audit` | 2026-11-23 |
| 36 | `dbt/36_dbt_pro_docs_unused_gold_warning.png` | Generación de docs en PRO: mismo aviso de `gold` sin modelos | 2026-11-23 |
| 37 | `snowflake/37_snowflake_pre_schemas_duplicated_by_macro_bug.png` | `PRE_MB_SILVER_DB` con 12 esquemas: los limpios (`CORE`, `STAGING`, `REFERENCE`, `SNAPSHOTS`, `DBT_TEST__AUDIT`) y los 5 `CORE_*` antiguos que dejó el macro vacío | 2026-11-24 |
| 38 | `snowflake/38_snowflake_pro_schemas_duplicated_by_macro_bug.png` | Lo mismo en `PRO_MB_SILVER_DB`: esquemas limpios y `CORE_*` antiguos pendientes de borrar | 2026-11-24 |
| 39 | `snowflake/39_snowflake_pre_schemas_clean_after_drop.png` | `PRE_MB_SILVER_DB` tras borrar los `CORE_*`: quedan los 5 esquemas limpios más `INFORMATION_SCHEMA` y `PUBLIC` (7) | 2026-11-24 |
| 40 | `snowflake/40_snowflake_pro_schemas_clean_after_drop.png` | `PRO_MB_SILVER_DB` tras borrar los `CORE_*`: mismos 7 esquemas | 2026-11-24 |
| 41 | `dbt/41_dbt_gold_build_33_pass.png` | `dbt build -s gold` en el IDE (rama `feature-dbt-gold`): 6 modelos y sus tests, 33 correctos, 0 avisos, 0 errores | 2026-11-24 |
| 42 | `dbt/42_dbt_gold_tests_dimensions.png` | Detalle del build de gold: tests `not_null` y `unique` de las dimensiones (familia, fecha, impuesto, modelo) | 2026-11-24 |
| 43 | `dbt/43_dbt_gold_tests_fct_sales.png` | Detalle del build de gold: tests de `fct_sales` (claves únicas y no nulas, y `relationships` con las dimensiones) | 2026-11-24 |
| 44 | `snowflake/44_snowflake_fct_sales_counts_after_delta2.png` | `fct_sales` en DEV tras el delta 2: 44.382 ventas (= silver), todas con modelo, 44.170 con concesionario, 44.304 con impuesto y 78 con fecha desconocida (-1) | 2026-11-24 |
| 45 | `dbt/45_dbt_gold_build_2_warnings.png` | `dbt build -s gold` con los tests nuevos: 36 tests, 34 correctos, 2 avisos esperados, 0 errores | 2026-11-24 |
| 46 | `dbt/46_dbt_gold_warn_212_sales_without_dealer.png` | Aviso de `not_null_fct_sales_dealer_id`: 212 ventas con un concesionario que no existe en el maestro (D15) | 2026-11-24 |
| 47 | `dbt/47_dbt_gold_warn_78_sales_without_tax.png` | Aviso de `not_null_fct_sales_tax_id`: 78 ventas sin impuesto (las de fecha imposible, D-066) | 2026-11-24 |
| 48 | `snowflake/48_snowflake_reporting_role_grants_on_gold.png` | `show grants` de `MB_REPORTING_ROLE` tras `04_reporting_grants.sql`: usage en las bases gold y select en las tablas | 2026-11-24 |
| 49 | `snowflake/49_snowflake_recalls_copy_0_files_before_upload.png` | `COPY INTO` de los recalls ejecutado antes de subir el fichero: "0 files processed" (no falla, simplemente no hay nada que cargar) | 2026-11-24 |
| 50 | `snowflake/50_snowflake_recalls_copy_14603_rows_loaded.png` | `COPY INTO` tras subir el CSV: 14.603 filas leídas y cargadas, 0 errores | 2026-11-24 |
| 51 | `snowflake/51_snowflake_recalls_bronze_14603_rows_181_campaigns.png` | Bronce de recalls: 14.603 filas y 181 campañas distintas | 2026-11-24 |
| 52 | `dbt/52_dbt_recalls_build_26_pass.png` | `dbt build -s +fct_campaign_line`: 26 correctos (staging, silver, dimensiones, hecho y tests), 0 avisos, 0 errores | 2026-11-24 |
| 53 | `snowflake/53_snowflake_gold_campaign_lines_525_141_campaigns.png` | `fct_campaign_line` en DEV: 525 líneas y 141 campañas distintas (coincide con lo previsto, D-068) | 2026-11-24 |
| 54 | `snowflake/54_snowflake_gold_dim_component_100.png` | `dim_component`: 100 componentes | 2026-11-24 |
| 55 | `snowflake/55_snowflake_gold_dim_family_23.png` | `dim_family`: 23 familias (22 del catálogo de ventas más el CLS, que solo tiene defectos) | 2026-11-24 |
| 56 | `dbt/56_dbt_pre_job_success_with_gold_and_recalls.png` | Job `PRE · build` en Success con gold y recalls (71 tests, con avisos esperados) | 2026-11-24 |
| 57 | `dbt/57_dbt_pre_warn_78_sale_date_71_tests.png` | PRE: aviso de 78 fechas de venta nulas, guardadas en `PRE_MB_SILVER_DB.dbt_test__audit` (esquema limpio, sin `core_`) | 2026-11-24 |
| 58 | `dbt/58_dbt_pre_warn_212_sales_without_dealer.png` | PRE: aviso de 212 ventas sin concesionario en `fct_sales` | 2026-11-24 |
| 59 | `dbt/59_dbt_pre_warn_78_sales_without_tax.png` | PRE: aviso de 78 ventas sin impuesto en `fct_sales` | 2026-11-24 |
| 60 | `dbt/60_dbt_pro_job_success_with_gold_and_recalls.png` | Job `PRO · build` en Success con gold y recalls: ya hay gold en `PRO_MB_GOLD_DB` para Power BI | 2026-11-24 |
| 61 | `dbt/61_dbt_job_pro_semanal_schedule_monday_6_utc.png` | Configuración del job `PRO · semanal`: *Run on schedule*, a las 6:00 UTC, solo los lunes | 2026-11-24 |
| 62 | `dbt/62_dbt_job_pro_semanal_next_run_monday_7_cet.png` | Job `PRO · semanal` creado en el entorno PRO: próxima ejecución el lunes 30/11/2026 a las 7:00 CET (6:00 UTC) | 2026-11-24 |
| 63 | `dbt/63_dbt_seed_fx_rates_success.png` | `dbt seed -s fx_rates` en verde: tipos de cambio mensuales simulados cargados (D-069) | 2026-11-24 |
| 64 | `dbt/64_dbt_fct_sales_build_with_net_eur_3_warnings.png` | `dbt build -s fct_sales` con el neto en EUR: 14 resultados, 11 correctos y 3 avisos esperados (concesionario, tipo de cambio e impuesto) | 2026-11-24 |
| 65 | `snowflake/65_snowflake_net_eur_average_by_currency.png` | Control de cordura del neto en EUR por moneda: EUR 31.949 ventas (media 52.386), GBP 9.561 (52.805) y CHF 2.872 (58.482); suman 44.382 | 2026-11-24 |
| 66 | `dbt/66_dbt_pre_job_success_with_net_eur.png` | Job `PRE · build` en Success tras la segunda promoción (neto en EUR y descripciones de silver) | 2026-11-24 |
| 67 | `dbt/67_dbt_pro_job_success_with_net_eur.png` | Job `PRO · build` en Success con el neto en EUR: es el gold que lee Power BI | 2026-11-24 |
| 68 | `snowflake/68_snowflake_reporting_role_reads_pro_fct_sales.png` | Con `MB_REPORTING_ROLE` se lee `PRO_MB_GOLD_DB.SALES.FCT_SALES`: 44.382 ventas y 2.342.399.904 EUR de neto en total | 2026-11-24 |
| 69 | `snowflake/69_snowflake_reporting_role_reads_pro_campaign_lines.png` | Con `MB_REPORTING_ROLE` se lee `FCT_CAMPAIGN_LINE` de PRO: 525 líneas (Power BI podrá conectarse) | 2026-11-24 |
| 70 | `dbt/70_dbt_test_price_positive_fails_124_rows_d10.png` | El test de precio positivo falla con 124 filas en los datos normales: es el defecto D10 (precio cero o negativo, ~0,3 %), que ya viene en el generador | 2026-11-24 |
| 71 | `dbt/71_dbt_test_silver_sales_8_pass_2_warn.png` | `dbt test -s silver_sales` con los tests de alerta: 10 tests, 8 correctos, 2 avisos (78 fechas nulas y 124 precios no positivos) y 0 errores | 2026-11-24 |
| 72 | `snowflake/72_snowflake_demo_start_bronze_sales_45051.png` | Estado de partida de la demo: bronce de ventas con 45.051 filas y 44.382 `sale_id` distintos (tras el delta 2) | 2026-11-24 |
| 73 | `snowflake/73_snowflake_demo_start_bronze_dealers_256.png` | Estado de partida de la demo: bronce de concesionarios con 256 filas (lote 1 y delta 4) | 2026-11-24 |
| 74 | `snowflake/74_snowflake_demo_start_snapshot_131_128.png` | Estado de partida de la demo: snapshot con 131 versiones y 128 vigentes | 2026-11-24 |
| 75 | `dbt/75_dbt_seed_component_type_map_27_rows.png` | `dbt seed -s component_type_map`: 27 sistemas con su categoría cargados (D-071) | 2026-11-24 |
| 76 | `dbt/76_dbt_build_dim_component_6_pass.png` | `dbt build -s dim_component` con la categoría nueva: 6 resultados correctos, incluido el test de valores aceptados | 2026-11-24 |
| 77 | `snowflake/77_snowflake_uc5_lines_by_component_category.png` | UC5: líneas y campañas por categoría: mecánico 204 (66), electrónica y software 166 (34), eléctrico 128 (41), mixto 27 (14) | 2026-11-24 |
| 78 | `dbt/78_dbt_pre_job_success_with_uc5.png` | Job `PRE · build` en Success con UC5 (rama `pre`, commit 9fd5915) | 2026-11-24 |
| 79 | `dbt/79_dbt_pro_job_success_with_uc5.png` | Job `PRO · build` en Success con UC5 (rama `main`, commit 9a62758): el gold que lee Power BI | 2026-11-24 |
| 80 | `dbt/80_dbt_fct_sales_incremental_full_refresh_44382.png` | `fct_sales` ahora incremental en gold (D-072): `dbt build --full-refresh -s fct_sales` carga 44.382 filas (rama `feature-gold-incremental`) | 2026-11-24 |
| 81 | `dbt/81_dbt_fct_sales_incremental_rerun_0_rows.png` | Segunda ejecución sin `--full-refresh`: `fct_sales` procesa **0 filas** (no hay lotes nuevos); los 3 avisos esperados siguen siendo avisos | 2026-11-24 |
| 82 | `dbt/82_dbt_pre_full_refresh_fct_sales_44382.png` | Job `PRE · build` con `--full-refresh -s fct_sales` (una sola vez): `PRE_MB_GOLD_DB.sales.fct_sales` se crea incremental con 44.382 filas | 2026-11-24 |
| 83 | `dbt/83_dbt_pre_silver_sales_incremental_0_rows.png` | `PRE · build` ya con el comando normal: `silver_sales` incremental procesa 0 filas (no hay lotes nuevos) | 2026-11-24 |
| 84 | `dbt/84_dbt_pre_job_success_after_full_refresh.png` | Run de `PRE · build` en Success tras restaurar el comando normal (rama `pre`, commit 654c852) | 2026-11-24 |
| 85 | `dbt/85_dbt_pro_fct_sales_error_missing_loaded_at.png` | **Error real, útil para contar:** `PRO · build` sin `--full-refresh` falla en `fct_sales` (`correlated aggregate function MAX(_LOADED_AT)`), porque la tabla de PRO aún no tenía la columna `_loaded_at` | 2026-11-24 |
| 86 | `dbt/86_snowflake_pro_fct_sales_no_loaded_at_column.png` | Diagnóstico en Snowflake: `PRO_MB_GOLD_DB.SALES.FCT_SALES` no tiene la columna `_loaded_at` (el `--full-refresh` anterior no la había reconstruido) | 2026-11-24 |
| 87 | `dbt/87_dbt_pro_full_refresh_job_fct_sales_44382.png` | Job aparte `PRO · full refresh fct_sales` (`dbt build --full-refresh -s fct_sales`): `fct_sales` de PRO creada incremental con 44.382 filas | 2026-11-24 |
| 88 | `dbt/88_snowflake_pro_fct_sales_44382_with_loaded_at.png` | Snowflake: `fct_sales` de PRO ya tiene `_loaded_at`: 44.382 filas | 2026-11-24 |
| 89 | `dbt/89_dbt_pro_fct_sales_incremental_0_rows.png` | `PRO · build` con el comando normal: `fct_sales` incremental procesa 0 filas | 2026-11-24 |
| 90 | `dbt/90_dbt_pro_job_success_incremental_gold.png` | Run de `PRO · build` en Success (rama `main`, commit 472a6404) con el gold de ventas incremental: lo que lee Power BI | 2026-11-24 |
| 91 | `powerbi/91_powerbi_uc1_map_and_bars_first_version.png` | Primera versión del informe de Power BI en casa: mapa y barras de unidades vendidas por país (UC1); el grupo «(En blanco)» son las ventas sin concesionario en el maestro | 2026-11-24 |
| 92 | `powerbi/92_powerbi_uc1_units_sold_by_family_top6.png` | UC1 en Power BI: unidades vendidas por familia y año (6 principales), 2021-2025, con título «UC1», líneas rectas, marcadores y colores distintos | 2026-11-24 |
| 93 | `powerbi/93_powerbi_uc2_units_sold_by_body_type.png` | UC2 en Power BI: unidades vendidas por carrocería y año, 2021-2025 (SUV en cabeza y al alza, hatchback a la baja; nota en el gráfico: descapotable con el SL desde 2022 y el CLE Cabriolet desde 2024; 2025 hasta mediados de diciembre) | 2026-11-25 |
| 94 | `powerbi/94_powerbi_uc3_unidades_por_propulsion.png` | UC3 en Power BI: unidades vendidas por propulsión y año, 2021-2025 con leyenda explicativa de las propulsiones y eje desde 0; HEV y BEV suben, gasolina y diésel bajan. Datos simulados | 2026-11-25 |
| 95 | `powerbi/95_powerbi_uc5_campanas_por_categoria.png` | UC5 en Power BI: campañas de revisión en EE. UU. por año y categoría de componente, 2021-2025 (con leyenda de las cuatro categorías; sin desglose por familia, D-077) | 2026-11-25 |
| 96 | `powerbi/96_powerbi_uc4_top3_modelos_por_pais.png` | UC4 en Power BI: top 3 de modelos por país en 2025, ordenado por unidades vendidas (D-076); el GLC 200 es el primero en los seis países. Datos simulados | 2026-11-25 |

Las capturas 01-02 y 05-08 cuentan dos anécdotas útiles para la presentación: un error real y cómo se diagnosticó y resolvió (usuario en mayúsculas; ficheros subidos sin carpeta). Las siguientes capturas (carga correcta, dbt, tests, alertas, Power BI) se añaden con el siguiente número (80 en adelante).
