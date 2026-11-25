-- Permiso para mostrar/ocultar el botón "Auditado" en Ausentismos/Controles.
-- El proyecto no usa migraciones de Django (las carpetas migrations/ están vacías),
-- por lo que el cambio se aplica manualmente en cada entorno (MariaDB/MySQL).
INSERT INTO usu_permiso (PERMISO, PERMISO_NAME, CATEGORIA)
SELECT 'AUDITAR AUSENTISMOS', 'aus_auditado', ID
FROM usu_permiso_categ
WHERE CATEGORIA = 'GESTION EMPLEADOS'
  AND NOT EXISTS (
      SELECT 1 FROM usu_permiso WHERE PERMISO_NAME = 'aus_auditado'
  );

-- El permiso debe asignarse a cada usuario desde el formulario de usuarios.
-- Los administradores (tipoUsr = 0) lo tienen automáticamente.

-- Rollback:
-- DELETE FROM usu_permiso WHERE PERMISO_NAME = 'aus_auditado';
