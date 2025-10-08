-- SQL скрипт для создания индексов для оптимизации запросов
-- Этот файл содержит все рекомендуемые индексы для улучшения производительности

-- Удаляем существующие индексы если они есть
DROP INDEX IF EXISTS idx_students_room;
DROP INDEX IF EXISTS idx_students_sex;
DROP INDEX IF EXISTS idx_students_birthday;
DROP INDEX IF EXISTS idx_students_room_sex;

-- Основные индексы для оптимизации JOIN операций
CREATE INDEX idx_students_room ON students(room);
COMMENT ON INDEX idx_students_room IS 'Индекс для оптимизации JOIN между students и rooms';

-- Индекс для фильтрации по полу студентов
CREATE INDEX idx_students_sex ON students(sex);
COMMENT ON INDEX idx_students_sex IS 'Индекс для быстрой фильтрации студентов по полу';

-- Индекс для вычисления возраста студентов
CREATE INDEX idx_students_birthday ON students(birthday);
COMMENT ON INDEX idx_students_birthday IS 'Индекс для оптимизации вычислений возраста';

-- Составной индекс для запросов с группировкой по комнате и полу
CREATE INDEX idx_students_room_sex ON students(room, sex);
COMMENT ON INDEX idx_students_room_sex IS 'Составной индекс для запросов по комнате и полу одновременно';

-- Дополнительные индексы для специфических запросов

-- Индекс для быстрого поиска студентов по имени (если потребуется)
-- CREATE INDEX idx_students_name ON students(name);

-- Частичный индекс только для мужчин (пример оптимизации для частых запросов)
-- CREATE INDEX idx_students_male ON students(room) WHERE sex = 'M';

-- Частичный индекс только для женщин
-- CREATE INDEX idx_students_female ON students(room) WHERE sex = 'F';

-- Функциональный индекс для возраста (если часто используется)
-- CREATE INDEX idx_students_age ON students(EXTRACT(YEAR FROM AGE(CURRENT_DATE, birthday)));

-- Вывод информации о созданных индексах
SELECT 
    schemaname,
    tablename,
    indexname,
    indexdef
FROM pg_indexes 
WHERE tablename IN ('students', 'rooms')
ORDER BY tablename, indexname;
