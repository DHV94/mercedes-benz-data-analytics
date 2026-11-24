# Guía de Power BI (para trabajar sin Claude delante)

Objetivo: un informe de **2-3 páginas** sobre el gold de PRO, que se pueda enseñar en la presentación del jueves. Esta guía es autocontenida: sigue los pasos en orden.

> Sugerencia al empezar: graba la pantalla (Win+Alt+R) mientras haces la conexión y el modelo; sirve de respaldo para la defensa.

## 1. Qué hay en gold (modelo en estrella)
| Tabla | Qué es | Clave |
|---|---|---|
| `fct_sales` | Una fila por venta (Europa) | `sale_id` |
| `fct_campaign_line` | Una fila por línea de campaña de defectos (datos reales NHTSA) | `campaign_line_id` |
| `dim_date` | Calendario 2020-2027 + fila `-1` "Unknown" | `date_id` (AAAAMMDD) |
| `dim_model` | 51 variantes (carrocería, motorización) | `model_id` |
| `dim_family` | 23 familias. **Compartida** por los dos hechos | `family_id` |
| `dim_dealer` | Versiones de concesionario (SCD2); la venta apunta a la vigente | `dealer_id` |
| `dim_tax` | Tasas de impuesto con vigencia | `tax_id` |
| `dim_component` | Componentes defectuosos | `component_id` |

## 2. Conexión a Snowflake
Conector **Snowflake** de Power BI (Obtener datos → Snowflake). Los valores concretos (cuenta, usuario) son los que ya usaste en clase; **no los pegues en el repositorio**.

| Campo | Valor |
|---|---|
| Servidor | el de tu cuenta, el mismo que en Snowsight (`...snowflakecomputing.com`) |
| Almacén (warehouse) | `WH_MB` |
| Opciones avanzadas → Rol | `MB_REPORTING_ROLE` |
| Base de datos | `PRO_MB_GOLD_DB` |
| Esquema | `SALES` |
| Modo | **Importar** (más rápido para la demo) |

Si falla la conexión o la autenticación: **Plan B** abajo.

Selecciona las 8 tablas de la sección 1.

## 3. Relaciones (Vista de modelo)
Todas **uno a varios**, filtrando de la dimensión al hecho, dirección única.

| Desde (1) | Hasta (varios) | Activa |
|---|---|---|
| `dim_date[date_id]` | `fct_sales[sale_date_id]` | **Sí** |
| `dim_date[date_id]` | `fct_sales[delivery_date_id]` | **No** (inactiva) |
| `dim_date[date_id]` | `fct_campaign_line[campaign_date_id]` | Sí |
| `dim_model[model_id]` | `fct_sales[model_id]` | Sí |
| `dim_family[family_id]` | `fct_sales[family_id]` | Sí |
| `dim_family[family_id]` | `fct_campaign_line[family_id]` | Sí |
| `dim_dealer[dealer_id]` | `fct_sales[dealer_id]` | Sí |
| `dim_tax[tax_id]` | `fct_sales[tax_id]` | Sí |
| `dim_component[component_id]` | `fct_campaign_line[component_id]` | Sí |

Por qué `delivery_date_id` queda inactiva: Power BI solo permite una relación activa entre dos tablas. Las dos fechas del hecho (venta y entrega) usan la misma `dim_date` (es una dimensión que juega dos papeles: *role-playing*). Para medidas por fecha de entrega se activa con `USERELATIONSHIP` (ver medidas).

Detalles:
- Marca `dim_date[full_date]` como **tabla de fechas** (clic derecho en la tabla → Marcar como tabla de fechas).
- Ordena `month_name` por `month` (Columna → Ordenar por columna) para que los meses salgan en orden.
- La fila `date_id = -1` ("Unknown") agrupa las ventas con fecha imposible o sin entregar: déjala, se explica en la defensa.

## 4. Medidas (DAX)
Crea una tabla de medidas vacía (`Medidas`) y añade:

```
Unidades vendidas = SUM(fct_sales[units_sold])

Ventas registradas = COUNTROWS(fct_sales)

Devoluciones y cancelaciones =
CALCULATE(COUNTROWS(fct_sales), fct_sales[status] IN {"RETURNED", "CANCELLED"})

% devoluciones y cancelaciones = DIVIDE([Devoluciones y cancelaciones], [Ventas registradas])

Precio medio (moneda local) = AVERAGE(fct_sales[price_local])

Ingresos netos EUR =
CALCULATE(SUM(fct_sales[price_net_eur]), fct_sales[status] = "SOLD")

Precio medio neto EUR =
CALCULATE(AVERAGE(fct_sales[price_net_eur]), fct_sales[status] = "SOLD")

Unidades entregadas =
CALCULATE([Unidades vendidas], USERELATIONSHIP(dim_date[date_id], fct_sales[delivery_date_id]))

Campañas = DISTINCTCOUNT(fct_campaign_line[campaign_id])

Líneas de campaña = COUNTROWS(fct_campaign_line)

Líneas electrónica y software =
CALCULATE([Líneas de campaña], dim_component[component_category] = "ELECTRONICS_SOFTWARE")

% electrónica y software = DIVIDE([Líneas electrónica y software], [Líneas de campaña])
```

**Importes:** `price_local` está en **tres monedas** (EUR, GBP, CHF): **no lo sumes entre países**. Para ingresos totales usa `price_net_eur` (precio sin impuestos en euros, con el tipo de cambio mensual del seed `fx_rates`, valores simulados). Solo se cuentan las ventas en estado `SOLD`. Las ventas sin fecha válida (78) no tienen tipo de cambio y quedan sin neto en EUR: es un aviso de dbt esperado.

**No sumes `units_affected`** de las campañas: es la cifra de la campaña repetida en cada línea (D-058). Cuenta campañas y líneas.

## 5. Informe propuesto
**Página 1 · Ventas**
- Tarjetas: Unidades vendidas, Ingresos netos EUR, Ventas registradas, % devoluciones y cancelaciones.
- Columnas: Unidades vendidas por mes (`dim_date[month_name]`, con `year` en el eje o como segmentación).
- Barras: Unidades vendidas por `dim_family[family_name]`.
- Barras: por `dim_model[propulsion]` (BEV, PHEV, HEV...).
- Columnas o líneas: Ingresos netos EUR por mes y por país (`dim_dealer[country_name]`).
- Segmentaciones: año, país (`dim_dealer[country_name]`), moneda (`fct_sales[local_currency]`).

**Página 2 · Defectos (campañas NHTSA)**
- Tarjetas: Campañas, Líneas de campaña.
- Barras: Líneas de campaña por `dim_family[family_name]`.
- Barras: por `dim_component[component_type]`.
- **Periodo de UC5 y de las campañas: 2021 a 2025** (D-071). Pon en la página un filtro `dim_date[year]` entre 2021 y 2025 y deja fuera 2020 y 2026: 2026 llega solo hasta el 2/10 y es parcial. Dilo en una nota del gráfico.
- **UC5 (la pregunta del proyecto):** columnas apiladas de líneas de campaña por año (`dim_date[year]`) con la leyenda `dim_component[component_category]` (electrónica y software, eléctrico, mecánico y mixto/otros), y la tarjeta `% electrónica y software`.
- Línea: campañas por año (`dim_date[year]`).
- Segmentación: familia (`dim_family`). Como la familia es compartida, la misma segmentación puede filtrar ventas y campañas.

**Página 3 · Calidad del dato (opcional, muy buena para la defensa)**
- Ventas con fecha desconocida: `COUNTROWS(FILTER(fct_sales, fct_sales[sale_date_id] = -1))` (esperado: 78).
- Ventas sin concesionario: `COUNTROWS(FILTER(fct_sales, ISBLANK(fct_sales[dealer_id])))` (esperado: 212).
- Texto: son las alertas que dbt avisa y no esconde (D-066).

## 6. Cifras para comprobar que los datos son los correctos
| Dato | Esperado (tras el delta 2) |
|---|---|
| `fct_sales` filas | 44.382 |
| Sin `exchange_rate` | 78 (las de fecha imposible) |
| Con `sale_date_id = -1` | 78 |
| Sin `dealer_id` | 212 |
| Sin `tax_id` | 78 |
| `fct_campaign_line` filas | 525 |
| Campañas distintas | 141 |
| Componentes | 100 |
| Líneas por categoría | ELECTRONICS_SOFTWARE 166 · ELECTRICAL 128 · MECHANICAL 204 · MIXED_OTHER 27 |
| Campañas por categoría (se solapan: una campaña puede tener de las dos) | 34 · 41 · 66 · 14 |
| Familias en `dim_family` | 23 (el CLS tiene defectos y ninguna venta) |

Si has cargado más deltas, las ventas serán más; consulta `docs/es/live_demo_script.md`.

## 7. Plan B si no hay conexión a Snowflake
1. En casa (o con acceso), en Snowsight, con rol `MB_REPORTING_ROLE`, ejecuta `select * from PRO_MB_GOLD_DB.SALES.<tabla>` para cada una de las 8 tablas y descarga el resultado (*Download* → CSV).
2. Guarda los CSV en Drive.
3. En Power BI: Obtener datos → Texto/CSV, y repite las relaciones de la sección 3.

## 8. Guardar el trabajo
- Guarda el `.pbix` en Drive y, si pesa poco, en `powerbi/` del repositorio (no subas credenciales).
- Haz capturas de cada página para la presentación y las guardas como evidencias numeradas en `docs/evidence/`.
