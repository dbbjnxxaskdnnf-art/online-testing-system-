from __future__ import annotations

import hashlib
import json
from datetime import datetime
from pathlib import Path
from uuid import uuid4

import streamlit as st


DATA_FILE = Path(__file__).with_name("python_quiz_data.json")
LANGUAGES = {"ru": "Русский", "en": "English", "kk": "Қазақша"}


COPY: dict[str, dict[str, str]] = {
    "header_note": {"ru": "Быстрый вызов, отличная энергия.", "en": "A quick challenge for a bright mind.", "kk": "Ақылға арналған қысқа сынақ."},
    "home": {"ru": "Главная", "en": "Home", "kk": "Басты бет"},
    "teacher_results": {"ru": "Результаты учеников", "en": "Student results", "kk": "Оқушы нәтижелері"},
    "sign_in": {"ru": "Войти", "en": "Sign in", "kk": "Кіру"},
    "register": {"ru": "Регистрация", "en": "Register", "kk": "Тіркелу"},
    "logout": {"ru": "Выйти", "en": "Log out", "kk": "Шығу"},
    "hero_eyebrow": {"ru": "Маленькая победа для мозга", "en": "A small win for your brain", "kk": "Миға арналған шағын жеңіс"},
    "hero_title": {"ru": "Будьте любопытны. Поиграйте немного.", "en": "Stay curious. Play a little.", "kk": "Қызық болыңыз. Біраз ойнап көріңіз."},
    "hero_description": {
        "ru": "Небольшие викторины для пауз между делами. Выберите карточку, доверьтесь интуиции и узнайте ещё что-нибудь интересное.",
        "en": "Short quizzes for the spaces between things. Pick a card, trust your instincts, and learn something new.",
        "kk": "Істер арасындағы үзіліске арналған қысқа викториналар. Карточканы таңдап, біліміңізді сынап көріңіз.",
    },
    "round_time": {"ru": "Раунды по 2–3 минуты", "en": "2–3 minute rounds", "kk": "2–3 минуттық раундтар"},
    "save_note": {"ru": "Регистрация нужна только для сохранения результата", "en": "Register to save your result", "kk": "Нәтижені сақтау үшін тіркеліңіз"},
    "choose_mood": {"ru": "Выберите настроение", "en": "Choose a mood", "kk": "Көңіл-күйді таңдаңыз"},
    "think_about": {"ru": "О чём сегодня думаем?", "en": "What are we thinking about today?", "kk": "Бүгін не туралы ойланамыз?"},
    "all_quizzes": {"ru": "Все викторины", "en": "All quizzes", "kk": "Барлық викториналар"},
    "for_you": {"ru": "Для вас", "en": "For you", "kk": "Сіз үшін"},
    "geography": {"ru": "География", "en": "Geography", "kk": "География"},
    "culture": {"ru": "Культура", "en": "Culture", "kk": "Мәдениет"},
    "science": {"ru": "Наука", "en": "Science", "kk": "Ғылым"},
    "questions": {"ru": "вопросов", "en": "questions", "kk": "сұрақ"},
    "start": {"ru": "Начать", "en": "Start", "kk": "Бастау"},
    "choose_quiz": {"ru": "Выберите викторину", "en": "Choose a quiz", "kk": "Викторинаны таңдаңыз"},
    "no_quizzes": {"ru": "Эта полка ещё наполняется.", "en": "This shelf is still filling up.", "kk": "Бұл сөре әлі толтырылуда."},
    "back_to_quizzes": {"ru": "К викторинам", "en": "Back to quizzes", "kk": "Викториналарға"},
    "question": {"ru": "Вопрос", "en": "Question", "kk": "Сұрақ"},
    "check_answer": {"ru": "Проверить ответ", "en": "Check answer", "kk": "Жауапты тексеру"},
    "next": {"ru": "Следующий вопрос", "en": "Next question", "kk": "Келесі сұрақ"},
    "see_result": {"ru": "Узнать результат", "en": "See result", "kk": "Нәтижені көру"},
    "excellent": {"ru": "Отлично!", "en": "Excellent!", "kk": "Керемет!"},
    "good_try": {"ru": "Хорошая попытка.", "en": "Good try.", "kk": "Жақсы талпыныс."},
    "correct_answer": {"ru": "Правильный ответ", "en": "Correct answer", "kk": "Дұрыс жауап"},
    "round_finished": {"ru": "Раунд завершён", "en": "Round complete", "kk": "Раунд аяқталды"},
    "your_result": {"ru": "Ваш результат", "en": "Your result", "kk": "Сіздің нәтижеңіз"},
    "correct": {"ru": "правильных", "en": "correct", "kk": "дұрыс"},
    "play_again": {"ru": "Сыграть ещё раз", "en": "Play again", "kk": "Қайта ойнау"},
    "short_review": {"ru": "Короткий разбор", "en": "Quick review", "kk": "Қысқаша талдау"},
    "result_high": {"ru": "У вас удивительно любознательный ум.", "en": "You have a wonderfully curious mind.", "kk": "Сіздің ізденімпаз ойыңыз керемет."},
    "result_mid": {"ru": "Отличное начало — впереди ещё много интересного.", "en": "A great start — there is more to discover.", "kk": "Керемет бастама — алда әлі көп жаңалық бар."},
    "result_low": {"ru": "Каждый хороший факт начинается с правильной ошибки.", "en": "Every good fact starts with a useful mistake.", "kk": "Әр жақсы білім пайдалы қателіктен басталады."},
    "auth_title": {"ru": "Войдите в Quizly", "en": "Sign in to Quizly", "kk": "Quizly-ге кіріңіз"},
    "auth_subtitle": {"ru": "Сохраняйте результаты и учитесь в своём ритме.", "en": "Save results and learn at your own pace.", "kk": "Нәтижелерді сақтап, өз қарқыныңызбен үйреніңіз."},
    "name": {"ru": "Имя", "en": "Name", "kk": "Аты"},
    "email": {"ru": "Электронная почта", "en": "Email", "kk": "Электрондық пошта"},
    "password": {"ru": "Пароль", "en": "Password", "kk": "Құпиясөз"},
    "role": {"ru": "Роль", "en": "Role", "kk": "Рөл"},
    "student": {"ru": "Ученик", "en": "Student", "kk": "Оқушы"},
    "teacher": {"ru": "Учитель", "en": "Teacher", "kk": "Мұғалім"},
    "sign_in_action": {"ru": "Войти в аккаунт", "en": "Sign in", "kk": "Аккаунтқа кіру"},
    "register_action": {"ru": "Зарегистрироваться", "en": "Register", "kk": "Тіркелу"},
    "invalid_login": {"ru": "Проверьте почту и пароль.", "en": "Check your email and password.", "kk": "Пошта мен құпиясөзді тексеріңіз."},
    "already_exists": {"ru": "Пользователь с такой почтой уже есть.", "en": "An account with this email already exists.", "kk": "Бұл поштаға тіркелген аккаунт бар."},
    "teacher_only": {"ru": "Эта страница доступна только учителю.", "en": "This page is for teachers only.", "kk": "Бұл бет мұғалімдерге ғана арналған."},
    "teacher_panel": {"ru": "Панель учителя", "en": "Teacher panel", "kk": "Мұғалім панелі"},
    "teacher_panel_hint": {"ru": "Здесь отображаются результаты учеников.", "en": "Student results appear here.", "kk": "Оқушылардың нәтижелері осында көрсетіледі."},
    "no_results": {"ru": "Пока нет результатов учеников.", "en": "There are no student results yet.", "kk": "Әзірге оқушы нәтижелері жоқ."},
    "student_column": {"ru": "Ученик", "en": "Student", "kk": "Оқушы"},
    "quiz_column": {"ru": "Викторина", "en": "Quiz", "kk": "Викторина"},
    "score_column": {"ru": "Результат", "en": "Score", "kk": "Нәтиже"},
    "date_column": {"ru": "Дата", "en": "Date", "kk": "Күні"},
    "sign_in_to_save": {"ru": "Войдите или зарегистрируйтесь, чтобы сохранять результаты.", "en": "Sign in or register to save your results.", "kk": "Нәтижені сақтау үшін кіріңіз немесе тіркеліңіз."},
    "create_test": {"ru": "Создать тест", "en": "Create a test", "kk": "Тест жасау"},
    "create_test_title": {"ru": "Создайте свой тест", "en": "Create your own test", "kk": "Өз тестіңізді жасаңыз"},
    "create_test_hint": {"ru": "Добавьте вопросы и правильные ответы — ученики увидят тест в общем списке.", "en": "Add questions and correct answers — students will see the test in the quiz list.", "kk": "Сұрақтар мен дұрыс жауаптарды қосыңыз — оқушылар тесті жалпы тізімнен көреді."},
    "test_title": {"ru": "Название теста", "en": "Test title", "kk": "Тест атауы"},
    "test_description": {"ru": "Описание теста", "en": "Test description", "kk": "Тест сипаттамасы"},
    "test_category": {"ru": "Категория", "en": "Category", "kk": "Санат"},
    "question_prompt": {"ru": "Вопрос", "en": "Question", "kk": "Сұрақ"},
    "answer_option": {"ru": "Вариант", "en": "Option", "kk": "Нұсқа"},
    "correct_option": {"ru": "Правильный вариант", "en": "Correct option", "kk": "Дұрыс нұсқа"},
    "save_test": {"ru": "Сохранить тест", "en": "Save test", "kk": "Тестті сақтау"},
    "test_required": {"ru": "Заполните название, описание, вопросы и все варианты ответов.", "en": "Fill in the title, description, questions, and all answer options.", "kk": "Атауды, сипаттаманы, сұрақтарды және барлық жауап нұсқаларын толтырыңыз."},
    "custom_difficulty": {"ru": "Тест учителя", "en": "Teacher test", "kk": "Мұғалім тесті"},
}


QUIZZES = [
    {
        "id": "curious-mix",
        "title": {"ru": "Любопытная смесь", "en": "Curious mix", "kk": "Қызықты қоспа"},
        "description": {"ru": "Наука, история, культура и приятные неожиданности.", "en": "Science, history, culture, and pleasant surprises.", "kk": "Ғылым, тарих, мәдениет және қызықты тосынсыйлар."},
        "category": "for_you",
        "difficulty": {"ru": "Разминка", "en": "Warm-up", "kk": "Жаттығу"},
        "questions": [
            {"prompt": {"ru": "У какого животного отпечатки пальцев похожи на человеческие?", "en": "Which animal has fingerprints similar to humans?", "kk": "Қай жануардың саусақ іздері адамдікіне ұқсайды?"}, "options": [{"ru": "Коала", "en": "Koala", "kk": "Коала"}, {"ru": "Выдра", "en": "Otter", "kk": "Кәмшат"}, {"ru": "Лемур", "en": "Lemur", "kk": "Лемур"}, {"ru": "Тигр", "en": "Tiger", "kk": "Жолбарыс"}], "answer": 0, "fact": {"ru": "Отпечатки коалы имеют петли и завитки, как у человека.", "en": "Koala fingerprints have loops and whorls like human fingerprints.", "kk": "Коаланың саусақ іздерінде адамдікіндей ілмектер мен бұрылыстар бар."}},
            {"prompt": {"ru": "Какая буква не встречается в таблице химических элементов?", "en": "Which letter does not appear in the periodic table?", "kk": "Химиялық элементтер кестесінде қай әріп кездеспейді?"}, "options": [{"ru": "J", "en": "J", "kk": "J"}, {"ru": "Q", "en": "Q", "kk": "Q"}, {"ru": "X", "en": "X", "kk": "X"}, {"ru": "Z", "en": "Z", "kk": "Z"}], "answer": 0, "fact": {"ru": "Буква J — единственная, которой нет в обозначениях элементов.", "en": "J is the only letter absent from element symbols.", "kk": "J әрпі элемент таңбаларында кездеспейтін жалғыз әріп."}},
            {"prompt": {"ru": "Какой океан самый маленький?", "en": "Which ocean is the smallest?", "kk": "Ең кішкентай мұхит қайсы?"}, "options": [{"ru": "Индийский", "en": "Indian", "kk": "Үнді"}, {"ru": "Атлантический", "en": "Atlantic", "kk": "Атлант"}, {"ru": "Северный Ледовитый", "en": "Arctic", "kk": "Солтүстік Мұзды"}, {"ru": "Южный", "en": "Southern", "kk": "Оңтүстік"}], "answer": 2, "fact": {"ru": "Площадь Северного Ледовитого океана — около 14 миллионов квадратных километров.", "en": "The Arctic Ocean covers about 14 million square kilometers.", "kk": "Солтүстік Мұзды мұхиттың ауданы шамамен 14 миллион шаршы километр."}},
        ],
    },
    {
        "id": "world-in-miniature",
        "title": {"ru": "Мир в миниатюре", "en": "World in miniature", "kk": "Шағын әлем"},
        "description": {"ru": "Большие места и маленькие детали. Путешествие по планете.", "en": "Big places and small details. A trip around our planet.", "kk": "Үлкен жерлер мен шағын деректер. Планетаға саяхат."},
        "category": "geography",
        "difficulty": {"ru": "Легко", "en": "Easy", "kk": "Оңай"},
        "questions": [
            {"prompt": {"ru": "В какой стране находится старейший парламент мира?", "en": "Which country has the world's oldest parliament?", "kk": "Әлемдегі ең көне парламент қай елде орналасқан?"}, "options": [{"ru": "Исландия", "en": "Iceland", "kk": "Исландия"}, {"ru": "Швеция", "en": "Sweden", "kk": "Швеция"}, {"ru": "Канада", "en": "Canada", "kk": "Канада"}, {"ru": "Греция", "en": "Greece", "kk": "Грекия"}], "answer": 0, "fact": {"ru": "Исландский альтинг был основан в 930 году.", "en": "The Icelandic Alþingi was founded in 930.", "kk": "Исландияның Альтингі 930 жылы құрылған."}},
            {"prompt": {"ru": "Какой остров самый большой в Средиземном море?", "en": "Which is the largest island in the Mediterranean?", "kk": "Жерорта теңізіндегі ең үлкен арал қайсы?"}, "options": [{"ru": "Крит", "en": "Crete", "kk": "Крит"}, {"ru": "Сицилия", "en": "Sicily", "kk": "Сицилия"}, {"ru": "Кипр", "en": "Cyprus", "kk": "Кипр"}, {"ru": "Сардиния", "en": "Sardinia", "kk": "Сардиния"}], "answer": 1, "fact": {"ru": "Сицилия — крупнейший регион Италии.", "en": "Sicily is Italy's largest region.", "kk": "Сицилия — Италияның ең үлкен аймағы."}},
            {"prompt": {"ru": "Над какой страной возвышается гора Килиманджаро?", "en": "Mount Kilimanjaro rises above which country?", "kk": "Килиманджаро тауы қай елде орналасқан?"}, "options": [{"ru": "Кения", "en": "Kenya", "kk": "Кения"}, {"ru": "Эфиопия", "en": "Ethiopia", "kk": "Эфиопия"}, {"ru": "Танзания", "en": "Tanzania", "kk": "Танзания"}, {"ru": "Уганда", "en": "Uganda", "kk": "Уганда"}], "answer": 2, "fact": {"ru": "Килиманджаро — самая высокая гора Африки.", "en": "Kilimanjaro is the highest mountain in Africa.", "kk": "Килиманджаро — Африкадағы ең биік тау."}},
        ],
    },
    {
        "id": "studio-brain",
        "title": {"ru": "Культурный радар", "en": "Culture radar", "kk": "Мәдениет радары"},
        "description": {"ru": "Кино, дизайн, музыка и детали культуры.", "en": "Film, design, music, and cultural details.", "kk": "Кино, дизайн, музыка және мәдениет деректері."},
        "category": "culture",
        "difficulty": {"ru": "Игриво", "en": "Playful", "kk": "Ойын сияқты"},
        "questions": [
            {"prompt": {"ru": "Кто расписал потолок Сикстинской капеллы?", "en": "Who painted the ceiling of the Sistine Chapel?", "kk": "Сикстин капелласының төбесін кім салған?"}, "options": [{"ru": "Леонардо да Винчи", "en": "Leonardo da Vinci", "kk": "Леонардо да Винчи"}, {"ru": "Микеланджело", "en": "Michelangelo", "kk": "Микеланджело"}, {"ru": "Рафаэль", "en": "Raphael", "kk": "Рафаэль"}, {"ru": "Караваджо", "en": "Caravaggio", "kk": "Караваджо"}], "answer": 1, "fact": {"ru": "Микеланджело работал над потолком с 1508 по 1512 год.", "en": "Michelangelo worked on the ceiling from 1508 to 1512.", "kk": "Микеланджело төбеде 1508–1512 жылдары жұмыс істеген."}},
            {"prompt": {"ru": "Как называется песня, исполняемая одним человеком?", "en": "What do we call a song performed by one person?", "kk": "Бір адам орындайтын ән қалай аталады?"}, "options": [{"ru": "Соло", "en": "Solo", "kk": "Соло"}, {"ru": "Дуэт", "en": "Duet", "kk": "Дуэт"}, {"ru": "Хор", "en": "Choir", "kk": "Хор"}, {"ru": "Увертюра", "en": "Overture", "kk": "Увертюра"}], "answer": 0, "fact": {"ru": "Слово «соло» происходит от итальянского «один».", "en": "The word “solo” comes from the Italian word for “alone”.", "kk": "«Соло» сөзі итальян тіліндегі «бір» сөзінен шыққан."}},
            {"prompt": {"ru": "Из скольких строк традиционно состоит хайку?", "en": "How many lines does a traditional haiku have?", "kk": "Дәстүрлі хайку неше жолдан тұрады?"}, "options": [{"ru": "Трёх", "en": "Three", "kk": "Үш"}, {"ru": "Четырёх", "en": "Four", "kk": "Төрт"}, {"ru": "Шести", "en": "Six", "kk": "Алты"}, {"ru": "Двух", "en": "Two", "kk": "Екі"}], "answer": 0, "fact": {"ru": "Классическая схема хайку — 5, 7, 5 слогов в трёх строках.", "en": "The classic haiku pattern is 5, 7, 5 syllables across three lines.", "kk": "Классикалық хайку үш жолда 5, 7, 5 буыннан тұрады."}},
        ],
    },
    {
        "id": "why-things-work",
        "title": {"ru": "Почему всё работает", "en": "Why things work", "kk": "Заттар неге жұмыс істейді?"},
        "description": {"ru": "Повседневная наука для внимательных.", "en": "Everyday science for curious minds.", "kk": "Ізденімпаздарға арналған күнделікті ғылым."},
        "category": "science",
        "difficulty": {"ru": "Заставит подумать", "en": "Think a little", "kk": "Ойлануға"},
        "questions": [
            {"prompt": {"ru": "Почему лёд плавает на поверхности воды?", "en": "Why does ice float on water?", "kk": "Мұз неге суда қалқып жүреді?"}, "options": [{"ru": "Он холоднее", "en": "It is colder", "kk": "Ол суығырақ"}, {"ru": "Он менее плотный", "en": "It is less dense", "kk": "Оның тығыздығы төмен"}, {"ru": "В нём больше кислорода", "en": "It has more oxygen", "kk": "Онда оттегі көп"}, {"ru": "Он тяжелее", "en": "It is heavier", "kk": "Ол ауырлау"}], "answer": 1, "fact": {"ru": "При замерзании вода расширяется, поэтому лёд менее плотный.", "en": "Water expands when it freezes, making ice less dense.", "kk": "Су қатқанда кеңейеді, сондықтан мұздың тығыздығы төмен."}},
            {"prompt": {"ru": "Какая сила удерживает планеты на орбитах?", "en": "What force keeps planets in orbit?", "kk": "Планеталарды орбитада қандай күш ұстап тұрады?"}, "options": [{"ru": "Трение", "en": "Friction", "kk": "Үйкеліс"}, {"ru": "Магнетизм", "en": "Magnetism", "kk": "Магнетизм"}, {"ru": "Гравитация", "en": "Gravity", "kk": "Гравитация"}, {"ru": "Давление", "en": "Pressure", "kk": "Қысым"}], "answer": 2, "fact": {"ru": "Гравитация удерживает планеты рядом с Солнцем.", "en": "Gravity keeps planets moving around the Sun.", "kk": "Гравитация планеталарды Күнді айналып қозғалуға ұстайды."}},
            {"prompt": {"ru": "Какой газ растения поглощают во время фотосинтеза?", "en": "Which gas do plants absorb during photosynthesis?", "kk": "Өсімдіктер фотосинтез кезінде қандай газды сіңіреді?"}, "options": [{"ru": "Кислород", "en": "Oxygen", "kk": "Оттегі"}, {"ru": "Азот", "en": "Nitrogen", "kk": "Азот"}, {"ru": "Углекислый газ", "en": "Carbon dioxide", "kk": "Көмірқышқыл газы"}, {"ru": "Водород", "en": "Hydrogen", "kk": "Сутек"}], "answer": 2, "fact": {"ru": "Растения превращают углекислый газ и воду в сахар с помощью света.", "en": "Plants use light to turn carbon dioxide and water into sugar.", "kk": "Өсімдіктер жарық көмегімен көмірқышқыл газы мен суды қантқа айналдырады."}},
        ],
    },
]


def tr(value: dict[str, str]) -> str:
    return value.get(st.session_state.language, value["ru"])


def t(key: str) -> str:
    return COPY[key][st.session_state.language]


def localize(value: str) -> dict[str, str]:
    return {language: value for language in LANGUAGES}


def load_store() -> dict[str, list[dict]]:
    if not DATA_FILE.exists():
        return {"users": [], "results": [], "quizzes": []}
    try:
        data = json.loads(DATA_FILE.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        st.error(f"Не удалось прочитать файл данных: {error}")
        return {"users": [], "results": [], "quizzes": []}
    return {"users": data.get("users", []), "results": data.get("results", []), "quizzes": data.get("quizzes", [])}


def save_store(store: dict[str, list[dict]]) -> None:
    DATA_FILE.write_text(json.dumps(store, ensure_ascii=False, indent=2), encoding="utf-8")


def all_quizzes(store: dict[str, list[dict]] | None = None) -> list[dict]:
    current_store = store if store is not None else load_store()
    return QUIZZES + current_store.get("quizzes", [])


def password_hash(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def set_page(page: str) -> None:
    st.session_state.page = page
    st.session_state.nav = page


def reset_quiz(quiz: dict) -> None:
    st.session_state.active_quiz_id = quiz["id"]
    st.session_state.question_index = 0
    st.session_state.answers = []
    st.session_state.answer_checked = False
    st.session_state.last_result = None
    set_page("play")


def active_quiz() -> dict | None:
    quiz_id = st.session_state.get("active_quiz_id")
    return next((quiz for quiz in all_quizzes() if quiz["id"] == quiz_id), None)


def save_result(quiz: dict, score: int) -> None:
    user = st.session_state.get("user")
    if not user:
        return
    store = load_store()
    total = len(quiz["questions"])
    store["results"].append(
        {
            "id": str(uuid4()),
            "user_name": user["name"],
            "user_email": user["email"],
            "quiz_id": quiz["id"],
            "quiz_title": quiz["title"],
            "score": score,
            "total": total,
            "percentage": round(score / total * 100),
            "created_at": datetime.now().isoformat(timespec="seconds"),
        }
    )
    save_store(store)


def finish_quiz(quiz: dict) -> None:
    answers = st.session_state.answers
    score = sum(answer == question["answer"] for answer, question in zip(answers, quiz["questions"]))
    st.session_state.last_result = {"score": score, "total": len(quiz["questions"]), "quiz_id": quiz["id"]}
    save_result(quiz, score)
    set_page("results")


def render_sidebar() -> None:
    st.sidebar.title("⚡ Quizly")
    st.sidebar.caption(t("header_note"))
    st.sidebar.selectbox("Language / Язык / Тіл", list(LANGUAGES), format_func=lambda code: LANGUAGES[code], key="language")
    st.sidebar.divider()

    page_options = ["home", "auth"]
    if st.session_state.get("user"):
        page_options.append("results")
        if st.session_state.user["role"] == "teacher":
            page_options.extend(["create_test", "teacher_results"])
    labels = {
        "home": t("home"),
        "auth": t("sign_in") if not st.session_state.get("user") else t("logout"),
        "results": t("your_result"),
        "create_test": t("create_test"),
        "teacher_results": t("teacher_results"),
    }
    current_page = st.session_state.get("page", "home")
    if current_page not in page_options:
        current_page = "home"
        st.session_state.page = "home"
    selected = st.sidebar.radio("Menu", page_options, index=page_options.index(current_page), format_func=lambda key: labels[key], key="nav")
    if selected != current_page:
        if selected == "auth" and st.session_state.get("user"):
            st.session_state.user = None
            set_page("home")
        else:
            set_page(selected)
        st.rerun()

    if st.session_state.get("user"):
        st.sidebar.success(f"{st.session_state.user['name']} · {t(st.session_state.user['role'])}")
        if st.sidebar.button(t("logout"), use_container_width=True):
            st.session_state.user = None
            set_page("home")
            st.rerun()


def render_home() -> None:
    st.caption(t("hero_eyebrow"))
    st.title(t("hero_title"))
    st.write(t("hero_description"))
    st.info(f"⏱️ {t('round_time')}  ·  📝 {t('save_note')}")
    st.divider()
    st.subheader(t("think_about"))

    category_keys = ["all", "for_you", "geography", "culture", "science"]
    category_labels = {"all": t("all_quizzes"), **{key: t(key) for key in category_keys[1:]}}
    selected_category = st.selectbox(t("choose_mood"), category_keys, format_func=lambda key: category_labels[key])
    filtered = [quiz for quiz in all_quizzes() if selected_category == "all" or quiz["category"] == selected_category]

    for start in range(0, len(filtered), 2):
        columns = st.columns(2)
        for column, quiz in zip(columns, filtered[start : start + 2]):
            with column:
                st.subheader(tr(quiz["title"]))
                st.write(tr(quiz["description"]))
                st.caption(f"{tr(quiz['difficulty'])} · {len(quiz['questions'])} {t('questions')} · 2 min")
                if st.button(f"{t('start')} →", key=f"start_{quiz['id']}", use_container_width=True):
                    reset_quiz(quiz)
                    st.rerun()


def render_auth() -> None:
    st.title(t("auth_title"))
    st.write(t("auth_subtitle"))
    mode = st.radio("Mode", ["login", "register"], format_func=lambda value: t("sign_in") if value == "login" else t("register"), horizontal=True)

    with st.form("auth_form"):
        name = st.text_input(t("name")) if mode == "register" else ""
        email = st.text_input(t("email"))
        password = st.text_input(t("password"), type="password")
        role = st.selectbox(t("role"), ["student", "teacher"], format_func=lambda value: t(value)) if mode == "register" else "student"
        submitted = st.form_submit_button(t("register_action") if mode == "register" else t("sign_in_action"), use_container_width=True)

    if not submitted:
        return
    clean_email = email.strip().lower()
    if not clean_email or not password or (mode == "register" and not name.strip()):
        st.warning(t("invalid_login"))
        return
    store = load_store()

    if mode == "register":
        if any(user["email"] == clean_email for user in store["users"]):
            st.error(t("already_exists"))
            return
        user = {"id": str(uuid4()), "name": name.strip(), "email": clean_email, "password_hash": password_hash(password), "role": role}
        store["users"].append(user)
        save_store(store)
        st.session_state.user = user
        set_page("home")
        st.success(t("register"))
        st.rerun()

    user = next((candidate for candidate in store["users"] if candidate["email"] == clean_email and candidate["password_hash"] == password_hash(password)), None)
    if not user:
        st.error(t("invalid_login"))
        return
    st.session_state.user = user
    set_page("home")
    st.rerun()


def render_play() -> None:
    quiz = active_quiz()
    if not quiz:
        set_page("home")
        st.rerun()
        return

    index = st.session_state.question_index
    question = quiz["questions"][index]
    st.button(f"← {t('back_to_quizzes')}", on_click=lambda: set_page("home"))
    st.progress((index + 1) / len(quiz["questions"]))
    st.caption(f"{t('question')} {index + 1} / {len(quiz['questions'])}")
    st.header(tr(question["prompt"]))

    if not st.session_state.answer_checked:
        selected = st.radio("Answer", list(range(len(question["options"]))), format_func=lambda option: tr(question["options"][option]), key=f"answer_{quiz['id']}_{index}")
        if st.button(t("check_answer"), type="primary", use_container_width=True):
            st.session_state.answers.append(selected)
            st.session_state.answer_checked = True
            st.rerun()
        return

    selected = st.session_state.answers[-1]
    correct = selected == question["answer"]
    if correct:
        st.success(f"{t('excellent')} {tr(question['fact'])}")
    else:
        st.error(f"{t('good_try')} {t('correct_answer')}: {tr(question['options'][question['answer']])}")
        st.info(tr(question["fact"]))

    next_label = t("see_result") if index == len(quiz["questions"]) - 1 else t("next")
    if st.button(next_label, type="primary", use_container_width=True):
        if index == len(quiz["questions"]) - 1:
            finish_quiz(quiz)
        else:
            st.session_state.question_index += 1
            st.session_state.answer_checked = False
        st.rerun()


def render_results() -> None:
    result = st.session_state.get("last_result")
    if not result:
        st.info(t("no_results"))
        return
    quiz = next(quiz for quiz in all_quizzes() if quiz["id"] == result["quiz_id"])
    score = result["score"]
    total = result["total"]
    st.title(t("round_finished"))
    st.metric(tr(quiz["title"]), f"{score} / {total}", f"{round(score / total * 100)}%")
    if score == total:
        st.success(t("result_high"))
    elif score >= total / 2:
        st.info(t("result_mid"))
    else:
        st.warning(t("result_low"))

    st.subheader(t("short_review"))
    for index, question in enumerate(quiz["questions"]):
        correct = st.session_state.answers[index] == question["answer"]
        label = "✅" if correct else "❌"
        st.write(f"{label} {tr(question['prompt'])}")

    if not st.session_state.get("user"):
        st.info(t("sign_in_to_save"))
    if st.button(t("play_again"), type="primary"):
        reset_quiz(quiz)
        st.rerun()


def render_create_test() -> None:
    user = st.session_state.get("user")
    if not user or user["role"] != "teacher":
        st.warning(t("teacher_only"))
        return

    st.title(t("create_test_title"))
    st.write(t("create_test_hint"))
    question_count = st.number_input(t("questions"), min_value=1, max_value=10, value=3, step=1, key="create_question_count")

    with st.form("create_test_form"):
        title = st.text_input(t("test_title"))
        description = st.text_area(t("test_description"))
        category = st.selectbox(t("test_category"), ["for_you", "geography", "culture", "science"], format_func=lambda value: t(value))
        draft_questions: list[dict] = []
        for index in range(int(question_count)):
            st.subheader(f"{t('question_prompt')} {index + 1}")
            prompt = st.text_area(t("question_prompt"), key=f"create_prompt_{index}")
            options = [
                st.text_input(f"{t('answer_option')} {chr(65 + option_index)}", key=f"create_option_{index}_{option_index}")
                for option_index in range(4)
            ]
            answer = st.selectbox(t("correct_option"), list(range(4)), format_func=lambda option: chr(65 + option), key=f"create_correct_{index}")
            draft_questions.append({"prompt": prompt, "options": options, "answer": answer})
        submitted = st.form_submit_button(t("save_test"), use_container_width=True)

    if not submitted:
        return
    if not title.strip() or not description.strip() or any(
        not question["prompt"].strip() or any(not option.strip() for option in question["options"])
        for question in draft_questions
    ):
        st.error(t("test_required"))
        return

    new_quiz = {
        "id": f"teacher-{uuid4()}",
        "title": localize(title.strip()),
        "description": localize(description.strip()),
        "category": category,
        "difficulty": localize(t("custom_difficulty")),
        "questions": draft_questions,
    }
    store = load_store()
    store["quizzes"].insert(0, new_quiz)
    save_store(store)
    set_page("home")
    st.success(t("save_test"))
    st.rerun()


def render_teacher_results() -> None:
    user = st.session_state.get("user")
    if not user or user["role"] != "teacher":
        st.warning(t("teacher_only"))
        return
    st.title(t("teacher_panel"))
    st.write(t("teacher_panel_hint"))
    if st.button(t("create_test"), type="primary"):
        set_page("create_test")
        st.rerun()
    results = load_store()["results"]
    if not results:
        st.info(t("no_results"))
        return
    rows = [
        {
            t("student_column"): result["user_name"],
            t("quiz_column"): tr(result["quiz_title"]),
            t("score_column"): f"{result['score']} / {result['total']} ({result['percentage']}%)",
            t("date_column"): result["created_at"].replace("T", " "),
        }
        for result in results
    ]
    st.dataframe(rows, use_container_width=True, hide_index=True)


def initialise() -> None:
    defaults = {
        "language": "ru",
        "page": "home",
        "nav": "home",
        "user": None,
        "active_quiz_id": None,
        "question_index": 0,
        "answers": [],
        "answer_checked": False,
        "last_result": None,
    }
    for key, value in defaults.items():
        st.session_state.setdefault(key, value)


st.set_page_config(page_title="Quizly", page_icon="⚡", layout="wide")
initialise()
render_sidebar()

if st.session_state.page == "home":
    render_home()
elif st.session_state.page == "auth":
    render_auth()
elif st.session_state.page == "play":
    render_play()
elif st.session_state.page == "results":
    render_results()
elif st.session_state.page == "create_test":
    render_create_test()
elif st.session_state.page == "teacher_results":
    render_teacher_results()