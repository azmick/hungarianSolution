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
            entry = Entry(window, bg='#909090', fg="white", width=cell_width)  # Hücre boyutunu ayarla
            entry.place(x=150 + j * (cell_width * 7),
                        y=135 + i * 28)  # Hücreleri yerleştirmek için place yöntemini kullanın
            matrix_entries[i].append(entry)


# Matris boyutlarına göre matrisi oluştur
def create_matrix(rows, columns):
    global is_okkey
    clear_grid()
    create_grid(rows, columns)
    delete_buttons()
    # Hesapla düğmesini ekleyin
    calculate_button = Button(window, bg='#909090', fg="white", text="Hesapla", command=calculate_hungarian)
    calculate_button.place(x=150 + ((columns) * 56), y=100 + rows * 28.5)  # Yerleştirmek için place yöntemini kullanın
    buttons.append(calculate_button)
    if is_okkey:
        result_label.config(bg='#898989', fg="white")
        sum_label.config(bg='#898989', fg="white")
    result_label.place(x=150, y=100 + (rows + 1) * 30)
    sum_label.place(x=300 if columns <= 12 else 300 + (columns * 5), y=100 + (rows + 1) * 30)


def SumResult(list):
    a = 0
    for item in list:
        for value in item:
            a += value
    return a


def calculate_hungarian():
    global is_okkey
    try:
        r = int(entry_rows.get())
        c = int(entry_columns.get())
        fake_c = 0
        fake_r = 0

        if c > r:
            fake_r = c
            fake_c = c
        else:
            fake_c = r
            fake_r = r

        cost_matrix = np.zeros((fake_r, fake_c), dtype=int)
        default_matrix = np.zeros((fake_r, fake_c), dtype=int)

        for i in range(r):
            for j in range(c):
                cost_matrix[i, j] = int(matrix_entries[i][j].get())
                default_matrix[i, j] = int(matrix_entries[i][j].get())

        if checkbox_var.get():
            maxValue = cost_matrix.max()
            for i in range(r):
                for j in range(c):
                    if cost_matrix[i, j] != -1:
                        cost_matrix[i, j] = maxValue - int(matrix_entries[i][j].get())
                    else:
                        cost_matrix[i, j] = 999999999
        else:
            for i in range(r):
                for j in range(c):
                    if cost_matrix[i, j] == -1:
                        cost_matrix[i, j] = 999999999

        r = fake_r
        c = fake_c
        # Macar Çözümü
        RowDecrease(cost_matrix, c, r)
        ColumnDecrease(cost_matrix, r, c)
        result_matrix = FindLines(cost_matrix, c, r, default_matrix)
        # Sonuç matrisini oluştur ve görüntüle

        result_label.config(text="Sonuç Matrisi:\n" + str(result_matrix), fg="white", borderwidth=3, relief="groove")
        sum_label.config(text="Toplam sonuç:\n" + str(SumResult(result_matrix)), fg="white", borderwidth=3,
                         relief="groove")

        is_okkey = True

    except ValueError:
        messagebox.showerror("Hata", "Lütfen geçerli bir sayı girin.")


chosenZeros = []


def FindLines(cost_matrix, m, n, default_matrix):
    allZerosList = []  # fill allZerosList list // # X,Y,IsMarked,XCount,YCount, lineX, lineY
    lineCount = 0

    for i in range(n):
        for j in range(m):
            if (cost_matrix[i][j] == 0):
                allZerosList.append([i, j, False, 0, 0, 0, 0])  # fill allZerosList list
    for i in range(len(allZerosList)):  # tüm sıfırları tek tek dön
        yCount = 0
        xCount = 0
        for j in range(len(allZerosList)):  # bir adet sıfır için satır ve sütundaki toplam sıfır değerlerini bul
            if (allZerosList[i][1] == allZerosList[j][1]):
                yCount += 1
            if (allZerosList[i][0] == allZerosList[j][0]):
                xCount += 1
        allZerosList[i][3] = xCount
        allZerosList[i][4] = yCount

    for i in range(len(allZerosList)):  # tüm sıfırları tek tek dön
        yCount = 0
        xCount = 0
        if allZerosList[i][2] != True:  # if unmark
            if allZerosList[i][4] > allZerosList[i][
                3]:  # Y ekseni (sütun kontrolü)  # 0'ların eksenlerindeki 0 sayılarını karşılaştır
                for k in range(len(allZerosList)):
                    if allZerosList[i][1] == allZerosList[k][1]:
                        allZerosList[k][2] = True
                        allZerosList[k][6] = 1
            else:  # X ekseni (satır kontrolü)
                for k in range(len(allZerosList)):
                    if allZerosList[i][0] == allZerosList[k][0]:
                        allZerosList[k][2] = True
                        allZerosList[k][5] = 1

            lineCount += 1
    # çizgiler bulundu, sıfırları bulucaz.
    # Find single zeros
    FindSingleZeros(cost_matrix, default_matrix, allZerosList, lineCount, m)  # fill the chozenZeros list

    # sıfırların konumunu bulduk
    return FindResultMatrix(default_matrix, m, n)


def FindSingleZeros(cost_matrix, default_matrix, allZerosList, lineCount, m):
    if lineCount >= m:
        for i in range(len(allZerosList)):  # tüm markable değerlerini false'a çektik
            allZerosList[i][2] = False

        for k in range(m):
            for i in range(
                    len(allZerosList)):  # satır veya sütünda sadece bir tane bulunan sıfırları tek tek alma kısmı
                if allZerosList[i][2]:
                    continue
                if (allZerosList[i][3] == (k + 1)) | (allZerosList[i][4] == (k + 1)):
                    allZerosList[i][2] = True
                    chosenZeros.append([allZerosList[i][0], allZerosList[i][1]])
                    for j in range(len(allZerosList)):  # seçilen sıfırın satı ve sütunundaki düğer sıfırları kilitliyor
                        if (allZerosList[j][0] == allZerosList[i][0]) | (allZerosList[j][1] == allZerosList[i][1]):
                            allZerosList[j][2] = True
    else:
        emanuelList = []
        for x in range(m):
            for y in range(m):
                counter = 0
                foundX = False
                foundY = False
                for k in allZerosList:
                    if (k[0] == x) & (k[5] == 1) & (not foundX):
                        counter += 1
                        foundX = True
                    if (k[1] == y) & (k[6] == 1) & (not foundY):
                        counter += 1
                        foundY = True
                emanuelList.append([cost_matrix[x][y], x, y, counter])
        emanuelList.sort(key=lambda xx: (xx[3], xx[0]))
        minValue = emanuelList[0][0]
        for item in emanuelList:
            if item[3] == 0:
                item[0] -= minValue
            if item[3] == 2:
                item[0] += minValue
        for item in emanuelList:
            cost_matrix[item[1]][item[2]] = item[0]

        FindLines(cost_matrix, m, m, default_matrix)


def FindResultMatrix(default_matrix, m, n):
    result_matrix = np.zeros((n, m), dtype=int)
    for i in range(len(chosenZeros)):
        result_matrix[chosenZeros[i][0]][chosenZeros[i][1]] = default_matrix[chosenZeros[i][0]][chosenZeros[i][1]]
    return result_matrix


def RowDecrease(cost_matrix, m, n):
    for i in range(n):
        rowList = []
        for j in range(m):
            rowList.append(cost_matrix[i][j])
        rowList.sort()
        minValue = rowList[0]
        for j in range(m):
            cost_matrix[i][j] -= minValue


def ColumnDecrease(cost_matrix, m, n):
    for i in range(n):
        rowList = []
        for j in range(m):
            rowList.append(cost_matrix[j][i])
        rowList.sort()
        minValue = rowList[0]
        for j in range(m):
            cost_matrix[j][i] -= minValue


# Ana pencereyi oluştur
window = tk.Tk()
window.title("Macar Çözümü Uygulaması")

window.configure(bg="#909090", height=500, width=700)

checkbox_var = tk.BooleanVar()
checkbox = tk.Checkbutton(window, text="", variable=checkbox_var, fg="white", bg="#909090", selectcolor="#909090")
checkbox.place(x=145, y=10)
label = tk.Label(window, text="Maksimizasyon", bg="#909090", fg="white")
label.place(x=50, y=10)

# Satır ve sütun giriş alanlarını ekleyin
label_rows = Label(window, text="Satır Sayısı:", bg="#909090", fg="white")
label_rows.place(x=50, y=40)
entry_rows = Entry(window, bg='#909090', fg="white")
entry_rows.place(x=150, y=40)

label_columns = Label(window, text="Sütun Sayısı:", fg="white", bg="#909090")
label_columns.place(x=50, y=70)
entry_columns = Entry(window, bg='#909090', fg="white")
entry_columns.place(x=150, y=70)

# Matris oluştur butonunu ekleyin
create_matrix_button = Button(window, bg='#909090', fg="white", text="Matrisi Oluştur",
                              command=lambda: create_matrix(int(entry_rows.get()), int(entry_columns.get())))
create_matrix_button.place(x=50, y=130)

# Sonuç matrisini görüntülemek için etiket oluşturun
result_label = Label(window, bg='#909090', fg="white")
sum_label = Label(window, bg='#909090', fg="white")
result_label.place(x=50, y=180)
sum_label.place(x=100, y=230)

window.mainloop()
