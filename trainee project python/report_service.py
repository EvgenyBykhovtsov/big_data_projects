"""
Модуль для генерации отчетов
Реализует Command Pattern для различных типов отчетов
"""

from typing import List, Dict, Any
from abc import ABC, abstractmethod
from database import DatabaseRepository


class ReportCommandInterface(ABC):
    """Интерфейс для команд отчетов (Command Pattern)"""
    
    @abstractmethod
    def execute(self) -> List[Dict[str, Any]]:
        pass
    
    @abstractmethod
    def get_title(self) -> str:
        pass


class RoomsWithStudentCountCommand(ReportCommandInterface):
    """Команда для получения списка комнат с количеством студентов"""
    
    def __init__(self, repository: DatabaseRepository):
        self.repository = repository
    
    def execute(self) -> List[Dict[str, Any]]:
        return self.repository.get_rooms_with_student_count()
    
    def get_title(self) -> str:
        return "Список комнат и количество студентов в каждой"


class SmallestAvgAgeRoomsCommand(ReportCommandInterface):
    """Команда для получения 5 комнат с наименьшим средним возрастом"""
    
    def __init__(self, repository: DatabaseRepository, limit: int = 5):
        self.repository = repository
        self.limit = limit
    
    def execute(self) -> List[Dict[str, Any]]:
        return self.repository.get_rooms_with_smallest_avg_age(self.limit)
    
    def get_title(self) -> str:
        return f"{self.limit} комнат с наименьшим средним возрастом студентов"


class LargestAgeDifferenceRoomsCommand(ReportCommandInterface):
    """Команда для получения 5 комнат с наибольшей разницей в возрасте"""
    
    def __init__(self, repository: DatabaseRepository, limit: int = 5):
        self.repository = repository
        self.limit = limit
    
    def execute(self) -> List[Dict[str, Any]]:
        return self.repository.get_rooms_with_largest_age_difference(self.limit)
    
    def get_title(self) -> str:
        return f"{self.limit} комнат с наибольшей разницей в возрасте студентов"


class MixedGenderRoomsCommand(ReportCommandInterface):
    """Команда для получения комнат с разнополыми студентами"""
    
    def __init__(self, repository: DatabaseRepository):
        self.repository = repository
    
    def execute(self) -> List[Dict[str, Any]]:
        return self.repository.get_mixed_gender_rooms()
    
    def get_title(self) -> str:
        return "Список комнат, где живут разнополые студенты"


class ReportService:
    """Сервис для генерации отчетов (Invoker в Command Pattern)"""
    
    def __init__(self, repository: DatabaseRepository):
        self.repository = repository
        self.commands = {
            'rooms_count': RoomsWithStudentCountCommand(repository),
            'smallest_avg_age': SmallestAvgAgeRoomsCommand(repository),
            'largest_age_diff': LargestAgeDifferenceRoomsCommand(repository),
            'mixed_gender': MixedGenderRoomsCommand(repository)
        }
    
    def generate_report(self, report_type: str) -> tuple[List[Dict[str, Any]], str]:
        """Генерирует отчет указанного типа"""
        if report_type not in self.commands:
            raise ValueError(f"Неизвестный тип отчета: {report_type}. Доступные: {list(self.commands.keys())}")
        
        command = self.commands[report_type]
        data = command.execute()
        title = command.get_title()
        
        return data, title
    
    def get_available_reports(self) -> List[str]:
        """Возвращает список доступных отчетов"""
        return list(self.commands.keys())
    
    def generate_all_reports(self) -> Dict[str, tuple[List[Dict[str, Any]], str]]:
        """Генерирует все доступные отчеты"""
        results = {}
        for report_type in self.commands.keys():
            data, title = self.generate_report(report_type)
            results[report_type] = (data, title)
        return results
