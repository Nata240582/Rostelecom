class Config:
    BASE_URL = "https://b2c.passport.rt.ru"
    TIMEOUT = 15

    # Тестовые данные
    TEST_PHONE = "+79103943017"
    TEST_EMAIL = "nata_kozlova254@mail.ru"
    TEST_LOGIN = "rtkid_1234567890123"
    TEST_PASSWORD = "Rfkbyrfvfkbyrf852!"

    # Невалидные данные
    INVALID_PASSWORD = "WrongPassword123"
    SHORT_PASSWORD = "4567"
    CYRILLIC_PASSWORD = "ПриветПароль77"

    # Данные для регистрации
    NEW_NAME = "Иван"
    NEW_LASTNAME = "Иванов"
    NEW_EMAIL = "new_user@mail.ru"
    NEW_PASSWORD = "NewPassword123"