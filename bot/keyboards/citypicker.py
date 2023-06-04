from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def get_country_keyboard() -> ReplyKeyboardMarkup:
    # Клавиатура для выбора стран
    country_keyboard = ReplyKeyboardBuilder()
    country_keyboard.add(
        KeyboardButton(text='Россия'),
        KeyboardButton(text='Турция'),
        KeyboardButton(text='Израиль'),
        KeyboardButton(text='Армения'),
        KeyboardButton(text='Сербия'),
        KeyboardButton(text='Беларусь'),
        KeyboardButton(text='Грузия'),
        KeyboardButton(text='Казахстан'),
        KeyboardButton(text='Кыргызстан'),
        KeyboardButton(text='Азербайджан'),
        KeyboardButton(text='ОАЭ'),
        KeyboardButton(text='Черногория'),
        KeyboardButton(text='Болгария'),
        KeyboardButton(text='Греция'),
        KeyboardButton(text='Кипр'),
    )
    country_keyboard.adjust(3)
    return country_keyboard.as_markup(resize_keyboard=True)


# Словарь с городами для каждой страны
cities_by_country = {
    'Россия': ['Москва', 'Санкт-Петербург', 'Казань', 'Сочи', 'Самара', 'Калининград', 'Краснодар', 'Екатеринбург',
               'Новосибирск', 'Ростов-на-Дону', 'Уфа', 'Пермь', 'Красноярск', 'Грозный', 'Махачкала',
               'Минеральные воды', 'Владикавказ', 'Иркутск', 'Волгоград', 'Нижний Новгород', 'Омск', 'Сургут',
               'Челябинск', 'Петрозаводск', 'Оренбург', 'Кемерово', 'Братск', 'Астрахань', 'Саратов', 'Тюмень',
               'Ставрополь'],
    'Турция': ['Анталья', 'Стамбул', 'Аланья', 'Измир', 'Анкара', 'Даламан', 'Ризе', 'Адана', 'Мерсин', 'Трабзон',
               'Кайсери', 'Самсун'],
    'Сербия': ['Белград', 'Нови-Сад'],
    'Израиль': ['Тель-Авив', 'Иерусалим', 'Беэр-Шева', 'Хайфа'],
    'Армения': ['Ереван', 'Гюмри'],
    'Грузия': ['Тбилиси', 'Батуми', 'Кутаиси'],
    'Казахстан': ['Алматы', 'Астана', 'Шымкент', 'Атырау', 'Актау'],
    'Беларусь': ['Минск'],
    'ОАЭ': ['Дубай', 'Шарджа', 'Абу-Даби'],
    'Кыргызстан': ['Бишкек', 'Ош'],
    'Черногория': ['Тиват', 'Будва', 'Котор', 'Подгорица', 'Петровац', 'Херцег-Нови', 'Цетине', 'Бар'],
    'Болгария': ['София', 'Варна', 'Бургас', 'Несебыр', 'Солнечный Берег'],
    'Греция': ['Афины', 'Салоники'],
    'Кипр': ['Лимассол', 'Ларнака', 'Айя-Напа', 'Пафос'],
    'Азербайджан': ['Баку', 'Гянджа', 'Нахичевань', 'Ленкорань', 'Габала'],
}


# Функция для создания клавиатуры с городами выбранной страны
def city_keyboard(country):
    keyboard = ReplyKeyboardBuilder()
    if country in cities_by_country:
        for city in cities_by_country[country]:
            keyboard.add(KeyboardButton(text=city))
    keyboard.add(KeyboardButton(text='Назад'))
    keyboard.adjust(3)
    return keyboard.as_markup(resize_keyboard=True)
