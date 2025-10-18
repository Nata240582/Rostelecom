import subprocess
import sys


def run_tests():
    """Запуск всех тестов"""
    commands = [
        "pytest tests/test_auth.py -v --html=reports/auth_report.html",
        "pytest tests/test_temp_code.py -v --html=reports/temp_code_report.html",
        "pytest tests/test_recovery.py -v --html=reports/recovery_report.html",
        "pytest tests/test_registration.py -v --html=reports/registration_report.html",
        "pytest tests/test_ui_structure.py -v --html=reports/ui_report.html"
        "pytest tests/test_cookie_popup.py -v --html=reports/cookie_popup_report.html"
    ]

    for cmd in commands:
        print(f"\n Запуск: {cmd}")
        result = subprocess.run(cmd, shell=True)
        if result.returncode != 0:
            print(f" Тесты завершились с ошибкой: {cmd}")

    print("\n Все тесты завершены!")


def run_cookie_tests():
    """Запуск только тестов cookie popup"""
    commands = [
        "pytest tests/test_cookie_popup.py -v -s --html=reports/cookie_detailed_report.html"
    ]

    for cmd in commands:
        print(f"\n Запуск тестов Cookie Popup: {cmd}")
        result = subprocess.run(cmd, shell=True)

    print("\n Тесты Cookie Popup завершены!")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "cookie":
        run_cookie_tests()
    else:
        run_tests()