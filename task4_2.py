from typing import Union

class Hero:
    def __init__(self, name: str, hp: Union[float, int] = 100, attack: Union[float, int] = 1):
        """
        Базовый класс Героя.
        Реализует фундаментальную логику здоровья, атаки и инкапсуляцию данных.

        :param name: Имя героя
        :param hp: Кол-во здоровье (по умолчанию 100)
        :param attack: Наносимый урон героем (по умолчанию 1)

        Также создаётся переменная exp=0.0, lvl=1, которые можно изменять
        """
        # Использование защищенных атрибутов (_) для инкапсуляции.
        # Это предотвращает прямой доступ и несанкционированное изменение состояния объекта.
        self._name = name
        self._hp = hp
        self._max_hp = hp
        self._attack = attack
        self.lvl = 1
        self.exp = 0.0


        if not isinstance(hp, Union[float, int]):
            raise TypeError('Тип данных для здоровья должно быть int или float')
        if hp <= 0:
            raise ValueError('Кол-во здовроье должно быть положительным числом')

        if not isinstance(attack, Union[float, int]):
            raise TypeError('Тип данных для атаки должно быть int или float')
        if attack < 0:
            raise ValueError('Атака не может быть отрицательным числом')


    @property
    def name(self) -> str:
        return self._name

    @property
    def hp(self) -> Union[int, float]:
        return self._hp

    @hp.setter
    def hp(self, value: Union[int, float]) -> None:
        """Сеттер для контроля уровня HP (не ниже 0 и не выше максимума)."""
        if value < 0:
            self._hp = 0
        elif value > self._max_hp:
            self._hp = self._max_hp
        else:
            self._hp = value

    @property
    def attack(self) -> Union[int, float]:
        return self._attack


    def take_damage(self, damage: Union[int, float]) -> str:
        """Метод получения урона"""
        self._hp -= damage
        return f'Герой {self.name} получил {damage} урона, его здоровье на данный момент: {self.hp}'

    def level_up(self, rate: Union[int, float]) -> None:
        """Повышение уровня и характеристик."""
        self._max_hp *= rate
        self._attack *= rate
        self.lvl += 1

    def rest(self) -> str:
        """Базовый метод отдыха: восстанавливает 10 единиц HP."""
        self.hp += 10
        return f'{self.name} отдыхает. HP: {self.hp}'

    def attack_enemy(self, enemy: 'Monster') -> str:
        """Нанесение урона противнику."""
        enemy.hp -= self.attack
        return f"{self.name} атакует {enemy.name} на {self.attack} ед."

    def __str__(self):
        return f"Герой {self.name}: HP={self.hp}, ATK={self.attack}, LVL={self.lvl}, EXP={self.exp}"

    def __repr__(self):
        return f"Hero(name='{self.name}', hp={self.hp}, attack={self.attack})"



class Warrior(Hero):
    """
    Дочерний класс Воина. Специализируется на ближнем бою.
    """
    def __init__(self, name: str, hp: Union[int, float] = 150, attack: Union[int, float] = 15):
        """
        :param name: Имя воина
        :param hp: Кол-во здоровья воина (по умолчанию 150)
        :param attack: Наносимый урон воином (по умолчанию 15)
        """
        # Расширение конструктора базового класса предустановленными значениями
        super().__init__(name, hp, attack)

    def ultra_attack(self, monster: 'Monster') -> str:
        """Уникальный метод: мощная атака."""
        damage = self.attack * 1.5
        monster.hp -= damage
        return f'Вы атаковали {monster.name} суперспособностью на {damage} ед. урона.'

    def take_damage(self, damage: Union[int, float]) -> str:
        """
        ПЕРЕГРУЗКА: Воин носит броню, поэтому получает на 20% меньше урона.
        Обоснование: Классовая особенность для повышения выживаемости танка.
        """
        reduced_damage = damage * 0.8
        return super().take_damage(reduced_damage)

    def __str__(self) -> str:
        return f"Воин {self.name}: HP={self.hp}, ATK={self.attack}, LVL={self.lvl}, EXP={self.exp}"

    def __repr__(self) -> str:
        return f"Warrior(name='{self.name}', hp={self.hp}, attack={self.attack})"


class Priest(Hero):
    """
    Дочерний класс Жреца. Специализируется на лечении.
    """
    def __init__(self, name: str, hp: Union[int, float] = 90, attack: Union[int, float] = 10, heal_power: Union[int, float] = 20):
        """
        :param name: Имя жреца
        :param hp: Кол-во здоровья жреца (по умолчанию 90)
        :param attack: Наносимый урон жрецом (по умолчанию 10)
        :param heal_power: Кол-во hp, которое может восстановить при помощи своей способности (по умолчанию 20)
        """
        super().__init__(name, hp, attack)
        self.heal_power = heal_power

        if not isinstance(heal_power, Union[float, int]):
            raise TypeError('Тип данных для хила должно быть int или float')
        if heal_power <= 0:
            raise ValueError('Хил должен быть положительным числом')

    def cast_heal(self, target: Hero) -> str:
        """Уникальный метод: лечение союзника или себя."""
        target.hp += self.heal_power
        return f'{self.name} вылечил {target.name}, теперь HP: {target.hp}'

    def __str__(self) -> str:
        return f"Жрец {self.name}: HP={self.hp}, ATK={self.attack}, LVL={self.lvl}, EXP={self.exp}"

    def __repr__(self) -> str:
        return f"Priest(name='{self.name}', hp={self.hp}, attack={self.attack}, heal_power={self.heal_power})"




class Monster:
    """
    Класс монстра.
    :param name: Имя монстра
    :param hp: Кол-во здоровья монстра (по умолчанию 100)
    :param attack: Наносимый урон монстром (по умолчанию 5)
    :param exp: Кол-во опыта, получаемый за его убийство (по умолчанию 10)
    """
    def __init__(self, name: str, hp: Union[int, float] = 100, attack: Union[int, float] = 5, exp: Union[int, float] = 10):
        # Использование защищенных атрибутов (_) для инкапсуляции.
        # Это предотвращает прямой доступ и несанкционированное изменение состояния объекта.
        self.name = name
        self._hp = hp
        self.attack = attack
        self.exp = exp

        if not isinstance(hp, Union[float, int]):
            raise TypeError('Тип данных для здоровья должно быть int или float')
        if hp <= 0:
            raise ValueError('Кол-во здовроье должно быть положительным числом')

        if not isinstance(attack, Union[float, int]):
            raise TypeError('Тип данных для атаки должно быть int или float')
        if attack < 0:
            raise ValueError('Атака не может быть отрицательным числом')

        if not isinstance(exp, Union[int, float]):
            raise TypeError('Тип данных для опыта должно быть int или float')
        if exp < 0:
            raise ValueError('Кол-во опыта не может быть отрицательным числом')

    @property
    def hp(self) -> Union[int, float]:
        return self._hp

    @hp.setter
    def hp(self, value: Union[int, float]) -> None:
        self._hp = max(0, value)


    def __str__(self):
        return f"Монстр {self.name}: HP={self.hp}, ATK={self.attack}, EXP={self.exp}"

    def __repr__(self):
        return f"Monster(name='{self.name}', hp={self.hp}, attack={self.attack}, exp={self.exp})"




if __name__ == "__main__":
    # Write your solution here
    warrior = Warrior('Король')
    priest = Priest('Лорд')
    orc = Monster('Орк', 150, 20, 150)

    print(warrior)
    print(warrior.attack_enemy(orc))
    print(warrior.take_damage(orc.attack))
    print(priest.cast_heal(warrior))

    print(orc)
    print(f"Здоровье героя: {warrior.hp}")

