# Esquema de las diapositivas (versión del 24/11/2026)

Sustituye al apartado 2 de `slides_notes.md`, que se redactó antes de construir nada. Aquí el contenido ya es **lo que existe de verdad**. El diseño visual lo haces tú; este documento dice qué contar, en qué orden, con qué prueba y cuánto tiempo.

**Duración:** 12 minutos de exposición (máximo 15) + preguntas. La demo en directo dura 3-4 minutos y va dentro de los 12.

## Idea central (una frase)
> «Construí una plataforma de datos completa y reproducible: de un fichero que llega sucio a un informe, con tres entornos, tests que avisan de los defectos y una demo en directo de carga incremental e historial.»

Todo lo que no ayude a esa frase se queda fuera.

## Indicaciones del autor para la presentación (24/11, mandan sobre el guion)
- **Foco:** las **decisiones** (con la alternativa que se descartó y por qué), los **problemas resueltos** (contados como historias: error, diagnóstico, solución) y **qué resuelve el proyecto** para el negocio. Menos «cómo se hace» y más «por qué se hizo así».
- **Cierre:** termina con un **bloque de IA** que recalque el **valor humano**: qué hizo la IA (explicar, revisar, escribir parte del código) y qué hiciste tú (conocimiento del automóvil y del negocio, el grano, la clasificación de defectos, el alcance, las decisiones y la comprobación de que los números tienen sentido). Va como **último bloque**, después de aprendizajes y límites. Material: `defense_justifications.md` (apartado 11), `ai_collaboration_log.md` y `decisions_log.md`.
- **Historias de problemas resueltos listas para contar** (con evidencia): el `generate_schema_name` vacío que creó esquemas `CORE_*` (evidencias 37-40); el gold incremental que falló en PRO por falta de `_loaded_at` y se arregló con un `--full-refresh` aparte (evidencias 85-90); las «rutas de acceso ambiguas» de Power BI (`defense_justifications.md`, apartado 14); la clasificación de defectos corregida tras ver que eléctrico no es electrónico (apartado 9).

## Guion

| # | Diapositiva | Min | Qué dice | Qué se ve (prueba) |
|---|---|---|---|---|
| 1 | **Portada** | 0:15 | Título, nombre, formación | El coche en miniatura sobre la mesa |
| 2 | **Por qué este proyecto** | 1:30 | Gancho breve; «me gustan los coches»; el cambio de motores (combustión, híbrido, eléctrico) y la pregunta original: qué se vende, dónde y qué carrocería | Una cifra comprobada del mercado (ver `slides_notes.md`, §2b) |
| 3 | **Qué quiero responder** | 1:00 | Las 5 preguntas de negocio (UC1–UC5): familia, carrocería, propulsión, top 3 por región y campañas de defectos | Lista de 5 iconos |
| 4 | **Datos y arquitectura** | 1:30 | Ventas **simuladas** (generador reproducible) y defectos **reales** (NHTSA). Bronze → staging → silver → gold → Power BI | Diagrama de capas (README) |
| 5 | **Vocabulario del coche** | 0:30 | Familia, modelo, carrocería, propulsión, año modelo (una sola frase por concepto) | Tabla de `slides_notes.md` §2c |
| 6 | **Modelo dimensional** | 1:45 | Grano de cada tabla, estrella pura: `dim_family` compartida por ventas y campañas, y por qué no hay copo de nieve | Diagrama dimensional v7 |
| 7 | **Cómo está construido** | 1:30 | Medallion en dbt: staging limpia, silver deduplica y traduce, gold modela. Macros y variables | Linaje de dbt (captura por hacer) |
| 8 | **Entornos y jobs** | 1:00 | DEV, PRE y PRO con el mismo código; la variable `DBT_ENV_NAME`; ramas → PR → `develop` → `pre` → `main`; jobs manuales y el programado del lunes | Evidencias 27-29, 56-62 |
| 9 | **DEMO EN DIRECTO** | 3:30 | **Incremental** (delta 3: 160 filas y luego 0) y **snapshot** (delta 5: DE-0014 con tres versiones) | `demo_jueves.md` |
| 10 | **Calidad y alertas** | 1:00 | Los tests no esconden los defectos: 78 fechas, 212 sin concesionario, 124 precios. El delta 6 hace fallar los tests | Evidencias 45-47, 70-71 y vídeo de alertas |
| 11 | **Resultados en Power BI** | 1:15 | Ventas por familia, carrocería, propulsión y región; defectos por familia y por sistema | Capturas del informe (esta tarde) |
| 12 | **Aprendizajes, límites y futuro** | 1:15 | Lo que aprendí; lo que es simulado; lo que haría con más tiempo | Ver abajo |

Suma: unos 15 min si se va despacio. Para llegar a 12, acorta 2 (motivación), 5 y 7, que son las que se pueden contar de pie sin diapositiva.

### Diapositiva 12 (cierre): lo que dices tú, antes de que pregunten
- **Aprendizajes:** una pipeline reproducible importa más que una consulta bonita; los defectos de datos hay que verlos y medirlos, no esconderlos; separar entornos y roles evita errores caros.
- **Límites (dilos tú):** las ventas son simuladas; una sola región terminada (Europa); los defectos son de EE. UU. y las ventas de Europa, por eso no se dividen (D-020, D-039); la carga es manual; todos los roles los usa una sola persona; los tipos de cambio son simulados.
- **Futuro:** más regiones (el mismo patrón: su bronce, staging y silver, y el mismo gold); carga semanal automática; usuarios de servicio y SSO; un bronce por entorno.
- **Equipo internacional simulado:** código, commits y pull requests en inglés con formato *Conventional Commits*; documentación en español e inglés (`defense_justifications.md`, apartado 10).
- **Qué aportas tú frente a una IA:** el conocimiento del automóvil y del negocio, que decidió el grano, la clasificación de defectos y las reglas (`defense_justifications.md`, apartado 11).
- **Sobre el uso de IA (dilo con naturalidad):** el repositorio incluye el registro de decisiones y el de colaboración con la IA. La IA explicó, revisó y escribió parte del código; **las decisiones de diseño son tuyas** y puedes defenderlas.

## Las 5 decisiones que mejor enseñan criterio (diapositivas 4, 6 y 10)
1. Ventas simuladas + defectos reales (D-001), sin mezclar cifras (D-020).
2. Estrella pura con `dim_family` compartida (D-059).
3. Los defectos de datos se avisan y se guardan, no se corrigen en silencio (D-066, D-070).
4. Tres entornos con el mismo código y variables de entorno (D-067).
5. Neto en euros con el tipo de cambio del mes de la venta (D-069).

## Evidencias que faltan por guardar
- [ ] Linaje de dbt (grafo completo)
- [ ] Snapshot con las tres versiones de DE-0014 (se hace en el ensayo)
- [ ] Informe de Power BI (las tres páginas)
- [ ] Historial de ramas y pull requests en GitHub
- [ ] Vídeo de la demo y de las alertas (fuera del repositorio)

## Plan para preparar las diapositivas
| Cuándo | Qué |
|---|---|
| Esta tarde (clase) | Power BI y capturas; llevar las preguntas de `class_questions.md` |
| Miércoles mañana | Diseño: portada, motivación, vocabulario, arquitectura y modelo; ensayo de la demo |
| Miércoles tarde | Cierre y límites; preguntas de defensa; ensayo cronometrado |
| Jueves mañana | Último ensayo y revisión; entrega del repositorio y las diapositivas |

## Preguntas de defensa que conviene ensayar
Detalle en `defense_justifications.md` y `roles_permissions.md`. Las seis más probables:
1. ¿Por qué el hecho es incremental en silver y en gold? (coherencia de extremo a extremo, tras consultarlo con el profesorado, D-072; la primera ejecución de cada entorno necesitó `--full-refresh`)
2. ¿Qué pasa si llega una venta repetida? (`merge` por `sale_id`; el reenvío no duplica)
3. ¿Por qué un snapshot y no una tabla con fechas? (historial automático de cambios, sin perder el nombre anterior)
4. ¿Cómo sabes que los datos son correctos? (tests, avisos con filas guardadas, recuentos que cuadran entre capas)
5. ¿Por qué tres entornos y cómo evitas tocar PRO? (variable de entorno, rama y permisos por rol)
6. ¿Qué harías con datos reales y más volumen? (ingesta automática, usuarios de servicio, un bronce por entorno)

## Borrador del autor revisado (25/11): este es el guion a seguir
| # | Diapositiva | Min | Contenido |
|---|---|---|---|
| 1 | Motivación | 1:00 | Por qué este trabajo |
| 2 | Casos de uso | 1:00 | Dos descartados (predicción de modelo nuevo por región; pentesting y ciberseguridad del coche) y las cinco preguntas finales: UC1 familias, UC2 carrocería, UC3 propulsión, UC4 top 3 modelos por país en 2025, UC5 campañas mecánicas frente a electrónica/software |
| 3 | Datos y arquitectura | 1:00 | Ventas **simuladas** y campañas **reales** (NHTSA, EE. UU.); medallion |
| 4 | Modelos | 1:45 | **Conceptual → lógico → dimensional**, con sus versiones. La decisión estrella frente a copo de nieve es del **dimensional**. Mucho tiempo y atención |
| 5 | Demo en directo | 3:00 | Tabla incremental y snapshot (`demo_jueves.md`) |
| 6 | Calidad y alertas | 0:45 | Tests, avisos con filas guardadas |
| 7 | Resultados en Power BI | 1:30 | La respuesta a cada pregunta |
| 8 | Entornos, ramas y jobs | 1:00 | DEV, PRE, PRO; PR; job semanal |
| 9 | Ciberseguridad | 0:30 | Roles de mínimo privilegio, lectura para Power BI, clave para dbt, sin secretos en el repositorio |
| 10 | Mejoras | 0:30 | Bronce crudo de campañas, más regiones, ingesta automática, usuarios de servicio |
| 11 | Toma de decisiones, IA y mi aportación | 1:00 | **Cómo decidí y cómo lo registré** (`decisions_log.md`: contexto, opciones, decisión y porqué; incluye lo descartado y lo que cambió, p. ej. D-072 tras consultar al profesorado). Qué hizo la IA y qué decidí yo. Captura del registro |

Total: **13:00**. En cada diapositiva, una decisión con su alternativa descartada; en la 11, el **método**: el registro de decisiones.

**Control del tiempo (25/11):** los 2 minutos de margen no se planifican, y a partir del minuto 10 puede haber presión para terminar. Por eso la demo y los resultados deben estar contados hacia el minuto 10 (si hace falta, modelos en 1:30). Si aprietan: diapositivas 8, 9 y 10 en una frase cada una (1:00 en total) y la 11 (decisiones, IA y mi aportación) se mantiene.

### Cómo contar UC5 (diapositiva 7)
- «Esta clasificación es mía: NHTSA solo indica el sistema afectado.»
- «Eléctrico no es electrónico, y por eso van separados. La iluminación es eléctrica salvo que el componente diga software o módulo de control. Lo ambiguo, como los airbags, va a una categoría mixta.»
- «Lo mecánico lidera de 2021 a 2024; en 2025 lo supera lo eléctrico.» 2025 no es comparable sin más: solo hay modelos hasta 2025 y los recientes han tenido menos tiempo para acumular campañas.
- Si preguntan por modelo o familia: «el modelo lo permite; es una mejora del informe» (D-077).

### Mejoras: métricas que podríamos mostrar (diapositiva 10)
Salen del gold actual, sin cambiar dbt:
- Ingresos netos en euros y precio medio neto por país y familia (con tipos de cambio simulados).
- Porcentaje de devoluciones y cancelaciones.
- Días entre la venta y la entrega.
- Ranking de concesionarios (contando por `dealer_code`, no por versión).
- Campañas por familia, junto a las unidades vendidas, **sin ratio** (EE. UU. frente a Europa).
- Unidades afectadas por campaña (una vez por campaña, nunca sumando líneas).
