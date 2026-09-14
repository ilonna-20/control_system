class CrewMember:
    def __init__(self, name):
        self.name = name


class Commander(CrewMember):
    def __init__(self, name):
        super().__init__(name)
        self.is_target_acquired = False

    def aim(self, target):
        print(f"{self.name} прицілюється на {target}.")
        self.is_target_acquired = True


class Gunner(CrewMember):
    def __init__(self, name):
        super().__init__(name)

    def fire(self, weapon, target_acquired):
        if target_acquired:
            print(f"{self.name} відкриває вогонь з {weapon}!")
        else:
            print("Постріл скасовано: ціль не зафіксована.")


class Driver(CrewMember):
    def __init__(self, name):
        super().__init__(name)


class Crew:
    def __init__(self, commander, driver, gunner):
        self.commander = commander
        self.driver = driver
        self.gunner = gunner

    def is_complete(self):
        return (self.commander is not None and
                self.driver is not None and
                self.gunner is not None)


class CrewAssignment:
    def __init__(self):
        self.crew = None

    def assign_crew(self, commander, driver, gunner):
        self.crew = Crew(commander, driver, gunner)
        if self.crew.is_complete():
            print("Екіпаж призначено успішно.")
        else:
            print("Помилка: Екіпаж неповний! Танк не може рухатись або стріляти.")

class FuelTank:
    def __init__(self, max_capacity=1000, min_fuel_for_movement=50):
        self.max_capacity = max_capacity
        self.current_level = max_capacity
        self.min_fuel_for_movement = min_fuel_for_movement

    def refuel(self):
        if self.current_level < self.max_capacity:
            fuel_needed = self.max_capacity - self.current_level
            self.current_level = self.max_capacity
            print(f"Танк заправлений на {fuel_needed} літрів. Поточний рівень пального: {self.current_level} літрів.")
        else:
            print("Танк вже заправлений на повний бак.")

    def display_fuel_level(self):
        print(f"Поточний рівень пального: {self.current_level} літрів (Макс. {self.max_capacity} літрів)")

    def consume(self, speed):
        fuel_consumption = 20 + speed * 0.2
        self.current_level = max(self.current_level - fuel_consumption, 0)
        print(f"Витрачено {fuel_consumption:.1f} л пального. Залишилось: {self.current_level:.1f} л.")
        if self.current_level < self.min_fuel_for_movement:
            print("Попередження: Критично низький рівень пального!")
        return fuel_consumption

class Engine:
    def __init__(self, fuel_tank):
        self.is_on = False
        self.fuel_tank = fuel_tank

    def start(self):
        if self.fuel_tank.current_level > 0:
            self.is_on = True
            print("Двигун увімкнено.")
        else:
            print("Не вистачає пального для запуску двигуна.")

    def stop(self):
        self.is_on = False
        print("Двигун вимкнено.")

    def run(self):
        print("Двигун працює." if self.is_on else "Двигун вимкнений.")


class MovementSystem:
    def __init__(self, engine, fuel_tank):
        self.engine = engine
        self.fuel_tank = fuel_tank
        self.speed = 0
        self.is_moving = False
        self.direction = "вперед"
        self.range_remaining = 0

    def change_speed(self, new_speed):
        if 0 <= new_speed <= 70:
            self.speed = new_speed
            print(f"Швидкість встановлена на {self.speed} км/год.")
        else:
            print("Швидкість повинна бути в межах від 0 до 70 км/год.")

    def choose_direction(self):
        directions = ["вперед", "назад", "вліво", "вправо"]
        print("\nОберіть напрям руху:")
        for i, d in enumerate(directions, 1):
            print(f"{i}. {d}")
        try:
            choice = int(input("Вибір: "))
            if 1 <= choice <= len(directions):
                self.direction = directions[choice - 1]
                print(f"Обрано напрям руху: {self.direction}")
            else:
                print("Невірний вибір.")
        except ValueError:
            print("Невірний ввід.")

    def display_range(self):
        if self.speed > 0:
            self.range_remaining = self.fuel_tank.current_level / (self.speed * 0.2)
        else:
            self.range_remaining = 0
        print(f"Дальність ходу: {self.range_remaining:.1f} км.")

    def move(self):
        if not self.engine.is_on:
            print("Помилка: Двигун не увімкнений. Ввімкніть двигун.")
        elif self.fuel_tank.current_level == 0:
            print("Помилка: Немає пального. Заправте танк.")
        elif self.fuel_tank.current_level < self.fuel_tank.min_fuel_for_movement:
            print(f"Помилка: Недостатньо пального для руху. Мінімум {self.fuel_tank.min_fuel_for_movement} літрів.")
        elif self.speed <= 0:
            print("Помилка: Швидкість має бути більше 0 км/год для руху.")
        else:
            self.is_moving = True
            self.fuel_tank.consume(self.speed)
            self.display_range()
            print(f"Танк рухається з швидкістю {self.speed} км/год.")

    def move_distance(self):
        try:
            distance = float(input("Введіть бажану відстань (км): "))
            if distance <= 0:
                print("Відстань має бути додатньою.")
                return
        except ValueError:
            print("Невірний ввід відстані.")
            return

        required_fuel = 20 + (self.speed * 0.2 * distance)
        if self.fuel_tank.current_level < required_fuel:
            possible_distance = ((self.fuel_tank.current_level - 20) /
                                 (self.speed * 0.2)) if self.fuel_tank.current_level > 20 else 0
            print(f"Недостатньо пального для {distance:.1f} км. Максимальна дистанція: {possible_distance:.1f} км.")
            return

        self.fuel_tank.current_level -= required_fuel
        print(f"Танк проїхав {distance:.1f} км, витратив {required_fuel:.1f} л пального. Залишок пального: {self.fuel_tank.current_level:.1f} л.")
        if self.speed > 0:
            self.range_remaining = self.fuel_tank.current_level / (self.speed * 0.2)
        print(f"Орієнтовно можна проїхати ще {self.range_remaining:.1f} км.")

    def stop(self):
        if self.is_moving:
            self.is_moving = False
            print("Танк зупинився.")
        else:
            print("Танк вже стоїть.")


class WeaponSystem:
    def __init__(self):
        self.selected_weapon = None

    def choose_weapon(self):
        weapons = ["Основна гармата", "Кулемет", "Протитанкова керована ракета"]
        for i, weapon in enumerate(weapons, 1):
            print(f"{i}. {weapon}")
        try:
            choice = int(input("Вибір: "))
            if 1 <= choice <= len(weapons):
                self.selected_weapon = weapons[choice - 1]
                print(f"Озброєння обрано: {self.selected_weapon}")
            else:
                print("Невірний вибір озброєння.")
        except ValueError:
            print("Невірний ввід.")


class TankControlSystem:
    def __init__(self, specifications):
        self.specifications = specifications

    def display_specifications(self):
        print("Технічні характеристики танка:")
        for category, specs in self.specifications.items():
            print(f"{category}: {specs}")


class PowerPlant:
    def run(self):
        print("\nСилова установка:")
        print("- Контролює витрату палива")
        print("- Генерує потужність")
        print("- Охолоджує двигун\n")


class ArmorProtection:
    def run(self):
        print("\nЗахисні системи:")
        print("- Реактивна броня")
        print("- Засоби маскування\n")


class OpticalElectronicSystem:
    def __init__(self):
        self.night_vision_on = False

    def toggle_night_vision(self):
        self.night_vision_on = not self.night_vision_on
        status = "увімкнено" if self.night_vision_on else "вимкнено"
        print(f"Нічне бачення {status}.")

    def run(self):
        print("\nОптико-електронні системи:")
        print("Камери, тепловізори")
        print(f"Нічне бачення: {'Увімкнено' if self.night_vision_on else 'Вимкнено'}\n")


class SystemManager:
    def __init__(self, tank_name, engine, fuel_tank, movement_system,
                 power_plant, weapon_system, armor_protection, control_system,
                 optical_electronic_system):
        self.tank_name = tank_name
        self.engine = engine
        self.fuel_tank = fuel_tank
        self.movement_system = movement_system
        self.power_plant = power_plant
        self.weapon_system = weapon_system
        self.armor_protection = armor_protection
        self.control_system = control_system
        self.optical_electronic_system = optical_electronic_system

    def run_systems(self):
        print(f"\nЗапуск усіх систем для танка {self.tank_name}:")
        if self.engine.is_on and self.fuel_tank.current_level > 0:
            self.movement_system.display_range()
            self.power_plant.run()
            print("\nБойова система:")
            print(f"- Вибране озброєння: {self.weapon_system.selected_weapon}")
            self.armor_protection.run()
            self.control_system.display_specifications()
            self.optical_electronic_system.run()
        else:
            print("Помилка: Двигун вимкнений.")


class CombatControl:
    def __init__(self, crew_assignment, weapon_system):
        self.crew_assignment = crew_assignment
        self.weapon_system = weapon_system

    def aim_and_fire(self):
        if not self.crew_assignment.crew or not self.crew_assignment.crew.is_complete():
            print("Помилка: Екіпаж неповний! Танк не може рухатись або стріляти.")
            return
        if not self.weapon_system.selected_weapon:
            print("Озброєння не вибране!")
            return
        self.crew_assignment.crew.commander.aim("ворожу ціль")
        self.crew_assignment.crew.gunner.fire(
            self.weapon_system.selected_weapon,
            self.crew_assignment.crew.commander.is_target_acquired
        )


class Tank:
    def __init__(self, name):
        self.name = name
        self.fuel_tank = FuelTank(max_capacity=1000, min_fuel_for_movement=50)
        self.engine = Engine(self.fuel_tank)
        self.movement_system = MovementSystem(self.engine, self.fuel_tank)
        self.power_plant = PowerPlant()
        self.weapon_system = WeaponSystem()
        self.armor_protection = ArmorProtection()
        self.specifications = {
            "Максимальна швидкість": "70 км/год",
            "Паливний бак (ємність)": "1000 л",
            "Екіпаж": "3 людини",
            "Озброєння": "Основна гармата, Кулемет, Протитанкова керована ракета",
            "Захисні системи": "Реактивна броня, Засоби маскування",
            "Оптико-електронні системи": "Камери, тепловізори, нічне бачення"
        }
        self.control_system = TankControlSystem(self.specifications)
        self.optical_electronic_system = OpticalElectronicSystem()
        self.crew_assignment = CrewAssignment()
        self.system_manager = SystemManager(
            self.name, self.engine, self.fuel_tank, self.movement_system,
            self.power_plant, self.weapon_system, self.armor_protection,
            self.control_system, self.optical_electronic_system
        )
        self.combat_control = CombatControl(self.crew_assignment, self.weapon_system)

    def diagnostics(self):
        print("\nДіагностика систем:")
        print(f" Двигун: {'Увімкнено' if self.engine.is_on else 'Вимкнено'}")
        print(f" Рух: {'Рухається' if self.movement_system.is_moving else 'Стоїть'}")
        print(f" Поточна швидкість: {self.movement_system.speed} км/год")
        weapon = self.weapon_system.selected_weapon if self.weapon_system.selected_weapon else "Не вибрано"
        print(f" Поточне озброєння: {weapon}")
        print(f" Нічне бачення: {'Увімкнено' if self.optical_electronic_system.night_vision_on else 'Вимкнено'}")
        print(f" Рівень пального: {self.fuel_tank.current_level:.1f} л\n")

    def choose_action(self):
        print("\nЩо зробити з танком?")
        actions = [
            "1. Запустити двигун",
            "2. Зупинити двигун",
            "3. Рухатися",
            "4. Зупинити рух",
            "5. Заправити танк",
            "6. Переглянути рівень пального",
            "7. Переглянути технічні характеристики",
            "8. Переглянути дальність ходу",
            "9. Змінити швидкість",
            "10. Обрати озброєння",
            "11. Увімкнути/Вимкнути нічне бачення",
            "12. Провести діагностику",
            "13. Змінити напрямок",
            "14. Виконати прицілювання і постріл",
            "15. Проїхати задану відстань",
            "16. Запустити всі системи",
            "17. Вийти"
        ]
        for action in actions:
            print(action)

        choice = input("Вибір: ")
        if choice == "1":
            self.engine.start()
        elif choice == "2":
            self.engine.stop()
            self.movement_system.is_moving = False
        elif choice == "3":
            if not self.crew_assignment.crew or not self.crew_assignment.crew.is_complete():
                print("Помилка: Екіпаж неповний! Танк не може рухатись або стріляти.")
            else:
                self.movement_system.move()
        elif choice == "4":
            self.movement_system.stop()
        elif choice == "5":
            self.fuel_tank.refuel()
        elif choice == "6":
            self.fuel_tank.display_fuel_level()
        elif choice == "7":
            self.control_system.display_specifications()
        elif choice == "8":
            self.movement_system.display_range()
        elif choice == "9":
            try:
                new_speed = int(input("Введіть нову швидкість (км/год): "))
                self.movement_system.change_speed(new_speed)
            except ValueError:
                print("Невірний ввід. Введіть ціле число.")
        elif choice == "10":
            self.weapon_system.choose_weapon()
        elif choice == "11":
            self.optical_electronic_system.toggle_night_vision()
        elif choice == "12":
            self.diagnostics()
        elif choice == "13":
            self.movement_system.choose_direction()
        elif choice == "14":
            self.combat_control.aim_and_fire()
        elif choice == "15":
            if not self.crew_assignment.crew or not self.crew_assignment.crew.is_complete():
                print("Помилка: Екіпаж неповний! Танк не може рухатись або стріляти.")
            else:
                self.movement_system.move_distance()
        elif choice == "16":
            self.system_manager.run_systems()
        elif choice == "17":
            print("Вихід з програми.")
            exit()
        else:
            print("Такого вибору немає, введіть число згідно меню.")


if __name__ == "__main__":
    tank = Tank("T-90")
    commander = Commander("Командир Т-90 Ілонна")
    driver = Driver("Водій Т-90")
    gunner = Gunner("Навідник Т-90")
    tank.crew_assignment.assign_crew(commander, driver, gunner)
    while True:
        tank.choose_action()
