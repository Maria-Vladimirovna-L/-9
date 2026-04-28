import tkinter as tk
from tkinter import ttk, messagebox, END
import json

DATA_FILE = "movies.json"
movies = []
filtered_movies = []

# --- Работа с JSON ---
def load_movies():
    global movies, filtered_movies
    try:
        with open(DATA_FILE, "r") as f:
            movies = json.load(f)
    except FileNotFoundError:
        movies = []
    filtered_movies = movies.copy()
    update_table()

def save_movies():
    with open(DATA_FILE, "w") as f:
        json.dump(movies, f, indent=2)

# --- Валидация ---
def is_valid_year(year_str):
    return year_str.isdigit() and len(year_str) == 4

def is_valid_rating(rating_str):
    try:
        rating = float(rating_str)
        return 0 <= rating <= 10
    except ValueError:
        return False

# --- Логика приложения ---
def add_movie():
    title = entry_title.get().strip()
    genre = entry_genre.get().strip()
    year = entry_year.get().strip()
    rating = entry_rating.get().strip()

    if not title or not genre or not year or not rating:
        messagebox.showerror("Ошибка", "Все поля должны быть заполнены!")
        return

    if not is_valid_year(year):
        messagebox.showerror("Ошибка", "Год должен быть числом из 4 цифр!")
        return

    if not is_valid_rating(rating):
        messagebox.showerror("Ошибка", "Рейтинг должен быть числом от 0 до 10!")
        return

    movie = {
        "title": title,
        "genre": genre,
        "year": int(year),
        "rating": float(rating)
    }
    movies.append(movie)
    save_movies()
    load_movies() # Обновляем данные и таблицу

    # Очищаем поля формы
    entry_title.delete(0, END)
    entry_genre.delete(0, END)
    entry_year.delete(0, END)
    entry_rating.delete(0, END)
    entry_title.focus()

def filter_movies():
    global filtered_movies
    genre_filter = entry_filter_genre.get().lower()
    year_filter = entry_filter_year.get()
    
    filtered_movies = movies.copy()
    
    if genre_filter:
        filtered_movies = [m for m in filtered_movies if genre_filter in m["genre"].lower()]
    
    if year_filter and year_filter.isdigit():
        filtered_movies = [m for m in filtered_movies if str(m["year"]) == year_filter]
    
    update_table()

def reset_filters():
    global filtered_movies
    entry_filter_genre.delete(0, END)
    entry_filter_year.delete(0, END)
    filtered_movies = movies.copy()
    update_table()

def update_table():
    for i in treeview.get_children():
        treeview.delete(i)
    for movie in filtered_movies:
        treeview.insert("", END, values=(movie["title"], movie["genre"], movie["year"], movie["rating"]))


# --- GUI ---
root = tk.Tk()
root.title("Movie Library")
root.geometry("900x550")
root.resizable(False, False)
root.configure(bg="#f0f0f5")

# --- Форма добавления ---
frame_form = tk.Frame(root, bg="#f0f0f5")
frame_form.pack(pady=10, padx=15, fill=tk.X)

tk.Label(frame_form, text="Название:", bg="#f0f0f5").grid(row=0, column=0, sticky="e", padx=5)
entry_title = tk.Entry(frame_form, width=35)
entry_title.grid(row=0, column=1, columnspan=3, sticky="w", padx=5)

tk.Label(frame_form, text="Жанр:", bg="#f0f0f5").grid(row=1, column=0, sticky="e", padx=5)
entry_genre = tk.Entry(frame_form, width=25)
entry_genre.grid(row=1, column=1, sticky="w", padx=5)

tk.Label(frame_form, text="Год:", bg="#f0f0f5").grid(row=1, column=2, sticky="e", padx=5)
entry_year = tk.Entry(frame_form, width=10)
entry_year.grid(row=1, column=3, sticky="w", padx=5)

tk.Label(frame_form, text="Рейтинг:", bg="#f0f0f5").grid(row=2, column=0, sticky="e", padx=5)
entry_rating = tk.Entry(frame_form, width=10)
entry_rating.grid(row=2, column=1, sticky="w", padx=5)

btn_add = tk.Button(frame_form, text="Добавить фильм", command=add_movie)
btn_add.grid(row=2, column=3, pady=10)


# --- Фильтры ---
frame_filters = tk.Frame(root, bg="#f0f0f5")
frame_filters.pack(pady=10, padx=15, fill=tk.X)

tk.Label(frame_filters, text="Фильтр по жанру:", bg="#f0f0f5").grid(row=0, column=0, sticky="e", padx=(5,2))
entry_filter_genre = tk.Entry(frame_filters, width=25)
entry_filter_genre.grid(row=0, column=1, sticky="w", padx=(2,15))

tk.Label(frame_filters, text="Фильтр по году:", bg="#f0f0f5").grid(row=0, column=2, sticky="e", padx=(15,2))
entry_filter_year = tk.Entry(frame_filters, width=10)
entry_filter_year.grid(row=0, column=3, sticky="w", padx=(2,5))

btn_filter = tk.Button(frame_filters, text="Фильтровать", command=filter_movies)
btn_filter.grid(row=1, columnspan=4, pady=5)
btn_reset = tk.Button(frame_filters, text="Сбросить фильтр", command=reset_filters)
btn_reset.grid(row=2, columnspan=4)


# --- Таблица ---
frame_table = tk.Frame(root)
frame_table.pack(pady=15, padx=15, fill='both', expand=True)

columns = ("Название", "Жанр", "Год", "Рейтинг")
treeview = ttk.Treeview(frame_table, columns=columns, show='headings')
for col in columns:
    treeview.heading(col, text=col)
treeview.column("Название", width=350)
treeview.column("Жанр", width=150)
treeview.column("Год", width=70)
treeview.column("Рейтинг", width=70)
treeview.pack(fill='both', expand=True)


# Запуск загрузки данных при старте приложения и запуск главного цикла
load_movies()
root.mainloop()
