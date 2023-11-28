import tkinter as tk
from tkinter import Entry, Label, Button, messagebox

import numpy
import numpy as np
from scipy.optimize import linear_sum_assignment

# Maliyet matrisi giriş alanlarını oluşturun
matrix_entries = []
buttons = []  # Oluşturulan butonları saklayacak liste
is_okkey = False
labels = []

def clear_grid():
    for row in matrix_entries:
        for entry in row:
            entry.destroy()
    matrix_entries.clear()

def delete_buttons():
    for button in buttons:
        button.destroy()
    buttons.clear()  # Butonlar listesini temizleyin

def delete_labels():
    for label in labels:
        label.config(text="")

def create_grid(rows, columns):
    cell_width = 8  # Hücre genişliği

    for i in range(rows):
        matrix_entries.append([])
        for j in range(columns):
            entry = Entry(window,bg='#909090',fg="white", width=cell_width)  # Hücre boyutunu ayarla
            entry.place(x=150 + j * (cell_width * 7), y=135 + i * 28)  # Hücreleri yerleştirmek için place yöntemini kullanın
            matrix_entries[i].append(entry)

# Matris boyutlarına göre matrisi oluştur
def create_matrix(rows, columns):
    global is_okkey
    clear_grid()
    create_grid(rows, columns)
    delete_buttons()
    # Hesapla düğmesini ekleyin
    calculate_button = Button(window,bg='#909090',fg="white", text="Hesapla", command=calculate_hungarian)
    calculate_button.place(x=150 + ((columns) * 56), y=100 + rows * 28.5)  # Yerleştirmek için place yöntemini kullanın
    buttons.append(calculate_button)
    if is_okkey:
        result_label.config(bg='#898989',fg="white")
        sum_label.config(bg='#898989',fg="white")
    result_label.place(x=150, y=100 + (rows + 1) * 30)
    sum_label.place(x= 300 if columns <= 12 else 300 + (columns * 5)  , y=100 + (rows + 1) * 30 )
def SumResult(list):
    a = 0
    for item in list:
        for value in item:
            a += value
    return a
def calculate_hungarian():
    global is_okkey
    try:
        n = int(entry_rows.get())
        m = int(entry_columns.get())

        cost_matrix = np.zeros((n, m), dtype=int)
        default_matrix = np.zeros((n, m), dtype=int)

        for i in range(n):
            for j in range(m):
                cost_matrix[i, j] = int(matrix_entries[i][j].get())
                default_matrix[i, j] = int(matrix_entries[i][j].get())

        if checkbox_var.get():
            maxValue = cost_matrix.max()
            for i in range(n):
                for j in range(m):
                    if cost_matrix[i, j] != -1:
                        cost_matrix[i, j] = maxValue - int(matrix_entries[i][j].get())
                    else:
                        cost_matrix[i, j] = 999999999

        # Macar Çözümü
        row_ind, col_ind = linear_sum_assignment(cost_matrix)
        matches = list(zip(row_ind, col_ind))

        # Sonuç matrisini oluştur ve görüntüle
        result_matrix = np.zeros_like(default_matrix)
        for row, col in matches:
            result_matrix[row, col] = default_matrix[row, col]  # Eşleşme olan hücreleri işaretle

        result_label.config(text="Sonuç Matrisi:\n" + str(result_matrix),fg="white",borderwidth=3, relief="groove")
        sum_label.config(text="Toplam sonuç:\n" + str(SumResult(result_matrix)),fg="white",borderwidth=3, relief="groove")

        is_okkey = True

    except ValueError:
        messagebox.showerror("Hata", "Lütfen geçerli bir sayı girin.")

# Ana pencereyi oluştur
window = tk.Tk()
window.title("Macar Çözümü Uygulaması")

window.configure(bg="#909090")

checkbox_var = tk.BooleanVar()
checkbox = tk.Checkbutton(window, text="", variable=checkbox_var, fg="white",bg="#909090",selectcolor="#909090")
checkbox.place(x=145, y=10)
label = tk.Label(window, text="Maksimizasyon",bg="#909090",fg="white")
label.place(x=50, y=10)

# Satır ve sütun giriş alanlarını ekleyin
label_rows = Label(window, text="Satır Sayısı:",bg="#909090",fg="white")
label_rows.place(x=50, y=40)
entry_rows = Entry(window,bg='#909090',fg="white")
entry_rows.place(x=150, y=40)

label_columns = Label(window, text="Sütun Sayısı:",fg="white",bg="#909090")
label_columns.place(x=50, y=70)
entry_columns = Entry(window,bg='#909090',fg="white")
entry_columns.place(x=150, y=70)

# Matris oluştur butonunu ekleyin
create_matrix_button = Button(window, bg='#909090',fg="white",text="Matrisi Oluştur", command=lambda: create_matrix(int(entry_rows.get()), int(entry_columns.get())))
create_matrix_button.place(x=50, y=130)

# Sonuç matrisini görüntülemek için etiket oluşturun
result_label = Label(window,bg='#909090',fg="white")
sum_label = Label(window,bg='#909090',fg="white")
result_label.place(x=50, y=180)
sum_label.place(x=100, y=230)

window.mainloop()