"""
Главный модуль приложения
Реализует Facade Pattern для упрощения взаимодействия с системой
"""

import argparse
import os
import sys
from typing import Optional

from database import PostgreSQLConnection, DatabaseRepository
from data_loader import JSONDataLoader, DataProcessor
from export_service import ExportService
from report_service import ReportService


class StudentRoomAnalyzer:
    """Фасад для анализа данных студентов и комнат (Facade Pattern)"""
    
    def __init__(self, db_config: dict):
        # Инициализация компонентов системы
        self.db_connection = PostgreSQLConnection(**db_config)
        self.repository = DatabaseRepository(self.db_connection)
        self.data_processor = DataProcessor(JSONDataLoader())
        self.export_service = ExportService()
        self.report_service = ReportService(self.repository)
    
    def setup_database(self) -> None:
        """Создает схему базы данных"""
        schema_file = os.path.join(os.path.dirname(__file__), 'schema.sql')
        if not os.path.exists(schema_file):
            raise FileNotFoundError(f"Файл схемы не найден: {schema_file}")
        
        print("Создание схемы базы данных...")
        self.repository.create_schema(schema_file)
        print("Схема базы данных создана успешно")
    
    def load_data(self, students_file: str, rooms_file: str) -> None:
        """Загружает данные из JSON файлов в базу данных"""
        print("Загрузка данных...")
        
        # Загружаем и валидируем данные комнат
        rooms_data = self.data_processor.load_and_validate_rooms(rooms_file)
        self.repository.insert_rooms(rooms_data)
        
        # Загружаем и валидируем данные студентов
        students_data = self.data_processor.load_and_validate_students(students_file)
        self.repository.insert_students(students_data)
        
        print("Данные загружены успешно")
    
    def generate_and_export_reports(self, output_format: str = 'json') -> None:
        """Генерирует все отчеты и экспортирует их в папку results"""
        print(f"Генерация отчетов в формате {output_format}...")
        
        # Создаем папку results если её нет
        results_dir = self._ensure_results_directory()
        
        reports = self.report_service.generate_all_reports()
        
        for report_type, (data, title) in reports.items():
            filename = os.path.join(results_dir, f"{report_type}.{output_format}")
            self.export_service.save_to_file(data, output_format, title, filename)
            print(f"Отчет '{title}': {len(data)} записей")
    
    def generate_single_report(self, report_type: str, output_format: str = 'json') -> None:
        """Генерирует один конкретный отчет в папку results"""
        print(f"Генерация отчета '{report_type}' в формате {output_format}...")
        
        # Создаем папку results если её нет
        results_dir = self._ensure_results_directory()
        
        data, title = self.report_service.generate_report(report_type)
        filename = os.path.join(results_dir, f"{report_type}.{output_format}")
        self.export_service.save_to_file(data, output_format, title, filename)
        print(f"Отчет '{title}': {len(data)} записей")
    
    def _ensure_results_directory(self) -> str:
        """
        Создает папку results если её нет и возвращает путь к ней.
        
        Returns:
            str: Путь к папке results
        """
        results_dir = "results"
        if not os.path.exists(results_dir):
            os.makedirs(results_dir)
            print(f"Создана папка: {results_dir}")
        return results_dir
    
    def close(self) -> None:
        """Закрывает соединение с базой данных"""
        self.db_connection.close()


def create_argument_parser() -> argparse.ArgumentParser:
    """Создает парсер аргументов командной строки"""
    parser = argparse.ArgumentParser(
        description='Анализатор данных студентов и комнат',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Примеры использования:
  python main.py --students data/students.json --rooms data/rooms.json --format json
  python main.py --students data/students.json --rooms data/rooms.json --format xml --report rooms_count
        """
    )
    
    parser.add_argument(
        '--students',
        required=True,
        help='Путь к файлу с данными студентов (JSON)'
    )
    
    parser.add_argument(
        '--rooms',
        required=True,
        help='Путь к файлу с данными комнат (JSON)'
    )
    
    parser.add_argument(
        '--format',
        choices=['json', 'xml'],
        default='json',
        help='Формат вывода результатов (по умолчанию: json)'
    )
    
    parser.add_argument(
        '--report',
        choices=['rooms_count', 'smallest_avg_age', 'largest_age_diff', 'mixed_gender'],
        help='Тип отчета для генерации (если не указан, генерируются все отчеты)'
    )
    
    parser.add_argument(
        '--db-host',
        default='localhost',
        help='Хост базы данных PostgreSQL (по умолчанию: localhost)'
    )
    
    parser.add_argument(
        '--db-port',
        type=int,
        default=5432,
        help='Порт базы данных PostgreSQL (по умолчанию: 5432)'
    )
    
    parser.add_argument(
        '--db-name',
        default='students_db',
        help='Имя базы данных PostgreSQL (по умолчанию: students_db)'
    )
    
    parser.add_argument(
        '--db-user',
        default='evgenijbyhovcov',
        help='Пользователь базы данных PostgreSQL (по умолчанию: evgenijbyhovcov)'
    )
    
    parser.add_argument(
        '--db-password',
        default='password',
        help='Пароль базы данных PostgreSQL (по умолчанию: password)'
    )
    
    return parser


def main():
    """Главная функция приложения"""
    parser = create_argument_parser()
    args = parser.parse_args()
    
    # Проверяем существование файлов
    if not os.path.exists(args.students):
        print(f"Ошибка: Файл студентов не найден: {args.students}")
        sys.exit(1)
    
    if not os.path.exists(args.rooms):
        print(f"Ошибка: Файл комнат не найден: {args.rooms}")
        sys.exit(1)
    
    # Конфигурация базы данных
    db_config = {
        'host': args.db_host,
        'port': args.db_port,
        'database': args.db_name,
        'user': args.db_user,
        'password': args.db_password
    }
    
    analyzer = None
    try:
        # Создаем анализатор
        analyzer = StudentRoomAnalyzer(db_config)
        
        # Настраиваем базу данных
        analyzer.setup_database()
        
        # Загружаем данные
        analyzer.load_data(args.students, args.rooms)
        
        # Генерируем отчеты
        if args.report:
            analyzer.generate_single_report(args.report, args.format)
        else:
            analyzer.generate_and_export_reports(args.format)
        
        print("Обработка завершена успешно!")
        
    except Exception as e:
        print(f"Ошибка: {e}")
        sys.exit(1)
    
    finally:
        if analyzer:
            analyzer.close()


if __name__ == "__main__":
    main()
