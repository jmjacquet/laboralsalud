# Propuesta de solución: indicador de Auditoría Médica en Ausentismos/Controles

**Referencia:** Requerimiento de Sistema del 20/11/2026 – *Incorporación de indicador de auditoría médica en la pestaña "Ausentismos/Controles del día"*

---

## 1. Resumen

Se propone incorporar al sistema un **indicador de auditoría médica por evolución**, de modo que el coordinador médico pueda marcar las evoluciones que ya revisó y distinguirlas, en cualquier momento de la jornada, de las que aún están pendientes.

La propuesta toma la primera alternativa planteada en el requerimiento (**casilla de verificación con tilde**) y la integra con los mecanismos que el sistema ya utiliza para trabajar sobre varios registros a la vez (selección por casillas y botón general en la parte superior, igual que "Generar Informe" y "Enviar Informe").

Con esto se resuelve el problema descripto: si durante la mañana se auditan 20 evoluciones y luego se incorporan 30 nuevas, al finalizar la jornada las 20 auditadas seguirán mostrando el tilde y las 30 nuevas aparecerán sin marca, evitando revisar nuevamente la totalidad de los casos.

---

## 2. Funcionamiento propuesto

### 2.1. Nueva columna "Auditado"

- Se agrega la columna **"Auditado"** en la grilla de **Ausentismos/Controles del día** (pantalla de inicio) y en la grilla de **Gestión Ausentismos/Controles**.
- Se ubica a continuación de la casilla de selección, para que sea visible de inmediato.
- Su estado inicial es **"No auditado"** para todas las evoluciones. En ese caso la celda se muestra **vacía**.
- Cuando la evolución está auditada, la celda muestra un **tilde verde (✔)**.
- La columna puede ordenarse, de modo que las evoluciones auditadas o pendientes queden agrupadas.

### 2.2. Cómo marcar evoluciones como auditadas

1. El coordinador médico selecciona con las **casillas de verificación** de la grilla las evoluciones que ya revisó. También puede usar la casilla del encabezado para seleccionar todas.
2. Presiona el botón **"Marcar Auditado"**, ubicado en la parte superior de la grilla, junto a "Generar Informe" y "Enviar Informe".
3. El sistema registra las evoluciones seleccionadas como auditadas y actualiza la grilla, que pasa a mostrar el tilde en cada una de ellas.

Esto permite auditar de a una evolución o por lotes (por ejemplo, al terminar de revisar un grupo de casos), según le resulte más cómodo al coordinador durante la jornada.

> El botón "Marcar Auditado" está disponible para los usuarios que cuentan con permiso de carga/modificación de ausentismos, igual que los botones de informes.

### 2.3. Fecha, hora y usuario de la auditoría

- Al marcar una evolución como auditada, el sistema **guarda la fecha y la hora** en que se realizó la acción y el **usuario** de quien presionó "Marcar Auditado" (el nombre de usuario con el que ingresó al sistema).
- Esa información se muestra en dos columnas al **final** de la grilla: **"F.Auditado"** y **"Auditado por"**.
- Ambas columnas están **ocultas por defecto**. Se pueden mostrar u ocultar en cualquier momento con el botón de selección de columnas (ícono de lista) que ya existe en la barra de herramientas de la grilla.

### 2.4. Qué ocurre cuando una evolución se modifica

Una auditoría es válida para el contenido que fue revisado. Por lo tanto, **cuando se actualiza el ausentismo/control, la evolución vuelve automáticamente a "No auditado"** (se quita el tilde y se borran la fecha de auditoría y el usuario que la realizó). Esto ocurre cuando:

- se edita el ausentismo/control y se guardan los cambios;
- se carga un nuevo control (seguimiento) sobre la evolución;
- se modifica o elimina un control existente.

De esta manera, el tilde significa siempre que **la evolución se revisó en su versión actual**, y las evoluciones modificadas después de ser auditadas quedan nuevamente identificadas como pendientes de revisión.

### 2.5. Persistencia del estado durante la jornada

El estado de auditoría se **guarda en el sistema**. Por este motivo:

- se mantiene aunque durante el día se incorporen nuevos empleados a la pestaña;
- se mantiene si el usuario cierra sesión, recarga la página o cambia de equipo;
- es visible para todos los usuarios habilitados de la empresa.

El requerimiento indica que alcanza con que la información persista durante 24 horas. La solución propuesta la conserva sin límite de tiempo, lo que además permite consultar posteriormente qué evoluciones fueron auditadas, cuándo y por quién (ver punto 3). No se agrega ninguna marca ni dato en el texto de la historia clínica.

---

## 3. Filtro de búsqueda por estado de auditoría

En la **Búsqueda Avanzada** de *Gestión Ausentismos/Controles* se agregan tres nuevos parámetros:

| Parámetro | Descripción |
|---|---|
| **Auditoría** | Permite elegir entre **Todos**, **Auditados** y **No auditados**. Por defecto: *Todos*. |
| **Auditoría Desde** | Fecha inicial del rango. |
| **Auditoría Hasta** | Fecha final del rango (inclusive). |

El rango de fechas se interpreta según la opción elegida:

- **Auditados:** el rango se aplica a la **fecha y hora en que se realizó la auditoría**. Ejemplo: *Auditados, desde 20/11/2026 hasta 20/11/2026* devuelve todo lo auditado durante ese día.
- **No auditados:** como las evoluciones pendientes aún no tienen fecha de auditoría, el rango se aplica a la **fecha de la evolución** (fecha de carga o fecha de alguno de sus controles). Ejemplo: *No auditados, desde 20/11/2026 hasta 20/11/2026* devuelve las evoluciones del día que aún no fueron revisadas.
- **Todos:** el rango de auditoría no se aplica.

Pueden indicarse ambas fechas o solamente una (en ese caso el rango queda abierto hacia el otro extremo). El filtro puede combinarse con el resto de los parámetros de búsqueda existentes (empresa, empleado, tipo de ausentismo, vigencia, etc.).

---

## 4. Resumen de cambios visibles para el usuario

| Pantalla | Cambio |
|---|---|
| Inicio – Ausentismos/Controles del día | Nueva columna **Auditado** (tilde). Nuevo botón **Marcar Auditado**. Nuevas columnas ocultas **F.Auditado** y **Auditado por**. |
| Gestión Ausentismos/Controles | Ídem anterior, más los nuevos filtros de **Auditoría** en la Búsqueda Avanzada. |
| Edición de ausentismos / carga de controles | Sin cambios de uso. Al guardar, la evolución vuelve a "No auditado". |

---

## 5. Alcance y consideraciones

- La **segunda alternativa** del requerimiento (opción "Auditado" en el menú desplegable de cada evolución, con cambio de color de la fila) **no forma parte de esta propuesta**. Si se considerara útil, puede incorporarse en una etapa posterior sin modificar lo descripto.
- No se incorpora la posibilidad de **desmarcar manualmente** una evolución como auditada: el estado se restablece únicamente cuando la evolución se modifica. Si se requiere desmarcar manualmente, puede agregarse como mejora.
- El usuario que se guarda es el **nombre de usuario de ingreso** de quien presiona el botón, no el nombre y apellido.
- Las columnas de tilde, fecha de auditoría y usuario auditor no se incluyen en las exportaciones a Excel, PDF e impresión de la grilla.
- Para su puesta en producción es necesario agregar tres campos a la base de datos (estado de auditoría, fecha/hora de auditoría y usuario que auditó). Los registros existentes quedarán como **"No auditado"**. Se realizará durante una ventana de mantenimiento breve, sin pérdida de información.

---

## 6. Criterios de aceptación

1. Todas las evoluciones nuevas y existentes se muestran inicialmente sin tilde en la columna **Auditado**.
2. Al seleccionar una o más evoluciones y presionar **Marcar Auditado**, cada una muestra el tilde.
3. Al incorporarse nuevos empleados a la pestaña durante el día, las evoluciones ya auditadas conservan el tilde.
4. Las columnas **F.Auditado** y **Auditado por** se encuentran ocultas por defecto. Al mostrarlas, indican la fecha y hora de la auditoría y el usuario que la marcó.
5. Al modificar una evolución auditada (edición o carga de un control), pierde el tilde, la fecha de auditoría y el usuario auditor.
6. En la Búsqueda Avanzada es posible filtrar por **Auditados** o **No auditados** dentro de un rango de fechas.
