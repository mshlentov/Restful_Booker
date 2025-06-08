import pytest
import requests

from constants import BASE_URL

class TestBookings:

    def test_create_booking(self, auth_session, booking_data):
        # Создаём бронирование
        create_booking = auth_session.post(f"{BASE_URL}/booking", json=booking_data)
        assert create_booking.status_code == 200, "Ошибка при создании брони"

        booking_id = create_booking.json().get("bookingid")
        assert booking_id is not None, "Идентификатор брони не найден в ответе"
        assert create_booking.json()["booking"]["firstname"] == booking_data["firstname"], "Заданное имя не совпадает"
        assert create_booking.json()["booking"]["totalprice"] == booking_data["totalprice"], "Заданная стоимость не совпадает"

        # Проверяем, что бронирование можно получить по ID
        get_booking = auth_session.get(f"{BASE_URL}/booking/{booking_id}")
        assert get_booking.status_code == 200, "Бронь не найдена"
        assert get_booking.json()["lastname"] == booking_data["lastname"], "Заданная фамилия не совпадает"

        # Удаляем бронирование
        deleted_booking = auth_session.delete(f"{BASE_URL}/booking/{booking_id}")
        assert deleted_booking.status_code == 201, "Бронь не удалилась"

        # Проверяем, что бронирование больше недоступно
        get_booking = auth_session.get(f"{BASE_URL}/booking/{booking_id}")
        assert get_booking.status_code == 404, "Бронь не удалилась"


    def test_full_update_booking(self, auth_session, booking_data, update_booking_data):
        # Создаём бронирование
        create_booking = auth_session.post(f"{BASE_URL}/booking", json=booking_data)
        assert create_booking.status_code == 200, "Ошибка при создании брони"

        #Сохраняем ID созданной записи
        booking_id = create_booking.json().get("bookingid")

        # Обновляем данные для созданного бронирования
        update_booking = auth_session.put(f"{BASE_URL}/booking/{booking_id}", json=update_booking_data)
        assert update_booking.status_code == 200, "Ошибка при изменение брони"

        # Получаем бронирование
        get_booking = auth_session.get(f"{BASE_URL}/booking/{booking_id}")

        # Проверяем, что данные обновились
        assert get_booking.json()["firstname"] == update_booking_data["firstname"], "Заданное имя не совпадает"
        assert get_booking.json()["lastname"] == update_booking_data["lastname"], "Заданная фамилия не совпадает"
        assert get_booking.json()["totalprice"] == update_booking_data["totalprice"], "Заданная стоимость не совпадает"


    def test_partial_update_booking(self, auth_session, booking_data, partial_update_booking_data):
        # Создаём бронирование
        create_booking = auth_session.post(f"{BASE_URL}/booking", json=booking_data)
        assert create_booking.status_code == 200, "Ошибка при создании брони"

        # Сохраняем ID созданной записи
        booking_id = create_booking.json().get("bookingid")

        # Частично обновляем данные для созданного бронирования
        update_booking = auth_session.patch(f"{BASE_URL}/booking/{booking_id}", json=partial_update_booking_data)
        assert update_booking.status_code == 200, "Ошибка при частичном изменение брони"

        # Получаем бронирование
        get_booking = auth_session.get(f"{BASE_URL}/booking/{booking_id}")

        # Проверяем, что данные частично обновились
        assert get_booking.json()["firstname"] == partial_update_booking_data["firstname"], "Заданное имя не совпадает"
        assert get_booking.json()["lastname"] == partial_update_booking_data["lastname"], "Заданная фамилия не совпадает"

        # Проверяем, что другие данные не изменились
        assert get_booking.json()["totalprice"] == booking_data["totalprice"], "Заданная стоимость не совпадает"


    def test_negative_get_booking(self, auth_session):
        # Сохраняем ID несуществующей записи
        booking_id = 0

        # Пытаемся получить несуществующее бронирование
        get_booking = auth_session.get(f"{BASE_URL}/booking/{booking_id}")

        # Проверяем, что возвращается 404 ошибка
        assert get_booking.status_code == 404, "Некорректное поведение системы при запросе не существующей записи"


    def test_negative_partial_update_booking(self, auth_session, booking_data, partial_update_booking_data):
        # Создаём бронирование
        create_booking = auth_session.post(f"{BASE_URL}/booking", json=booking_data)
        assert create_booking.status_code == 200, "Ошибка при создании брони"

        # Сохраняем ID созданной записи
        booking_id = create_booking.json().get("bookingid")

        # Частично обновляем данные для созданного бронирования, НО без авторизации
        update_booking = requests.patch(f"{BASE_URL}/booking/{booking_id}", json=partial_update_booking_data)
        assert update_booking.status_code == 403, "Отсутствует ошибка 403 при изменение бронирования без авторизации"

        # Получаем бронирование
        get_booking = auth_session.get(f"{BASE_URL}/booking/{booking_id}")

        # Проверяем что данные не изменились
        assert get_booking.json()["firstname"] == booking_data["firstname"], "Заданное имя не совпадает"
        assert get_booking.json()["lastname"] == booking_data["lastname"], "Заданная фамилия не совпадает"

    def test_negative_create_booking(self, auth_session, partial_update_booking_data):
        # Пытаемся создать бронирование, где в качестве данных передаются не все обязательные поля
        create_booking = auth_session.post(f"{BASE_URL}/booking", json=partial_update_booking_data)
        assert create_booking.status_code == 500, "Ошибка при валидации обязательных полей"










