from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time


def diagnose_site():
    print("=== ДИАГНОСТИКА САЙТА РОСТЕЛЕКОМ ===")

    chrome_options = Options()
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")

    driver = webdriver.Chrome(options=chrome_options)

    urls_to_test = [
        "https://b2c.passport.rt.ru",
        "https://lk.rt.ru",
        "https://start.rt.ru"
    ]

    for url in urls_to_test:
        print(f"\n Тестируем URL: {url}")
        try:
            driver.get(url)
            time.sleep(5)

            print(f" Заголовок: {driver.title}")
            print(f" Текущий URL: {driver.current_url}")

            # Поиск всех элементов
            print("\n Поиск элементов:")

            # Поля ввода
            inputs = driver.find_elements(By.TAG_NAME, "input")
            print(f" Найдено полей ввода: {len(inputs)}")
            for i, inp in enumerate(inputs):
                inp_id = inp.get_attribute("id") or "нет id"
                inp_name = inp.get_attribute("name") or "нет name"
                inp_type = inp.get_attribute("type") or "нет type"
                inp_placeholder = inp.get_attribute("placeholder") or "нет placeholder"
                print(
                    f"  {i + 1}. id='{inp_id}', name='{inp_name}', type='{inp_type}', placeholder='{inp_placeholder}'")

            # Кнопки
            buttons = driver.find_elements(By.TAG_NAME, "button")
            print(f" Найдено кнопок: {len(buttons)}")
            for i, btn in enumerate(buttons):
                btn_id = btn.get_attribute("id") or "нет id"
                btn_text = btn.text.replace('\n', ' ')[:50] or "нет текста"
                print(f"  {i + 1}. id='{btn_id}', text='{btn_text}'")

            # Ссылки
            links = driver.find_elements(By.TAG_NAME, "a")
            important_links = [link for link in links if
                               any(x in link.text.lower() for x in ['забыл', 'восстан', 'регистр', 'войти'])]
            print(f"🔗 Найдено важных ссылок: {len(important_links)}")
            for i, link in enumerate(important_links):
                link_id = link.get_attribute("id") or "нет id"
                link_text = link.text.replace('\n', ' ')[:30] or "нет текста"
                print(f"  {i + 1}. id='{link_id}', text='{link_text}'")

            # Табы
            tabs = driver.find_elements(By.CSS_SELECTOR, "[class*='tab'], [id*='tab']")
            print(f"📑 Найдено табов: {len(tabs)}")
            for i, tab in enumerate(tabs):
                tab_id = tab.get_attribute("id") or "нет id"
                tab_text = tab.text.replace('\n', ' ')[:20] or "нет текста"
                tab_class = tab.get_attribute("class")
                print(f"  {i + 1}. id='{tab_id}', text='{tab_text}', class='{tab_class}'")

            # Делаем скриншот
            driver.save_screenshot(f"diagnostic_{url.split('//')[1].split('/')[0]}.png")
            print(f"Скриншот сохранен: diagnostic_{url.split('//')[1].split('/')[0]}.png")

        except Exception as e:
            print(f" Ошибка: {e}")

    driver.quit()
    print("\n Диагностика завершена!")


if __name__ == "__main__":
    diagnose_site()