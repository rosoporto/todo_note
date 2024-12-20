import os
import logging
import pandas as pd
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext


# Включим логирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)


class NoteBot:
    def __init__(self, token):
        self.token = token
        self.updater = Updater(token)
        self.dispatcher = self.updater.dispatcher
        self.notes_file = 'data/notes.csv'

        # Загрузим заметки
        self.notes = self.load_notes()

        # Добавим обработчики команд
        self.dispatcher.add_handler(CommandHandler("start", self.send_command_overview))
        self.dispatcher.add_handler(CommandHandler("add", self.add_note))
        self.dispatcher.add_handler(CommandHandler("show", self.show_notes))
        self.dispatcher.add_handler(CommandHandler("mark", self.mark_note))
        self.dispatcher.add_handler(CommandHandler("delete", self.delete_note))

    def load_notes(self):
        if not os.path.exists(self.notes_file) or os.path.getsize(self.notes_file) == 0:
            # Создаем файл с заголовками, если он не существует или пуст
            pd.DataFrame(columns=["note"]).to_csv(self.notes_file, index=False)
            return pd.DataFrame(columns=["note"])  # Возвращаем пустой DataFrame с заголовками
        return pd.read_csv(self.notes_file)

    def save_notes(self):
        self.notes.to_csv(self.notes_file, index=False)

    def send_command_overview(self, update: Update, context: CallbackContext) -> None:
        command_overview = (
            "Добро пожаловать в NoteBot! Вот доступные команды:\n"
            "/add <текст заметки> - Добавить новую заметку.\n"
            "/show - Показать все заметки.\n"
            "/mark <номер заметки> - Пометить заметку как выполненную.\n"
            "/delete <номер заметки> - Удалить заметку.\n"
        )
        update.message.reply_text(command_overview)

    def add_note(self, update: Update, context: CallbackContext) -> None:
        note = ' '.join(context.args)
        print(context.args)  # Это должно выводить список аргументов
        if note:
            # Создаем новый DataFrame для добавляемой заметки
            new_note = pd.DataFrame({'note': [note], 'status': ['pending']})

            # Объединяем с существующими заметками
            self.notes = pd.concat([self.notes, new_note], ignore_index=True)

            # Сохраняем обновленный DataFrame обратно в CSV
            self.save_notes()
            update.message.reply_text(f'Заметка добавлена: {note}')
        else:
            update.message.reply_text('Пожалуйста, введите текст заметки.')

    def show_notes(self, update: Update, context: CallbackContext) -> None:
        if self.notes.empty:
            update.message.reply_text('Нет заметок.')
        else:
            response = []
            for index, row in self.notes.iterrows():
                status = '✔️' if row['status'] == 'completed' else '❌'
                response.append(f'{index + 1}. {row["note"]} {status}')
            update.message.reply_text('\n'.join(response))

    def mark_note(self, update: Update, context: CallbackContext) -> None:
        try:
            note_number = int(context.args[0])
            if note_number <= 0 or note_number > len(self.notes):
                update.message.reply_text('Неверный номер заметки.')
                return
            self.notes.at[note_number - 1, 'status'] = 'completed'
            self.save_notes()
            update.message.reply_text(f'Заметка {note_number} помечена как выполненная.')
        except (ValueError, IndexError):
            update.message.reply_text('Пожалуйста, введите корректный номер заметки.')

    def delete_note(self, update: Update, context: CallbackContext) -> None:
        try:
            note_number = int(context.args[0])
            if note_number <= 0 or note_number > len(self.notes):
                update.message.reply_text('Неверный номер заметки.')
                return
            self.notes = self.notes.drop(note_number - 1).reset_index(drop=True)
            self.save_notes()
            update.message.reply_text(f'Заметка {note_number} удалена.')
        except (ValueError, IndexError):
            update.message.reply_text('Пожалуйста, введите корректный номер заметки.')

    def start(self):
        self.updater.start_polling()
        self.updater.idle()


if __name__ == '__main__':
    # Получаем токен из переменной окружения
    token = os.getenv("TELEGRAM_TOKEN")
    if not token:
        raise ValueError("Токен Telegram не установлен. Установите переменную окружения TELEGRAM_TOKEN.")
    
    bot = NoteBot(token)
    bot.start()
