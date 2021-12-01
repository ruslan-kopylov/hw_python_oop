class InfoMessage:
    def __init__(self,
                 training_type,
                 duration,
                 distance,
                 speed,
                 calories,
                 ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self):
        """Информационное сообщение о тренировке."""
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {"%.3f" % self.duration}; '
                f'Дистанция: {"%.3f" % self.distance}; '
                f'Скорость: {"%.3f" % self.speed}; '
                f'Потрачено ккал: {"%.3f" % self.calories}.')


class Training:
    """Базовый класс тренировки."""
    M_IN_KM: int = 1000
    LEN_STEP: float = 0.65

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
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""

        pass

    def show_training_info(self) -> InfoMessage:
        message = InfoMessage(training, self.duration,
                              self.get_distance(), self.get_mean_speed(),
                              self.get_spent_calories())
        """Вернуть информационное сообщение о выполненной тренировке."""
        return message.get_message()


class Running(Training):
    """Тренировка: бег."""
    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        super().__init__(action, duration, weight)

    def __str__(self) -> str:
        return 'Running'

    def get_spent_calories(self) -> float:
        run_kof_1 = 18
        run_kof_2 = 20
        return ((run_kof_1 * self.get_mean_speed() - run_kof_2)
                * self.weight / self.M_IN_KM * (self.duration * 60))


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def __str__(self) -> str:
        return 'SportsWalking'

    def get_spent_calories(self) -> float:
        walk_kof_1 = 0.035
        walk_kof_2 = 0.029
        return ((walk_kof_1 * self.weight
                + (self.get_mean_speed() ** 2
                 // self.height) * walk_kof_2
                * self.weight) * (self.duration * 60))


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: int,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.count_pool = count_pool
        self.length_pool = length_pool

    def __str__(self) -> str:
        return 'Swimming'

    def get_mean_speed(self) -> float:
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        return (self.get_mean_speed() + 1.1) * 2 * self.weight


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    workouts = {'SWM': Swimming,
                'RUN': Running,
                'WLK': SportsWalking}
    return workouts[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info)


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
