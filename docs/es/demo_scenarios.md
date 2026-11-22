# Guion de pruebas y demo: lote 1 y 6 deltas (Europa)

> Sirve para probar en casa, en clase y en directo. Cada paso dice qué fichero cargar y qué debe pasar. Los números de **bronze** son exactos (salen de `reference/delta_plan.csv`). Los de silver suponen que las filas con defectos se **marcan** pero no se pierden; si decidimos descartar alguna (por ejemplo fechas imposibles), se anotará aquí. Semilla 42 (`python data/data_generator/generate_europe.py --output data/data_generator/output`).

## Cómo se usa
1. Carga el fichero en bronze (el stage conserva el nombre del fichero y la fecha de carga).
2. Ejecuta la pipeline (dbt).
3. Compara con la tabla. Repite el paso 2 **sin cargar nada** para comprobar que no cambia nada (idempotencia).

## Escenario de ventas

| Paso | Fichero | Filas del fichero | Qué contiene | Filas acumuladas en bronze | Ventas únicas (`sale_id`) esperadas en silver | Qué demuestra |
|---|---|---|---|---|---|---|
| 0 | `batch_1/sales_eu_2021…2025.csv` | 44.733 | Historial hasta 30-11-2025, con 661 filas duplicadas exactas | 44.733 | **44.072** | Carga inicial y limpieza (duplicados, formatos) |
| 1 | `delta_1` | 156 | 156 ventas nuevas | 44.889 | **44.228** | Carga incremental normal |
| 2 | `delta_2` | 162 | 154 nuevas + 8 filas reenviadas idénticas | 45.051 | **44.382** | Idempotencia: las 8 reenviadas no crean duplicados |
| 3 | `delta_3` | 160 | 150 nuevas + 10 correcciones de ventas antiguas (6 pasan a `returned`, 4 cambian de precio) | 45.211 | **44.532** | Actualización por `sale_id`: sin duplicados, 10 filas con valores nuevos |
| 4 | `delta_4` | 134 | 134 nuevas | 45.345 | **44.666** | Carga normal + cambios de concesionario (ver abajo) |
| 5 | `delta_5` | 164 | 164 nuevas | 45.509 | **44.830** | Carga normal + cierres y concesionario nuevo (ver abajo) |
| 6 | `delta_6` | 180 | 170 nuevas + **10 filas de alerta** | 45.689 | **45.000** (las 10 de alerta no deben entrar o deben quedar marcadas) | Tests y alertas |

Prueba extra de **idempotencia** en cualquier paso: ejecutar la pipeline dos veces seguidas no cambia ningún recuento.

## Escenario de concesionarios (snapshot SCD2)
Cada delta trae su `dealer_master.csv` completo (como una extracción del sistema origen). El guion es fijo, igual en cada ejecución.

| Paso | Cambio en el maestro | Filas totales en el snapshot | Concesionarios vigentes (`is_current`) |
|---|---|---|---|
| 0 (batch_1) | 128 concesionarios | 128 | 128 |
| 1-3 | Sin cambios | 128 | 128 |
| 4 | **3 renombrados** (DE-0014, FR-0177, ES-0254: se añade « Partner») | 131 | 128 |
| 5 | **2 cierran** el 22-12-2025 (GB-0112, IT-0278); DE-0014 **cambia de nombre otra vez** (« Group»); **abre CH-0999** (Garage Stern Bern, 21-12-2025) | 135 | 129 |
| 6 | Sin cambios (el snapshot **no** debe crear versiones nuevas) | 135 | 129 |

DE-0014 acaba con **3 versiones**: «Autohaus München», «… Partner» y «… Partner Group». Es el ejemplo ideal para enseñar el historial. Las fechas del snapshot significan «detectado el» (ver `defense_justifications.md`, apartado 4).

## Filas de alerta del delta 6 (`reference/alert_rows.csv`)
Ventas con id `EU-2025-900001` a `EU-2025-900010`. Cada una debe hacer fallar un test y disparar la alerta:

| `sale_id` | Defecto | Test que debe saltar |
|---|---|---|
| 900001 | `tax_regime` = `XXX` | régimen no está en el seed de equivalencias |
| 900002 | `tax_regime` vacío | ídem |
| 900003 | régimen reducido en un país sin reducido (CH) | una venta debe casar con exactamente un impuesto |
| 900004 | precio 0 | precio positivo |
| 900005 | precio negativo | precio positivo |
| 900006 y 900007 | fecha de venta futura (2026) | fecha no futura |
| 900008 y 900009 | concesionario inexistente (`DE-9999`, `FR-9999`) | relación con el maestro de concesionarios |
| 900010 | estado `unknown` | valores aceptados de estado |

## Notas
- Las filas «normales» también llevan los defectos aleatorios de siempre (D03-D20, D24), por eso silver tiene trabajo en todos los pasos; el guion cuenta ventas únicas, no filas limpias.
- Si se cambian la semilla, `--rows` o el catálogo, los números cambian: regenerar el guion con `reference/delta_plan.csv`.

## Dos niveles de prueba
- **Secuencia completa (una vez, en el primer ensayo de casa)**: los 7 pasos de las tablas de arriba, para comprobar que la pipeline hace lo correcto en todos los casos. Aquí sí importan todos los recuentos.
- **Demo corta (resto de ensayos y directo, unos 3 minutos)**: solo lo que se ve bien en pantalla:
  1. Ejecutar la pipeline dos veces sin datos nuevos: los recuentos no cambian (idempotencia).
  2. Cargar un delta de ventas (`delta_2`, que también trae filas reenviadas): las ventas únicas suben exactamente lo previsto y las repetidas no cuentan.
  3. Cargar un cambio de concesionario (`delta_4`): `select * from snapshot where dealer_code = 'DE-0014'` muestra la versión nueva y la antigua cerrada.
  4. (Si da tiempo) `delta_6`: los tests fallan y salta la alerta.

## Plan de ensayos
| Ensayo | Dónde | Cuándo | Qué se hace |
|---|---|---|---|
| 1 | Casa | Antes del martes | Secuencia completa; se anotan tiempos, recuentos y fallos |
| 2 | Casa | Antes del martes | Demo corta, **grabada** como prueba de que funciona (el 1 también, si se puede) |
| 3 | Ordenador de clase | Martes | Demo corta. Comprobar antes el acceso (navegador, dbt Cloud, Snowsight, posible doble factor) |
| 4 | Directo | Jueves 26 | Demo corta; si algo falla, plan B con la grabación del ensayo 2 |

**¿Hace falta volver al estado inicial entre ensayos?** Para la demo corta, solo si se quiere repetir **los mismos números**. Hay solo dos deltas con cambios de concesionarios (4 y 5) y cuatro ensayos, así que sin reset no se puede enseñar el snapshot cuatro veces. La solución es que el reset sea **un script corto** (vaciar bronze, borrar los esquemas de silver y gold de la prueba y el snapshot, y recargar `batch_1`); lo escribimos cuando exista la pipeline. Antes de cada ensayo se comprueba que `output/manifest.json` tiene los mismos SHA-256.

**Registro de cada ensayo** (evidencia): fecha, equipo, número de ensayo, recuentos (¿coinciden con las tablas?), tiempo de cada carga y de dbt, incidencias.
