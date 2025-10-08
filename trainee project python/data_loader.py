"""
Модуль для загрузки данных из JSON файлов
Реализует Single Responsibility Principle - отвечает только за загрузку данных
"""

import json
from typing import List, Dict, Any
from abc import ABC, abstractmethod


class DataLoaderInterface(ABC):
    """Интерфейс для загрузки данных (Interface Segregation Principle)"""
    
    @abstractmethod
    def load_data(self, file_path: str) -> List[Dict[str, Any]]:
        pass


class JSONDataLoader(DataLoaderInterface):
    """Конкретная реализация загрузчика JSON данных"""
    
    def load_data(self, file_path: str) -> List[Dict[str, Any]]:
        """Загружает данные из JSON файла"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                
            if not isinstance(data, list):
                raise ValueError(f"Ожидался список в файле {file_path}")
                
            return data
            
        except FileNotFoundError:
            raise FileNotFoundError(f"Файл {file_path} не найден")
        except json.JSONDecodeError as e:
            raise ValueError(f"Ошибка парсинга JSON в файле {file_path}: {e}")
        except Exception as e:
            raise Exception(f"Ошибка при загрузке файла {file_path}: {e}")


class DataValidator:
    """Класс для валидации данных (Single Responsibility Principle)"""
    
    @staticmethod
    def validate_room_data(room: Dict[str, Any]) -> bool:
        """Валидирует данные комнаты"""
        required_fields = ['id', 'name']
        
        for field in required_fields:
            if field not in room:
                raise ValueError(f"Отсутствует обязательное поле '{field}' в данных комнаты")
        
        if not isinstance(room['id'], int):
            raise ValueError("Поле 'id' должно быть целым числом")
        
        if not isinstance(room['name'], str) or not room['name'].strip():
            raise ValueError("Поле 'name' должно быть непустой строкой")
        
        return True
    
    @staticmethod
    def validate_student_data(student: Dict[str, Any]) -> bool:
        """Валидирует данные студента"""
        required_fields = ['id', 'name', 'birthday', 'room', 'sex']
        
        for field in required_fields:
            if field not in student:
                raise ValueError(f"Отсутствует обязательное поле '{field}' в данных студента")
        
        if not isinstance(student['id'], int):
            raise ValueError("Поле 'id' должно быть целым числом")
        
        if not isinstance(student['name'], str) or not student['name'].strip():
            raise ValueError("Поле 'name' должно быть непустой строкой")
        
        if not isinstance(student['room'], int):
            raise ValueError("Поле 'room' должно быть целым числом")
        
        if student['sex'] not in ['M', 'F']:
            raise ValueError("Поле 'sex' должно быть 'M' или 'F'")
        
        # Проверяем формат даты
        if not isinstance(student['birthday'], str):
            raise ValueError("Поле 'birthday' должно быть строкой")
        
        return True


class DataProcessor:
    """Класс для обработки и подготовки данных (Single Responsibility Principle)"""
    
    def __init__(self, data_loader: DataLoaderInterface):
        self.data_loader = data_loader
        self.validator = DataValidator()
    
    def load_and_validate_rooms(self, file_path: str) -> List[Dict[str, Any]]:
        """Загружает и валидирует данные комнат"""
        rooms_data = self.data_loader.load_data(file_path)
        
        for room in rooms_data:
            self.validator.validate_room_data(room)
        
        print(f"Загружено и проверено {len(rooms_data)} комнат")
        return rooms_data
    
    def load_and_validate_students(self, file_path: str) -> List[Dict[str, Any]]:
        """Загружает и валидирует данные студентов"""
        students_data = self.data_loader.load_data(file_path)
        
        for student in students_data:
            self.validator.validate_student_data(student)
        
        print(f"Загружено и проверено {len(students_data)} студентов")
        return students_data
