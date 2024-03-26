from enum import Enum


class Distribution(str, Enum):
    TEXT_FOR_EXTRA = """
        Привет!
        На этой неделе в нашем проекте «Кофе вслепую ☕» нечетное количество
        участников, поэтому имя коллеги тебе придет на следующей неделе.
        Но сейчас не теряй возможность, пригласи на чашечку кофе любого
        коллегу и предложи ему присоединиться к нашему проекту
        (конечно, если он еще не участвует)!
        Отличного дня и продуктивной недели😊
    """


class Mailing(str, Enum):
    MEETING_MESSAGE = '''
        Ваша пара для Кофе вслепую {} {} ({}).
        Договоритесь с коллегой о кофе брейке на этой неделе 🗓
        Приятного времяпровождения!
    '''
    MEET_OK = 'Да'
    MEET_FALSE = 'Нет'
    MEET_END_OF_WEEK = 'Встретимся в конце недели'
    REMINDER_MAILING = 'Удалось ли уже встретиться с коллегой и выпить чашечку кофе?'
