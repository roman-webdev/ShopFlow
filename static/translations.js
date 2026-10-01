'use strict';
const dictionary = {
  "Collection": {
    "en": "Collection",
    "ru": "Коллекция",
    "uk": "Колекція"
  },
  "Our approach": {
    "en": "Our approach",
    "ru": "Наш подход",
    "uk": "Наш підхід"
  },
  "Considered essentials. Small upgrades, lasting favorites.": {
    "en": "Considered essentials. Small upgrades, lasting favorites.",
    "ru": "Продуманные вещи. Маленькие перемены надолго.",
    "uk": "Продумані речі. Маленькі зміни надовго."
  },
  "Demo store · No real charges": {
    "en": "Demo store · No real charges",
    "ru": "Демо-магазин · Без реальных платежей",
    "uk": "Демо-магазин · Без реальних платежів"
  },
  "Bag": {
    "en": "Bag",
    "ru": "Корзина",
    "uk": "Кошик"
  },
  "Wishlist": {
    "en": "Wishlist",
    "ru": "Избранное",
    "uk": "Обране"
  },
  "Language": {
    "en": "Language",
    "ru": "Язык",
    "uk": "Мова"
  },
  "Main navigation": {
    "en": "Main navigation",
    "ru": "Основная навигация",
    "uk": "Основна навігація"
  },
  "Good things. Less noise.": {
    "en": "Good things. Less noise.",
    "ru": "Хорошие вещи. Меньше шума.",
    "uk": "Хороші речі. Менше шуму."
  },
  "Thoughtfully chosen for your everyday.": {
    "en": "Thoughtfully chosen for your everyday.",
    "ru": "Выбрано с заботой о вашем дне.",
    "uk": "Вибрано з турботою про ваш день."
  },
  "Explore": {
    "en": "Explore",
    "ru": "Открывайте",
    "uk": "Відкривайте"
  },
  "Store admin": {
    "en": "Store admin",
    "ru": "Управление магазином",
    "uk": "Керування магазином"
  },
  "A portfolio project by Roman": {
    "en": "A portfolio project by Roman",
    "ru": "Проект для портфолио Романа",
    "uk": "Проєкт для портфоліо Романа"
  },
  "No physical deliveries. Local illustrative product assets.": {
    "en": "No physical deliveries. Local illustrative product assets.",
    "ru": "Без доставки. Локальные иллюстрации товаров.",
    "uk": "Без доставки. Локальні ілюстрації товарів."
  },
  "OBJECTS FOR A BETTER EVERYDAY": {
    "en": "OBJECTS FOR A BETTER EVERYDAY",
    "ru": "ВЕЩИ, КОТОРЫЕ ДЕЛАЮТ ДЕНЬ ЛУЧШЕ",
    "uk": "РЕЧІ, ЩО РОБЛЯТЬ ДЕНЬ КРАЩИМ"
  },
  "Small upgrades.": {
    "en": "Small upgrades.",
    "ru": "Маленькие перемены.",
    "uk": "Маленькі зміни."
  },
  "Better days.": {
    "en": "Better days.",
    "ru": "Лучше каждый день.",
    "uk": "Краще щодня."
  },
  "Meet your next everyday favorite. Considered design, useful details, and a little more joy in the ordinary.": {
    "en": "Meet your next everyday favorite. Considered design, useful details, and a little more joy in the ordinary.",
    "ru": "Найдите свою новую любимую вещь. Продуманный дизайн, полезные детали и больше радости в привычном.",
    "uk": "Знайдіть свою нову улюблену річ. Продуманий дизайн, корисні деталі й більше радості у звичному."
  },
  "Explore the collection": {
    "en": "Explore the collection",
    "ru": "Открыть коллекцию",
    "uk": "Відкрити колекцію"
  },
  "Selected with purpose. Made for daily life.": {
    "en": "Selected with purpose. Made for daily life.",
    "ru": "Выбрано со смыслом. Для каждого дня.",
    "uk": "Вибрано зі змістом. Для кожного дня."
  },
  "IN FOCUS": {
    "en": "IN FOCUS",
    "ru": "В ФОКУСЕ",
    "uk": "У ФОКУСІ"
  },
  "Studio headphones": {
    "en": "Studio headphones",
    "ru": "Студийные наушники",
    "uk": "Студійні навушники"
  },
  "Find your focus": {
    "en": "Find your focus",
    "ru": "Найдите свой фокус",
    "uk": "Знайдіть свій фокус"
  },
  "Sound, without the noise.": {
    "en": "Sound, without the noise.",
    "ru": "Звук без лишнего шума.",
    "uk": "Звук без зайвого шуму."
  },
  "↗ Designed for daily life": {
    "en": "↗ Designed for daily life",
    "ru": "↗ Для каждого дня",
    "uk": "↗ Для кожного дня"
  },
  "◈ Thoughtfully curated": {
    "en": "◈ Thoughtfully curated",
    "ru": "◈ Продуманная коллекция",
    "uk": "◈ Продумана колекція"
  },
  "⌁ Demo shipping included": {
    "en": "⌁ Demo shipping included",
    "ru": "⌁ Демо-доставка включена",
    "uk": "⌁ Демо-доставку включено"
  },
  "◇ Test checkout, zero real charges": {
    "en": "◇ Test checkout, zero real charges",
    "ru": "◇ Тестовая оплата без списаний",
    "uk": "◇ Тестова оплата без списань"
  },
  "Store benefits": {
    "en": "Store benefits",
    "ru": "Преимущества магазина",
    "uk": "Переваги магазину"
  },
  "FIND YOUR FLOW": {
    "en": "FIND YOUR FLOW",
    "ru": "НАЙДИТЕ СВОЙ РИТМ",
    "uk": "ЗНАЙДІТЬ СВІЙ РИТМ"
  },
  "A place for every part of your day.": {
    "en": "A place for every part of your day.",
    "ru": "Для каждого момента вашего дня.",
    "uk": "Для кожної миті вашого дня."
  },
  "Sound": {
    "en": "Sound",
    "ru": "Звук",
    "uk": "Звук"
  },
  "Carry": {
    "en": "Carry",
    "ru": "Сумки",
    "uk": "Сумки"
  },
  "Home": {
    "en": "Home",
    "ru": "Дом",
    "uk": "Дім"
  },
  "Lifestyle": {
    "en": "Lifestyle",
    "ru": "Стиль жизни",
    "uk": "Стиль життя"
  },
  "All": {
    "en": "All",
    "ru": "Все",
    "uk": "Усі"
  },
  "THE EVERYDAY EDIT": {
    "en": "THE EVERYDAY EDIT",
    "ru": "КОЛЛЕКЦИЯ НА КАЖДЫЙ ДЕНЬ",
    "uk": "КОЛЕКЦІЯ НА ЩОДЕНЬ"
  },
  "The collection": {
    "en": "The collection",
    "ru": "Коллекция",
    "uk": "Колекція"
  },
  "A little upgrade. A lasting favorite.": {
    "en": "A little upgrade. A lasting favorite.",
    "ru": "Маленькая перемена. Любимая вещь надолго.",
    "uk": "Маленька зміна. Улюблена річ надовго."
  },
  "Search the collection": {
    "en": "Search the collection",
    "ru": "Поиск по коллекции",
    "uk": "Пошук у колекції"
  },
  "Search products": {
    "en": "Search products",
    "ru": "Найти товар",
    "uk": "Знайти товар"
  },
  "Maximum price": {
    "en": "Maximum price",
    "ru": "Максимальная цена",
    "uk": "Максимальна ціна"
  },
  "Any price": {
    "en": "Any price",
    "ru": "Любая цена",
    "uk": "Будь-яка ціна"
  },
  "In stock only": {
    "en": "In stock only",
    "ru": "Только в наличии",
    "uk": "Лише в наявності"
  },
  "Sort by": {
    "en": "Sort by",
    "ru": "Сортировка",
    "uk": "Сортування"
  },
  "Filter category": {
    "en": "Filter category",
    "ru": "Фильтр категории",
    "uk": "Фільтр категорії"
  },
  "Featured": {
    "en": "Featured",
    "ru": "Рекомендуемые",
    "uk": "Рекомендовані"
  },
  "Newest": {
    "en": "Newest",
    "ru": "Сначала новые",
    "uk": "Спочатку нові"
  },
  "Price: low to high": {
    "en": "Price: low to high",
    "ru": "Цена по возрастанию",
    "uk": "Ціна за зростанням"
  },
  "Price: high to low": {
    "en": "Price: high to low",
    "ru": "Цена по убыванию",
    "uk": "Ціна за спаданням"
  },
  "LESS, BUT BETTER": {
    "en": "LESS, BUT BETTER",
    "ru": "МЕНЬШЕ, НО ЛУЧШЕ",
    "uk": "МЕНШЕ, АЛЕ КРАЩЕ"
  },
  "Room for what": {
    "en": "Room for what",
    "ru": "Место для того,",
    "uk": "Місце для того,"
  },
  "really matters.": {
    "en": "really matters.",
    "ru": "что важно.",
    "uk": "що важливо."
  },
  "Useful, beautiful, quietly different. We choose objects that earn their place in your life, one small detail at a time.": {
    "en": "Useful, beautiful, quietly different. We choose objects that earn their place in your life, one small detail at a time.",
    "ru": "Полезные, красивые, особенные. Мы выбираем вещи, которые заслуживают места в вашей жизни — деталь за деталью.",
    "uk": "Корисні, красиві, особливі. Ми вибираємо речі, що заслуговують місця у вашому житті — деталь за деталлю."
  },
  "Find your essentials": {
    "en": "Find your essentials",
    "ru": "Найти свои вещи",
    "uk": "Знайти свої речі"
  },
  "THE SLOW MORNING EDIT": {
    "en": "THE SLOW MORNING EDIT",
    "ru": "ДЛЯ НЕСПЕШНОГО УТРА",
    "uk": "ДЛЯ НЕКВАПЛИВОГО РАНКУ"
  },
  "LITTLE THINGS, BIG DIFFERENCE": {
    "en": "LITTLE THINGS, BIG DIFFERENCE",
    "ru": "МАЛЕНЬКИЕ ВЕЩИ МЕНЯЮТ МНОГОЕ",
    "uk": "МАЛЕНЬКІ РЕЧІ ЗМІНЮЮТЬ БАГАТО"
  },
  "Everyday favorites, in their words.": {
    "en": "Everyday favorites, in their words.",
    "ru": "Любимые вещи — словами покупателей.",
    "uk": "Улюблені речі — словами покупців."
  },
  "Illustrative reviews for this portfolio demo.": {
    "en": "Illustrative reviews for this portfolio demo.",
    "ru": "Примеры отзывов для демо-проекта.",
    "uk": "Приклади відгуків для демо-проєкту."
  },
  "The kind of details you notice every morning. Simple, useful, beautiful.": {
    "en": "The kind of details you notice every morning. Simple, useful, beautiful.",
    "ru": "Детали, которые замечаешь каждое утро. Просто, полезно и красиво.",
    "uk": "Деталі, які помічаєш щоранку. Просто, корисно й красиво."
  },
  "My daily setup feels a little calmer. The headphones are my new favorite.": {
    "en": "My daily setup feels a little calmer. The headphones are my new favorite.",
    "ru": "Рабочее место стало спокойнее. Наушники — моя новая любимая вещь.",
    "uk": "Робоче місце стало спокійнішим. Навушники — моя нова улюблена річ."
  },
  "Everything I need, nothing extra. A thoughtful collection worth exploring.": {
    "en": "Everything I need, nothing extra. A thoughtful collection worth exploring.",
    "ru": "Всё нужное, ничего лишнего. Продуманная коллекция, которую стоит изучить.",
    "uk": "Усе потрібне, нічого зайвого. Продумана колекція, яку варто дослідити."
  },
  "Home collection · Demo review": {
    "en": "Home collection · Demo review",
    "ru": "Для дома · Демо-отзыв",
    "uk": "Для дому · Демо-відгук"
  },
  "Sound collection · Demo review": {
    "en": "Sound collection · Demo review",
    "ru": "Звук · Демо-отзыв",
    "uk": "Звук · Демо-відгук"
  },
  "Carry collection · Demo review": {
    "en": "Carry collection · Demo review",
    "ru": "Сумки · Демо-отзыв",
    "uk": "Сумки · Демо-відгук"
  },
  "A LITTLE GOOD IN YOUR INBOX": {
    "en": "A LITTLE GOOD IN YOUR INBOX",
    "ru": "НЕМНОГО ХОРОШЕГО В ВАШЕЙ ПОЧТЕ",
    "uk": "ТРОХИ ХОРОШОГО У ВАШІЙ ПОШТІ"
  },
  "Stay in the flow.": {
    "en": "Stay in the flow.",
    "ru": "Будьте в ритме.",
    "uk": "Будьте в ритмі."
  },
  "New finds, fresh ideas. A demo signup, no emails sent.": {
    "en": "New finds, fresh ideas. A demo signup, no emails sent.",
    "ru": "Новые находки и идеи. Демо-подписка без отправки писем.",
    "uk": "Нові знахідки та ідеї. Демо-підписка без надсилання листів."
  },
  "Your email": {
    "en": "Your email",
    "ru": "Ваш email",
    "uk": "Ваш email"
  },
  "Email address": {
    "en": "Email address",
    "ru": "Адрес email",
    "uk": "Адреса email"
  },
  "Join the list": {
    "en": "Join the list",
    "ru": "Подписаться",
    "uk": "Підписатися"
  },
  "Your bag": {
    "en": "Your bag",
    "ru": "Ваша корзина",
    "uk": "Ваш кошик"
  },
  "Continue to checkout": {
    "en": "Continue to checkout",
    "ru": "Перейти к оформлению",
    "uk": "Перейти до оформлення"
  },
  "Clear bag": {
    "en": "Clear bag",
    "ru": "Очистить корзину",
    "uk": "Очистити кошик"
  },
  "Continue shopping": {
    "en": "Continue shopping",
    "ru": "Продолжить покупки",
    "uk": "Продовжити покупки"
  },
  "Checkout": {
    "en": "Checkout",
    "ru": "Оформление заказа",
    "uk": "Оформлення замовлення"
  },
  "Full name": {
    "en": "Full name",
    "ru": "Имя и фамилия",
    "uk": "Ім’я та прізвище"
  },
  "Email": {
    "en": "Email",
    "ru": "Email",
    "uk": "Email"
  },
  "Phone": {
    "en": "Phone",
    "ru": "Телефон",
    "uk": "Телефон"
  },
  "City": {
    "en": "City",
    "ru": "Город",
    "uk": "Місто"
  },
  "Street address": {
    "en": "Street address",
    "ru": "Адрес доставки",
    "uk": "Адреса доставки"
  },
  "Order summary": {
    "en": "Order summary",
    "ru": "Ваш заказ",
    "uk": "Ваше замовлення"
  },
  "USD · Demo shipping included · No additional charges": {
    "en": "USD · Demo shipping included · No additional charges",
    "ru": "USD · Демо-доставка включена · Без доплат",
    "uk": "USD · Демо-доставку включено · Без доплат"
  },
  "Close product": {
    "en": "Close product",
    "ru": "Закрыть товар",
    "uk": "Закрити товар"
  },
  "Close bag": {
    "en": "Close bag",
    "ru": "Закрыть корзину",
    "uk": "Закрити кошик"
  },
  "Close checkout": {
    "en": "Close checkout",
    "ru": "Закрыть оформление",
    "uk": "Закрити оформлення"
  },
  "Loading": {
    "en": "Loading",
    "ru": "Загрузка",
    "uk": "Завантаження"
  },
  "New": {
    "en": "New",
    "ru": "Новинка",
    "uk": "Новинка"
  },
  "Sale": {
    "en": "Sale",
    "ru": "Скидка",
    "uk": "Знижка"
  },
  "Bestseller": {
    "en": "Bestseller",
    "ru": "Бестселлер",
    "uk": "Бестселер"
  },
  "Sold out": {
    "en": "Sold out",
    "ru": "Нет в наличии",
    "uk": "Немає в наявності"
  },
  "Available now": {
    "en": "Available now",
    "ru": "В наличии",
    "uk": "У наявності"
  },
  "Back soon": {
    "en": "Back soon",
    "ru": "Скоро вернётся",
    "uk": "Незабаром повернеться"
  },
  "Add to bag": {
    "en": "Add to bag",
    "ru": "В корзину",
    "uk": "У кошик"
  },
  "Added to your bag": {
    "en": "Added to your bag",
    "ru": "Добавлено в корзину",
    "uk": "Додано в кошик"
  },
  "Removed from your bag": {
    "en": "Removed from your bag",
    "ru": "Удалено из корзины",
    "uk": "Видалено з кошика"
  },
  "Bag cleared": {
    "en": "Bag cleared",
    "ru": "Корзина очищена",
    "uk": "Кошик очищено"
  },
  "Quantity": {
    "en": "Quantity",
    "ru": "Количество",
    "uk": "Кількість"
  },
  "Increase quantity": {
    "en": "Increase quantity",
    "ru": "Увеличить количество",
    "uk": "Збільшити кількість"
  },
  "Decrease quantity": {
    "en": "Decrease quantity",
    "ru": "Уменьшить количество",
    "uk": "Зменшити кількість"
  },
  "Remove": {
    "en": "Remove",
    "ru": "Удалить",
    "uk": "Видалити"
  },
  "Total": {
    "en": "Total",
    "ru": "Итого",
    "uk": "Разом"
  },
  "Your bag is waiting for something good.": {
    "en": "Your bag is waiting for something good.",
    "ru": "Ваша корзина ждёт любимых вещей.",
    "uk": "Ваш кошик чекає на улюблені речі."
  },
  "No products found. Try different filters.": {
    "en": "No products found. Try different filters.",
    "ru": "Товаров не найдено. Измените фильтры.",
    "uk": "Товарів не знайдено. Змініть фільтри."
  },
  "Reset filters": {
    "en": "Reset filters",
    "ru": "Сбросить фильтры",
    "uk": "Скинути фільтри"
  },
  "Variant": {
    "en": "Variant",
    "ru": "Вариант",
    "uk": "Варіант"
  },
  "Standard": {
    "en": "Standard",
    "ru": "Стандартный",
    "uk": "Стандартний"
  },
  "In stock": {
    "en": "In stock",
    "ru": "В наличии",
    "uk": "У наявності"
  },
  "You might also like": {
    "en": "You might also like",
    "ru": "Вам также понравится",
    "uk": "Вам також сподобається"
  },
  "Saved to wishlist": {
    "en": "Saved to wishlist",
    "ru": "Добавлено в избранное",
    "uk": "Додано до обраного"
  },
  "Removed from wishlist": {
    "en": "Removed from wishlist",
    "ru": "Удалено из избранного",
    "uk": "Видалено з обраного"
  },
  "Stock limit reached": {
    "en": "Stock limit reached",
    "ru": "Достигнут лимит наличия",
    "uk": "Досягнуто ліміту наявності"
  },
  "Demo signup complete. No email will be sent.": {
    "en": "Demo signup complete. No email will be sent.",
    "ru": "Демо-подписка оформлена. Письма не отправляются.",
    "uk": "Демо-підписку оформлено. Листи не надсилаються."
  },
  "Demo checkout: no card details or real charges.": {
    "en": "Demo checkout: no card details or real charges.",
    "ru": "Демо-заказ без данных карты и реальных списаний.",
    "uk": "Демо-замовлення без даних картки та реальних списань."
  },
  "Stripe test checkout: no real payments.": {
    "en": "Stripe test checkout: no real payments.",
    "ru": "Тестовый Stripe checkout без реальных платежей.",
    "uk": "Тестовий Stripe checkout без реальних платежів."
  },
  "Place demo order": {
    "en": "Place demo order",
    "ru": "Оформить демо-заказ",
    "uk": "Оформити демо-замовлення"
  },
  "Continue to Stripe test": {
    "en": "Continue to Stripe test",
    "ru": "Перейти в тестовый Stripe",
    "uk": "Перейти в тестовий Stripe"
  },
  "Processing…": {
    "en": "Processing…",
    "ru": "Обработка…",
    "uk": "Обробка…"
  },
  "Unable to load the store. Please refresh.": {
    "en": "Unable to load the store. Please refresh.",
    "ru": "Не удалось загрузить магазин. Обновите страницу.",
    "uk": "Не вдалося завантажити магазин. Оновіть сторінку."
  },
  "Checkout failed. Please check your details and try again.": {
    "en": "Checkout failed. Please check your details and try again.",
    "ru": "Не удалось оформить заказ. Проверьте данные и повторите.",
    "uk": "Не вдалося оформити замовлення. Перевірте дані та повторіть."
  },
  "STORE MANAGEMENT": {
    "en": "STORE MANAGEMENT",
    "ru": "УПРАВЛЕНИЕ МАГАЗИНОМ",
    "uk": "КЕРУВАННЯ МАГАЗИНОМ"
  },
  "Dashboard": {
    "en": "Dashboard",
    "ru": "Панель управления",
    "uk": "Панель керування"
  },
  "Sign out": {
    "en": "Sign out",
    "ru": "Выйти",
    "uk": "Вийти"
  },
  "Products": {
    "en": "Products",
    "ru": "Товары",
    "uk": "Товари"
  },
  "Orders": {
    "en": "Orders",
    "ru": "Заказы",
    "uk": "Замовлення"
  },
  "View store": {
    "en": "View store",
    "ru": "Открыть магазин",
    "uk": "Відкрити магазин"
  },
  "Revenue (demo/test)": {
    "en": "Revenue (demo/test)",
    "ru": "Выручка (демо/тест)",
    "uk": "Виторг (демо/тест)"
  },
  "To fulfill": {
    "en": "To fulfill",
    "ru": "К выполнению",
    "uk": "До виконання"
  },
  "Add product +": {
    "en": "Add product +",
    "ru": "Добавить товар +",
    "uk": "Додати товар +"
  },
  "Product": {
    "en": "Product",
    "ru": "Товар",
    "uk": "Товар"
  },
  "Category": {
    "en": "Category",
    "ru": "Категория",
    "uk": "Категорія"
  },
  "Price": {
    "en": "Price",
    "ru": "Цена",
    "uk": "Ціна"
  },
  "Status": {
    "en": "Status",
    "ru": "Статус",
    "uk": "Статус"
  },
  "Action": {
    "en": "Action",
    "ru": "Действие",
    "uk": "Дія"
  },
  "Hidden": {
    "en": "Hidden",
    "ru": "Скрыт",
    "uk": "Прихований"
  },
  "Available": {
    "en": "Available",
    "ru": "В наличии",
    "uk": "У наявності"
  },
  "Edit ↗": {
    "en": "Edit ↗",
    "ru": "Изменить ↗",
    "uk": "Змінити ↗"
  },
  "Latest orders": {
    "en": "Latest orders",
    "ru": "Последние заказы",
    "uk": "Останні замовлення"
  },
  "Order": {
    "en": "Order",
    "ru": "Заказ",
    "uk": "Замовлення"
  },
  "Customer": {
    "en": "Customer",
    "ru": "Покупатель",
    "uk": "Покупець"
  },
  "Payment status": {
    "en": "Payment status",
    "ru": "Статус оплаты",
    "uk": "Статус оплати"
  },
  "Created": {
    "en": "Created",
    "ru": "Создан",
    "uk": "Створено"
  },
  "No orders yet. Try the storefront checkout.": {
    "en": "No orders yet. Try the storefront checkout.",
    "ru": "Заказов пока нет. Оформите заказ в магазине.",
    "uk": "Замовлень ще немає. Оформіть замовлення в магазині."
  },
  "← Dashboard": {
    "en": "← Dashboard",
    "ru": "← Панель управления",
    "uk": "← Панель керування"
  },
  "Edit product": {
    "en": "Edit product",
    "ru": "Редактировать товар",
    "uk": "Редагувати товар"
  },
  "New product": {
    "en": "New product",
    "ru": "Новый товар",
    "uk": "Новий товар"
  },
  "Name": {
    "en": "Name",
    "ru": "Название",
    "uk": "Назва"
  },
  "Image URL": {
    "en": "Image URL",
    "ru": "Путь к изображению",
    "uk": "Шлях до зображення"
  },
  "Description": {
    "en": "Description",
    "ru": "Описание",
    "uk": "Опис"
  },
  "Price (USD)": {
    "en": "Price (USD)",
    "ru": "Цена (USD)",
    "uk": "Ціна (USD)"
  },
  "Stock": {
    "en": "Stock",
    "ru": "Остаток",
    "uk": "Залишок"
  },
  "Variants (comma-separated)": {
    "en": "Variants (comma-separated)",
    "ru": "Варианты (через запятую)",
    "uk": "Варіанти (через кому)"
  },
  "Badge": {
    "en": "Badge",
    "ru": "Метка",
    "uk": "Позначка"
  },
  "None": {
    "en": "None",
    "ru": "Нет",
    "uk": "Немає"
  },
  "Localized names and descriptions (JSON)": {
    "en": "Localized names and descriptions (JSON)",
    "ru": "Названия и описания на разных языках (JSON)",
    "uk": "Назви й описи різними мовами (JSON)"
  },
  "Visible in store": {
    "en": "Visible in store",
    "ru": "Показывать в магазине",
    "uk": "Показувати в магазині"
  },
  "Available to order": {
    "en": "Available to order",
    "ru": "Доступен для заказа",
    "uk": "Доступний для замовлення"
  },
  "Save product ↗": {
    "en": "Save product ↗",
    "ru": "Сохранить товар ↗",
    "uk": "Зберегти товар ↗"
  },
  "Welcome back.": {
    "en": "Welcome back.",
    "ru": "С возвращением.",
    "uk": "З поверненням."
  },
  "Sign in to manage products and orders.": {
    "en": "Sign in to manage products and orders.",
    "ru": "Войдите для управления товарами и заказами.",
    "uk": "Увійдіть для керування товарами та замовленнями."
  },
  "Username": {
    "en": "Username",
    "ru": "Имя пользователя",
    "uk": "Ім’я користувача"
  },
  "Password": {
    "en": "Password",
    "ru": "Пароль",
    "uk": "Пароль"
  },
  "Sign in ↗": {
    "en": "Sign in ↗",
    "ru": "Войти ↗",
    "uk": "Увійти ↗"
  },
  "Invalid username or password.": {
    "en": "Invalid username or password.",
    "ru": "Неверное имя пользователя или пароль.",
    "uk": "Неправильне ім’я користувача або пароль."
  },
  "Too many attempts. Try again in 15 minutes.": {
    "en": "Too many attempts. Try again in 15 minutes.",
    "ru": "Слишком много попыток. Повторите через 15 минут.",
    "uk": "Забагато спроб. Повторіть через 15 хвилин."
  },
  "Check fields: positive price with two decimals and a local image URL, valid stock and comma-separated variants.": {
    "en": "Check fields: positive price with two decimals and a local image URL, valid stock and comma-separated variants.",
    "ru": "Проверьте цену, локальный путь изображения, остаток, варианты и JSON переводов.",
    "uk": "Перевірте ціну, локальний шлях зображення, залишок, варіанти та JSON перекладів."
  },
  "ORDER DETAILS": {
    "en": "ORDER DETAILS",
    "ru": "ДЕТАЛИ ЗАКАЗА",
    "uk": "ДЕТАЛІ ЗАМОВЛЕННЯ"
  },
  "THANK YOU FOR EXPLORING SHOPFLOW": {
    "en": "THANK YOU FOR EXPLORING SHOPFLOW",
    "ru": "СПАСИБО ЗА ЗАКАЗ В SHOPFLOW",
    "uk": "ДЯКУЄМО ЗА ЗАМОВЛЕННЯ В SHOPFLOW"
  },
  "Demo checkout complete. No money was charged.": {
    "en": "Demo checkout complete. No money was charged.",
    "ru": "Демо-заказ оформлен. Деньги не списывались.",
    "uk": "Демо-замовлення оформлено. Гроші не списувалися."
  },
  "Stripe test payment confirmed. No real money was charged.": {
    "en": "Stripe test payment confirmed. No real money was charged.",
    "ru": "Тестовая оплата Stripe подтверждена. Реальные деньги не списывались.",
    "uk": "Тестову оплату Stripe підтверджено. Реальні гроші не списувалися."
  },
  "This portfolio store does not ship physical products.": {
    "en": "This portfolio store does not ship physical products.",
    "ru": "Этот демо-магазин не доставляет реальные товары.",
    "uk": "Цей демо-магазин не доставляє реальні товари."
  },
  "Back to the collection ↗": {
    "en": "Back to the collection ↗",
    "ru": "Вернуться к коллекции ↗",
    "uk": "Повернутися до колекції ↗"
  },
  "Fulfillment status": {
    "en": "Fulfillment status",
    "ru": "Статус выполнения",
    "uk": "Статус виконання"
  },
  "Update status": {
    "en": "Update status",
    "ru": "Обновить статус",
    "uk": "Оновити статус"
  },
  "unfulfilled": {
    "en": "unfulfilled",
    "ru": "Новый",
    "uk": "Новий"
  },
  "processing": {
    "en": "processing",
    "ru": "В обработке",
    "uk": "В обробці"
  },
  "shipped": {
    "en": "shipped",
    "ru": "Отправлен",
    "uk": "Відправлено"
  },
  "cancelled": {
    "en": "cancelled",
    "ru": "Отменён",
    "uk": "Скасовано"
  },
  "pending": {
    "en": "pending",
    "ru": "Ожидает оплаты",
    "uk": "Очікує оплати"
  },
  "demo_paid": {
    "en": "demo_paid",
    "ru": "Демо-заказ оформлен",
    "uk": "Демо-замовлення оформлено"
  },
  "paid_test": {
    "en": "paid_test",
    "ru": "Тестовая оплата подтверждена",
    "uk": "Тестову оплату підтверджено"
  },
  "payment_error": {
    "en": "payment_error",
    "ru": "Ошибка оплаты",
    "uk": "Помилка оплати"
  },
  "Graphite": {
    "en": "Graphite",
    "ru": "Графит",
    "uk": "Графіт"
  },
  "Sand": {
    "en": "Sand",
    "ru": "Песочный",
    "uk": "Пісочний"
  },
  "Ink": {
    "en": "Ink",
    "ru": "Чернильный",
    "uk": "Чорнильний"
  },
  "Olive": {
    "en": "Olive",
    "ru": "Оливковый",
    "uk": "Оливковий"
  },
  "Silver": {
    "en": "Silver",
    "ru": "Серебристый",
    "uk": "Сріблястий"
  },
  "Black": {
    "en": "Black",
    "ru": "Чёрный",
    "uk": "Чорний"
  },
  "Chalk": {
    "en": "Chalk",
    "ru": "Молочный",
    "uk": "Молочний"
  },
  "Clay": {
    "en": "Clay",
    "ru": "Терракотовый",
    "uk": "Теракотовий"
  },
  "Cream": {
    "en": "Cream",
    "ru": "Кремовый",
    "uk": "Кремовий"
  },
  "Blue": {
    "en": "Blue",
    "ru": "Синий",
    "uk": "Синій"
  },
  "Body": {
    "en": "Body",
    "ru": "Корпус",
    "uk": "Корпус"
  },
  "Kit": {
    "en": "Kit",
    "ru": "Комплект",
    "uk": "Комплект"
  },
  "Natural": {
    "en": "Natural",
    "ru": "Натуральный",
    "uk": "Натуральний"
  },
  "A5 / Ink": {
    "en": "A5 / Ink",
    "ru": "A5 / Чернильный",
    "uk": "A5 / Чорнильний"
  },
  "A5 / Clay": {
    "en": "A5 / Clay",
    "ru": "A5 / Терракотовый",
    "uk": "A5 / Теракотовий"
  },
  "Considered essentials for living, working and unwinding.": {
    "en": "Considered essentials for living, working and unwinding.",
    "ru": "Продуманные вещи для жизни, работы и отдыха.",
    "uk": "Продумані речі для життя, роботи та відпочинку."
  },
  "ShopFlow — everyday, elevated": {
    "en": "ShopFlow — everyday, elevated",
    "ru": "ShopFlow — лучше каждый день",
    "uk": "ShopFlow — краще щодня"
  }
};

dictionary['WORTH A CLOSER LOOK']={en:'WORTH A CLOSER LOOK',ru:'ПРИСМОТРИТЕСЬ К ДЕТАЛЯМ',uk:'ПРИДИВІТЬСЯ ДО ДЕТАЛЕЙ'};
dictionary['Your next daily favorite.']={en:'Your next daily favorite.',ru:'Любимые вещи на каждый день.',uk:'Улюблені речі на щодень.'};
dictionary['Best sellers']={en:'Best sellers',ru:'Бестселлеры',uk:'Бестселери'};
dictionary['New arrivals']={en:'New arrivals',ru:'Новинки',uk:'Новинки'};
dictionary['Featured collections']={en:'Featured collections',ru:'Рекомендуемые коллекции',uk:'Рекомендовані колекції'};

dictionary['Variants']={en:'Variants',ru:'Варианты',uk:'Варіанти'};

Object.assign(dictionary,{
'Considered objects':{en:'Considered objects',ru:'Продуманных вещей',uk:'Продуманих речей'},
'Daily rituals':{en:'Daily rituals',ru:'Ритма жизни',uk:'Ритми життя'},
'Your own flow':{en:'Your own flow',ru:'Твой собственный ритм',uk:'Твій власний ритм'},
'ONE DAY. YOUR WAY.':{en:'ONE DAY. YOUR WAY.',ru:'ТВОЙ ДЕНЬ. ТВОИ ПРАВИЛА.',uk:'ТВІЙ ДЕНЬ. ТВОЇ ПРАВИЛА.'},
'Good design moves with you.':{en:'Good design moves with you.',ru:'Дизайн в твоём ритме.',uk:'Дизайн у твоєму ритмі.'},
'From the first sip to the last idea. Explore the objects that make your day feel different.':{en:'From the first sip to the last idea. Explore the objects that make your day feel different.',ru:'От первого глотка до последней идеи. Открой вещи, с которыми обычный день становится особенным.',uk:'Від першого ковтка до останньої ідеї. Відкрий речі, з якими звичайний день стає особливим.'},
'A slower morning.':{en:'A slower morning.',ru:'Утро без спешки.',uk:'Ранок без поспіху.'},
'Find your focus.':{en:'Find your focus.',ru:'Поймай фокус.',uk:'Знайди свій фокус.'},
'Take it with you.':{en:'Take it with you.',ru:'Бери с собой.',uk:'Бери з собою.'}
});
Object.assign(dictionary,{
'Small upgrades.':{en:'Small upgrades.',ru:'Твой ритм.',uk:'Твій ритм.'},
'Better days.':{en:'Better days.',ru:'Твои вещи.',uk:'Твої речі.'}
});

dictionary['Demo products. No physical deliveries.']={en:'Demo products. No physical deliveries.',ru:'Демо-товары. Без реальной доставки.',uk:'Демо-товари. Без реальної доставки.'};
