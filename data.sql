BEGIN;

INSERT INTO usuario (id, username, password) VALUES
('b5b8c640-71f4-4f92-91fe-3f8ee59c1011', 'alice', 'alice_pwd_hash'),
('a63f4dbb-15ee-4ac4-920f-7b5c9f0b2022', 'bob',   'bob_pwd_hash');

INSERT INTO perfil (id, nombre, pais, usuario_id) VALUES
('11111111-1111-1111-1111-111111111111', 'Alice Smith', 'USA', 'b5b8c640-71f4-4f92-91fe-3f8ee59c1011'),
('22222222-2222-2222-2222-222222222222', 'Bob Jones',   'Canada', 'a63f4dbb-15ee-4ac4-920f-7b5c9f0b2022');

INSERT INTO acceso (id, ultimo_login) VALUES
('b5b8c640-71f4-4f92-91fe-3f8ee59c1011', '2026-02-17 10:00:00'),
('a63f4dbb-15ee-4ac4-920f-7b5c9f0b2022', '2026-02-17 11:15:00');

INSERT INTO categoria (id, nombre) VALUES
('33333333-3333-3333-3333-333333333333', 'Action'),
('44444444-4444-4444-4444-444444444444', 'RPG');

INSERT INTO plataforma (id, nombre) VALUES
('55555555-5555-5555-5555-555555555555', 'PC'),
('66666666-6666-6666-6666-666666666666', 'PlayStation 5'),
('77777777-7777-7777-7777-777777777777', 'Xbox Series X');

-- categoria_id is UNIQUE in your model, so each category can only be used once here
INSERT INTO videojuego (id, nombre, descripcion, url_imagen, categoria_id) VALUES
('88888888-8888-8888-8888-888888888888', 'Cyber Quest', 'Sci-fi action game', 'https://example.com/cyber-quest.jpg', '33333333-3333-3333-3333-333333333333'),
('99999999-9999-9999-9999-999999999999', 'Dragon Realm', 'Fantasy RPG adventure', 'https://example.com/dragon-realm.jpg', '44444444-4444-4444-4444-444444444444');

INSERT INTO videojuego_plataforma (videojuego_id, plataforma_id) VALUES
('88888888-8888-8888-8888-888888888888', '55555555-5555-5555-5555-555555555555'),
('88888888-8888-8888-8888-888888888888', '66666666-6666-6666-6666-666666666666'),
('99999999-9999-9999-9999-999999999999', '55555555-5555-5555-5555-555555555555'),
('99999999-9999-9999-9999-999999999999', '77777777-7777-7777-7777-777777777777');

COMMIT;
