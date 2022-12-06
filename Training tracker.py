from dataclasses import dataclass


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке"""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        """Сохранить информацию о тренировке в читабельном виде"""
        return (f'Тип тренировки: {self.training_type}\n'
                f'Длительность: {self.duration:.3f} ч\n'
                f'Дистанция: {self.distance:.3f} км\n'
                f'Средняя скорость: {self.speed:.3f} км/ч\n'
                f'Потрачено калорий: {self.calories:.3f}\n'
                f'--------------------------------------')


class Training:
    """Общий класс для тренировок"""
    LEN_STEP: float = 0.65
    M_IN_KM: float = 1000
    MINUTES_IN_HOUR: float = 60

    def __init__(self, action: int, duration: float, weight: float) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию, преодоленной за тренировку"""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднее значение скорости на дистанции"""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий"""
        raise NotImplementedError('Method get_spent_calories should be used to subclasses')

    def show_training_info(self) -> InfoMessage:
        """Сохранить информацию о треннировке"""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка по бегу"""
    COEFFICIENT_OF_SPEED: float = 18
    DECREASE_THE_VALUE_OF_SPEED: float = 20

    def get_spent_calories(self):
        """Получить информацию о затраченных калориях на бег"""
        return ((self.COEFFICIENT_OF_SPEED * self.get_mean_speed() - self.DECREASE_THE_VALUE_OF_SPEED)
                * self.weight / self.M_IN_KM * self.MINUTES_IN_HOUR)


class SportsWalking(Training):
    """Тренировка по спортивной хотьбе"""
    FIRST_COEFFICIENT_OF_WEIGHT: float = 0.035
    SECOND_COEFFICIENT_OF_WEIGHT: float = 0.029
    DEGREE_OF_SPEED: float = 2

    def __init__(self, action: int, duration: float, weight: float, height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self):
        """Получить информацию о затраченных калориях на спортивную хотьбу"""
        return ((self.FIRST_COEFFICIENT_OF_WEIGHT * self.weight
                + (self.get_mean_speed() ** self.DEGREE_OF_SPEED // self.height)
                 * self.SECOND_COEFFICIENT_OF_WEIGHT * self.weight) * self.MINUTES_IN_HOUR)


class Swimming(Training):
    """Тренировка по плаванию"""
    INCREASE_THE_VALUE_OF_SPEED: float = 1.1
    THIRD_COEFFICIENT_OF_WEIGHT: float = 2

    def __init__(self, action: int, duration: float, weight: float, length_pool: float, count_pool: float) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить информацию о средней скорости плавания"""
        return self.length_pool * self.count_pool / self.M_IN_KM / self.MINUTES_IN_HOUR

    def get_spent_calories(self):
        """Получить информацию о затраченных калориях на плавание"""
        return (self.get_mean_speed() + self.INCREASE_THE_VALUE_OF_SPEED) * 2 * self.THIRD_COEFFICIENT_OF_WEIGHT


def read_package(training_type: str, info: list) -> Training:
    """Получить данные полученные от датчиков."""
    training_dict = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    if training_type not in training_dict:
        raise ValueError('Данный тип тренировки не поддерживается.')
    return training_dict[training_type](*info)


def main(activity: Training) -> None:
    """Главная функция."""
    info = activity.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
