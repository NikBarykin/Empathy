import random
from agent import Agent, AVAILABLE_CITIES

# MALE_NAMES = ("Ваня", "Олег", "Леша", "Макс", "Егор")
MALE_NAMES = tuple()
MALE_PICTURES = [
        "AgACAgIAAxkBAAPTZJ6UzwzkGrBNKoCREV_wOZZeS-sAAsHMMRt--PFIAAHRjBjaArQ9AQADAgADcwADLwQ",
        "AgACAgIAAxkBAAPaZJ6Vi7G_R-71mT-BgVCRB5BIMdkAAsjMMRt--PFIvhO86_6XvlMBAAMCAANzAAMvBA"]


FEMALE_NAMES = (
        "Лия",
        "Анастасия",
        "Александра",
        "Дарья",
        "Анна",
        "Мария",
        "Елена",
        "Ксения",
        "София",
        "Екатерина",
        "Наталья",
        "Вероника",
        "Валерия",
        "Диана",
        "Маргарита",
        "Юлия",
        "Алина",
        "Ольга",
        "Арина",
        "Татьяна",
        )

FEMALE_PICTURES = (
        "AgACAgIAAxkBAAPRZJ6UlQOepvv5gbtP52npF5jk7p4AAsLMMRt--PFIDlOStB3xcjsBAAMCAANzAAMvBA",
        "AgACAgIAAxkBAAPXZJ6VakWrRZRSYDJxwqBXNnR-NxMAAsfMMRt--PFI_F7X1LUUmAEBAAMCAANzAAMvBA",
        "AgACAgIAAxkBAAIC4GSf6Ng8d4O0VhwX8o-UQlbXRidmAAIEyjEbfvgBSc5S0y8hYOmiAQADAgADcwADLwQ",
        "AgACAgIAAxkBAAIC4mSf6O5yL0g_QMF9t2UhVR44xbmGAAIFyjEbfvgBSXY_4yV1vkmEAQADAgADcwADLwQ"
        )

MALE_SELF_DESCRIPTIONS = (
        "Я активный, веселый, дружелюбный парень со стремлением к достижению больших вещей. Ищу партнершу, с которой могу проводить незабываемое время. Я люблю играть в видео игры, хорошо знаю Питон и С++, интересуюсь веб-разработкой и дизайном.",
        "Я душевный, интеллигентный, интровертный мужчина, охотный путешественник и большой любитель кино. Я чувствую себя комфортно со всеми и рад исследовать новое. У меня есть крепкие компьютерные навыки и уверенные знания в программировании, самоучитель C++, Python и веб-разработки.",
        "Я социальный и энергичный мужчина, увлекающийся всеми аспектами жизни. Люблю путешествовать, любящий друга и защитник, социально активный и помогающий другим. Хорошо знаю Питон, С++, Rust и веб-распространение, а также люблю играть панк и хард-рок.")

FEMALE_SELF_DESCRIPTIONS = (
        "Привет! Я веселая и энергичная девушка, которая любит активный образ жизни. Обожаю путешествовать, открывать новые места и встречать интересных людей. Ищу партнера, с которым смогу делить свои приключения и создавать незабываемые воспоминания.",

"Приветствую! Я творческая и нежная девушка, увлекающаяся искусством и музыкой. Мои увлечения включают рисование, пение и танцы. Ищу вторую половинку, с кем смогу разделить свои творческие идеи и вместе создавать что-то прекрасное.",

"Привет! Я интеллектуальная и целеустремленная девушка, увлеченная наукой и образованием. Люблю читать книги, учиться чему-то новому и развиваться как личность. Ищу партнера, с кем смогу вести умные и глубокие разговоры, а также поддерживать и вдохновлять друг друга на достижение целей.",

"Привет! Я заботливая и семейно ориентированная девушка, ценящая домашний уют и теплые отношения. Обожаю готовить вкусные блюда, проводить время с близкими и заботиться о своих близких. Ищу партнера, с кем смогу создать крепкую и счастливую семью.",

"Привет! Я спортивная и здоровая девушка, увлеченная фитнесом и заботой о своем теле. Люблю заниматься спортом, ходить в тренажерный зал и заниматься йогой. Ищу партнера, который разделяет мою страсть к здоровому образу жизни и готов вместе достигать новых спортивных целей.",)

MIN_AGE = 18
MAX_AGE = 30

NAMES = MALE_NAMES + FEMALE_NAMES

NO_AGENTS = 10

lines = []

for i in range (NO_AGENTS):
    name = random.choice(NAMES)
    age = random.randint(MIN_AGE, MAX_AGE)

    if name in MALE_NAMES:
        gender = "мужчина"
        pictures = MALE_PICTURES
        description = random.choice(MALE_SELF_DESCRIPTIONS)
    else:
        gender = "женщина"
        pictures = FEMALE_PICTURES
        description = random.choice(FEMALE_SELF_DESCRIPTIONS)

    agent = Agent(
            i,
            "username",
            name,
            age,
            gender,
            random.choice(AVAILABLE_CITIES),
            random.choice(pictures),
            description,
            -1,
            -1,
            )

    lines.append(agent.serialize())

with open("setup.txt", "w", encoding="utf-8") as f:
    f.writelines('\n'.join(lines))
