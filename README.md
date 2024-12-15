# Todo Note Bot

Это Telegram-бот для управления заметками. Вы можете добавлять, отображать, помечать и удалять заметки с помощью простых команд.

## Установка

### Предварительные требования

- Python 3.9 или выше
- pip
- Telegram-аккаунт для использования бота

### Клонирование репозитория

```bash
git clone https://github.com/rosoporto/todo_note.git
cd todo_note
```

### Создание и активация виртуального окружения
```bash
python -m venv venv
source venv/bin/activate
```

### Установите зависимости с помощью pip:

```bash
pip install -r requirements.txt
```

### Настройка

Получите токен для вашего бота от BotFather.
Установите переменную окружения TELEGRAM_TOKEN с вашим токеном:

```bash
export TELEGRAM_TOKEN="ваш_токен_здесь"
```

### Использование

Запустите бота:

```bash
python todo_note/bot.py
```

Команды:

* Добавление заметки: /add <ваша заметка>
* * Пример: /add Купить молоко
* Показ всех заметок: /show
* Пометка заметки как выполненной: /mark <номер заметки>
* * Пример: /mark 1
* Удаление заметки: /delete <номер заметки>
* * Пример: /delete 2

### Docker

Вы также можете запустить бота в Docker. Для этого выполните следующие шаги:

#### Сборка образа:

```bash
docker build -t todo_note .
```

#### Запуск контейнера

```bash
docker run -d --name todo_note_container -e TELEGRAM_TOKEN="ваш_токен_здесь" todo_note
```

### Контрибьюция

Если вы хотите внести изменения в проект, пожалуйста, создайте форк репозитория и отправьте пулл-реквест.