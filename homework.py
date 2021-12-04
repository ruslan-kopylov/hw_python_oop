from typing import List


class InfoMessage:
    def __init__(self,
                 training_type: str,
                 duration_h: float,
                 distance_km: float,
                 speed_km_per_h: float,
                 calories_kcal: float,
                 ) -> None:
        self.training_type = training_type
        self.duration_h = duration_h
        self.distance_km = distance_km
        self.speed_km_per_h = speed_km_per_h
        self.calories_kcal = calories_kcal

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
                 action_qt: int,
                 duration_h: float,
                 weight_kg: float,
                 ) -> None:
        self.action_qt = action_qt
        self.duration_h = duration_h
        self.weight_kg = weight_kg

    def get_distance_km(self) -> float:
        """Получить дистанцию в км."""
        return self.action_qt * self.LEN_STEP_M / self.M_IN_KM

    def get_mean_speed_km_per_h(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance_km() / self.duration_h

    def get_spent_calories_kcal(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(type(self).__name__, self.duration_h,
                           self.get_distance_km(),
                           self.get_mean_speed_km_per_h(),
                           self.get_spent_calories_kcal())


class Running(Training):
    """Тренировка: бег."""
    RUN_KOF_1: int = 18
    RUN_KOF_2: int = 20

    def get_spent_calories_kcal(self) -> float:
        return ((self.RUN_KOF_1 * self.get_mean_speed_km_per_h()
                - self.RUN_KOF_2)
                * self.weight_kg / self.M_IN_KM
                * (self.duration_h * self.MIN_IN_HOUR))


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    WALK_KOF_1: float = 0.035
    WALK_KOF_2: float = 0.029

    def __init__(self,
                 action_qt: int,
                 duration_h: float,
                 weight_kg: float,
                 height_cm: float,
                 ) -> None:
        super().__init__(action_qt, duration_h, weight_kg)
        self.height_cm: float = height_cm

    def get_spent_calories_kcal(self) -> float:
        return ((self.WALK_KOF_1 * self.weight_kg
                + (self.get_mean_speed_km_per_h() ** 2
                 // self.height_cm) * self.WALK_KOF_2
                * self.weight_kg) * (self.duration_h * self.MIN_IN_HOUR))


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP_M: float = 1.38
    CALORIES_KOF_1: float = 1.1
    CALORIES_KOF_2: int = 2

    def __init__(self,
                 action_qt: int,
                 duration_h: float,
                 weight_kg: float,
                 length_pool_m: float,
                 count_pool_qt: int,
                 ) -> None:
        super().__init__(action_qt, duration_h, weight_kg)
        self.count_pool_qt: float = count_pool_qt
        self.length_pool_m: float = length_pool_m

    def get_mean_speed_km_per_h(self) -> float:
        return (self.length_pool_m * self.count_pool_qt
                / self.M_IN_KM / self.duration_h)

    def get_spent_calories_kcal(self) -> float:
        return ((self.get_mean_speed_km_per_h() + self.CALORIES_KOF_1)
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
