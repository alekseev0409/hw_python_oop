from dataclasses import dataclass
from typing import Type


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str # название тренировки
    duration: float # длительность
    distance: float # дистанция
    speed: float # скорость
    calories: float # калории

    def get_message(self) -> str:
        """Возвращает строку с результатами тренировки."""

        return  (f'Тип тренировки: {self.training_type};'
                 f'Длительность: {self.duration:.3f} ч.;'
                 f'Дистанция: {self.distance:.3f} км; '
                 f'Ср. скорость: {self.speed:.3f} км/ч;'
                 f'Потрачено ккал: {self.calories:.3f}.')

class Training:
    """Базовый класс тренировки."""

    LEN_STEP: float = 0.65 # расстояние за один шаг
    M_IN_KM: float = 1000 # перевод - метров в одном км
    MIN_IN_H: float = 60.0 # перевод - минут в одном часе

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action: int = action # кол-во совершенных действий
        self.duration: float = duration # длительность тренировки в часах
        self.weight: float = weight # вес спортсмена

    def get_distance(self) -> float:
        """Получить дистанцию в км."""

        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""

        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(type(self).__name__, self.duration,
                           self.get_distance(), self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER: float = 18
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""

        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER * self.get_mean_speed()
                 + self.CALORIES_MEAN_SPEED_SHIFT) * self.weight
                / self.M_IN_KM * self.duration * self.MIN_IN_H)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    CALORIES_WEIGHT_MULTIPLIER: float = 0.035
    CALORIES_SPEED_HEIGHT_MULTIPLIER: float = 0.029
    CM_IN_M: float = 100.0 # перевод - см в одном метре
    KMH_IN_MSEC: float = 0.278 # перевод - км/ч в м/с


    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float,
                 ) -> None:
        super().__init__(action, duration, weight) # использовали конструктор из класса родителя

        self.height: float = height # рост в метрах

    def get_spent_calories(self) -> float:
        # """Получить количество затраченных калорий."""

        speed_kmh_in_msec = self.get_mean_speed() * self.KMH_IN_MSEC
        height_m = self.height / self.CM_IN_M

        return (self.CALORIES_WEIGHT_MULTIPLIER * self.weight +
               (speed_kmh_in_msec ** 2 / height_m) *
                self.CALORIES_SPEED_HEIGHT_MULTIPLIER * self.weight) * self.duration * self.MIN_IN_H


class Swimming(Training):
    """Тренировка: плавание."""
    COEFF_SPEED: float = 1.1
    COEFF_WEIGHT: float = 2
    LEN_STEP: float = 1.38 # расстояние, преодолеваемое за один гребок

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool_m: float = length_pool # длина бассейна в метрах
        self.count_pool_qty: float = count_pool # сколько раз пользователь переплыл бассейн

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        
        return self.length_pool_m * self.count_pool_qty / self.M_IN_KM / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""

        return ((self.get_mean_speed() + self.COEFF_SPEED)
                * self.COEFF_WEIGHT * self.weight * self.duration)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    dict_training: dict[str, Type[Training]] = {'RUN': Running,
                                                'SWM': Swimming,
                                                'WLK': SportsWalking,
                                                }
    return dict_training[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    print(training.show_training_info().get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)

