"""
Модуль для работы с базой данных PostgreSQL
Реализует паттерн Repository для работы с данными
"""

import psycopg2
from typing import List, Dict, Any, Optional
from abc import ABC, abstractmethod


class DatabaseConnectionInterface(ABC):
    """Интерфейс для подключения к базе данных (Interface Segregation Principle)"""
    
    @abstractmethod
    def connect(self) -> Any:
        pass
    
    @abstractmethod
    def execute_query(self, query: str, params: tuple = None) -> List[Dict]:
        pass
    
    @abstractmethod
    def execute_script(self, script: str) -> None:
        pass
    
    @abstractmethod
    def close(self) -> None:
        pass


class PostgreSQLConnection(DatabaseConnectionInterface):
    """Конкретная реализация подключения к PostgreSQL"""
    
    def __init__(self, host: str, database: str, user: str, password: str, port: int = 5432):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.port = port
        self.connection = None
    
    def connect(self) -> psycopg2.extensions.connection:
        """Устанавливает соединение с базой данных"""
        if self.connection is None or self.connection.closed:
            self.connection = psycopg2.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password,
                port=self.port
            )
        return self.connection
    
    def execute_query(self, query: str, params: tuple = None) -> List[Dict]:
        """Выполняет SQL запрос и возвращает результат"""
        connection = self.connect()
        cursor = connection.cursor()
        
        try:
            cursor.execute(query, params)
            
            # Если есть результат (SELECT запрос)
            if cursor.description:
                columns = [desc[0] for desc in cursor.description]
                rows = cursor.fetchall()
                return [dict(zip(columns, row)) for row in rows]
            else:
                # Для INSERT, UPDATE, DELETE
                connection.commit()
                return []
                
        except Exception as e:
            connection.rollback()
            raise e
        finally:
            cursor.close()
    
    def execute_script(self, script: str) -> None:
        """Выполняет SQL скрипт"""
        connection = self.connect()
        cursor = connection.cursor()
        
        try:
            cursor.execute(script)
            connection.commit()
        except Exception as e:
            connection.rollback()
            raise e
        finally:
            cursor.close()
    
    def close(self) -> None:
        """Закрывает соединение с базой данных"""
        if self.connection and not self.connection.closed:
            self.connection.close()


class DatabaseRepository:
    """Repository для работы с данными студентов и комнат"""
    
    def __init__(self, db_connection: DatabaseConnectionInterface):
        self.db = db_connection
    
    def create_schema(self, schema_file: str) -> None:
        """Создает схему базы данных из SQL файла"""
        with open(schema_file, 'r', encoding='utf-8') as file:
            schema_script = file.read()
        self.db.execute_script(schema_script)
    
    def insert_rooms(self, rooms_data: List[Dict]) -> None:
        """Вставляет данные комнат в базу данных"""
        for room in rooms_data:
            query = "INSERT INTO rooms (id, name) VALUES (%s, %s) ON CONFLICT (id) DO NOTHING"
            self.db.execute_query(query, (room['id'], room['name']))
    
    def insert_students(self, students_data: List[Dict]) -> None:
        """Вставляет данные студентов в базу данных"""
        for student in students_data:
            query = """
            INSERT INTO students (id, name, birthday, room, sex) 
            VALUES (%s, %s, %s, %s, %s) 
            ON CONFLICT (id) DO NOTHING
            """
            self.db.execute_query(query, (
                student['id'],
                student['name'],
                student['birthday'],
                student['room'],
                student['sex']
            ))
    
    def get_rooms_with_student_count(self) -> List[Dict]:
        """Получает список комнат и количество студентов в каждой"""
        query = """
        SELECT 
            r.id,
            r.name,
            COUNT(s.id) as student_count
        FROM rooms r
        LEFT JOIN students s ON r.id = s.room
        GROUP BY r.id, r.name
        ORDER BY r.id
        """
        return self.db.execute_query(query)
    
    def get_rooms_with_smallest_avg_age(self, limit: int = 5) -> List[Dict]:
        """Получает 5 комнат с наименьшим средним возрастом студентов"""
        query = """
        SELECT 
            r.id,
            r.name,
            ROUND(AVG(EXTRACT(YEAR FROM AGE(CURRENT_DATE, s.birthday))), 2) as avg_age
        FROM rooms r
        INNER JOIN students s ON r.id = s.room
        GROUP BY r.id, r.name
        HAVING COUNT(s.id) > 0
        ORDER BY avg_age ASC
        LIMIT %s
        """
        return self.db.execute_query(query, (limit,))
    
    def get_rooms_with_largest_age_difference(self, limit: int = 5) -> List[Dict]:
        """Получает 5 комнат с наибольшей разницей в возрасте студентов"""
        query = """
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
        LIMIT %s
        """
        return self.db.execute_query(query, (limit,))
    
    def get_mixed_gender_rooms(self) -> List[Dict]:
        """Получает список комнат, где живут студенты разного пола"""
        query = """
        SELECT 
            r.id,
            r.name,
            COUNT(DISTINCT s.sex) as gender_count
        FROM rooms r
        INNER JOIN students s ON r.id = s.room
        GROUP BY r.id, r.name
        HAVING COUNT(DISTINCT s.sex) > 1
        ORDER BY r.id
        """
        return self.db.execute_query(query)
