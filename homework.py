class InfoMessage:
    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float,
                 ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def show_training_info(self) -> None:
        """Информационное сообщение о тренировке."""
        print(f'Тип тренировки:{self.training_type};'
              'Длительность: {self.duration};'
              'Дистанция: {round(self.distance, 3)};'
              'Скорость: ' + round(self.speed, 3) + ';'
              'Потрачено ккал: {self.calories}.')


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
        distance = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        mean_speed = self.get_distance(self.action) / self.duration
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""

        pass

    def show_training_info(self) -> InfoMessage:
        return InfoMessage.show_training_info()
        """Вернуть информационное сообщение о выполненной тренировке."""
        pass


pass


class Running(Training):
    """Тренировка: бег."""
    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        run_kof_1 = 18
        run_kof_2 = 20
        spent_calories = ((run_kof_1 * self.get_mean_speed() - run_kof_2)
                          * self.weight / self.M_IN_KM * self.duration)
        return spent_calories


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

    def get_spent_calories(self) -> float:
        walk_kof_1 = 0.035
        walk_kof_2 = 0.029
        spent_calories = ((walk_kof_1 * self.weight + (self.get_mean_speed**2
                          // self.height) * walk_kof_2
                          * self.weight) * self.duration)
        return spent_calories


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

    def get_mean_speed(self) -> float:
        mean_speed = (self.length_pool * self.count_pool
                      / self.M_IN_KM / self.duration)
        return mean_speed

    def get_spent_calories(self) -> float:
        spent_calories = (self.get_mean_speed() + 1.1) * 2 * self.weight
        return spent_calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    workouts = {'SWM': Swimming,
                'RUN': Running,
                'WLK': SportsWalking}
    training = workouts[workout_type](Training(data))
    return training


def main(training: Training) -> None:
    """Главная функция."""
    info = InfoMessage(training.show_training_info())
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
