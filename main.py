import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import random
import datetime

from tasks import TASKS
from storage import load_history, save_history

TASK_TYPES = ["учёба", "спорт", "работа"]


def on_generate():
    """Генерирует случайную задачу из текущего пула и добавляет в историю."""
    pool = get_filtered_pool()
    if not pool:
        messagebox.showinfo("Нет задач", "По выбранному фильтру задачи не найдены.")
        return

    task = random.choice(pool)
    current_task_var.set(f'{task["task"]}  [{task["type"]}]')

    record = {
        "task": task["task"],
        "type": task["type"],
        "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    history.append(record)
    save_history(history)
    refresh_history_list()


def get_filtered_pool() -> list:
    """Возвращает пул задач с учётом выбранного типа фильтра."""
    selected_type = filter_type_combo.get()
    if selected_type and selected_type != "Все":
        return [t for t in all_tasks if t["type"] == selected_type]
    return all_tasks[:]


def refresh_history_list():
    """Обновляет список истории задач."""
    history_listbox.delete(0, tk.END)
    for rec in history:
        history_listbox.insert(
            tk.END,
            f'[{rec.get("date", "")}] [{rec["type"]}]  {rec["task"]}',
        )


def on_add_custom():
    """Открывает диалог для добавления своей задачи."""
    task_text = simpledialog.askstring("Новая задача", "Введите текст задачи:")
    if task_text is None:
        return
    if not task_text.strip():
        messagebox.showerror("Ошибка", "Текст задачи не может быть пустым.")
        return

    type_win = tk.Toplevel(root)
    type_win.title("Тип задачи")
    type_win.geometry("260x120")
    type_win.grab_set()

    tk.Label(type_win, text="Выберите тип задачи:").pack(pady=8)
    type_var = tk.StringVar(value="учёба")
    ttk.Combobox(type_win, values=TASK_TYPES, textvariable=type_var, state="readonly", width=16).pack()

    def confirm():
        all_tasks.append({"task": task_text.strip(), "type": type_var.get()})
        type_win.destroy()
        messagebox.showinfo("Успех", "Задача добавлена!")

    tk.Button(type_win, text="Добавить", command=confirm, bg="#4CAF50", fg="white").pack(pady=8)


# ── Главное окно ──────────────────────────────────────────────────────────────
root = tk.Tk()
root.title("Random Task Generator — Генератор задач")
root.geometry("680x580")
root.resizable(False, False)

all_tasks = TASKS[:]

# ── Фильтр ────────────────────────────────────────────────────────────────────
flt = tk.LabelFrame(root, text="Фильтр по типу задачи", padx=10, pady=6)
flt.pack(fill=tk.X, padx=12, pady=8)

tk.Label(flt, text="Тип:").pack(side=tk.LEFT)
filter_type_combo = ttk.Combobox(flt, values=["Все"] + TASK_TYPES, state="readonly", width=16)
filter_type_combo.set("Все")
filter_type_combo.pack(side=tk.LEFT, padx=8)

# ── Кнопки ────────────────────────────────────────────────────────────────────
btn_frm = tk.Frame(root)
btn_frm.pack(fill=tk.X, padx=12, pady=4)
tk.Button(
    btn_frm, text="🎲  Сгенерировать задачу", command=on_generate,
    bg="#673AB7", fg="white", padx=14, pady=5,
).pack(side=tk.LEFT, padx=4)
tk.Button(
    btn_frm, text="➕  Добавить свою задачу", command=on_add_custom,
    bg="#FF5722", fg="white", padx=14, pady=5,
).pack(side=tk.LEFT, padx=4)

# ── Текущая задача ────────────────────────────────────────────────────────────
task_frm = tk.LabelFrame(root, text="Текущая задача", padx=10, pady=8)
task_frm.pack(fill=tk.X, padx=12, pady=6)
current_task_var = tk.StringVar(value="Нажмите «Сгенерировать задачу»")
tk.Label(task_frm, textvariable=current_task_var, font=("Arial", 12, "bold"),
         wraplength=600, anchor=tk.W, justify=tk.LEFT).pack(fill=tk.X)

# ── История ───────────────────────────────────────────────────────────────────
hist_frm = tk.LabelFrame(root, text="История сгенерированных задач", padx=8, pady=6)
hist_frm.pack(fill=tk.BOTH, expand=True, padx=12, pady=6)
history_listbox = tk.Listbox(hist_frm, font=("Consolas", 9), height=14)
sb = ttk.Scrollbar(hist_frm, orient=tk.VERTICAL, command=history_listbox.yview)
history_listbox.configure(yscrollcommand=sb.set)
history_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
sb.pack(side=tk.RIGHT, fill=tk.Y)

# ── Загрузка ──────────────────────────────────────────────────────────────────
history = load_history()
refresh_history_list()

root.mainloop()
