# Roles y permisos: cómo está organizado y cómo se organizaría en real

Tema para la presentación (idea del autor). Primero lo que **hay**, luego lo que **haría una empresa**, y una lista corta de preguntas probables.

## 1. Lo que hay en este proyecto
Principio: **mínimo privilegio** y **separación por entorno**. Cada rol puede hacer solo lo que necesita su trabajo.

| Rol | Qué puede hacer | Qué NO puede hacer |
|---|---|---|
| `MB_INGEST_ROLE` | Escribir en **bronce**: crear tablas, stages y formatos de archivo, y cargar con `COPY INTO` | Leer o escribir silver y gold |
| `DEV_MB_TRANSFORM_ROLE` | Leer bronce. Crear y escribir en `DEV_MB_SILVER_DB` y `DEV_MB_GOLD_DB` | Escribir en bronce, ni en PRE ni en PRO |
| `PRE_MB_TRANSFORM_ROLE` | Leer bronce. Escribir en `PRE_MB_SILVER_DB` y `PRE_MB_GOLD_DB` | Escribir en bronce, DEV o PRO |
| `PRO_MB_TRANSFORM_ROLE` | Leer bronce. Escribir en `PRO_MB_SILVER_DB` y `PRO_MB_GOLD_DB` | Escribir en bronce, DEV o PRE |
| `MB_REPORTING_ROLE` | Solo **leer gold** (Power BI), con el almacén `WH_MB` | Escribir en cualquier sitio; leer bronce o silver |

Los roles de sistema de Snowflake se usan así: `SYSADMIN` es dueño de las bases de datos, y `SECURITYADMIN` crea los roles y reparte los permisos (los scripts de `snowflake/`).

Tres detalles que se defienden bien:
1. **Un fallo en PRE nunca toca PRO.** Si falta la variable `DBT_ENV_NAME` en un job de PRE, el rol de PRE no puede escribir en DEV y el job falla (ruidoso, no silencioso).
2. **Power BI no usa un rol de transformación.** Solo lee gold; si alguien roba esa credencial no puede borrar ni modificar nada.
3. **`future grants`:** los permisos de lectura sobre tablas que aún no existen. Así, cuando dbt recrea una tabla, el permiso no se pierde.

## 2. Simplificaciones de este proyecto (decirlas tú antes de que pregunten)
- **Una sola persona tiene todos los roles.** En el proyecto, todos los roles están concedidos al mismo usuario. En una empresa no.
- **Un único bronce** para DEV, PRE y PRO (la ingesta es manual y los datos son los mismos).
- **Un único rol de reporting** para todos los informes.
- **La clave de dbt Cloud** es de un usuario personal, no de un usuario de servicio.

## 3. Cómo se organizaría en una empresa
| Idea | Cómo |
|---|---|
| Personas distintas, roles distintos | Un equipo de ingesta (`INGEST`), uno de ingeniería de datos (desarrolla en DEV) y uno de consumo (informes). Nadie desarrolla directamente en PRO |
| Usuarios de servicio | dbt en PRO, la ingesta y Power BI usan **usuarios de servicio** con autenticación por **clave** (no personas ni contraseñas) |
| Acceso de las personas | **SSO** (inicio de sesión único de la empresa) y **MFA**; los roles se asignan por grupos, no persona a persona |
| Despliegue a PRO | Solo lo hace el job de dbt Cloud desde la rama `main`, tras el PR. Las personas no escriben en PRO |
| Datos sensibles | **Políticas de enmascarado** para datos personales (por ejemplo el VIN en el informe) y **políticas de acceso por fila** (un equipo solo ve sus países) |
| Roles por informe o por equipo | Varios roles de reporting con acceso a las vistas o tablas que les toca, no a todo gold |
| Control de gasto | Límites de consumo (*resource monitors*) en el almacén |
| Auditoría | El historial de accesos de Snowflake (`ACCESS_HISTORY`) dice quién leyó qué |
| Entornos | Un bronce por entorno o una copia sin coste (`clone`) para no probar sobre datos vivos |

## 4. Preguntas probables y respuesta corta
- **¿Por qué tres roles de transformación y no uno?** Para que un error en DEV o PRE no pueda tocar PRO: es separación de entornos con permisos, no solo con nombres.
- **¿Por qué Power BI no usa el rol de transformación?** Porque solo necesita leer; con un rol de solo lectura el riesgo de un incidente es mínimo.
- **¿Quién puede escribir en bronce?** Solo `MB_INGEST_ROLE`; dbt lo trata como fuente de solo lectura.
- **¿Cómo se controla el acceso a datos personales?** Hoy no hay datos personales reales (todo simulado). En real, enmascarado y acceso por fila.
- **¿Qué mejorarías?** Usuarios de servicio, SSO y un bronce por entorno.
