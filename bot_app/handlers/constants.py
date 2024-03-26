from enum import Enum


class Admin(str, Enum):
    ADMIN_ONLY = 'Добро пожаловать в панель администратора!'
    DELETE_COMPLITE = 'Пользователь удалён'
    NOT_FOUND = 'Пользователь не найден. Введите команду повторно'
    ADD_ID = 'Введите id'
    ALL_USERS = 'Список всех пользователей'
    DELETE_USER = 'Удалить пользователя'
    DEACTIVATE_USER = 'Деактивировать пользователя'
    DEACTIVATE_COMPLITE = 'Пользователь деактивирован'
    MAIN_MENU = 'Главное меню'
    RETURN_TO_MENU = 'Вы вернулись в главное меню'
    ADD_USER_TO_ADMIN = 'Добавить пользователя в админы'
    ADD_EMAIL = 'Введите почту пользователя'
    SUCCESS = 'Пользователь стал администратором'
    ANTI_SUCCESS = 'Пользователь перестал быть администратором'
    ADMIN_ALREADY = 'Этот пользователь уже администратор'
    REMOVE_USER_FROM_ADMIN = 'Удалить пользователя из админов'
    NON_USER_ADMIN = 'Этот пользователь не является админом'


class InfoMessage(str, Enum):
    ABOUT_MSG = (
        'В нашей компании есть прекрасная традиция знакомиться '
        'за чашечкой горячего кофе ☕ в microsoft teams или в офисе.\n\n'
        'Раз в неделю будет автоматически приходить '
        'имя и фамилия коллеги в этот чат-бот '
        'вам остается договориться о дате и времени встречи '
        'в удобном для вас формате.\n\n'
        '«Кофе вслепую ☕» - это всегда:\n'
        '• прекрасная компания 💥;\n'
        '• приятный и неожиданный сюрприз 🎁;\n'
        '• помощь новым коллегам в адаптации 🤝;\n'
        '• новые знакомства 🤗\n'
    )
    ABOUT_PROJECT_MSG = (
        '<i>Милена Мелкова, cпециалист по продукту.</i>\n\n'
        '<b>«Кофе вслепую ☕»</b> - отличная возможность познакомиться\n'
        'с коллегами из других отделов,\n'
        'в том числе с менеджерами и директорами,\n'
        'которые тоже участвуют в проекте 🫶\n'
    )
    REVIEW_MSG = (
        '<i>Анастасия Родкина, младший менеджер'
        'по работе с ключевыми клиентами.</i>\n\n'
        'Крутая возможность пообщаться,'
        'лучше узнать новых сотрудников,'
        'наладить неформальный контакт'
        'в условиях удаленной работы… '
        'Поделиться своим опытом и получить заряд позитива! '
        'В крупных компаниях как наша - это необходимо! '
        'Спасибо за классный проект! 💫'
    ),
    COMMENTS_MSG = (
        '<i>Анна Борисевич, старший специалист'
        'по цифровому контенту.</i>\n\n'
        'Мне безумно нравится эта инициатива!\n'
        'уникальная возможность быстро '
        'познакомиться с коллегами, '
        'узнать что-то новое '
        'и зарядиться позитивной энергией на весь день 🤩\n\n'
        'Всем новичкам и бывалым '
        'искренне советую попробовать '
        'поучаствовать и получить приятные впечатления 🥰'
    ),
    START_MSG = (
        'Что умеет этот бот?\n\n'
        '☕️ Мы продолжаем нашу прекрасную традицию\n'
        'знакомиться за чашечкой горячего кофе или чая.\n\n'
        '🗓️ С кем ты разделишь капучино - решает случай.\n'
        'Каждый понедельник в этом боте будет происходить\n'
        'рассылка с именем коллеги,\n'
        'с кем вам нужно организовать встречу.\n\n'
        '🔁 Участники выбираются случайным образом,\n'
        'поэтому вы сможете выпить кофе с теми,\n'
        'с кем еще не пересекались по работе.\n\n'
        'Добро пожаловать🥰'
    )


class BaseCommands(str, Enum):
    ABOUT_PROJECT = 'О проекте'
    COMMENTS = 'Наши коллеги про'
    STOP_PARTICIPATE = 'Приостановить участие'
    CANT_STOP = 'Не удалось приостановить участие'
    RESTART_PARTICIPATE = 'Возобновить участие'
    RESTART_PARTICIPATE_MSG = 'Вы возобновили участие'
    CANT_RESTART_PARTICIPATE = 'Не удалось возобновить участие'
    NEXT_COMMENT = 'Следующий комментарий'
    MORE_COMMENT = 'Ещё комментарий'
    MAIN_MENU = 'Главное меню'
    RETURN_TO_MENU = 'Вы вернулись в главное меню'
    STOP_PARTICIPATE_MSG = (
        'Вы приостановили участие.\n'
        'Но в любой момент можете его возобновить 😊\n'
    ),


class UserRegictration(str, Enum):
    REGISTER = 'Регистрация'
    CANT_REGISTER = 'Вы уже зарегистрированы'
    ADD_NAME = 'Введите своё имя'
    CANCEL = 'отмена'
    CANCSEL_MSG = 'Действия отменены'
    BACK = 'назад'
    NO_STEP = 'Предыдущего шага нет, введите имя напишите "отмена"'
    ADD_LAST_NAME = 'Введите фамилию'
    ADD_EMAIL = 'Введите почту'
    EMAIL_DOMAIN = '@groupeseb'
    COMPLITE_MSG = 'Регистрация прошла успешно'
    INVALID_EMAIL = 'Вы ввели не корпоративную почту'
    EMAIL_EXIST = 'Пользователь с такой почтой уже существует. Введите другую почту'

    NAME_RULES = 'Имя должно содержать только буквы. Введите имя снова'
    LAST_NAME_RULES = 'Фамилия должна быть только из букв. Введите её заново.'


class CallbacksHandler(str, Enum):
    MESSAGE_CALLBACK = 'Хорошо!'
