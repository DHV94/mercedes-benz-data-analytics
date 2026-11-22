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

Las capturas 01-02 y 05-08 cuentan dos anécdotas útiles para la presentación: un error real y cómo se diagnosticó y resolvió (usuario en mayúsculas; ficheros subidos sin carpeta). Las siguientes capturas (carga correcta, dbt, tests, alertas, Power BI) se añaden con el siguiente número (21 en adelante).
