# Guion de la presentación (jueves 26/11, versión final)

Texto de las notas del orador de la presentación (V7). Total **12:00**. La presentación está fuera del repositorio.
Detalle de la demo en `snowflake/06_demo_live.sql` (con guion) y `snowflake/07_demo_screen.sql` (para pantalla).

### 1 · PORTADA · 0:15 · hasta 0:15
Hola, soy Daniel. He construido una plataforma de datos completa: de un fichero sucio a un informe fiable.

### 2 · MOTIVACIÓN · 0:45 · hasta 1:00
Me gustan los coches y el automóvil está cambiando: combustión, híbridos y eléctricos. Quiero saber qué se vende, dónde y de qué tipo.

### 3 · CASOS DE USO · 0:45 · hasta 1:45
Descarté dos ideas: predecir el siguiente modelo exigía un modelo predictivo, y para la ciberseguridad del coche no había datos públicos. Quedan cinco preguntas.

### 4 · DATOS Y ARQUITECTURA · 1:00 · hasta 2:45
Las ventas son simuladas, con un generador reproducible; las campañas son reales, de la NHTSA. No las divido entre sí. Bronze guarda el dato como llega; en campañas un script filtra antes de cargar. Staging pone tipos, silver limpia y gold modela.

### 5 · MODELO CONCEPTUAL · 0:35 · hasta 3:20
Fueron diez días, del 17 al 26. Del 20 al 22, modelar: entender el negocio antes de escribir código. Aquí está qué existe y cómo se relaciona.

### 6 · MODELO LÓGICO · 0:15 · hasta 3:35
(Enseñar en draw.io) Las mismas entidades con atributos y claves. Me fijo en Sales y Campaign line.

### 7 · MODELO DIMENSIONAL · 0:55 · hasta 4:30
Estrella pura con dos hechos: una fila por venta, y una por campaña, familia, año modelo y componente. Comparten dim_family. Descarté el copo de nieve. El diagrama refleja lo construido.

### 8 · DEMO · 2:00 · hasta 6:30
Mientras dbt trabaja se cuentan las diapositivas 9 y 10.

1) Bloque 1 (antes)
"En silver hay 44.382 ventas. Me fijo en dos: una está vendida y la otra tiene este precio. El concesionario DE-0014 tiene dos versiones."

2) Bloque 2 (carga) SOLO EN DIRECTO
"Llega un lote de ventas y un maestro de concesionarios. Los cargo en bronze, tal como llegan, con un rol solo de ingesta."

3) dbt: Enter
"La tabla de silver es incremental: solo procesa lo nuevo y hace merge por sale_id: inserta las ventas nuevas y actualiza las que ya existían. El snapshot compara los concesionarios; si algo cambió, cierra la versión antigua y abre otra."

4) Bloque 4
"Han llegado 160 filas, pero la tabla solo crece en 150: son 150 ventas nuevas y 10 cambios. Una pasa a devuelta y otra cambia de precio. No se duplican."
(160 · 150 · 10 · 44.532)

5) Bloque 5
"Tengo las tres versiones del concesionario, con desde cuándo y hasta cuándo; la vigente no tiene fin. La fecha es cuando dbt detectó el cambio."

### 9 · LINAJE · 0:30 · hasta 7:00
Cada flecha es un ref o un source: puedo seguir un dato del informe al fichero. dim_date no aparece porque se genera con SQL.

### 10 · CALIDAD Y GOBIERNO · 0:45 · hasta 7:45
Los tests avisan sin parar la carga; en fechas y precios guardan las filas. 45.051 filas en bronze son 44.382 ventas únicas y 41.732 vendidas; las distintas grafías se unen en 51 variantes. Las columnas están descritas, y estado, impuesto, familia y categoría tienen un test de valores permitidos.

### 11 · UC1 FAMILIA · 0:20 · hasta 8:05
El A-Class lidera hasta 2024; en 2025 pasa delante el GLC. 2025 llega hasta mediados de diciembre.

### 12 · UC2 CARROCERÍA · 0:20 · hasta 8:25
El SUV lidera y toca máximo en 2024; el hatchback baja. Los descapotables aparecen en 2022.

### 13 · UC3 PROPULSIÓN · 0:25 · hasta 8:50
La gasolina lidera hasta 2024; en 2025 la superan híbridos y eléctricos. HEV es híbrido sin enchufe; PHEV, enchufable.

### 14 · UC4 TOP 3 · 0:20 · hasta 9:10
El GLC 200 es primero en los seis países. Reino Unido y Suiza meten un eléctrico en su top 3.

### 15 · UC5 CAMPAÑAS · 0:20 · hasta 9:30
La clasificación es mía: NHTSA solo indica el sistema afectado, y eléctrico no es electrónico. Lo mecánico lidera de 2021 a 2024; 2025 no es comparable sin más.

### 16 · ENTORNOS Y JOBS · 0:50 · hasta 10:20
El mismo código en tres entornos. DBT_ENV_NAME decide en qué base de datos se escribe y DBT_BRONZE_DB de dónde se lee. Cambios por pull request, jobs manuales y uno semanal. Nombres en inglés, como en un equipo internacional.

### 17 · CIBERSEGURIDAD · 0:20 · hasta 10:40
Cada rol con lo mínimo, y Power BI solo lee. Límite: en el proyecto todos los roles los usa una sola persona.

### 18 · MEJORAS · 0:30 · hasta 11:10
Me quedo con dos: DevSecOps y un informe web que se comparta con un enlace, además de Power BI.

### 19 · DECISIONES E IA · 0:50 · hasta 12:00
Registré cada decisión, también las descartadas; esta cambió tras consultar al profesorado. La IA escribe rápido, pero no sabe de coches: vi que eléctrico no es electrónico. El criterio y las decisiones son míos.

### 20 · CIERRE · 0:00 · hasta 12:00
Muchas gracias. ¿Preguntas?
