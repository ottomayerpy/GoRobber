import asyncio
import json
import os

from channels.consumer import AsyncConsumer
from channels.exceptions import StopConsumer

from case.models import Case
from profile.models import UserProfile
from . import service
from .models import LiveTape, Statistic
from .service import log

# Настройка для вызова синхронных функций из асинхронных
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"


class GameConsumer(AsyncConsumer):
    def __init__(self, scope):
        super().__init__(scope)
        self.name = 'Game'

    async def send_socket(self, event: dict):
        """ Отправка сообщения клиенту """
        await self.send({
            'type': 'websocket.send',  # Сокет отправит сообщение
            'text': json.dumps({
                'head': event['head'],
                'data': event['data']
            })
        })

    async def websocket_connect(self, event):
        await self.send({
            'type': 'websocket.accept'  # Сокет открыт
        })

        service.enable_online_user(user=self.scope["user"])

        await self.channel_layer.group_add(
            self.name,
            self.channel_name,
        )

        await self.channel_layer.group_send(
            self.name,
            {
                'type': 'send_socket',
                'head': 'update_counter_online_users',
                'data': service.get_count_users_online()
            }
        )

    async def websocket_disconnect(self, event):
        # Ждем, чтобы счетчик онлайна с скакал
        # так как пользователь мог просто перейти на другую страницу
        await asyncio.sleep(3)
        # Если пользователь не онлайн
        if not service.disable_online_user(user=self.scope["user"]):
            # то обновляем счетчик онлайн пользователей
            await self.channel_layer.group_send(
                self.name,
                {
                    'type': 'send_socket',
                    'head': 'update_counter_online_users',
                    'data': service.get_count_users_online()
                }
            )

        await self.channel_layer.group_discard(
            self.name,
            self.channel_name
        )
        raise StopConsumer()

    async def websocket_receive(self, event):
        data = json.loads(event.get('text'))
        if data['userid'] == 'None':
            return

        command = data['command']
        user = UserProfile.objects.get(user_id=data['userid'])
        if command == 'create_game':
            case = Case.objects.get(name=data['case'])
            await self.create_game(
                case=case,
                user=user
            )
        elif command == 'play_game':
            case = Case.objects.get(name=data['case'])
            cell = data['cell']
            await self.play_game(
                case=case,
                user=user,
                cell=cell
            )
        elif command == 'end_game':
            case = Case.objects.get(name=data['case'])
            win = data['win']
            await self.end_game(
                case=case,
                user=user,
                win=win
            )
        elif command == 'get_game':
            case = Case.objects.get(name=data['case'])
            await self.get_game(
                case=case,
                user=user
            )
        elif command == 'send_message':
            value = 'success'
            await self.send_socket({
                'head': 'sendMessage',
                'data': value
            })
        elif command == 'Pay':
            value = int(data['value'])
            user.balance += value
            user.save()
            service.new_finance(
                user=user,
                name='Пополнение',
                sum_money=value,
                status='Выполнен'
            )
            service.new_user_event(
                user=user,
                description=f'Пополнил счет на сумму {value} ₽'
            )
            await self.send_socket({
                'head': 'Pay',
                'data': {
                    'status': 'success',
                    'balance': user.balance
                }
            })
        elif command == 'PayOut':
            value = int(data['value'])
            user.balance -= value
            user.save()
            service.new_finance(
                user=user,
                name='Вывод',
                sum_money=value,
                status='Выполнен'
            )
            service.new_user_event(
                user=user,
                description=f'Вывел со счета {value} ₽'
            )
            await self.send_socket({
                'head': 'PayOut',
                'data': {
                    'status': 'success',
                    'balance': user.balance
                }
            })
        else:
            await self.send_socket({
                'head': 'Error',
                'data': {
                    'description': 'NoneCommand'
                }
            })

    async def create_game(self, case: Case, user: UserProfile):
        """ Обработчик создания новой игры """
        # Если не достаточно денег для начала игры
        if case.cost > user.balance:
            await self.send_socket({
                'head': 'Error',
                'data': {
                    'description': 'create_game_negative-balance'
                }
            })
            return

        # Если уровень игрока меньше чем уровень кейса
        if user.level < case.level:
            await self.send_socket({
                'head': 'Error',
                'data': {
                    'description': 'create_game_low-level'
                }
            })
            return

        game = service.create_game(
            case=case,
            user=user
        )

        user.save()

        if not game['level'] == 0:
            await self.send_socket({
                'head': 'levels',
                'data': game['level']
            })

        await self.send_socket({
            'head': 'create_game',
            'data': game['data']
        })

    async def play_game(self, case: Case, user: UserProfile, cell: str):
        """ Обработчик нажатия ячейки в игре """
        game = service.play_game(
            case=case,
            user=user,
            cell=cell
        )

        if game['head'] != 'Error' and game['data']['win'] != 0:
            service.new_user_event(
                user=user,
                description=f'Открыл кейс {case.name} на сумму {game["data"]["win"]} ₽'
            )

            await self.new_live_tape(
                user=user,
                sum_win=game['data']['win']
            )

        await self.send_socket(game)

    async def end_game(self, case: Case, user: UserProfile, win: bool):
        """ Обработчик завершения игры """
        # try:
        data = service.end_game(
            case=case,
            user=user,
            win=win
        )

        user.save()

        await self.channel_layer.group_send(
            self.name,
            {
                'type': 'send_socket',
                'head': 'StatGames',
                'data': Statistic.objects.get(name='games').value
            }
        )

        await self.send_socket({
            'head': 'end_game',
            'data': data
        })

    async def get_game(self, case: Case, user: UserProfile):
        """ Возвращает сохраненую игру """
        game = service.get_game(
            user=user,
            case=case
        )

        if game is not None:
            await self.send_socket({
                'head': 'get_game',
                'data': game
            })

    async def new_live_tape(self, user: UserProfile, sum_win: int):
        """ Добавляет новый элемент в лайв ленту """
        LiveTape.objects.create(
            user=user,
            sum_win=sum_win,
        )

        await self.channel_layer.group_send(
            self.name,
            {
                'type': 'send_socket',
                'head': 'new_coin_in_live_tape',
                'data': {
                    'id': user.user_id,
                    'cost': sum_win,
                    'avatar': user.avatar.url
                }
            }
        )

        # Удаляем последний элемент в лайв ленте, если их становится больше 12, так как
        # в ленте выводится 12 элементов, чтобы не мусорить в БД
        live_tape = LiveTape.objects.all()
        if live_tape.count() > 12:
            last_element = live_tape.order_by('-id').last()
            last_element.delete()
