-- Auditoría médica de ausentismos.
-- El proyecto no usa migraciones de Django (las carpetas migrations/ están vacías),
-- por lo que el cambio de esquema se aplica manualmente en cada entorno (MariaDB/MySQL).
ALTER TABLE ausentismo
    ADD COLUMN auditado TINYINT(1) NOT NULL DEFAULT 0,
    ADD COLUMN fecha_auditado DATETIME NULL DEFAULT NULL,
    ADD COLUMN auditado_por VARCHAR(100) NULL DEFAULT NULL;

-- Rollback:
-- ALTER TABLE ausentismo
--     DROP COLUMN auditado_por,
--     DROP COLUMN fecha_auditado,
--     DROP COLUMN auditado;
