class InfoMessage:
    def __init__(self,
                 training_type,
                 duration: float,
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
        print(f'Тип тренировки:{self.training_type};'
              f'Длительность: {self.duration};'
              f'Дистанция: {self.distance};'
              f'Скорость: {self.speed};'
              f'Потрачено ккал: {self.calories}.')


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
        mean_speed = self.get_distance() / self.duration
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""

        pass

    def show_training_info(self) -> InfoMessage:
        message = InfoMessage(training, self.duration,
                              self.get_distance, self.get_mean_speed,
                              self.get_spent_calories)
        """Вернуть информационное сообщение о выполненной тренировке."""
        m = message.get_message()
        return m


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
        calories = ((run_kof_1 * self.get_mean_speed() - run_kof_2)
                    * self.weight / self.M_IN_KM * (self.duration * 60))
        return calories


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
        calories = ((walk_kof_1 * self.weight
                    + (self.get_mean_speed() ** 2
                     // self.height) * walk_kof_2
                    * self.weight) * (self.duration * 60))
        return calories


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
        calories = (self.get_mean_speed() + 1.1) * 2 * self.weight
        return calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    workouts = {'SWM': Swimming,
                'RUN': Running,
                'WLK': SportsWalking}
    training_type = workouts[workout_type](*data)
    return training_type


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
