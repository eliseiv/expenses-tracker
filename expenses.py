from tkinter import messagebox
from tkinter import ttk
import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import Calendar
import sqlite3
from datetime import datetime
import uuid

# Создание базы данных
db = sqlite3.connect('expenses.db')
c = db.cursor()
c.execute("""
    CREATE TABLE IF NOT EXISTS expenses (
        Category text,
        Amount real,
        Date text,
        Time text,
        ID text
    )
""")
db.commit()


# Функция для генерации уникального ID
def generate_short_id():
    return str(uuid.uuid4())[:10]


# Главное окно приложения
class ExpenseTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker")
        self.root.geometry("400x300")

        # Главное меню
        ttk.Label(root, text="Expense Tracker",
                  font=("Helvetica", 18)).pack(pady=10)

        ttk.Button(root, text="Add Expense", command=self.open_add_expense).pack(
            fill='x', padx=20, pady=5)
        ttk.Button(root, text="View Expenses", command=self.open_view_expenses).pack(
            fill='x', padx=20, pady=5)
        ttk.Button(root, text="Help", command=self.show_help).pack(
            fill='x', padx=20, pady=5)
        ttk.Button(root, text="Exit", command=root.quit).pack(
            fill='x', padx=20, pady=5)

    # Открыть окно добавления расходов
    def open_add_expense(self):
        AddExpenseWindow()

    # Открыть окно просмотра расходов
    def open_view_expenses(self):
        ViewExpensesWindow()

    # Окно помощи
    def show_help(self):
        messagebox.showinfo(
            "Help", "Use the buttons to add, view, and manage your expenses.")


# Окно для добавления расходов
class AddExpenseWindow:
    def __init__(self):
        self.window = tk.Toplevel()
        self.window.title("Add Expense")
        self.window.geometry("400x300")

        # Поле ввода категории
        ttk.Label(self.window, text="Category:").pack(pady=5)
        self.category_entry = ttk.Entry(self.window)
        self.category_entry.pack()

        # Поле ввода суммы
        ttk.Label(self.window, text="Amount:").pack(pady=5)
        self.amount_entry = ttk.Entry(self.window)
        self.amount_entry.pack()

        # Поле для выбора даты
        ttk.Label(self.window, text="Date:").pack(pady=5)
        self.date_frame = ttk.Frame(self.window)
        self.date_frame.pack(pady=5)

        self.date_entry = ttk.Entry(self.date_frame, width=20)
        self.date_entry.pack(side=tk.LEFT)

        calendar_icon = ttk.Button(
            self.date_frame, text="📅", command=self.open_calendar)
        calendar_icon.pack(side=tk.LEFT, padx=5)

        # Поле для выбора времени
        ttk.Label(self.window, text="Time:").pack(pady=5)
        self.time_frame = ttk.Frame(self.window)
        self.time_frame.pack(pady=5)

        self.time_entry = ttk.Entry(self.time_frame, width=20)
        self.time_entry.pack(side=tk.LEFT)

        time_icon = ttk.Button(self.time_frame, text="⏰",
                               command=self.open_time_picker)
        time_icon.pack(side=tk.LEFT, padx=5)

        # Кнопка для добавления расхода
        ttk.Button(self.window, text="Add",
                   command=self.add_expense).pack(pady=10)

    def open_calendar(self):
        """Открыть календарь для выбора даты."""
        self.calendar_window = tk.Toplevel(self.window)
        self.calendar_window.title("Select Date")
        self.calendar_window.geometry("300x300")

        cal = Calendar(self.calendar_window, date_pattern="dd-mm-yyyy")
        cal.pack(pady=20)

        def set_date():
            selected_date = cal.get_date()
            self.date_entry.delete(0, tk.END)
            self.date_entry.insert(0, selected_date)
            self.calendar_window.destroy()

        ttk.Button(self.calendar_window, text="Select",
                   command=set_date).pack(pady=10)

    def open_time_picker(self):
        """Открыть окно выбора времени."""
        def set_time():
            selected_time = f"{hour_var.get():02}:{minute_var.get():02}"
            self.time_entry.delete(0, tk.END)
            self.time_entry.insert(0, selected_time)
            self.time_window.destroy()

        self.time_window = tk.Toplevel(self.window)
        self.time_window.title("Select Time")
        self.time_window.geometry("200x150")

        # Часы и минуты
        hour_var = tk.IntVar(value=0)
        minute_var = tk.IntVar(value=0)

        ttk.Label(self.time_window, text="Hours:").pack(pady=5)
        hour_spinbox = ttk.Spinbox(
            self.time_window, from_=0, to=23, textvariable=hour_var, width=5)
        hour_spinbox.pack()

        ttk.Label(self.time_window, text="Minutes:").pack(pady=5)
        minute_spinbox = ttk.Spinbox(
            self.time_window, from_=0, to=59, textvariable=minute_var, width=5)
        minute_spinbox.pack()

        # Кнопка подтверждения
        ttk.Button(self.time_window, text="Set Time",
                   command=set_time).pack(pady=10)

    def add_expense(self):
        category = self.category_entry.get().strip()
        amount = self.amount_entry.get().strip()
        date = self.date_entry.get().strip()
        time = self.time_entry.get().strip()

        # Проверка обязательных полей
        if not category or not amount:
            messagebox.showerror("Error", "Category and Amount are required.")
            return

        try:
            amount = float(amount)
        except ValueError:
            messagebox.showerror("Error", "Amount must be a number.")
            return

        # Проверка даты и преобразование в YYYY-MM-DD для хранения в базе
        if not date:
            date = datetime.now().strftime("%Y-%m-%d")
        else:
            try:
                if "-" in date:
                    parsed_date = datetime.strptime(date, "%d-%m-%Y")
                elif "." in date:
                    parsed_date = datetime.strptime(date, "%d.%m.%Y")
                else:
                    raise ValueError
                date = parsed_date.strftime("%Y-%m-%d")
            except ValueError:
                messagebox.showerror(
                    "Error", "Invalid date format. Use DD-MM-YYYY or DD.MM.YYYY.")
                return

        # Проверка времени
        if not time:
            time = datetime.now().strftime("%H:%M:%S")
        else:
            try:
                datetime.strptime(time, "%H:%M")
                time += ":00"
            except ValueError:
                messagebox.showerror(
                    "Error", "Invalid time format. Use HH:MM.")
                return

        expense_id = generate_short_id()

        # Запись данных в базу данных
        c.execute("INSERT INTO expenses (Category, Amount, Date, Time, ID) VALUES (?, ?, ?, ?, ?)",
                  (category, amount, date, time, expense_id))
        db.commit()

        # Уведомление об успешном добавлении
        messagebox.showinfo("Success", "Expense added successfully.")
        self.window.destroy()


class ViewExpensesWindow:
    def __init__(self):
        self.window = tk.Toplevel()
        self.window.title("View Expenses")
        self.window.geometry("1000x600")

        # Уведомление вверху окна
        self.notification_label = ttk.Label(
            self.window, text="", foreground="red")
        self.notification_label.pack(pady=5)

        # Treeview для отображения расходов
        self.tree = ttk.Treeview(self.window, columns=(
            "Category", "Amount", "Date", "Time", "ID"), show="headings")
        self.tree.heading("Category", text="Category")
        self.tree.heading("Amount", text="Amount")
        self.tree.heading("Date", text="Date")
        self.tree.heading("Time", text="Time")
        self.tree.heading("ID", text="ID")
        self.tree.pack(fill='both', expand=True)

        # Кнопки управления
        button_frame = ttk.Frame(self.window)
        button_frame.pack(pady=10)

        ttk.Button(button_frame, text="Filter",
                   command=self.open_filter_window).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Reset",
                   command=self.reset_filters).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Edit Expense",
                   command=self.edit_expense).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Delete Expense",
                   command=self.delete_expense).pack(side=tk.LEFT, padx=5)

        # Загрузка всех расходов по умолчанию
        self.load_expenses()

    def load_expenses(self, category=None, date_from=None, date_to=None):
        for item in self.tree.get_children():
            self.tree.delete(item)

        query = "SELECT Category, Amount, Date, Time, ID FROM expenses WHERE 1=1"
        params = []

        if category:
            query += " AND Category LIKE ?"
            params.append(f"%{category}%")
        if date_from:
            query += " AND Date >= ?"
            params.append(date_from)
        if date_to:
            query += " AND Date <= ?"
            params.append(date_to)

        query += " ORDER BY Date DESC, Time DESC"

        for row in c.execute(query, params):
            category, amount, date, time, expense_id = row
            display_date = datetime.strptime(
                date, "%Y-%m-%d").strftime("%d-%m-%Y")
            self.tree.insert("", "end", values=(
                category, amount, display_date, time, expense_id))

    def reset_filters(self):
        self.load_expenses()

    def reset_filters(self):
        self.load_expenses()

    def open_filter_window(self):
        # Окно фильтрации
        self.filter_window = tk.Toplevel(self.window)
        self.filter_window.title("Filter Expenses")
        self.filter_window.geometry("400x400")

        # Поле для выбора категории
        ttk.Label(self.filter_window, text="Category:").pack(pady=5)
        self.category_entry = ttk.Combobox(
            self.filter_window, values=self.get_categories())
        self.category_entry.pack()
        self.category_entry.set("")

        # Поле для выбора начальной даты
        ttk.Label(self.filter_window, text="Date From:").pack(pady=5)
        date_from_frame = ttk.Frame(self.filter_window)
        date_from_frame.pack(pady=5)

        self.date_from_entry = ttk.Entry(date_from_frame, width=20)
        self.date_from_entry.pack(side=tk.LEFT)

        from_calendar_btn = ttk.Button(
            date_from_frame, text="📅", command=lambda: self.open_calendar(self.date_from_entry))
        from_calendar_btn.pack(side=tk.LEFT)

        # Поле для выбора конечной даты
        ttk.Label(self.filter_window, text="Date To:").pack(pady=5)
        date_to_frame = ttk.Frame(self.filter_window)
        date_to_frame.pack(pady=5)

        self.date_to_entry = ttk.Entry(date_to_frame, width=20)
        self.date_to_entry.pack(side=tk.LEFT)

        to_calendar_btn = ttk.Button(
            date_to_frame, text="📅", command=lambda: self.open_calendar(self.date_to_entry))
        to_calendar_btn.pack(side=tk.LEFT)

        # Кнопка подтверждения фильтрации
        ttk.Button(self.filter_window, text="Apply Filter",
                   command=self.apply_filter).pack(pady=20)

    def open_calendar(self, entry_field):
        # Открыть календарь и установить выбранную дату в поле ввода
        calendar_window = tk.Toplevel(self.filter_window)
        calendar_window.title("Select Date")
        calendar = Calendar(calendar_window, date_pattern="dd-mm-yyyy")
        calendar.pack(pady=20)

        def set_date():
            selected_date = calendar.get_date()
            entry_field.delete(0, tk.END)
            entry_field.insert(0, selected_date)
            calendar_window.destroy()

        ttk.Button(calendar_window, text="Select",
                   command=set_date).pack(pady=10)

    def apply_filter(self):
        # Получить данные из полей фильтрации
        category = self.category_entry.get().strip()
        date_from = self.date_from_entry.get().strip()
        date_to = self.date_to_entry.get().strip()

        # Проверить правильность формата дат
        try:
            date_from = datetime.strptime(
                date_from, "%d-%m-%Y").strftime("%Y-%m-%d") if date_from else None
            date_to = datetime.strptime(
                date_to, "%d-%m-%Y").strftime("%Y-%m-%d") if date_to else None
        except ValueError:
            messagebox.showerror(
                "Error", "Invalid date format. Use DD-MM-YYYY.")
            return

        # Загрузить отфильтрованные расходы
        self.load_expenses(category, date_from, date_to)
        self.filter_window.destroy()

    def get_categories(self):
        # Получить уникальные категории из базы данных
        c.execute("SELECT DISTINCT Category FROM expenses")
        return [row[0] for row in c.fetchall()]

    def notify(self, message):
        """Отображает уведомление и автоматически скрывает его через 3 секунды."""
        self.notification_label.config(text=message)
        self.window.after(
            3000, lambda: self.notification_label.config(text=""))

    def edit_expense(self):
        selected_item = self.tree.focus()
        if not selected_item:
            self.notify("Please select an expense to edit.")
            return

        values = self.tree.item(selected_item, "values")
        if not values:
            return

        category, amount, date, time, expense_id = values

        # Создание окна редактирования
        edit_window = tk.Toplevel(self.window)
        edit_window.title("Edit Expense")
        edit_window.geometry("400x300")

        ttk.Label(edit_window, text="Category:").pack(pady=5)
        category_entry = ttk.Entry(edit_window)
        category_entry.insert(0, category)
        category_entry.pack()

        ttk.Label(edit_window, text="Amount:").pack(pady=5)
        amount_entry = ttk.Entry(edit_window)
        amount_entry.insert(0, amount)
        amount_entry.pack()

        ttk.Label(edit_window, text="Date (DD-MM-YYYY):").pack(pady=5)
        date_entry = ttk.Entry(edit_window)
        date_entry.insert(0, date)
        date_entry.pack()

        ttk.Label(edit_window, text="Time (HH:MM):").pack(pady=5)
        time_entry = ttk.Entry(edit_window)
        time_entry.insert(0, time)
        time_entry.pack()

        def accept_changes():
            new_category = category_entry.get().strip()
            new_amount = amount_entry.get().strip()
            new_date = date_entry.get().strip()
            new_time = time_entry.get().strip()

            try:
                # Преобразование суммы
                new_amount = float(new_amount)

                # Проверка и преобразование формата даты
                new_date = datetime.strptime(
                    new_date, "%d-%m-%Y").strftime("%Y-%m-%d")

                # Проверка формата времени
                new_time = datetime.strptime(
                    new_time, "%H:%M:%S").strftime("%H:%M:%S")
            except ValueError:
                messagebox.showerror("Error", "Invalid data format.")
                return

            # Обновление записи в базе данных
            c.execute(
                "UPDATE expenses SET Category = ?, Amount = ?, Date = ?, Time = ? WHERE ID = ?",
                (new_category, new_amount, new_date, new_time, expense_id)
            )
            db.commit()
            self.load_expenses()
            edit_window.destroy()

        ttk.Button(edit_window, text="Accept",
                   command=accept_changes).pack(pady=10)
        ttk.Button(edit_window, text="Cancel",
                   command=edit_window.destroy).pack(pady=10)

    def delete_expense(self):
        selected_item = self.tree.focus()
        if not selected_item:
            self.notify("Please select an expense to delete.")
            return

        values = self.tree.item(selected_item, "values")
        if not values:
            return

        expense_id = values[4]

        confirm_window = tk.Toplevel(self.window)
        confirm_window.title("Confirm Deletion")
        confirm_window.geometry("300x150")

        ttk.Label(
            confirm_window, text="Are you sure you want to delete this expense?").pack(pady=20)

        def confirm_delete():
            c.execute("DELETE FROM expenses WHERE ID = ?", (expense_id,))
            db.commit()
            self.load_expenses()
            confirm_window.destroy()

        ttk.Button(confirm_window, text="Accept",
                   command=confirm_delete).pack(side=tk.LEFT, padx=10)
        ttk.Button(confirm_window, text="Cancel",
                   command=confirm_window.destroy).pack(side=tk.RIGHT, padx=10)


# Запуск приложения
if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTrackerApp(root)
    root.mainloop()
