-- Eliminar admins existentes con ese email
DELETE FROM admin WHERE email = 'admin@dime.com';

-- Insertar admin con contraseña: Admin12345678 (12 caracteres, cumple el mínimo del schema)
INSERT INTO admin (user_name, email, password)
VALUES (
    'admin',
    'admin@dime.com',
    '$2b$12$BOaz0rU8KunPMVkMoUxeBucHBzerLajhGbiEJu7jZLGsKqZESnb2e'
);
