import json
import datetime

class Note:
    def __init__(self, title, body):
        self.id = id(self)
        self.title = title
        self.body = body
        self.created_at = datetime.datetime.now()

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'body': self.body,
            'created_at': self.created_at.isoformat()
        }

class NoteApp:
    def __init__(self, filename):
        self.filename = filename
        self.notes = self.load_notes()

    def load_notes(self):
        try:
            with open(self.filename, 'r') as f:
                data = json.load(f)
                return [Note(n['title'], n['body']) for n in data]
        except FileNotFoundError:
            return []

    def save_notes(self):
        with open(self.filename, 'w') as f:
            json.dump([note.to_dict() for note in self.notes], f)

    def create_note(self, title, body):
        note = Note(title, body)
        self.notes.append(note)
        self.save_notes()

    def view_notes(self, start_date=None, end_date=None):
        for note in self.notes:
            if start_date and note.created_at < start_date:
                continue
            if end_date and note.created_at > end_date:
                continue
            print(f"ID: {note.id}\nTitle: {note.title}\nBody: {note.body}\nCreated At: {note.created_at}\n---")


    def delete_note(self, note_id):
        self.notes = [note for note in self.notes if note.id != note_id]
        self.save_notes()

    def update_note(self, note_id, title, body):
        for note in self.notes:
            if note.id == note_id:
                note.title = title
                note.body = body
                note.created_at = datetime.datetime.now()
        self.save_notes()

app = NoteApp('notes.json')

while True:
    command = input('Введите команду: \ncreate - создать заметку\nview - просмотреть заметки\nview_date - просмотреть заметки за определенный период\ndelete - удалить заметку\nupdate - обновить заметку\nquit - выйти из программы: ')
    if command == 'create':
        title = input('Введите заголовок: ')
        body = input('Введите текст заметки: ')
        app.create_note(title, body)
    elif command == 'view':
        app.view_notes()
    elif command == 'view_date':
        start_date_str = input('Введите начальную дату (YYYY-MM-DD): ')
        end_date_str = input('Введите конечную дату (YYYY-MM-DD): ')
        start_date = datetime.datetime.strptime(start_date_str, '%Y-%m-%d')
        end_date = datetime.datetime.strptime(end_date_str, '%Y-%m-%d')
        app.view_notes(start_date, end_date)
    elif command == 'delete':
        note_id = int(input('Введите ID заметки: '))
        app.delete_note(note_id)
    elif command == 'update':
        note_id = int(input('Введите ID заметки: '))
        title = input('Введите новый заголовок: ')
        body = input('Введите новый текст заметки: ')
        app.update_note(note_id, title, body)
    elif command == 'quit':
        break
    else:
        print('Неизвестная команда')

