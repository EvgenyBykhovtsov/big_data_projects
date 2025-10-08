"""
Модуль для экспорта данных в различные форматы
Реализует Strategy Pattern для поддержки разных форматов экспорта
"""

import json
import xml.etree.ElementTree as ET
from typing import List, Dict, Any
from abc import ABC, abstractmethod


class ExportStrategyInterface(ABC):
    """Интерфейс для стратегий экспорта (Strategy Pattern)"""
    
    @abstractmethod
    def export(self, data: List[Dict[str, Any]], title: str) -> str:
        pass


class JSONExportStrategy(ExportStrategyInterface):
    """Стратегия экспорта в JSON формат"""
    
    def export(self, data: List[Dict[str, Any]], title: str) -> str:
        """Экспортирует данные в JSON формат"""
        result = {
            "title": title,
            "data": data,
            "count": len(data)
        }
        return json.dumps(result, ensure_ascii=False, indent=2, default=str)


class XMLExportStrategy(ExportStrategyInterface):
    """Стратегия экспорта в XML формат"""
    
    def export(self, data: List[Dict[str, Any]], title: str) -> str:
        """Экспортирует данные в XML формат"""
        root = ET.Element("result")
        
        # Добавляем заголовок
        title_elem = ET.SubElement(root, "title")
        title_elem.text = title
        
        # Добавляем количество записей
        count_elem = ET.SubElement(root, "count")
        count_elem.text = str(len(data))
        
        # Добавляем данные
        data_elem = ET.SubElement(root, "data")
        
        for item in data:
            item_elem = ET.SubElement(data_elem, "item")
            for key, value in item.items():
                field_elem = ET.SubElement(item_elem, key)
                field_elem.text = str(value)
        
        return ET.tostring(root, encoding='unicode', method='xml')


class ExportService:
    """Сервис для экспорта данных (Context в Strategy Pattern)"""
    
    def __init__(self):
        self.strategies = {
            'json': JSONExportStrategy(),
            'xml': XMLExportStrategy()
        }
    
    def export_data(self, data: List[Dict[str, Any]], format_type: str, title: str) -> str:
        """Экспортирует данные в указанном формате"""
        if format_type.lower() not in self.strategies:
            raise ValueError(f"Неподдерживаемый формат: {format_type}. Доступные: {list(self.strategies.keys())}")
        
        strategy = self.strategies[format_type.lower()]
        return strategy.export(data, title)
    
    def save_to_file(self, data: List[Dict[str, Any]], format_type: str, title: str, filename: str) -> None:
        """Сохраняет экспортированные данные в файл"""
        exported_data = self.export_data(data, format_type, title)
        
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(exported_data)
        
        print(f"Данные сохранены в файл: {filename}")
    
    def get_supported_formats(self) -> List[str]:
        """Возвращает список поддерживаемых форматов"""
        return list(self.strategies.keys())
