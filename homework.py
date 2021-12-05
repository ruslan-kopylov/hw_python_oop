from typing import List


class InfoMessage:
    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float,
                 ) -> None:
        self.training_type = training_type
        self.duration_h = duration
        self.distance_km = distance
        self.speed_km_per_h = speed
        self.calories_kcal = calories

    def get_message(self) -> str:
        """Информационное сообщение о тренировке."""
        return(f'Тип тренировки: {self.training_type}; '
               f'Длительность: {self.duration_h:.3f} ч.; '
               f'Дистанция: {self.distance_km:.3f} км; '
               f'Ср. скорость: {self.speed_km_per_h:.3f} км/ч; '
               f'Потрачено ккал: {self.calories_kcal:.3f}.')


class Training:
    """Базовый класс тренировки."""
    M_IN_KM: int = 1000
    LEN_STEP_M: float = 0.65
    MIN_IN_HOUR: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action_steps = action
        self.duration_h = duration
        self.weight_kg = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action_steps * self.LEN_STEP_M / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration_h

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(type(self).__name__, self.duration_h,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    RUN_KOF_1: int = 18
    RUN_KOF_2: int = 20

    def get_spent_calories(self) -> float:
        return ((self.RUN_KOF_1 * self.get_mean_speed()
                - self.RUN_KOF_2)
                * self.weight_kg / self.M_IN_KM
                * (self.duration_h * self.MIN_IN_HOUR))


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    WALK_KOF_1: float = 0.035
    WALK_KOF_2: float = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height_cm: float = height

    def get_spent_calories(self) -> float:
        return ((self.WALK_KOF_1 * self.weight_kg
                + (self.get_mean_speed() ** 2
                 // self.height_cm) * self.WALK_KOF_2
                * self.weight_kg) * (self.duration_h * self.MIN_IN_HOUR))


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP_M: float = 1.38
    CALORIES_KOF_1: float = 1.1
    CALORIES_KOF_2: int = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: int,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.count_pool: float = count_pool
        self.length_pool_m: float = length_pool

    def get_mean_speed(self) -> float:
        return (self.length_pool_m * self.count_pool
                / self.M_IN_KM / self.duration_h)

    def get_spent_calories(self) -> float:
        return ((self.get_mean_speed() + self.CALORIES_KOF_1)
                * self.CALORIES_KOF_2 * self.weight_kg)


workouts = {'SWM': Swimming,
            'RUN': Running,
            'WLK': SportsWalking}


def read_package(workout_type: str, data: List[int]) -> Training:
    """Прочитать данные полученные от датчиков."""
    while workout_type not in workouts:
        print('unknown work type')
        return None
    else:
        return workouts[workout_type](*data)


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
        if training is not None:
            main(training)
        else:
            continue
