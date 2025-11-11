# run_tests.py
import subprocess
import sys
import os
from datetime import datetime


def run_tests_with_html_report():
    """Запускает тесты и генерирует HTML отчет"""

    # Создаем папку для отчетов
    reports_dir = "reports"
    os.makedirs(reports_dir, exist_ok=True)

    # Генерируем имя файла с timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = os.path.join(reports_dir, f"test_report_{timestamp}.html")

    # Команда для запуска pytest
    cmd = [
        sys.executable, "-m", "pytest",
        "test_bot.py",  # ваш файл с тестами
        f"--html={report_file}",
        "--self-contained-html",  # все в одном файле
        "-v",  # подробный вывод
        "--tb=short"  # короткие tracebacks
    ]

    print("🚀 Запуск тестов с генерацией HTML отчета...")
    print(f"📊 Отчет будет сохранен в: {report_file}")
    print("=" * 50)

    # Запускаем тесты
    result = subprocess.run(cmd, capture_output=True, text=True)

    # Выводим результат в консоль
    print(result.stdout)
    if result.stderr:
        print("Ошибки:", result.stderr)

    print("=" * 50)
    print(f"📁 HTML отчет: {report_file}")

    if result.returncode == 0:
        print("✅ Все тесты прошли успешно!")
    else:
        print(f"❌ Некоторые тесты не прошли (код: {result.returncode})")

    return result.returncode, report_file


if __name__ == "__main__":
    exit_code, report_path = run_tests_with_html_report()

    # Автоматически открываем отчет в браузере
    try:
        import webbrowser

        webbrowser.open(f"file://{os.path.abspath(report_path)}")
        print(f"🌐 Отчет открыт в браузере: {report_path}")
    except Exception as e:
        print(f"⚠️ Не удалось открыть отчет в браузере: {e}")

    sys.exit(exit_code)