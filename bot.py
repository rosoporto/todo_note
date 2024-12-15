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
        self.notes_file = 'notes.csv'

        # Загрузим заметки
        self.notes = self.load_notes()

        # Добавим обработчики команд
        self.dispatcher.add_handler(CommandHandler("add", self.add_note))
        self.dispatcher.add_handler(CommandHandler("show", self.show_notes))
        self.dispatcher.add_handler(CommandHandler("mark", self.mark_note))
        self.dispatcher.add_handler(CommandHandler("delete", self.delete_note))

    def load_notes(self):
        try:
            return pd.read_csv(self.notes_file)
        except FileNotFoundError:
            return pd.DataFrame(columns=['note', 'status'])

    def save_notes(self):
        self.notes.to_csv(self.notes_file, index=False)

    def add_note(self, update: Update, context: CallbackContext) -> None:
        note = ' '.join(context.args)
        if note:
            self.notes = self.notes.append({'note': note, 'status': 'pending'}, ignore_index=True)
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