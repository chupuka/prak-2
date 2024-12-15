import json

class Property:
    # недвижимость

    def __init__(self, title, rooms, price, walk_time_to_metro, has_repair):
        self.title = title
        self.rooms = rooms
        self.price = price
        self.walk_time_to_metro = walk_time_to_metro
        self.has_repair = has_repair

    def to_dict(self):
        return {
            'title': self.title,
            'rooms': self.rooms,
            'price': self.price,
            'walk_time_to_metro': self.walk_time_to_metro,
            'has_repair': self.has_repair
        }

class User:
    # пользователь или администратор

    def __init__(self, username, password, is_admin=False):
        self.username = username  # логинчик
        self.password = password  # паролик
        self.is_admin = is_admin  # администратор ли это
        self.purchase_history = []  # это история покупок
        self.cart = []  # это корзина

class RealtyApp:
    # управление пользователями и недвижимостью

    def __init__(self):
        self.properties = []  # это список недвижимости
        self.users = []  # а это список пользователей
        self.current_user = None
        self.load_data()

    def load_data(self):
        try:
            with open('properties.json', 'r') as f:
                properties_data = json.load(f)
                self.properties = [Property(**data) for data in properties_data]
        except FileNotFoundError:
            # Заглушки для недвижимости
            self.properties = [
                Property("Однокомнатная квартира", 1, 30000, 10, True),
                Property("Двухкомнатная квартира", 2, 50000, 5, False),
                Property("Трехкомнатная квартира", 3, 70000, 15, True)
            ]
            print("Файл недвижимости не найден. Используются заглушки.")

        try:
            with open('users.json', 'r') as f:
                users_data = json.load(f)
                self.users = [User(**data) for data in users_data]
        except FileNotFoundError:
            # Заглушки для пользователей
            self.users = [
                User("admin", "admin123", is_admin=True),
                User("user", "user123")
            ]
            print("Файл пользователей не найден. Используются заглушки.")

    def save_data(self):
        with open('properties.json', 'w') as f:
            json.dump([property.to_dict() for property in self.properties], f)

        with open('users.json', 'w') as f:
            json.dump([vars(user) for user in self.users], f)

    def register(self, username, password, is_admin=False):
        if any(user.username == username for user in self.users):
            print("Пользователь уже существует")
            return False

        new_user = User(username, password, is_admin)
        self.users.append(new_user)
        self.save_data()
        print("Регистрация прошла успешно!")
        return True

    def login(self, username, password):
        for user in self.users:
            if user.username == username and user.password == password:
                self.current_user = user
                print("Вы успешно вошли!")
                return True
        print("Неправильное имя пользователя или пароль")
        return False

    def add_property(self, title, rooms, price, walk_time_to_metro, has_repair):
        if self.current_user and self.current_user.is_admin:
            property = Property(title, rooms, price, walk_time_to_metro, has_repair)
            self.properties.append(property)
            self.save_data()
            print("Недвижимость добавлена")
        else:
            print("У вас нет прав для добавления недвижимости")

    def remove_property(self, title):
        if self.current_user and self.current_user.is_admin:
            self.properties = [p for p in self.properties if p.title != title]
            self.save_data()
            print("Недвижимость удалена.")
        else:
            print("У вас нет прав для удаления недвижимости")

    def update_property(self, title, new_data):
        for property in self.properties:
            if property.title == title:
                property.rooms = new_data.get("rooms", property.rooms)
                property.price = new_data.get("price", property.price)
                property.walk_time_to_metro = new_data.get("walk_time_to_metro", property.walk_time_to_metro)
                property.has_repair = new_data.get("has_repair", property.has_repair)
                self.save_data()
                print("Недвижимость обновлена")
                return
        print("Недвижимость не найдена.")

    def view_properties(self):
        if not self.properties:
            print("Нет доступной недвижимости.")
            return

        for property in self.properties:
            print(f"Название: {property.title}, Комнат: {property.rooms}, Стоимость: {property.price}, "
                  f"Время до метро: {property.walk_time_to_metro} мин, Ремонт: {'Да' if property.has_repair else 'Нет'}")

    def filter_properties(self, max_price=None, min_rooms=None):
        filtered_properties = self.properties
        if max_price is not None:
            filtered_properties = filter(lambda p: p.price <= max_price, filtered_properties)
        if min_rooms is not None:
            filtered_properties = filter(lambda p: p.rooms >= min_rooms, filtered_properties)

        for property in filtered_properties:
            print(f"Название: {property.title}, Комнат: {property.rooms}, Стоимость: {property.price}, "
                  f"Время до метро: {property.walk_time_to_metro} мин, Ремонт: {'Да' if property.has_repair else 'Нет'}")

    def add_to_cart(self, title):
        for property in self.properties:
            if property.title == title:
                self.current_user.cart.append(property)
                print(f"{title} добавлено в корзину")
                return
        print("Недвижимость не найдена")

    def view_cart(self):
        if not self.current_user.cart:
            print("Корзина пуста")
            return

        for property in self.current_user.cart:
            print(f"Название: {property.title}, Комнат: {property.rooms}, Стоимость: {property.price}")

    def checkout(self):
        if not self.current_user.cart:
            print("Корзина пуста. Невозможно завершить покупку.")
            return

        self.current_user.purchase_history.extend(self.current_user.cart)
        self.current_user.cart.clear()
        print("Покупка завершена. Спасибо за покупку!")

    def view_purchase_history(self):
        if not self.current_user.purchase_history:
            print("История покупок пуста")
            return

        for property in self.current_user.purchase_history:
            print(f"Покупка: {property.title}, Комнат: {property.rooms}, Стоимость: {property.price}")

    def update_account(self):
        new_password = input("Введите новый пароль: ")
        self.current_user.password = new_password
        self.save_data()
        print("Пароль обновлен")

    def user_menu(self):
        while True:
            print("\n--- Пользовательское меню ---")
            print("1. Просмотреть недвижимость")
            print("2. Фильтровать недвижимость")
            print("3. Добавить в корзину")
            print("4. Просмотреть корзину")
            print("5. Завершить покупку")
            print("6. Просмотреть историю покупок")
            print("7. Обновить учетную запись")
            print("8. Выйти")

            choice = input("Выберите опцию: ")
            if choice == '1':
                self.view_properties()
            elif choice == '2':
                max_price = float(input("Введите максимальную цену (или 0 для пропуска): ")) or None
                min_rooms = int(input("Введите минимальное количество комнат (или 0 для пропуска): ")) or None
                self.filter_properties(max_price, min_rooms)
            elif choice == '3':
                title = input("Введите название недвижимости, которую хотите добавить в корзину: ")
                self.add_to_cart(title)
            elif choice == '4':
                self.view_cart()
            elif choice == '5':
                self.checkout()
            elif choice == '6':
                self.view_purchase_history()
            elif choice == '7':
                self.update_account()
            elif choice == '8':
                self.current_user = None
                break
            else:
                print("Неверный выбор. Пожалуйста, попробуйте снова.")

    def admin_menu(self):
        while True:
            print("\n--- Меню администратора ---")
            print("1. Добавить недвижимость")
            print("2. Удалить недвижимость")
            print("3. Обновить недвижимость")
            print("4. Просмотреть пользователей")
            print("5. Управлять пользователями")
            print("6. Выйти")

            choice = input("Выберите опцию: ")
            if choice == '1':
                title = input("Введите название недвижимости: ")
                rooms = int(input("Введите количество комнат: "))
                price = float(input("Введите стоимость: "))
                walk_time_to_metro = int(input("Введите время до метро (в минутах): "))
                has_repair = input("Есть ли ремонт? (1 - да/2 - нет): ").lower() == '1'
                self.add_property(title, rooms, price, walk_time_to_metro, has_repair)
            elif choice == '2':
                title = input("Введите название недвижимости для удаления: ")
                self.remove_property(title)
            elif choice == '3':
                title = input("Введите название недвижимости для обновления: ")
                new_rooms = int(input("Введите новое количество комнат (или 0 для пропуска): ")) or None
                new_price = float(input("Введите новую цену (или 0 для пропуска): ")) or None
                new_walk_time_to_metro = int(input("Введите новое время до метро (или 0 для пропуска): ")) or None
                new_has_repair = input("Новый ремонт? (1 - да/2 - нет или оставьте пустым): ").lower() == '1' if input(
                    "Новый ремонт? (1 - да/2 - нет или оставьте пустым): ") else None

                new_data = {
                    'rooms': new_rooms,
                    'price': new_price,
                    'walk_time_to_metro': new_walk_time_to_metro,
                    'has_repair': new_has_repair
                }
                self.update_property(title, new_data)
            elif choice == '4':
                self.view_users()
            elif choice == '5':
                self.manage_users()
            elif choice == '6':
                break
            else:
                print("Неверный выбор. Пожалуйста, попробуйте снова.")

    def view_users(self):
        if not self.users:
            print("Нет зарегистрированных пользователей.")
            return

        for user in self.users:
            print(f"Имя пользователя: {user.username}, Администратор: {'Да' if user.is_admin else 'Нет'}")

    def manage_users(self):
        while True:
            print("\n--- Управление пользователями ---")
            print("1. Добавить пользователя")
            print("2. Удалить пользователя")
            print("3. Обновить данные пользователя")
            print("4. Выйти")

            choice = input("Выберите опцию: ")
            if choice == '1':
                username = input("Введите имя нового пользователя: ")
                password = input("Введите пароль нового пользователя: ")
                is_admin = input("Является ли администратором? (1 - да/2 - нет): ").lower() == '1'
                self.register(username, password, is_admin)
            elif choice == '2':
                username = input("Введите имя пользователя для удаления: ")
                self.users = [user for user in self.users if user.username != username]
                self.save_data()
                print("Пользователь удален.")
            elif choice == '3':
                username = input("Введите имя пользователя для обновления: ")
                for user in self.users:
                    if user.username == username:
                        new_password = input("Введите новый пароль (или оставьте пустым для пропуска): ")
                        if new_password:
                            user.password = new_password
                        print("Данные пользователя обновлены.")
                        self.save_data()
                        return
                print("Пользователь не найден.")
            elif choice == '4':
                break
            else:
                print("Неверный выбор. Пожалуйста, попробуйте снова.")

    def main_menu(self):
        while True:
            print("\n--- Главное меню ---")
            print("1. Регистрация")
            print("2. Вход")
            print("3. Выход")

            choice = input("Выберите опцию: ")
            if choice == '1':
                username = input("Введите имя пользователя: ")
                password = input("Введите пароль: ")
                is_admin = input("Является ли администратором? (1 - да/2 - нет): ").lower() == '1'
                self.register(username, password, is_admin)
            elif choice == '2':
                username = input("Введите имя пользователя: ")
                password = input("Введите пароль: ")
                if self.login(username, password):
                    if self.current_user.is_admin:
                        self.admin_menu()
                    else:
                        self.user_menu()
            elif choice == '3':
                print("Выход из приложения...")
                break
            else:
                print("Неверный выбор. Пожалуйста, попробуйте снова.")

if __name__ == "__main__":
    app = RealtyApp()
    app.main_menu()