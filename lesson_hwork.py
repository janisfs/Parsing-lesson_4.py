from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
import time


def search_wikipedia(query):
    browser = webdriver.Chrome()
    browser.get("https://ru.wikipedia.org")

    search_box = browser.find_element(By.ID, "searchInput")
    search_box.send_keys(query)
    search_box.send_keys(Keys.RETURN)
    time.sleep(2)  # Ждем, пока страница загрузится полностью

    return browser


def print_paragraphs(browser):
    paragraphs = browser.find_elements(By.TAG_NAME, "p")
    for i, p in enumerate(paragraphs):
        print(f"Параграф {i+1}: {p.text[:100]}...")  # Печатаем первые 100 символов каждого параграфа


def get_internal_links(browser):
    links = browser.find_elements(By.XPATH, "//a[@href]")
    internal_links = []
    for link in links:
        href = link.get_attribute("href")
        if "wikipedia.org" in href and not href.startswith("#"):
            internal_links.append(href)
    return internal_links


def main():
    query = input("Введите запрос для поиска в Википедии: ")
    browser = search_wikipedia(query)

    while True:
        action = input("Выберите действие: (1) Листать параграфы, (2) Перейти на связанную страницу, (3) Выйти: ")
        if action == '1':
            print_paragraphs(browser)
        elif action == '2':
            internal_links = get_internal_links(browser)
            if internal_links:
                print("Ссылки на связанные страницы:")
                for i, link in enumerate(internal_links):
                    print(f"{i+1}. {link}")
                choice = int(input("Введите номер ссылки для перехода: "))
                if 1 <= choice <= len(internal_links):
                    browser.get(internal_links[choice-1])
                    time.sleep(2)  # Ждем, пока страница загрузится полностью
                else:
                    print("Неверный номер ссылки.")
            else:
                print("Связанных страниц не найдено.")
        elif action == '3':
            break
        else:
            print("Неверный выбор. Пожалуйста, выберите снова.")

    browser.quit()


if __name__ == "__main__":
    main()
