-- Создание схемы базы данных для студентов и комнат
-- Связь many-to-one: много студентов в одной комнате

-- Удаляем таблицы если они существуют (для повторного запуска)
DROP TABLE IF EXISTS students CASCADE;
DROP TABLE IF EXISTS rooms CASCADE;

-- Создаем таблицу комнат
CREATE TABLE rooms (
    id INTEGER PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

-- Создаем таблицу студентов
CREATE TABLE students (
    id INTEGER PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    birthday TIMESTAMP NOT NULL,
    room INTEGER NOT NULL,
    sex CHAR(1) NOT NULL CHECK (sex IN ('M', 'F')),
    FOREIGN KEY (room) REFERENCES rooms(id)
);

-- Создаем индексы для оптимизации запросов
CREATE INDEX idx_students_room ON students(room);
CREATE INDEX idx_students_sex ON students(sex);
CREATE INDEX idx_students_birthday ON students(birthday);
CREATE INDEX idx_students_room_sex ON students(room, sex);
