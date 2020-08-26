import json
import random

from channels.auth import UserLazyObject

from case.models import Case
from profile.models import UserProfile
from .models import Payment
from .models import Statistic, LevelList, UserEvent, GameSession, LiveTape, PrizeWeight


def log(obj: object, title='') -> None:
    print(f'!!! Log {title} !!!')
    print(obj)


def new_finance(user: UserProfile, name: str, sum_money: int, status='Обработка') -> None:
    Payment.objects.create(
        user=user,
        name=name,
        sum_money=sum_money,
        status=status
    )


def enable_online_user(user: UserLazyObject) -> None:
    """ Пометить что пользователь подключился """
    # Если пользователь не аноним, то есть зарегистрирован
    if not user.is_anonymous:
        user = UserProfile.objects.get(user=user)
        user.is_connection = True
        user.quantity_connections += 1
        user.save()


def disable_online_user(user: UserLazyObject) -> bool:
    """ Пометить что пользователь разорвал подключение """
    if user.is_anonymous:
        return False

    user = UserProfile.objects.get(user=user)
    user.quantity_connections -= 1
    if user.quantity_connections == 0:
        user.is_connection = False
    user.save()
    return user.is_connection


def get_count_users_online() -> int:
    """ Возвращает количество онлайн пользователей """
    return UserProfile.objects.filter(is_connection=True).count()


def create_game(case: Case, user: UserProfile) -> dict:
    """ Обработчик создания новой игры """
    # Списываем с баланса стоимость кейса
    user.balance -= case.cost

    # Создаем новую сессию игры и получаем
    # количество доступных ячеек
    quantity_cells_available = create_game_session(
        case=case,
        user=user
    )

    # Начисляем пользователю статистику за игру
    user.experience += case.experience
    user.open_cases += 1
    user.spent_money += case.cost

    # Получаем новый уровень, если он повысился
    # если не повысился, то получим 0
    level = check_level_up(user=user)

    return {
        'data': {
            'balance': user.balance,
            'quantity_cells_available': quantity_cells_available,
        },
        'level': level
    }


def create_game_session(case: Case, user: UserProfile) -> int:
    """ Создает сессию игры """
    game = GameSession()
    game.user = user
    game.case = case

    prizes = json.loads(case.prizes)

    # Получаем количество доступных для открытия ячеек
    quantity_cells_available = 12
    for prize in prizes:
        if prize == 0:
            quantity_cells_available -= 1

    game.quantity_cells_available = quantity_cells_available
    game.unopened_cells = prizes
    game.cells = json.dumps(  # Формируем список для хранения значений ячеек
        dict.fromkeys(  # Список формата {"1": null, "2": null, ... "12": null}
            list(range(1, 13))
        )
    )

    # Если включен админ мод, то выбирам читерские веса
    if user.admin_mode:
        game.weight = PrizeWeight.objects.get(name='Admin').weights
    else:
        game.weight = PrizeWeight.objects.get(name='User').weights
    game.save()
    return quantity_cells_available


def check_level_up(user: UserProfile) -> int:
    """ Проверка нужно ли повышать уровень игроку """
    for level in LevelList.objects.all():
        if user.experience >= level.experience:
            if level.level - 1 == user.level:
                user.level = level.level
                user.balance += level.reward

                new_user_event(
                    user=user,
                    description=f'Достиг {level.level - 1} уровня'
                )
                return level.level
    return 0


def new_user_event(user: UserProfile, description: str) -> None:
    """ Создает новое событие у пользователя """
    UserEvent.objects.create(
        user=user,
        description=description
    )

    # Удаляем последнее событие пользователя,
    # если их не больше 12, так как, в шаблонах
    # больше 12 записей не выводится,
    # соответственно можно не хранить много записей
    event = UserEvent.objects.filter(user=user).order_by('-id')
    if event.count() > 12:
        event.last().delete()


def play_game(case: Case, user: UserProfile, cell: str) -> dict:
    """ Обработчик нажатия ячейки в игре """
    game = GameSession.objects.get(user=user, case=case)

    # На случай если игрок нажмет на ячейку, которая уже была открыта
    # или которой не существует
    try:
        if json.loads(game.cells)[cell] is not None:
            return {
                'head': 'Error',
                'data': {
                    'description': f'cell number {cell} is already open'
                }
            }
    except KeyError as err:
        return {
            'head': 'Error',
            'data': {
                'description': f'cell number {err} does not exist'
            }
        }

    # Загружаем список не использованных ячеек и весов
    unopened_cells = json.loads(game.unopened_cells)
    weight = json.loads(game.weight)

    # Рандомно выбираем выигрыш
    win = random.choices(unopened_cells, weights=weight)[0]

    # Удаляем использованое значение весов
    del weight[unopened_cells.index(win)]

    # Удаляем полученый выигрышь из списка не использованных ячеек
    unopened_cells.remove(win)

    # Записывам измененые списки в сессию
    game.unopened_cells = json.dumps(unopened_cells)
    game.weight = json.dumps(weight)

    # Если выпала не бомба, то есть не нулевой приз
    if not win == 0:
        game.sum_win = game.sum_win + win
        cells = json.loads(game.cells)
        cells.update({cell: win})
        game.cells = json.dumps(cells)
        game.quantity_cells_available -= 1

    game.save()

    return {
        'head': 'play_game',
        'data': {
            'win': win,
            'sum_win': game.sum_win
        }
    }


def end_game(case: Case, user: UserProfile, win: bool) -> dict:
    """ Обработчик завершения игры """
    game = GameSession.objects.get(user=user, case=case)
    unopened_cells = json.loads(game.unopened_cells)
    random.shuffle(unopened_cells)

    if win:
        user.balance += game.sum_win

    game.delete()

    statistic = Statistic.objects.get(name='games')
    statistic.value += 1
    statistic.save()

    return {
        'unopened_cells': unopened_cells,
        'balance': user.balance,
        'win': win
    }


def get_game(user: UserProfile, case=Case) -> dict:
    """ Возвращает сохраненую игру """
    try:
        game_session = GameSession.objects.get(user=user, case=case)

        open_cells = dict()

        # Получаем открытые ячейки
        for key, value in json.loads(game_session.cells).items():
            if value is not None:
                open_cells.update({key: value})

        return {
            'sum_win': game_session.sum_win,
            'quantity_cells_available': game_session.quantity_cells_available,
            'open_cells': open_cells
        }
    except GameSession.DoesNotExist:
        pass
    except ValueError as err:
        if "Field 'user_id' expected a number but got 'None'." in str(err):
            pass
        else:
            raise


def get_base_context(user_id: int) -> dict:
    """ Возвращает контекст необходимый для base.html """
    context = {
        # Количество пользователей
        'user_count': UserProfile.objects.all().count(),
        'games': Statistic.objects.get(name='games').value,  # Количество игр
        'live_tape': LiveTape.objects.all().order_by('-id'),  # Лайв лента
    }

    # Если пользователь авторизован
    if user_id is not None:
        # то добавляем его аватарку и баланс
        user = UserProfile.objects.get(id=user_id)
        context.update({
            'user_avatar': user.avatar.url,
            'balance': user.balance
        })

    return context
