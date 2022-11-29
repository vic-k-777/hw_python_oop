class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self, training_type, duration, distance, speed, calories):
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    MIN_IN_H: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        self.distance = self.action * self.LEN_STEP / self.M_IN_KM
        return (self.distance)

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        self.speed = self.get_distance() / self.duration
        return (self.speed)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        info = InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())
        return (info)


class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER = CMSM = 18
    CALORIES_MEAN_SPEED_SHIFT = CMSS = 1.79
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float) -> None:
        super().__init__(action, duration, weight)

    def get_distance(self) -> float:
        return (super().get_distance())

    def get_mean_speed(self) -> float:
        return (super().get_mean_speed())

    def get_spent_calories(self) -> float:
        self.calories = ((self.CMSM
                          * self.get_mean_speed()
                          + self.CMSS)
                         * self.weight / self.M_IN_KM
                         * self.duration * self.MIN_IN_H)
        return (self.calories)

    def show_training_info(self) -> InfoMessage:
        return (super().show_training_info())


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    CALORIES_WEIGHT_MULTIPLIER = CWM = 0.035
    CALORIES_SPEED_HEIGHT_MULTIPLIER = CSHM = 0.029
    CM_IN_M = 100
    KMH_IN_MSEC = 0.278

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_mean_distance(self) -> float:
        return super().get_distance()

    def get_mean_speed(self) -> float:
        return super().get_mean_speed()

    def get_spent_calories(self):
        duration_IN_MIN = self.duration * self.MIN_IN_H
        height_IN_M = self.height / self.CM_IN_M
        speed_IN_MSEC = self.get_mean_speed() * self.KMH_IN_MSEC
        self.calories = ((self.CWM * self.weight
                         + (speed_IN_MSEC**2 / height_IN_M)
                         * self.CSHM * self.weight) * duration_IN_MIN)
        return (self.calories)

    def show_training_info(self) -> InfoMessage:
        return super().show_training_info()


class Swimming(Training):
    """Тренировка: плавание."""
    CALORIES_WEIGHT_MULTIPLIER: float = 2
    CALORIES_MEAN_SPEED: float = 1.1
    LEN_STEP: float = 1.38
    M_IN_KM: int = 1000

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float):
        super().__init__(action,
                         duration,
                         weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_distance(self) -> float:
        return (super().get_distance())

    def get_mean_speed(self):
        return (self.length_pool * self.count_pool / self.M_IN_KM
                / self.duration)

    def get_spent_calories(self):
        spent_calories = ((self.get_mean_speed()
                          + self.CALORIES_MEAN_SPEED)
                          * self.CALORIES_WEIGHT_MULTIPLIER * self.weight
                          * self.duration)
        return (spent_calories)

    def show_training_info(self) -> InfoMessage:
        return super().show_training_info()


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_type = {'SWM': Swimming,
                     'RUN': Running,
                     'WLK': SportsWalking}
    training: Training = training_type[workout_type](*data)
    return (training)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
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
