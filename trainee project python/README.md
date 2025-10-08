# Анализатор данных студентов и комнат

Это приложение для анализа данных студентов и комнат с использованием PostgreSQL. Приложение загружает данные из JSON файлов, создает схему базы данных и генерирует различные отчеты.

## Архитектура решения

Приложение построено с использованием принципов **SOLID** и паттернов проектирования:

### Принципы SOLID:
- **S** - Single Responsibility: каждый класс отвечает за одну задачу
- **O** - Open/Closed: легко расширяется новыми форматами экспорта и типами отчетов
- **L** - Liskov Substitution: интерфейсы позволяют заменять реализации
- **I** - Interface Segregation: разделенные интерфейсы для разных задач
- **D** - Dependency Inversion: зависимости от абстракций, а не от конкретных классов

### Паттерны проектирования:
- **Repository Pattern** - для работы с данными
- **Strategy Pattern** - для экспорта в разные форматы
- **Command Pattern** - для различных типов отчетов
- **Facade Pattern** - для упрощения взаимодействия с системой

## Структура проекта

```
trainee project python/
├── data/
│   ├── students.json    # Данные студентов
│   └── rooms.json       # Данные комнат
├── results/             # Папка с результатами отчетов (создается автоматически)
│   ├── rooms_count.json
│   ├── smallest_avg_age.json
│   ├── largest_age_diff.json
│   └── mixed_gender.json
├── schema.sql           # SQL схема базы данных
├── indexes.sql          # Дополнительные индексы для оптимизации
├── database.py          # Работа с базой данных
├── data_loader.py       # Загрузка и валидация данных
├── export_service.py    # Экспорт в разные форматы
├── report_service.py    # Генерация отчетов
├── main.py             # Главный модуль
├── requirements.txt    # Зависимости Python
├── .gitignore          # Исключения для Git
└── README.md          # Документация
```

## Требования

- Python 3.8+
- PostgreSQL 12+
- pip

## Установка

1. **Создайте виртуальное окружение:**
```bash
python3 -m venv venv
source venv/bin/activate  # На Windows: venv\Scripts\activate
```

2. **Установите зависимости:**
```bash
pip3 install -r requirements.txt
```

**Если возникает ошибка с psycopg2-binary на Mac, попробуйте один из вариантов:**

```bash
# Вариант 1: Обновите pip и попробуйте снова
pip3 install --upgrade pip
pip3 install -r requirements.txt

# Вариант 2: Установите через Homebrew (если установлен)
brew install postgresql
pip3 install psycopg2

# Вариант 3: Установите конкретную версию
pip3 install psycopg2-binary==2.9.5

# Вариант 4: Установите без бинарной версии
pip3 install psycopg2

# Вариант 5: Если у вас Apple Silicon (M1/M2)
arch -arm64 pip install psycopg2-binary
```

3. **Настройте PostgreSQL:**

**Установка PostgreSQL на Mac:**
```bash
# Через Homebrew (рекомендуется)
brew install postgresql
brew services start postgresql

# Создайте базу данных под вашим пользователем
createdb students_db

# Или через psql:
psql postgres
CREATE DATABASE students_db;
\q
```

**Если PostgreSQL не установлен:**
- Скачайте с официального сайта: https://www.postgresql.org/download/macosx/
- Или используйте Postgres.app: https://postgresapp.com/

## Использование

### Базовое использование:
```bash
python3 main.py --students data/students.json --rooms data/rooms.json --format json
```

**Результат:** Все отчеты будут сохранены в папку `results/` в корне проекта. Папка создается автоматически при первом запуске.

### Полный список параметров:
```bash
python3 main.py --help
```

### Параметры командной строки:

- `--students` - Путь к файлу с данными студентов (обязательный)
- `--rooms` - Путь к файлу с данными комнат (обязательный)
- `--format` - Формат вывода: `json` или `xml` (по умолчанию: json)
- `--report` - Тип отчета (опционально, если не указан - генерируются все)
- `--db-host` - Хост PostgreSQL (по умолчанию: localhost)
- `--db-port` - Порт PostgreSQL (по умолчанию: 5432)
- `--db-name` - Имя базы данных (по умолчанию: students_db)
- `--db-user` - Пользователь БД (по умолчанию: evgenijbyhovcov)
- `--db-password` - Пароль БД (по умолчанию: password)

### Типы отчетов:

1. `rooms_count` - Список комнат и количество студентов в каждой
2. `smallest_avg_age` - 5 комнат с наименьшим средним возрастом студентов
3. `largest_age_diff` - 5 комнат с наибольшей разницей в возрасте студентов
4. `mixed_gender` - Список комнат, где живут разнополые студенты

### Примеры использования:

```bash
# Генерация всех отчетов в JSON формате (сохраняются в results/)
python3 main.py --students data/students.json --rooms data/rooms.json --format json

# Генерация конкретного отчета в XML формате (сохраняется в results/)
python3 main.py --students data/students.json --rooms data/rooms.json --format xml --report rooms_count

# Использование с кастомными настройками БД
python3 main.py --students data/students.json --rooms data/rooms.json \
  --db-host localhost --db-port 5432 --db-name my_db --db-user evgenijbyhovcov --db-password mypass
```

**Файлы результатов:**
После выполнения команд в папке `results/` появятся файлы:
- `results/rooms_count.json` - список комнат с количеством студентов
- `results/smallest_avg_age.json` - 5 комнат с наименьшим средним возрастом
- `results/largest_age_diff.json` - 5 комнат с наибольшей разницей возрастов  
- `results/mixed_gender.json` - комнаты с разнополыми студентами

## Схема базы данных

### Таблица `rooms`:
- `id` (INTEGER, PRIMARY KEY) - Уникальный идентификатор комнаты
- `name` (VARCHAR(255)) - Название комнаты

### Таблица `students`:
- `id` (INTEGER, PRIMARY KEY) - Уникальный идентификатор студента
- `name` (VARCHAR(255)) - Имя студента
- `birthday` (TIMESTAMP) - Дата рождения
- `room` (INTEGER, FOREIGN KEY) - Ссылка на комнату
- `sex` (CHAR(1)) - Пол студента ('M' или 'F')

### Индексы для оптимизации:
- `idx_students_room` - на поле `room`
- `idx_students_sex` - на поле `sex`
- `idx_students_birthday` - на поле `birthday`
- `idx_students_room_sex` - составной индекс на `room` и `sex`

## SQL запросы

### 1. Список комнат и количество студентов:
```sql
SELECT 
    r.id,
    r.name,
    COUNT(s.id) as student_count
FROM rooms r
LEFT JOIN students s ON r.id = s.room
GROUP BY r.id, r.name
ORDER BY r.id;
```

### 2. 5 комнат с наименьшим средним возрастом:
```sql
SELECT 
    r.id,
    r.name,
    ROUND(AVG(EXTRACT(YEAR FROM AGE(CURRENT_DATE, s.birthday))), 2) as avg_age
FROM rooms r
INNER JOIN students s ON r.id = s.room
GROUP BY r.id, r.name
HAVING COUNT(s.id) > 0
ORDER BY avg_age ASC
LIMIT 5;
```

### 3. 5 комнат с наибольшей разницей в возрасте:
```sql
SELECT 
    r.id,
    r.name,
    MAX(EXTRACT(YEAR FROM AGE(CURRENT_DATE, s.birthday))) - 
    MIN(EXTRACT(YEAR FROM AGE(CURRENT_DATE, s.birthday))) as age_difference
FROM rooms r
INNER JOIN students s ON r.id = s.room
GROUP BY r.id, r.name
HAVING COUNT(s.id) > 1
ORDER BY age_difference DESC
LIMIT 5;
```

### 4. Комнаты с разнополыми студентами:
```sql
SELECT 
    r.id,
    r.name,
    COUNT(DISTINCT s.sex) as gender_count
FROM rooms r
INNER JOIN students s ON r.id = s.room
GROUP BY r.id, r.name
HAVING COUNT(DISTINCT s.sex) > 1
ORDER BY r.id;
```

## Оптимизация запросов

### Рекомендуемые индексы:

1. **Основные индексы:**
   - `CREATE INDEX idx_students_room ON students(room);` - для JOIN операций
   - `CREATE INDEX idx_students_birthday ON students(birthday);` - для вычисления возраста
   - `CREATE INDEX idx_students_sex ON students(sex);` - для фильтрации по полу

2. **Составные индексы:**
   - `CREATE INDEX idx_students_room_sex ON students(room, sex);` - для запросов с группировкой по комнате и полу

3. **Дополнительные оптимизации:**
   - Использование `INNER JOIN` вместо `LEFT JOIN` где это возможно
   - Группировка и агрегация выполняются на уровне БД
   - Использование `HAVING` для фильтрации агрегированных данных

## Форматы вывода

### JSON формат:
```json
{
  "title": "Название отчета",
  "data": [
    {
      "id": 1,
      "name": "Room #1",
      "student_count": 5
    }
  ],
  "count": 1
}
```

### XML формат:
```xml
<result>
  <title>Название отчета</title>
  <count>1</count>
  <data>
    <item>
      <id>1</id>
      <name>Room #1</name>
      <student_count>5</student_count>
    </item>
  </data>
</result>
```

## Обработка ошибок

Приложение обрабатывает следующие типы ошибок:
- Отсутствие файлов данных
- Ошибки подключения к базе данных
- Ошибки валидации данных JSON
- Ошибки SQL запросов

## Тестирование

Для тестирования приложения убедитесь, что:
1. PostgreSQL запущен и доступен
2. База данных создана
3. JSON файлы существуют и имеют правильный формат
4. У пользователя есть права на создание таблиц в БД