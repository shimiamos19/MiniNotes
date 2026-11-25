import sys
import os
import json
import random
import uuid

from datetime import datetime, timedelta

from PySide6.QtWidgets import (
    QApplication, QWidget, QDialog, QLabel, QLineEdit, QTextEdit,
    QPushButton, QListWidget, QListWidgetItem, QVBoxLayout, QHBoxLayout,
    QMessageBox, QFrame, QCheckBox, QCalendarWidget, QToolButton,
    QComboBox, QStackedWidget, QFileDialog, QSystemTrayIcon,
    QMenu, QStyle, QSizeGrip
)

from PySide6.QtCore import (
    Qt, QDate, QTime, QUrl, QTimer, QLocale, QPoint
)

from PySide6.QtGui import QIcon, QDesktopServices


APP_VERSION = "1.5.0"
RELEASE_DATE = "25/11/2026"


def resource_path(relative_path):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)

    return os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        relative_path
    )


DATA_DIR = os.path.join(
    os.path.expanduser("~"),
    ".local",
    "share",
    "MiniNotes"
)

os.makedirs(DATA_DIR, exist_ok=True)

NOTES_FILE = os.path.join(DATA_DIR, "notes.json")
SETTINGS_FILE = os.path.join(DATA_DIR, "settings.json")


COLORS = {
    "pink": "#F8DCE5",
    "yellow": "#FFF0B8",
    "green": "#DCEFD9",
    "blue": "#DCEBFA",
    "white": "#FFFFFF"
}


TEXT = {
    "he": {
        "app_subtitle": "המקום הפשוט שלך למחשבות",
        "notes": "הפתקים שלי",
        "welcome": "ברוכים הבאים ל-MiniNotes\n\nבחרו פתק מהרשימה כדי לפתוח אותו.",
        "new_note": "+ יצירת פתק חדש",
        "saved_count": "{n} פתקים שמורים",
        "menu": "תפריט",
        "settings": "הגדרות",
        "about": "מידע על MiniNotes",
        "exit": "יציאה",
        "new": "פתק חדש",
        "edit": "עריכת פתק",
        "title": "כותרת הפתק",
        "title_ph": "כתוב כותרת...",
        "content": "תוכן הפתק",
        "content_ph": "כתוב כאן את המחשבות שלך...",
        "add_due": "להגדיר תאריך ושעה למשימה",
        "date": "תאריך:",
        "time": "שעה:",
        "save": "שמירה",
        "cancel": "ביטול",
        "missing_title": "יש להזין כותרת לפתק.",
        "missing_content": "יש להזין תוכן לפתק.",
        "past_due": "אי אפשר לקבוע משימה למועד שכבר עבר.",
        "edit_note": "עריכת פתק",
        "delete_note": "מחיקת פתק",
        "close": "סגירה",
        "add_calendar": "הוספה ליומן",
        "due": "מועד המשימה",
        "confirm_delete": "האם אתה בטוח שברצונך למחוק את הפתק?",
        "info_text": "אפליקציה לניהול פתקים ומשימות.",
        "settings_title": "הגדרות MiniNotes",
        "language": "שפה",
        "language_help": "בחר את שפת הממשק.",
        "notifications": "התראות",
        "notifications_help": "הצג הודעה במחשב כאשר מגיע מועד של משימה.",
        "enable_notifications": "הפעל התראות על מועדי משימות",
        "appearance": "מראה",
        "theme": "ערכת צבעים",
        "light": "בהירה",
        "dark": "כהה",
        "system": "לפי המערכת",
        "font_size": "גודל גופן",
        "normal": "רגיל",
        "large": "גדול",
        "backup": "גיבוי ושחזור",
        "backup_help": "ייצוא ושחזור של הפתקים שלך.",
        "export_backup": "ייצוא גיבוי",
        "import_backup": "ייבוא גיבוי",
        "information": "מידע ועדכונים",
        "version": "גרסה",
        "last_update": "תאריך עדכון",
        "apply": "החל",
        "ok": "אישור",
        "settings_saved": "ההגדרות נשמרו והוחלו.",
        "save_error": "לא ניתן לשמור את ההגדרות: {error}",
        "backup_exported": "הגיבוי יוצא בהצלחה.",
        "backup_imported": "הגיבוי יובא בהצלחה.",
        "backup_error": "פעולת הגיבוי נכשלה: {error}",
        "choose_backup": "בחר קובץ גיבוי",
        "backup_file": "קובצי JSON (*.json)",
        "calendar_missing": "לפתק הזה לא הוגדרו תאריך ושעה.",
        "calendar_created": "אירוע היומן נוצר ונפתח באפליקציית היומן.",
        "calendar_error": "לא ניתן ליצור אירוע ביומן: {error}",
        "calendar_open_error": "קובץ היומן נוצר, אך לא ניתן לפתוח אותו: {path}",
        "notification_title": "הגיע מועד המשימה",
        "notification_text": "{title}",
        "notification_fallback": "הגיע מועד המשימה: {title}",
        "about_title": "מידע על MiniNotes",
        "no_tray": "התראות שולחן העבודה אינן זמינות במחשב זה.",
        "search_ph": "חיפוש לפי כותרת או תוכן...",
        "sort": "מיון לפי",
        "sort_created": "פתקים חדשים",
        "sort_updated": "עודכנו לאחרונה",
        "sort_due": "מועד המשימה הקרוב",
        "sort_title": "סדר אלפביתי",
        "pin": "נעיצת פתק",
        "unpin": "ביטול נעיצה",
        "summary_notes": "פתקים",
        "summary_upcoming": "משימות קרובות",
        "summary_overdue": "משימות באיחור",
        "empty_title": "עדיין אין לך פתקים",
        "empty_text": "זה הזמן ליצור את הפתק הראשון שלך!",
        "no_results": "לא נמצאו פתקים מתאימים לחיפוש.",
        "show_floating": "הצג על שולחן העבודה",
        "remove_floating": "הסר משולחן העבודה",
        "floating_edit": "עריכה",
        "floating_minimize": "מזעור",
        "floating_close": "סגירה",
        "floating_notes": "פתקים צפים",
        "no_floating": "אין כרגע פתקים צפים.",
        "floating_minimized": "ממוזער",
        "restore_all": "החזר את כל הפתקים",
        "floating_help": "אפשר להציג פתקים על שולחן העבודה ולהחזיר אותם לכאן."
    },

    "en": {
        "app_subtitle": "A simple place for your thoughts",
        "notes": "My Notes",
        "welcome": "Welcome to MiniNotes\n\nSelect a note from the list to open it.",
        "new_note": "+ Create a new note",
        "saved_count": "{n} notes saved",
        "menu": "Menu",
        "settings": "Settings",
        "about": "About MiniNotes",
        "exit": "Exit",
        "new": "New note",
        "edit": "Edit note",
        "title": "Note title",
        "title_ph": "Enter a title...",
        "content": "Note content",
        "content_ph": "Write your thoughts here...",
        "add_due": "Set a date and time for this task",
        "date": "Date:",
        "time": "Time:",
        "save": "Save",
        "cancel": "Cancel",
        "missing_title": "Please enter a note title.",
        "missing_content": "Please enter note content.",
        "past_due": "A task cannot be scheduled in the past.",
        "edit_note": "Edit note",
        "delete_note": "Delete note",
        "close": "Close",
        "add_calendar": "Add to calendar",
        "due": "Task due",
        "confirm_delete": "Are you sure you want to delete this note?",
        "info_text": "An application for managing notes and tasks.",
        "settings_title": "MiniNotes Settings",
        "language": "Language",
        "language_help": "Choose the interface language.",
        "notifications": "Notifications",
        "notifications_help": "Show a desktop notification when a task is due.",
        "enable_notifications": "Enable task deadline notifications",
        "appearance": "Appearance",
        "theme": "Color theme",
        "light": "Light",
        "dark": "Dark",
        "system": "System default",
        "font_size": "Font size",
        "normal": "Normal",
        "large": "Large",
        "backup": "Backup & Restore",
        "backup_help": "Export and restore your notes.",
        "export_backup": "Export backup",
        "import_backup": "Import backup",
        "information": "Information & Updates",
        "version": "Version",
        "last_update": "Last updated",
        "apply": "Apply",
        "ok": "OK",
        "settings_saved": "Settings saved and applied.",
        "save_error": "Could not save settings: {error}",
        "backup_exported": "Backup exported successfully.",
        "backup_imported": "Backup imported successfully.",
        "backup_error": "Backup operation failed: {error}",
        "choose_backup": "Choose backup file",
        "backup_file": "JSON files (*.json)",
        "calendar_missing": "No date and time were set for this note.",
        "calendar_created": "The calendar event was created and opened.",
        "calendar_error": "Could not create calendar event: {error}",
        "calendar_open_error": "The calendar file was created but could not be opened: {path}",
        "notification_title": "Task is due",
        "notification_text": "{title}",
        "notification_fallback": "Task is due: {title}",
        "about_title": "About MiniNotes",
        "no_tray": "Desktop notifications are not available on this computer.",
        "search_ph": "Search by title or content...",
        "sort": "Sort by",
        "sort_created": "Newest notes",
        "sort_updated": "Recently updated",
        "sort_due": "Upcoming deadline",
        "sort_title": "Alphabetical",
        "pin": "Pin note",
        "unpin": "Unpin note",
        "summary_notes": "Notes",
        "summary_upcoming": "Upcoming tasks",
        "summary_overdue": "Overdue tasks",
        "empty_title": "You don't have any notes yet",
        "empty_text": "Create your first note to get started!",
        "no_results": "No notes match your search.",
        "show_floating": "Show on desktop",
        "remove_floating": "Remove from desktop",
        "floating_edit": "Edit",
        "floating_minimize": "Minimize",
        "floating_close": "Close",
        "floating_notes": "Floating notes",
        "no_floating": "There are no floating notes.",
        "floating_minimized": "Minimized",
        "restore_all": "Restore all notes",
        "floating_help": "Show notes on your desktop and restore them here."
    },

    "ru": {
        "app_subtitle": "Простое место для ваших мыслей",
        "notes": "Мои заметки",
        "welcome": "Добро пожаловать в MiniNotes\n\nВыберите заметку из списка.",
        "new_note": "+ Создать заметку",
        "saved_count": "Сохранено заметок: {n}",
        "menu": "Меню",
        "settings": "Настройки",
        "about": "О программе MiniNotes",
        "exit": "Выход",
        "new": "Новая заметка",
        "edit": "Изменить заметку",
        "title": "Заголовок заметки",
        "title_ph": "Введите заголовок...",
        "content": "Текст заметки",
        "content_ph": "Введите текст заметки...",
        "add_due": "Указать дату и время задачи",
        "date": "Дата:",
        "time": "Время:",
        "save": "Сохранить",
        "cancel": "Отмена",
        "missing_title": "Введите заголовок заметки.",
        "missing_content": "Введите текст заметки.",
        "past_due": "Нельзя назначить задачу на прошедшее время.",
        "edit_note": "Изменить заметку",
        "delete_note": "Удалить заметку",
        "close": "Закрыть",
        "add_calendar": "Добавить в календарь",
        "due": "Срок задачи",
        "confirm_delete": "Вы действительно хотите удалить эту заметку?",
        "info_text": "Приложение для управления заметками и задачами.",
        "settings_title": "Настройки MiniNotes",
        "language": "Язык",
        "language_help": "Выберите язык интерфейса.",
        "notifications": "Уведомления",
        "notifications_help": "Показывать уведомление, когда наступает срок задачи.",
        "enable_notifications": "Включить уведомления о сроках задач",
        "appearance": "Внешний вид",
        "theme": "Цветовая тема",
        "light": "Светлая",
        "dark": "Тёмная",
        "system": "Системная",
        "font_size": "Размер шрифта",
        "normal": "Обычный",
        "large": "Большой",
        "backup": "Резервное копирование",
        "backup_help": "Экспорт и восстановление заметок.",
        "export_backup": "Экспортировать копию",
        "import_backup": "Импортировать копию",
        "information": "Информация и обновления",
        "version": "Версия",
        "last_update": "Дата обновления",
        "apply": "Применить",
        "ok": "ОК",
        "settings_saved": "Настройки сохранены и применены.",
        "save_error": "Не удалось сохранить настройки: {error}",
        "backup_exported": "Резервная копия успешно экспортирована.",
        "backup_imported": "Резервная копия успешно импортирована.",
        "backup_error": "Ошибка резервного копирования: {error}",
        "choose_backup": "Выберите файл копии",
        "backup_file": "Файлы JSON (*.json)",
        "calendar_missing": "Для этой заметки не указаны дата и время.",
        "calendar_created": "Событие создано и открыто в календаре.",
        "calendar_error": "Не удалось создать событие: {error}",
        "calendar_open_error": "Файл календаря создан, но не может быть открыт: {path}",
        "notification_title": "Наступил срок задачи",
        "notification_text": "{title}",
        "notification_fallback": "Наступил срок задачи: {title}",
        "about_title": "О программе MiniNotes",
        "no_tray": "Уведомления рабочего стола недоступны на этом компьютере.",
        "search_ph": "Поиск по заголовку или содержанию...",
        "sort": "Сортировка",
        "sort_created": "Сначала новые",
        "sort_updated": "Недавно изменённые",
        "sort_due": "Ближайший срок",
        "sort_title": "По алфавиту",
        "pin": "Закрепить заметку",
        "unpin": "Открепить заметку",
        "summary_notes": "Заметки",
        "summary_upcoming": "Предстоящие задачи",
        "summary_overdue": "Просроченные задачи",
        "empty_title": "У вас пока нет заметок",
        "empty_text": "Создайте свою первую заметку!",
        "no_results": "Заметки не найдены.",
        "show_floating": "Показать на рабочем столе",
        "remove_floating": "Убрать с рабочего стола",
        "floating_edit": "Изменить",
        "floating_minimize": "Свернуть",
        "floating_close": "Закрыть",
        "floating_notes": "Плавающие заметки",
        "no_floating": "Нет плавающих заметок.",
        "floating_minimized": "Свернуто",
        "restore_all": "Восстановить все заметки",
        "floating_help": "Показывайте заметки на рабочем столе."
    }
}


DEFAULT_SETTINGS = {
    "language": "he",
    "notifications_enabled": True,
    "theme": "light",
    "font_size": "normal",
    "backup_folder": "",
    "sort_order": "updated"
}

CURRENT_SETTINGS = dict(DEFAULT_SETTINGS)


def tr(key, **kwargs):
    lang = CURRENT_SETTINGS.get("language", "he")

    template = TEXT.get(
        lang,
        TEXT["he"]
    ).get(
        key,
        TEXT["he"].get(key, key)
    )

    return template.format(**kwargs) if kwargs else template


def load_settings():
    result = dict(DEFAULT_SETTINGS)

    try:
        with open(SETTINGS_FILE, "r", encoding="utf-8") as file:
            saved = json.load(file)

        if isinstance(saved, dict):
            result.update(saved)

    except (OSError, json.JSONDecodeError):
        pass

    if result.get("language") not in TEXT:
        result["language"] = "he"

    if result.get("sort_order") not in (
        "created", "updated", "due", "title"
    ):
        result["sort_order"] = "updated"

    return result


def save_settings(settings):
    temporary_file = SETTINGS_FILE + ".tmp"

    with open(temporary_file, "w", encoding="utf-8") as file:
        json.dump(
            settings,
            file,
            ensure_ascii=False,
            indent=4
        )

    os.replace(temporary_file, SETTINGS_FILE)


def now_in_app_timezone():
    return datetime.now().replace(
        second=0,
        microsecond=0
    )


def parse_due(value):
    if not value:
        return None

    try:
        return datetime.fromisoformat(value)

    except (ValueError, TypeError):
        return None


def format_due(value):
    due = parse_due(value)

    if due is None:
        return None

    return due.strftime("%d/%m/%Y %H:%M")


def normalize_note(note, used_ids=None):
    if not isinstance(note, dict):
        return None

    if used_ids is None:
        used_ids = set()

    note.setdefault("title", "")
    note.setdefault("content", "")
    note.setdefault("color", "white")
    note.setdefault("due_datetime", None)
    note.setdefault("pinned", False)

    note.setdefault("floating", False)
    note.setdefault("floating_minimized", False)
    note.setdefault("floating_geometry", None)

    note_id = note.get("id")

    if not note_id or note_id in used_ids:
        note_id = str(uuid.uuid4())
        note["id"] = note_id

    used_ids.add(note_id)

    migration_time = now_in_app_timezone().isoformat(
        timespec="minutes"
    )

    if not note.get("created_at"):
        note["created_at"] = migration_time

    if not note.get("updated_at"):
        note["updated_at"] = note["created_at"]

    if note.get("color") not in COLORS:
        note["color"] = "white"

    if not isinstance(note.get("floating_geometry"), list):
        note["floating_geometry"] = None

    return note


def load_notes():
    try:
        with open(NOTES_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

        if isinstance(data, list):
            used_ids = set()
            notes = []

            for note in data:
                normalized = normalize_note(
                    note,
                    used_ids
                )

                if normalized is not None:
                    notes.append(normalized)

            return notes

    except (OSError, json.JSONDecodeError):
        pass

    old_file = os.path.join(DATA_DIR, "notes.txt")
    notes = []

    if os.path.exists(old_file):
        try:
            with open(old_file, "r", encoding="utf-8") as file:
                for line in file:
                    value = line.strip()

                    if value:
                        created = now_in_app_timezone().isoformat(
                            timespec="minutes"
                        )

                        notes.append({
                            "id": str(uuid.uuid4()),
                            "title": value[:35],
                            "content": value,
                            "color": random.choice(list(COLORS)),
                            "due_datetime": None,
                            "pinned": False,
                            "created_at": created,
                            "updated_at": created,
                            "floating": False,
                            "floating_minimized": False,
                            "floating_geometry": None
                        })

        except OSError:
            pass

    return notes


def save_notes(notes):
    temporary_file = NOTES_FILE + ".tmp"

    with open(temporary_file, "w", encoding="utf-8") as file:
        json.dump(
            notes,
            file,
            ensure_ascii=False,
            indent=4
        )

    os.replace(temporary_file, NOTES_FILE)


def direction():
    if CURRENT_SETTINGS.get("language") == "he":
        return Qt.LayoutDirection.RightToLeft

    return Qt.LayoutDirection.LeftToRight


def now_qdate():
    current = now_in_app_timezone()

    return QDate(
        current.year,
        current.month,
        current.day
    )


def apply_app_style(app):
    theme = CURRENT_SETTINGS.get("theme", "light")
    size = 16 if CURRENT_SETTINGS.get("font_size") == "large" else 14

    if theme == "system":
        app.setStyleSheet(
            f"QWidget {{ font-family: Arial; font-size: {size}px; }}"
        )
        return

    if theme == "dark":
        bg = "#202938"
        panel = "#2B3748"
        fg = "#F1F5F9"
        accent = "#4389E5"

    else:
        bg = "#F5F8FC"
        panel = "#FFFFFF"
        fg = "#243247"
        accent = "#3478D4"

    app.setStyleSheet(f"""
        QWidget {{
            background-color: {bg};
            color: {fg};
            font-family: Arial;
            font-size: {size}px;
        }}

        QLineEdit, QTextEdit, QTimeEdit,
        QComboBox, QListWidget, QStackedWidget {{
            background-color: {panel};
            border: 1px solid #8798AA;
            border-radius: 8px;
            padding: 7px;
        }}

        QPushButton {{
            background-color: {accent};
            color: white;
            border: none;
            border-radius: 8px;
            padding: 9px 15px;
            font-weight: bold;
        }}

        QPushButton:hover {{
            background-color: #2865B8;
        }}

        QToolButton {{
            background-color: {panel};
            border: 1px solid #8798AA;
            border-radius: 8px;
            padding: 7px 12px;
        }}

        QListWidget::item {{
            padding: 10px;
        }}

        QListWidget::item:selected {{
            background-color: #D7E8FC;
            color: #173B65;
        }}
    """)


def export_ics(note, parent):
    due = parse_due(note.get("due_datetime"))

    if due is None:
        QMessageBox.warning(
            parent,
            tr("add_calendar"),
            tr("calendar_missing")
        )
        return

    end = due + timedelta(hours=1)

    def escape_ics(value):
        return (
            str(value)
            .replace("\\", "\\\\")
            .replace(";", "\\;")
            .replace(",", "\\,")
            .replace("\n", "\\n")
        )

    lines = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//MiniNotes//EN",
        "CALSCALE:GREGORIAN",
        "BEGIN:VEVENT",
        f"UID:mininotes-{note.get('id', uuid.uuid4())}@mininotes",
        f"DTSTAMP:{datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')}",
        f"DTSTART:{due.strftime('%Y%m%dT%H%M%S')}",
        f"DTEND:{end.strftime('%Y%m%dT%H%M%S')}",
        f"SUMMARY:{escape_ics(note.get('title', ''))}",
        f"DESCRIPTION:{escape_ics(note.get('content', ''))}",
        "END:VEVENT",
        "END:VCALENDAR",
        ""
    ]

    folder = os.path.join(DATA_DIR, "calendar")
    os.makedirs(folder, exist_ok=True)

    path = os.path.join(
        folder,
        f"MiniNotes_{due.strftime('%Y%m%d_%H%M')}.ics"
    )

    try:
        with open(path, "w", encoding="utf-8", newline="") as file:
            file.write("\r\n".join(lines))

        opened = QDesktopServices.openUrl(
            QUrl.fromLocalFile(path)
        )

        if opened:
            QMessageBox.information(
                parent,
                tr("add_calendar"),
                tr("calendar_created")
            )

        else:
            QMessageBox.warning(
                parent,
                tr("add_calendar"),
                tr("calendar_open_error", path=path)
            )

    except OSError as error:
        QMessageBox.warning(
            parent,
            tr("add_calendar"),
            tr("calendar_error", error=error)
        )
class NoteEditor(QDialog):

    def __init__(self, parent=None, note=None):
        super().__init__(parent)

        self.setLayoutDirection(direction())
        self.setWindowTitle(
            tr("new") if note is None else tr("edit")
        )
        self.setMinimumSize(460, 500)

        layout = QVBoxLayout(self)

        self.title_label = QLabel(tr("title"))
        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText(tr("title_ph"))

        self.content_label = QLabel(tr("content"))
        self.content_input = QTextEdit()
        self.content_input.setPlaceholderText(tr("content_ph"))

        self.due_check = QCheckBox(tr("add_due"))

        self.date_label = QLabel(tr("date"))

        self.date_input = QLineEdit()
        self.date_input.setInputMask("00/00/0000;_")
        self.date_input.setText(
            now_qdate().toString("dd/MM/yyyy")
        )
        self.date_input.setLayoutDirection(
            Qt.LayoutDirection.LeftToRight
        )
        self.date_input.setAlignment(
            Qt.AlignmentFlag.AlignLeft
        )
        self.date_input.setMinimumWidth(110)

        self.calendar_button = QPushButton("📅")
        self.calendar_button.setFixedWidth(45)
        self.calendar_button.clicked.connect(
            self.open_calendar
        )

        self.time_label = QLabel(tr("time"))

        self.time_input = QLineEdit()
        self.time_input.setInputMask("00:00;_")
        self.time_input.setLayoutDirection(
            Qt.LayoutDirection.LeftToRight
        )
        self.time_input.setAlignment(
            Qt.AlignmentFlag.AlignLeft
        )
        self.time_input.setMinimumWidth(75)
        self.time_input.setMaximumWidth(90)

        current_clock = now_in_app_timezone()

        self.time_input.setText(
            f"{current_clock.hour:02d}:{current_clock.minute:02d}"
        )

        date_time_row = QHBoxLayout()
        date_time_row.setDirection(
            QHBoxLayout.Direction.LeftToRight
        )

        date_time_row.addWidget(self.date_label)
        date_time_row.addWidget(self.date_input)
        date_time_row.addWidget(self.calendar_button)
        date_time_row.addWidget(self.time_label)
        date_time_row.addWidget(self.time_input)

        layout.addWidget(self.title_label)
        layout.addWidget(self.title_input)
        layout.addWidget(self.content_label)
        layout.addWidget(self.content_input, 1)
        layout.addWidget(self.due_check)
        layout.addLayout(date_time_row)

        self.date_input.setEnabled(False)
        self.calendar_button.setEnabled(False)
        self.time_input.setEnabled(False)
        self.date_label.setEnabled(False)
        self.time_label.setEnabled(False)

        self.due_check.toggled.connect(
            self.toggle_due
        )

        if note:
            self.title_input.setText(
                note.get("title", "")
            )

            self.content_input.setPlainText(
                note.get("content", "")
            )

            due = parse_due(
                note.get("due_datetime")
            )

            if due:
                self.due_check.setChecked(True)

                self.date_input.setText(
                    f"{due.day:02d}/{due.month:02d}/{due.year:04d}"
                )

                self.time_input.setText(
                    f"{due.hour:02d}:{due.minute:02d}"
                )

        buttons = QHBoxLayout()

        save_button = QPushButton(tr("save"))
        cancel_button = QPushButton(tr("cancel"))

        save_button.clicked.connect(self.validate)
        cancel_button.clicked.connect(self.reject)

        buttons.addWidget(save_button)
        buttons.addWidget(cancel_button)

        layout.addLayout(buttons)

    def get_selected_date(self):
        return QDate.fromString(
            self.date_input.text(),
            "dd/MM/yyyy"
        )

    def get_selected_time(self):
        return QTime.fromString(
            self.time_input.text(),
            "HH:mm"
        )

    def open_calendar(self):
        dialog = QDialog(self)
        dialog.setWindowTitle(tr("date"))
        dialog.setLayoutDirection(direction())
        dialog.setMinimumWidth(320)

        layout = QVBoxLayout(dialog)

        calendar = QCalendarWidget()
        calendar.setMinimumDate(now_qdate())
        calendar.setLayoutDirection(direction())

        if CURRENT_SETTINGS.get("language") == "he":
            calendar_locale = QLocale(
                QLocale.Language.Hebrew,
                QLocale.Country.Israel
            )

        elif CURRENT_SETTINGS.get("language") == "en":
            calendar_locale = QLocale(
                QLocale.Language.English
            )

        else:
            calendar_locale = QLocale(
                QLocale.Language.Russian
            )

        calendar.setLocale(calendar_locale)

        current_date = self.get_selected_date()

        if current_date.isValid():
            calendar.setSelectedDate(current_date)
        else:
            calendar.setSelectedDate(now_qdate())

        calendar.setStyleSheet("""
            QCalendarWidget QWidget {
                background: #FFFFFF;
                color: #243247;
            }

            QCalendarWidget QWidget#qt_calendar_navigationbar {
                background: #1E3A5F;
            }

            QCalendarWidget QToolButton {
                color: white;
                background: transparent;
                padding: 5px;
            }

            QCalendarWidget QAbstractItemView {
                selection-background-color: #3478D4;
                selection-color: white;
            }
        """)

        layout.addWidget(calendar)

        buttons = QHBoxLayout()

        choose_button = QPushButton(tr("ok"))
        cancel_button = QPushButton(tr("cancel"))

        buttons.addWidget(choose_button)
        buttons.addWidget(cancel_button)

        layout.addLayout(buttons)

        choose_button.clicked.connect(dialog.accept)
        cancel_button.clicked.connect(dialog.reject)

        if dialog.exec() == QDialog.DialogCode.Accepted:
            selected = calendar.selectedDate()

            self.date_input.setText(
                selected.toString("dd/MM/yyyy")
            )

    def toggle_due(self, enabled):
        for widget in (
            self.date_input,
            self.calendar_button,
            self.time_input,
            self.date_label,
            self.time_label
        ):
            widget.setEnabled(enabled)

    def validate(self):
        if not self.title_input.text().strip():
            QMessageBox.warning(
                self,
                tr("title"),
                tr("missing_title")
            )
            return

        if not self.content_input.toPlainText().strip():
            QMessageBox.warning(
                self,
                tr("content"),
                tr("missing_content")
            )
            return

        if self.due_check.isChecked():
            date = self.get_selected_date()
            time = self.get_selected_time()

            if not date.isValid() or not time.isValid():
                QMessageBox.warning(
                    self,
                    tr("date_time"),
                    tr("past_due")
                )
                return

            chosen = datetime(
                date.year(),
                date.month(),
                date.day(),
                time.hour(),
                time.minute()
            )

            if chosen < now_in_app_timezone():
                QMessageBox.warning(
                    self,
                    tr("date_time"),
                    tr("past_due")
                )
                return

        self.accept()

    def get_note(self):
        due_value = None

        if self.due_check.isChecked():
            date = self.get_selected_date()
            time = self.get_selected_time()

            due_value = datetime(
                date.year(),
                date.month(),
                date.day(),
                time.hour(),
                time.minute()
            ).isoformat(timespec="minutes")

        return {
            "title": self.title_input.text().strip(),
            "content": self.content_input.toPlainText().strip(),
            "due_datetime": due_value
        }


class NoteView(QDialog):

    def __init__(self, note, parent=None):
        super().__init__(parent)

        self.note = note
        self.action = None

        self.setLayoutDirection(direction())
        self.setWindowTitle(
            note.get("title", "MiniNotes")
        )
        self.setMinimumSize(420, 430)

        layout = QVBoxLayout(self)

        paper = QFrame()

        paper.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS.get(note.get('color'), '#FFFFFF')};
                border: 1px solid #D8D2C8;
                border-radius: 12px;
            }}
        """)

        paper_layout = QVBoxLayout(paper)

        title = QLabel(note.get("title", ""))
        title.setWordWrap(True)
        title.setStyleSheet("""
            font-size: 22px;
            font-weight: bold;
            background: transparent;
        """)

        content = QLabel(note.get("content", ""))
        content.setWordWrap(True)

        alignment = (
            Qt.AlignmentFlag.AlignRight
            if direction() == Qt.LayoutDirection.RightToLeft
            else Qt.AlignmentFlag.AlignLeft
        )

        content.setAlignment(
            Qt.AlignmentFlag.AlignTop | alignment
        )
        content.setStyleSheet("background: transparent;")

        paper_layout.addWidget(title)
        paper_layout.addWidget(content, 1)

        due = format_due(note.get("due_datetime"))

        if due:
            due_label = QLabel(f"{tr('due')}: {due}")
            due_label.setStyleSheet(
                "background: transparent; font-weight: bold;"
            )
            paper_layout.addWidget(due_label)

        layout.addWidget(paper, 1)

        buttons = QHBoxLayout()

        edit_button = QPushButton(tr("edit_note"))
        delete_button = QPushButton(tr("delete_note"))
        close_button = QPushButton(tr("close"))

        pin_text = (
            tr("unpin")
            if note.get("pinned", False)
            else tr("pin")
        )

        pin_button = QPushButton(pin_text)

        floating_text = (
            tr("remove_floating")
            if note.get("floating", False)
            else tr("show_floating")
        )

        floating_button = QPushButton(floating_text)

        edit_button.clicked.connect(
            lambda: self.finish("edit")
        )

        delete_button.clicked.connect(
            lambda: self.finish("delete")
        )

        pin_button.clicked.connect(
            lambda: self.finish("toggle_pin")
        )

        floating_button.clicked.connect(
            lambda: self.finish("toggle_float")
        )

        close_button.clicked.connect(self.reject)

        buttons.addWidget(edit_button)
        buttons.addWidget(delete_button)
        buttons.addWidget(pin_button)
        buttons.addWidget(floating_button)

        if note.get("due_datetime"):
            calendar_button = QPushButton(tr("add_calendar"))
            calendar_button.clicked.connect(
                lambda: export_ics(note, self)
            )
            buttons.addWidget(calendar_button)

        buttons.addWidget(close_button)
        layout.addLayout(buttons)

    def finish(self, action):
        self.action = action
        self.accept()


class FloatingNote(QWidget):

    def __init__(self, parent, note):
        flags = (
            Qt.WindowType.Tool
            | Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
        )

        super().__init__(parent, flags)

        self.main_window = parent
        self.note_id = note["id"]
        self.allow_close = False
        self.drag_position = None

        self.setAttribute(
            Qt.WidgetAttribute.WA_DeleteOnClose,
            False
        )

        self.setWindowTitle(
            note.get("title", "MiniNotes")
        )

        self.setMinimumSize(230, 180)
        self.resize(300, 260)

        self.create_interface(note)

        geometry = note.get("floating_geometry")

        if (
            isinstance(geometry, list)
            and len(geometry) == 4
        ):
            try:
                x, y, width, height = map(int, geometry)

                self.setGeometry(
                    x,
                    y,
                    max(230, width),
                    max(180, height)
                )

            except (TypeError, ValueError):
                self.move(100, 100)

        else:
            offset = len(parent.floating_windows) * 30
            self.move(100 + offset, 100 + offset)

        self.geometry_timer = QTimer(self)
        self.geometry_timer.setSingleShot(True)
        self.geometry_timer.timeout.connect(
            self.save_geometry
        )

    def create_interface(self, note):
        root = QVBoxLayout(self)
        root.setContentsMargins(9, 8, 9, 5)
        root.setSpacing(4)

        paper = QFrame()
        paper.setObjectName("floatingPaper")

        color = COLORS.get(
            note.get("color"),
            "#FFFFFF"
        )

        paper.setStyleSheet(f"""
            QFrame#floatingPaper {{
                background-color: {color};
                border: 1px solid #D0C8BD;
                border-radius: 12px;
            }}

            QLabel {{
                background: transparent;
                color: #243247;
            }}

            QPushButton {{
                background-color: rgba(255,255,255,190);
                color: #243247;
                border: 1px solid rgba(100,100,100,70);
                border-radius: 6px;
                padding: 4px 7px;
                font-size: 12px;
            }}

            QPushButton:hover {{
                background-color: white;
            }}
        """)

        paper_layout = QVBoxLayout(paper)
        paper_layout.setContentsMargins(10, 8, 10, 8)
        paper_layout.setSpacing(7)

        header = QHBoxLayout()

        self.title_label = QLabel()
        self.title_label.setWordWrap(True)
        self.title_label.setStyleSheet("""
            font-size: 16px;
            font-weight: bold;
        """)

        self.edit_button = QPushButton(tr("floating_edit"))
        self.minimize_button = QPushButton("−")
        self.close_button = QPushButton("×")

        self.minimize_button.setToolTip(
            tr("floating_minimize")
        )

        self.close_button.setToolTip(
            tr("floating_close")
        )

        self.edit_button.clicked.connect(
            self.edit_note
        )

        self.minimize_button.clicked.connect(
            self.minimize_note
        )

        self.close_button.clicked.connect(
            self.remove_note
        )

        header.addWidget(self.title_label, 1)
        header.addWidget(self.edit_button)
        header.addWidget(self.minimize_button)
        header.addWidget(self.close_button)

        paper_layout.addLayout(header)

        self.content_label = QLabel()
        self.content_label.setWordWrap(True)
        self.content_label.setAlignment(
            Qt.AlignmentFlag.AlignTop
        )
        self.content_label.setStyleSheet(
            "font-size: 14px;"
        )

        paper_layout.addWidget(
            self.content_label,
            1
        )

        self.due_label = QLabel()
        self.due_label.setStyleSheet(
            "font-weight: bold; font-size: 12px;"
        )

        paper_layout.addWidget(self.due_label)

        root.addWidget(paper, 1)

        resize_row = QHBoxLayout()
        resize_row.addStretch()

        resize_grip = QSizeGrip(self)
        resize_row.addWidget(resize_grip)

        root.addLayout(resize_row)

        self.update_note(note)

    def update_note(self, note):
        self.title_label.setText(
            note.get("title", "")
        )

        self.content_label.setText(
            note.get("content", "")
        )

        self.setWindowTitle(
            note.get("title", "MiniNotes")
        )

        due = format_due(
            note.get("due_datetime")
        )

        self.due_label.setText(
            f"{tr('due')}: {due}" if due else ""
        )

        self.setLayoutDirection(direction())

        color = COLORS.get(
            note.get("color"),
            "#FFFFFF"
        )

        paper = self.findChild(
            QFrame,
            "floatingPaper"
        )

        if paper:
            paper.setStyleSheet(f"""
                QFrame#floatingPaper {{
                    background-color: {color};
                    border: 1px solid #D0C8BD;
                    border-radius: 12px;
                }}

                QLabel {{
                    background: transparent;
                    color: #243247;
                }}

                QPushButton {{
                    background-color: rgba(255,255,255,190);
                    color: #243247;
                    border: 1px solid rgba(100,100,100,70);
                    border-radius: 6px;
                    padding: 4px 7px;
                    font-size: 12px;
                }}

                QPushButton:hover {{
                    background-color: white;
                }}
            """)

    def edit_note(self):
        self.main_window.edit_note_by_id(
            self.note_id
        )

    def minimize_note(self):
        self.main_window.minimize_floating_note(
            self.note_id
        )

    def remove_note(self):
        self.main_window.stop_floating_note(
            self.note_id
        )

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_position = (
                event.globalPosition().toPoint()
                - self.frameGeometry().topLeft()
            )

            event.accept()

    def mouseMoveEvent(self, event):
        if (
            self.drag_position is not None
            and event.buttons() & Qt.MouseButton.LeftButton
        ):
            self.move(
                event.globalPosition().toPoint()
                - self.drag_position
            )

            event.accept()

    def mouseReleaseEvent(self, event):
        self.drag_position = None
        self.geometry_timer.start(400)
        event.accept()

    def moveEvent(self, event):
        super().moveEvent(event)

        if hasattr(self, "geometry_timer"):
            self.geometry_timer.start(400)

    def resizeEvent(self, event):
        super().resizeEvent(event)

        if hasattr(self, "geometry_timer"):
            self.geometry_timer.start(400)

    def save_geometry(self):
        self.main_window.update_floating_geometry(
            self.note_id,
            self.geometry()
        )

    def shutdown(self):
        self.allow_close = True

        if hasattr(self, "geometry_timer"):
            self.geometry_timer.stop()

        self.save_geometry()
        self.close()

    def closeEvent(self, event):
        if not self.allow_close:
            self.main_window.stop_floating_note(
                self.note_id
            )

        event.accept()
class SettingsDialog(QDialog):

    def __init__(self, settings, parent=None):
        super().__init__(parent)

        self.settings = settings
        self.applied = dict(settings)

        self.setWindowTitle(tr("settings_title"))
        self.setMinimumSize(720, 470)
        self.setLayoutDirection(direction())

        root = QVBoxLayout(self)

        self.heading = QLabel(tr("settings_title"))
        self.heading.setStyleSheet(
            "font-size: 22px; font-weight: bold;"
        )

        root.addWidget(self.heading)

        body = QHBoxLayout()

        self.navigation = QListWidget()
        self.navigation.setMaximumWidth(180)

        self.stack = QStackedWidget()

        body.addWidget(self.navigation)
        body.addWidget(self.stack, 1)

        root.addLayout(body, 1)

        self.pages = {}
        self.build_pages()

        self.navigation.currentRowChanged.connect(
            self.stack.setCurrentIndex
        )

        self.navigation.setCurrentRow(0)

        self.page_keys = [
            "language",
            "notifications",
            "appearance",
            "backup",
            "information"
        ]

        buttons = QHBoxLayout()

        self.apply_btn = QPushButton(tr("apply"))
        self.ok_btn = QPushButton(tr("ok"))
        self.close_btn = QPushButton(tr("close"))

        self.apply_btn.clicked.connect(
            self.apply_settings
        )

        self.ok_btn.clicked.connect(
            self.accept_settings
        )

        self.close_btn.clicked.connect(
            self.reject
        )

        buttons.addWidget(self.apply_btn)
        buttons.addWidget(self.ok_btn)
        buttons.addWidget(self.close_btn)

        root.addLayout(buttons)

    def add_page(self, key, title):
        page = QWidget()
        layout = QVBoxLayout(page)

        label = QLabel(title)
        label.setWordWrap(True)

        layout.addWidget(label)

        self.navigation.addItem(title)
        self.stack.addWidget(page)

        self.pages[key] = (
            page,
            layout,
            label
        )

        return layout

    def build_pages(self):

        # שפה
        layout = self.add_page(
            "language",
            tr("language")
        )

        self.language_help = QLabel(
            tr("language_help")
        )

        layout.addWidget(self.language_help)

        self.language_combo = QComboBox()
        self.language_combo.addItem(
            "עברית",
            "he"
        )
        self.language_combo.addItem(
            "English",
            "en"
        )
        self.language_combo.addItem(
            "Русский",
            "ru"
        )

        index = self.language_combo.findData(
            self.settings.get("language", "he")
        )

        self.language_combo.setCurrentIndex(
            max(0, index)
        )

        layout.addWidget(self.language_combo)
        layout.addStretch()

        # התראות
        layout = self.add_page(
            "notifications",
            tr("notifications")
        )

        self.notifications_help = QLabel(
            tr("notifications_help")
        )

        self.notifications_help.setWordWrap(True)
        layout.addWidget(self.notifications_help)

        self.notifications_check = QCheckBox(
            tr("enable_notifications")
        )

        self.notifications_check.setChecked(
            self.settings.get(
                "notifications_enabled",
                True
            )
        )

        layout.addWidget(self.notifications_check)
        layout.addStretch()

        # מראה
        layout = self.add_page(
            "appearance",
            tr("appearance")
        )

        self.theme_label = QLabel(tr("theme"))
        layout.addWidget(self.theme_label)

        self.theme_combo = QComboBox()

        self.theme_combo.addItem(
            tr("light"),
            "light"
        )
        self.theme_combo.addItem(
            tr("dark"),
            "dark"
        )
        self.theme_combo.addItem(
            tr("system"),
            "system"
        )

        index = self.theme_combo.findData(
            self.settings.get("theme", "light")
        )

        self.theme_combo.setCurrentIndex(
            max(0, index)
        )

        layout.addWidget(self.theme_combo)

        self.font_label = QLabel(tr("font_size"))
        layout.addWidget(self.font_label)

        self.font_combo = QComboBox()

        self.font_combo.addItem(
            tr("normal"),
            "normal"
        )
        self.font_combo.addItem(
            tr("large"),
            "large"
        )

        index = self.font_combo.findData(
            self.settings.get("font_size", "normal")
        )

        self.font_combo.setCurrentIndex(
            max(0, index)
        )

        layout.addWidget(self.font_combo)
        layout.addStretch()

        # גיבוי ושחזור
        layout = self.add_page(
            "backup",
            tr("backup")
        )

        self.backup_help = QLabel(
            tr("backup_help")
        )

        layout.addWidget(self.backup_help)

        self.export_btn = QPushButton(
            tr("export_backup")
        )

        self.import_btn = QPushButton(
            tr("import_backup")
        )

        self.export_btn.clicked.connect(
            self.export_backup
        )

        self.import_btn.clicked.connect(
            self.import_backup
        )

        layout.addWidget(self.export_btn)
        layout.addWidget(self.import_btn)
        layout.addStretch()

        # מידע ועדכונים
        layout = self.add_page(
            "information",
            tr("information")
        )

        self.version_label = QLabel(
            f"{tr('version')}: {APP_VERSION}"
        )

        self.release_label = QLabel(
            f"{tr('last_update')}: {RELEASE_DATE}"
        )

        layout.addWidget(self.version_label)
        layout.addWidget(self.release_label)
        layout.addStretch()

    def collect(self):
        return {
            **self.applied,
            "language": self.language_combo.currentData(),
            "notifications_enabled": (
                self.notifications_check.isChecked()
            ),
            "theme": self.theme_combo.currentData(),
            "font_size": self.font_combo.currentData()
        }

    def apply_settings(self):
        new_settings = self.collect()

        try:
            save_settings(new_settings)

        except OSError as error:
            QMessageBox.critical(
                self,
                tr("settings_title"),
                tr("save_error", error=error)
            )
            return False

        self.settings.clear()
        self.settings.update(new_settings)

        self.applied = dict(new_settings)

        global CURRENT_SETTINGS

        CURRENT_SETTINGS.clear()
        CURRENT_SETTINGS.update(new_settings)

        self.parent().settings_changed()

        self.retranslate_dialog()

        QMessageBox.information(
            self,
            tr("settings_title"),
            tr("settings_saved")
        )

        return True

    def retranslate_dialog(self):
        self.setLayoutDirection(direction())
        self.setWindowTitle(tr("settings_title"))
        self.heading.setText(tr("settings_title"))

        page_names = [
            "language",
            "notifications",
            "appearance",
            "backup",
            "information"
        ]

        for index, key in enumerate(self.page_keys):
            title = tr(key)

            self.navigation.item(index).setText(title)

            self.pages[page_names[index]][2].setText(
                title
            )

        self.language_help.setText(
            tr("language_help")
        )

        self.notifications_help.setText(
            tr("notifications_help")
        )

        self.notifications_check.setText(
            tr("enable_notifications")
        )

        self.apply_btn.setText(tr("apply"))
        self.ok_btn.setText(tr("ok"))
        self.close_btn.setText(tr("close"))

        self.theme_label.setText(tr("theme"))
        self.font_label.setText(tr("font_size"))

        self.export_btn.setText(
            tr("export_backup")
        )

        self.import_btn.setText(
            tr("import_backup")
        )

        self.theme_combo.setItemText(
            0,
            tr("light")
        )

        self.theme_combo.setItemText(
            1,
            tr("dark")
        )

        self.theme_combo.setItemText(
            2,
            tr("system")
        )

        self.font_combo.setItemText(
            0,
            tr("normal")
        )

        self.font_combo.setItemText(
            1,
            tr("large")
        )

        self.backup_help.setText(
            tr("backup_help")
        )

        self.version_label.setText(
            f"{tr('version')}: {APP_VERSION}"
        )

        self.release_label.setText(
            f"{tr('last_update')}: {RELEASE_DATE}"
        )

    def accept_settings(self):
        if self.apply_settings():
            self.accept()

    def reject(self):
        self.settings.clear()
        self.settings.update(self.applied)

        global CURRENT_SETTINGS

        CURRENT_SETTINGS.clear()
        CURRENT_SETTINGS.update(self.applied)

        self.parent().settings_changed()

        super().reject()

    def export_backup(self):
        folder = (
            self.settings.get("backup_folder")
            or DATA_DIR
        )

        path, _ = QFileDialog.getSaveFileName(
            self,
            tr("export_backup"),
            os.path.join(
                folder,
                "MiniNotes_backup.json"
            ),
            tr("backup_file")
        )

        if not path:
            return

        try:
            with open(path, "w", encoding="utf-8") as file:
                json.dump(
                    self.parent().notes,
                    file,
                    ensure_ascii=False,
                    indent=4
                )

            QMessageBox.information(
                self,
                tr("backup"),
                tr("backup_exported")
            )

        except (OSError, TypeError) as error:
            QMessageBox.warning(
                self,
                tr("backup"),
                tr("backup_error", error=error)
            )

    def import_backup(self):
        path, _ = QFileDialog.getOpenFileName(
            self,
            tr("choose_backup"),
            "",
            tr("backup_file")
        )

        if not path:
            return

        try:
            with open(path, "r", encoding="utf-8") as file:
                imported_notes = json.load(file)

            if (
                not isinstance(imported_notes, list)
                or any(
                    not isinstance(note, dict)
                    for note in imported_notes
                )
            ):
                raise ValueError(
                    "Invalid backup format"
                )

            used_ids = set()
            notes = []

            for note in imported_notes:
                normalized = normalize_note(
                    note,
                    used_ids
                )

                if normalized is not None:
                    notes.append(normalized)

            self.parent().close_all_floating_windows()

            self.parent().notes = notes

            self.parent().save_notes()
            self.parent().restore_floating_notes()
            self.parent().refresh_notes()
            self.parent().build_tray_menu()

            QMessageBox.information(
                self,
                tr("backup"),
                tr("backup_imported")
            )

        except (
            OSError,
            json.JSONDecodeError,
            ValueError
        ) as error:
            QMessageBox.warning(
                self,
                tr("backup"),
                tr("backup_error", error=error)
            )


def __init__(self):
    super().__init__()

    self.settings = load_settings()

    CURRENT_SETTINGS.clear()
    CURRENT_SETTINGS.update(self.settings)

    self.notes = load_notes()
    self.notified = set()

    self.floating_windows = {}

    self.setWindowTitle("MiniNotes")
    self.setMinimumSize(850, 620)
    self.setLayoutDirection(direction())

    self.setWindowIcon(
        QIcon(resource_path("mininotes.ico"))
    )

    # יצירת הממשק
    self.create_interface()

    # יצירת סמל מגש המערכת לפני רענון הפתקים
    self.tray = QSystemTrayIcon(self)

    if not self.windowIcon().isNull():
        tray_icon = self.windowIcon()
    else:
        tray_icon = QApplication.style().standardIcon(
            QStyle.StandardPixmap.SP_ComputerIcon
        )

    self.tray.setIcon(tray_icon)

    self.tray.setVisible(
        QSystemTrayIcon.isSystemTrayAvailable()
    )

    self.tray.activated.connect(
        self.tray_activated
    )

    # כעת ניתן לרענן את הפתקים בבטחה
    self.refresh_notes()

    self.build_tray_menu()

    # הפעלת מערכת ההתראות
    self.notification_timer = QTimer(self)

    self.notification_timer.timeout.connect(
        self.check_notifications
    )

    self.notification_timer.start(15000)

    self.apply_style()

    # שחזור פתקים צפים לאחר טעינת הממשק
    QTimer.singleShot(
        300,
        self.restore_floating_notes
    )
    def create_interface(self):

        root = QVBoxLayout(self)
        root.setContentsMargins(24, 20, 24, 20)
        root.setSpacing(12)

        # כותרת עליונה
        header = QHBoxLayout()

        self.menu_button = QToolButton()
        self.menu_button.setText("☰")

        self.menu_button.clicked.connect(
            self.show_main_menu
        )

        header.addWidget(self.menu_button)
        header.addStretch()

        self.title_label = QLabel("MiniNotes")

        self.title_label.setStyleSheet(
            "font-size: 27px; font-weight: bold;"
        )

        header.addWidget(self.title_label)

        header.addStretch()
        header.addSpacing(45)

        root.addLayout(header)

        self.subtitle_label = QLabel(
            tr("app_subtitle")
        )

        self.subtitle_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        root.addWidget(self.subtitle_label)

        # אזור סיכום
        summary_layout = QHBoxLayout()

        self.total_summary = QLabel()
        self.upcoming_summary = QLabel()
        self.overdue_summary = QLabel()

        for label in (
            self.total_summary,
            self.upcoming_summary,
            self.overdue_summary
        ):
            label.setAlignment(
                Qt.AlignmentFlag.AlignCenter
            )

            label.setMinimumHeight(48)

            label.setStyleSheet("""
                QLabel {
                    background-color: #FFFFFF;
                    border: 1px solid #D8E1EC;
                    border-radius: 9px;
                    padding: 8px;
                    font-weight: bold;
                }
            """)

            summary_layout.addWidget(label)

        root.addLayout(summary_layout)

        # חיפוש
        self.search_input = QLineEdit()

        self.search_input.setPlaceholderText(
            tr("search_ph")
        )

        self.search_input.setClearButtonEnabled(True)

        self.search_input.textChanged.connect(
            self.refresh_notes
        )

        root.addWidget(self.search_input)

        # מיון
        sort_layout = QHBoxLayout()

        self.sort_label = QLabel(tr("sort"))

        self.sort_combo = QComboBox()

        self.sort_combo.addItem(
            tr("sort_updated"),
            "updated"
        )

        self.sort_combo.addItem(
            tr("sort_created"),
            "created"
        )

        self.sort_combo.addItem(
            tr("sort_due"),
            "due"
        )

        self.sort_combo.addItem(
            tr("sort_title"),
            "title"
        )

        current_sort = self.settings.get(
            "sort_order",
            "updated"
        )

        sort_index = self.sort_combo.findData(
            current_sort
        )

        self.sort_combo.setCurrentIndex(
            max(0, sort_index)
        )

        self.sort_combo.currentIndexChanged.connect(
            self.change_sort
        )

        sort_layout.addWidget(self.sort_label)
        sort_layout.addWidget(self.sort_combo)
        sort_layout.addStretch()

        root.addLayout(sort_layout)

        # אזור תוכן
        content = QHBoxLayout()

        self.notes_list = QListWidget()
        self.notes_list.setMinimumWidth(300)

        self.notes_list.itemDoubleClicked.connect(
            self.open_note
        )

        self.notes_label = QLabel(tr("notes"))

        right_panel = QVBoxLayout()

        right_panel.addWidget(self.notes_label)
        right_panel.addWidget(self.notes_list, 1)

        self.welcome_label = QLabel()

        self.welcome_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.welcome_label.setWordWrap(True)

        self.welcome_label.setStyleSheet("""
            QLabel {
                font-size: 18px;
                padding: 25px;
            }
        """)

        content.addLayout(right_panel, 1)
        content.addWidget(self.welcome_label, 1)

        root.addLayout(content, 1)

        # כפתורים תחתונים
        bottom_buttons = QHBoxLayout()

        self.add_button = QPushButton(
            tr("new_note")
        )

        self.add_button.clicked.connect(
            self.add_note
        )

        self.floating_button = QPushButton(
            tr("floating_notes")
        )

        self.floating_button.clicked.connect(
            self.show_floating_menu
        )

        bottom_buttons.addWidget(
            self.add_button,
            2
        )

        bottom_buttons.addWidget(
            self.floating_button,
            1
        )

        root.addLayout(bottom_buttons)

        self.status_label = QLabel()

        self.status_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        root.addWidget(self.status_label)

    def apply_style(self):
        apply_app_style(QApplication.instance())
        self.setLayoutDirection(direction())

    def show_main_menu(self):

        menu = QMenu(self)
        menu.setLayoutDirection(direction())

        settings_action = menu.addAction(
            tr("settings")
        )

        about_action = menu.addAction(
            tr("about")
        )

        menu.addSeparator()

        exit_action = menu.addAction(
            tr("exit")
        )

        chosen = menu.exec(
            self.menu_button.mapToGlobal(
                self.menu_button.rect().bottomLeft()
            )
        )

        if chosen == settings_action:
            self.open_settings()

        elif chosen == about_action:
            QMessageBox.information(
                self,
                tr("about_title"),
                f"MiniNotes {APP_VERSION}\n{tr('info_text')}"
            )

        elif chosen == exit_action:
            self.close()

    def open_settings(self):
        dialog = SettingsDialog(
            self.settings,
            self
        )

        dialog.exec()

    def settings_changed(self):
        self.setLayoutDirection(direction())

        self.apply_style()
        self.retranslate()
        self.refresh_all_floating_windows()
        self.build_tray_menu()

    def retranslate(self):
        self.subtitle_label.setText(
            tr("app_subtitle")
        )

        self.notes_label.setText(
            tr("notes")
        )

        self.search_input.setPlaceholderText(
            tr("search_ph")
        )

        self.sort_label.setText(
            tr("sort")
        )

        self.sort_combo.setItemText(
            0,
            tr("sort_updated")
        )

        self.sort_combo.setItemText(
            1,
            tr("sort_created")
        )

        self.sort_combo.setItemText(
            2,
            tr("sort_due")
        )

        self.sort_combo.setItemText(
            3,
            tr("sort_title")
        )

        self.add_button.setText(
            tr("new_note")
        )

        self.floating_button.setText(
            tr("floating_notes")
        )

        self.refresh_notes()

    def change_sort(self):
        selected = self.sort_combo.currentData()

        if not selected:
            return

        self.settings["sort_order"] = selected

        try:
            save_settings(self.settings)

        except OSError:
            pass

        self.refresh_notes()

    def update_summary(self):
        now = now_in_app_timezone()
        upcoming_limit = now + timedelta(days=7)

        upcoming = 0
        overdue = 0

        for note in self.notes:
            due = parse_due(
                note.get("due_datetime")
            )

            if due is None:
                continue

            if due < now:
                overdue += 1

            elif due <= upcoming_limit:
                upcoming += 1

        self.total_summary.setText(
            f"{tr('summary_notes')}: {len(self.notes)}"
        )

        self.upcoming_summary.setText(
            f"{tr('summary_upcoming')}: {upcoming}"
        )

        self.overdue_summary.setText(
            f"{tr('summary_overdue')}: {overdue}"
        )

    def get_sorted_notes(self):
        sort_order = self.sort_combo.currentData()

        notes = list(enumerate(self.notes))

        if sort_order == "created":
            notes.sort(
                key=lambda entry: entry[1].get(
                    "created_at",
                    ""
                ),
                reverse=True
            )

        elif sort_order == "due":
            notes.sort(
                key=lambda entry: (
                    entry[1].get("due_datetime")
                    or "9999-12-31T23:59"
                )
            )

        elif sort_order == "title":
            notes.sort(
                key=lambda entry: (
                    entry[1].get(
                        "title",
                        ""
                    ).casefold()
                )
            )

        else:
            notes.sort(
                key=lambda entry: entry[1].get(
                    "updated_at",
                    ""
                ),
                reverse=True
            )

        # פתקים נעוצים תמיד מופיעים בראש הרשימה
        notes.sort(
            key=lambda entry: not entry[1].get(
                "pinned",
                False
            )
        )

        return notes

    def refresh_notes(self):
        self.notes_list.clear()

        search_text = (
            self.search_input.text().strip().casefold()
        )

        sorted_notes = self.get_sorted_notes()

        visible_count = 0

        for index, note in sorted_notes:
            title = note.get("title", "")
            content = note.get("content", "")

            searchable_text = (
                title + " " + content
            ).casefold()

            if (
                search_text
                and search_text not in searchable_text
            ):
                continue

            due = format_due(
                note.get("due_datetime")
            )

            display = ""

            if note.get("pinned", False):
                display += "📌  "

            if note.get("floating", False):
                display += "▣  "

            display += title

            if due:
                display += f"\n     {due}"

            item = QListWidgetItem(display)

            item.setData(
                Qt.ItemDataRole.UserRole,
                index
            )

            self.notes_list.addItem(item)

            visible_count += 1

        if not self.notes:
            self.welcome_label.setText(
                f"{tr('empty_title')}\n\n{tr('empty_text')}"
            )

        elif visible_count == 0:
            self.welcome_label.setText(
                tr("no_results")
            )

        else:
            self.welcome_label.setText(
                tr("welcome")
            )

        self.update_summary()

        self.status_label.setText(
            tr("saved_count", n=len(self.notes))
        )

        if hasattr(self, "tray") and self.tray is not None:
            self.build_tray_menu()
            
    def save_notes(self):
        save_notes(self.notes)

    def add_note(self):
        dialog = NoteEditor(self)

        if dialog.exec() == QDialog.DialogCode.Accepted:
            note = dialog.get_note()

            now = now_in_app_timezone().isoformat(
                timespec="minutes"
            )

            note["id"] = str(uuid.uuid4())

            note["color"] = random.choice(
                list(COLORS)
            )

            note["pinned"] = False
            note["created_at"] = now
            note["updated_at"] = now

            note["floating"] = False
            note["floating_minimized"] = False
            note["floating_geometry"] = None

            self.notes.append(note)

            self.save_notes()
            self.refresh_notes()

    def open_note(self, item):
        index = item.data(
            Qt.ItemDataRole.UserRole
        )

        if (
            index is None
            or not 0 <= index < len(self.notes)
        ):
            return

        dialog = NoteView(
            self.notes[index],
            self
        )

        dialog.exec()

        if dialog.action == "toggle_float":
            note_id = self.notes[index]["id"]

            if self.notes[index].get("floating", False):
                self.stop_floating_note(note_id)

            else:
                self.start_floating_note(
                    self.notes[index]
                )

            return

        if dialog.action == "toggle_pin":
            self.notes[index]["pinned"] = not (
                self.notes[index].get(
                    "pinned",
                    False
                )
            )

            self.notes[index]["updated_at"] = (
                now_in_app_timezone().isoformat(
                    timespec="minutes"
                )
            )

            self.save_notes()
            self.refresh_notes()

        elif dialog.action == "edit":
            self.edit_note_at_index(index)

        elif dialog.action == "delete":
            answer = QMessageBox.question(
                self,
                tr("delete_note"),
                tr("confirm_delete"),
                QMessageBox.StandardButton.Yes |
                QMessageBox.StandardButton.No
            )

            if answer == QMessageBox.StandardButton.Yes:
                note_id = self.notes[index].get("id")

                if note_id:
                    window = self.floating_windows.pop(
                        note_id,
                        None
                    )

                    if window:
                        window.shutdown()

                self.notes.pop(index)

                self.save_notes()
                self.refresh_notes()

    def edit_note_at_index(self, index):
        if not 0 <= index < len(self.notes):
            return

        editor = NoteEditor(
            self,
            self.notes[index]
        )

        if editor.exec() != QDialog.DialogCode.Accepted:
            return

        old_note = self.notes[index]
        updated = editor.get_note()

        updated["id"] = old_note.get(
            "id",
            str(uuid.uuid4())
        )

        updated["color"] = old_note.get(
            "color",
            "white"
        )

        updated["pinned"] = old_note.get(
            "pinned",
            False
        )

        updated["created_at"] = old_note.get(
            "created_at",
            ""
        )

        updated["updated_at"] = (
            now_in_app_timezone().isoformat(
                timespec="minutes"
            )
        )

        updated["floating"] = old_note.get(
            "floating",
            False
        )

        updated["floating_minimized"] = old_note.get(
            "floating_minimized",
            False
        )

        updated["floating_geometry"] = old_note.get(
            "floating_geometry"
        )

        self.notes[index] = updated

        self.save_notes()
        self.refresh_notes()

        note_id = updated["id"]

        if note_id in self.floating_windows:
            window = self.floating_windows[note_id]
            window.update_note(updated)

        self.build_tray_menu()

    def edit_note_by_id(self, note_id):
        for index, note in enumerate(self.notes):
            if note.get("id") == note_id:
                self.edit_note_at_index(index)
                return

    # -----------------------------------------
    # ניהול פתקים צפים
    # -----------------------------------------

    def get_note_by_id(self, note_id):
        for note in self.notes:
            if note.get("id") == note_id:
                return note

        return None

    def start_floating_note(self, note):
        note_id = note["id"]

        note["floating"] = True
        note["floating_minimized"] = False

        window = self.floating_windows.get(note_id)

        if window is None:
            window = FloatingNote(
                self,
                note
            )

            self.floating_windows[note_id] = window

        else:
            window.update_note(note)

        window.show()
        window.raise_()
        window.activateWindow()

        self.save_notes()
        self.refresh_notes()

    def stop_floating_note(self, note_id):
        note = self.get_note_by_id(note_id)

        if note is None:
            return

        note["floating"] = False
        note["floating_minimized"] = False

        window = self.floating_windows.pop(
            note_id,
            None
        )

        if window:
            window.allow_close = True
            window.geometry_timer.stop()
            window.save_geometry()
            window.hide()

        self.save_notes()
        self.refresh_notes()

    def minimize_floating_note(self, note_id):
        note = self.get_note_by_id(note_id)

        if note is None:
            return

        note["floating"] = True
        note["floating_minimized"] = True

        window = self.floating_windows.get(note_id)

        if window:
            window.save_geometry()
            window.hide()

        self.save_notes()
        self.build_tray_menu()

    def restore_floating_note(self, note_id):
        note = self.get_note_by_id(note_id)

        if note is None:
            return

        note["floating"] = True
        note["floating_minimized"] = False

        window = self.floating_windows.get(note_id)

        if window is None:
            window = FloatingNote(
                self,
                note
            )

            self.floating_windows[note_id] = window

        else:
            window.update_note(note)

        window.show()
        window.raise_()
        window.activateWindow()

        self.save_notes()
        self.build_tray_menu()

    def restore_floating_notes(self):
        for note in self.notes:
            if (
                note.get("floating", False)
                and not note.get(
                    "floating_minimized",
                    False
                )
            ):
                self.start_floating_note(note)

        self.build_tray_menu()

    def restore_all_floating_notes(self):
        for note in self.notes:
            if note.get("floating", False):
                self.restore_floating_note(
                    note["id"]
                )

        self.build_tray_menu()

    def update_floating_geometry(self, note_id, geometry):
        note = self.get_note_by_id(note_id)

        if note is None:
            return

        note["floating_geometry"] = [
            geometry.x(),
            geometry.y(),
            geometry.width(),
            geometry.height()
        ]

        try:
            self.save_notes()

        except OSError:
            pass

    def refresh_all_floating_windows(self):
        for note_id, window in list(
            self.floating_windows.items()
        ):
            note = self.get_note_by_id(note_id)

            if note is not None:
                window.update_note(note)

    def close_all_floating_windows(self):
        for window in list(
            self.floating_windows.values()
        ):
            window.shutdown()

        self.floating_windows.clear()

    # -----------------------------------------
    # תפריט פתקים צפים
    # -----------------------------------------

    def build_tray_menu(self):
        menu = QMenu(self)

        menu.setLayoutDirection(direction())

        show_main_action = menu.addAction(
            tr("app_subtitle")
        )

        show_main_action.triggered.connect(
            self.show_main_window
        )

        floating_menu = menu.addMenu(
            tr("floating_notes")
        )

        floating_notes = [
            note for note in self.notes
            if note.get("floating", False)
        ]

        if not floating_notes:
            empty_action = floating_menu.addAction(
                tr("no_floating")
            )

            empty_action.setEnabled(False)

        else:
            for note in floating_notes:
                title = note.get(
                    "title",
                    "MiniNotes"
                )

                if note.get("floating_minimized", False):
                    title += f" ({tr('floating_minimized')})"

                action = floating_menu.addAction(title)

                note_id = note["id"]

                action.triggered.connect(
                    lambda checked=False, current_id=note_id:
                    self.restore_floating_note(current_id)
                )

            floating_menu.addSeparator()

            restore_all_action = floating_menu.addAction(
                tr("restore_all")
            )

            restore_all_action.triggered.connect(
                self.restore_all_floating_notes
            )

        menu.addSeparator()

        settings_action = menu.addAction(
            tr("settings")
        )

        settings_action.triggered.connect(
            self.open_settings
        )

        exit_action = menu.addAction(
            tr("exit")
        )

        exit_action.triggered.connect(
            self.close
        )

        self.tray.setContextMenu(menu)

    def show_floating_menu(self):
        menu = QMenu(self)

        menu.setLayoutDirection(direction())

        floating_notes = [
            note for note in self.notes
            if note.get("floating", False)
        ]

        if not floating_notes:
            empty_action = menu.addAction(
                tr("no_floating")
            )

            empty_action.setEnabled(False)

        else:
            for note in floating_notes:
                title = note.get(
                    "title",
                    "MiniNotes"
                )

                if note.get("floating_minimized", False):
                    title += f" ({tr('floating_minimized')})"

                action = menu.addAction(title)

                note_id = note["id"]

                action.triggered.connect(
                    lambda checked=False, current_id=note_id:
                    self.restore_floating_note(current_id)
                )

            menu.addSeparator()

            restore_all_action = menu.addAction(
                tr("restore_all")
            )

            restore_all_action.triggered.connect(
                self.restore_all_floating_notes
            )

        menu.exec(
            self.floating_button.mapToGlobal(
                self.floating_button.rect().bottomLeft()
            )
        )

    def tray_activated(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.DoubleClick:
            self.show_main_window()

    def show_main_window(self):
        self.showNormal()
        self.raise_()
        self.activateWindow()

    # -----------------------------------------
    # התראות
    # -----------------------------------------

    def check_notifications(self):
        if not self.settings.get(
            "notifications_enabled",
            True
        ):
            return

        now = now_in_app_timezone()

        for index, note in enumerate(self.notes):
            due = parse_due(
                note.get("due_datetime")
            )

            if due is None:
                continue

            key = (
                f"{note.get('id', index)}:"
                f"{note.get('due_datetime')}"
            )

            if due <= now and key not in self.notified:
                self.notified.add(key)

                title = tr("notification_title")

                message = tr(
                    "notification_text",
                    title=note.get("title", "")
                )

                if self.tray.isVisible():
                    self.tray.showMessage(
                        title,
                        message,
                        QSystemTrayIcon.MessageIcon.Information,
                        10000
                    )

                else:
                    QMessageBox.information(
                        self,
                        title,
                        tr(
                            "notification_fallback",
                            title=note.get("title", "")
                        )
                    )

    # -----------------------------------------
    # סגירת האפליקציה
    # -----------------------------------------

    def closeEvent(self, event):
        # שומרים את המיקום והגודל של החלונות
        # אבל לא מבטלים את מצב הפתק הצף.
        self.close_all_floating_windows()

        self.save_notes()

        self.tray.hide()

        event.accept()


if __name__ == "__main__":

    app = QApplication(sys.argv)

    settings = load_settings()

    CURRENT_SETTINGS.clear()
    CURRENT_SETTINGS.update(settings)

    app.setLayoutDirection(direction())

    window = MiniNotes()
    window.show()

    sys.exit(app.exec())