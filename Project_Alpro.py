
import customtkinter as ctk
from tkinter import END
from tkinter import simpledialog, messagebox

import matplotlib.pyplot as plt

from datetime import datetime
from collections import defaultdict

import csv
import os
import time

# ================= DATA =================

food_db = {
    "Nasi Goreng 🍚": 500,
    "Bakso 🍜": 300,
    "Mie Ayam 🍲": 450,
    "Ayam Goreng 🍗": 250,
    "Es Teh 🧋": 150
}

riwayat_harian = []
riwayat_detail = []

TARGET_HARIAN = 2000

FILE_HISTORY = "history.csv"
FOOD_FILE = "foods.csv"
DAILY_FILE = "daily_summary.csv"

# ================= FUNCTIONS =================

def tambah_konsumsi():

    makanan = makanan_var.get()

    # ==========================
    # Validasi makanan
    # ==========================

    if not makanan:

        messagebox.showerror(
            "Error",
            "Silakan pilih makanan."
        )

        return

    # ==========================
    # Validasi porsi
    # ==========================

    try:

        porsi = int(
            porsi_entry.get()
        )

        if porsi <= 0:

            messagebox.showerror(
                "Error",
                "Jumlah porsi harus lebih dari 0."
            )

            return

    except ValueError:

        messagebox.showerror(
            "Error",
            "Masukkan jumlah porsi yang valid."
        )

        return

    # ==========================
    # Hitung kalori
    # ==========================

    kalori = food_db[makanan] * porsi

    tanggal = datetime.now().strftime("%Y-%m-%d")

    waktu = datetime.now().strftime("%H:%M")

    # ==========================
    # Simpan ke list
    # ==========================

    riwayat_harian.append(
        kalori
    )

    riwayat_detail.append([
        tanggal,
        waktu,
        makanan,
        porsi,
        kalori
    ])

    # ==========================
    # Simpan ke history.csv
    # ==========================

    simpan_csv()

    # ==========================
    # Update riwayat
    # ==========================

    update_riwayat()

    # ==========================
    # Hitung total kalori
    # ==========================

    total = sum(
        riwayat_harian
    )

    kalori_label.configure(
        text=f"{total} kcal"
    )

    persen = min(
        total / TARGET_HARIAN,
        1
    )

    progress.set(
        persen
    )

    progress_label.configure(
        text=f"{int(persen*100)}%"
    )

    # ==========================
    # Update status
    # ==========================

    if total < 1500:

        status_label.configure(
            text="KURANG ⚠️",
            text_color="#F5A623"
        )

    elif total <= TARGET_HARIAN:

        status_label.configure(
            text="IDEAL ✅",
            text_color="#28A745"
        )

    else:

        status_label.configure(
            text="BERLEBIH 🔥",
            text_color="#E74C3C"
        )

    # ==========================
    # Bersihkan form
    # ==========================

    porsi_entry.delete(
        0,
        END
    )

    dropdown.set("")


def update_riwayat():

    riwayat_box.delete("1.0", END)

    if not riwayat_detail:
        riwayat_box.insert(
            END,
            "Belum ada konsumsi hari ini."
        )
        return

    for item in reversed(riwayat_detail):

        try:
            riwayat_box.insert(
                END,
                f"{item[0]} | {item[1]} | {item[2]} | {item[3]} porsi | {item[4]} kcal\n"
            )

        except:
            pass

def simpan_csv():

    with open(
        FILE_HISTORY,
        "w",
        newline="",
        encoding="utf-8"
    ) as f:

        writer = csv.writer(f)

        writer.writerow([
            "Tanggal",
            "Waktu",
            "Makanan",
            "Porsi",
            "Kalori"
        ])

        writer.writerows(riwayat_detail)

def load_csv():

    riwayat_harian.clear()
    riwayat_detail.clear()

    if not os.path.exists(FILE_HISTORY):

        update_riwayat()

        return

    today = datetime.now().strftime("%Y-%m-%d")

    with open(
        FILE_HISTORY,
        newline="",
        encoding="utf-8"
    ) as f:

        reader = csv.reader(f)

        next(reader, None)

        for row in reader:

            if len(row) != 5:
                continue

            try:

                tanggal = row[0]

                if tanggal != today:
                    continue

                waktu = row[1]
                makanan = row[2]
                porsi = int(row[3])
                kalori = int(row[4])

                riwayat_detail.append([
                    tanggal,
                    waktu,
                    makanan,
                    porsi,
                    kalori
                ])

                riwayat_harian.append(kalori)

            except:
                continue

    update_riwayat()

    total = sum(riwayat_harian)

    kalori_label.configure(
        text=f"{total} kcal"
    )

    persen = min(
        total / TARGET_HARIAN,
        1
    )

    progress.set(persen)

    progress_label.configure(
        text=f"{int(persen * 100)}%"
    )

    if total < 1500:

        status_label.configure(
            text="KURANG ⚠️",
            text_color="#F5A623"
        )

    elif total <= TARGET_HARIAN:

        status_label.configure(
            text="IDEAL ✅",
            text_color="#28A745"
        )

    else:

        status_label.configure(
            text="BERLEBIH 🔥",
            text_color="#E74C3C"
        )

def load_progress():

    if not os.path.exists(DAILY_FILE):
        return 0

    with open(
        DAILY_FILE,
        newline="",
        encoding="utf-8"
    ) as f:

        reader = csv.reader(f)

        data = list(reader)

    return len(data)

def simpan_makanan():

    with open(
        FOOD_FILE,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(file)

        for nama, kalori in food_db.items():
            writer.writerow([nama, kalori])

def load_makanan():

    if not os.path.exists(FOOD_FILE):
        return

    with open(
        FOOD_FILE,
        newline="",
        encoding="utf-8"
    ) as file:

        reader = csv.reader(file)

        for row in reader:

            if len(row) != 2:
                continue

            try:
                food_db[row[0]] = int(row[1])
            except:
                continue

def tambah_makanan_baru():

    nama = simpledialog.askstring(
        "Tambah Makanan",
        "Masukkan nama makanan:"
    )

    if not nama:
        return

    try:
        kalori = int(
            simpledialog.askstring(
                "Kalori",
                "Kalori per porsi:"
            )
        )

    except:
        messagebox.showerror(
            "Error",
            "Kalori harus berupa angka."
        )
        return

    food_db[nama] = kalori

    dropdown.configure(
        values=list(food_db.keys())
    )

    simpan_makanan()

    messagebox.showinfo(
        "Berhasil",
        f"{nama} berhasil ditambahkan!"
    )

def simpan_hari_ini():

    if len(riwayat_harian) == 0:

        messagebox.showinfo(
            "Info",
            "Belum ada konsumsi hari ini."
        )

        return

    total = sum(riwayat_harian)

    # ==========================
    # Baca progress mingguan
    # ==========================

    data = []

    if os.path.exists(DAILY_FILE):

        with open(
            DAILY_FILE,
            newline="",
            encoding="utf-8"
        ) as f:

            reader = csv.reader(f)

            for row in reader:

                if len(row) != 2:
                    continue

                data.append(row)

    # ==========================
    # Reset jika sudah 7 hari
    # ==========================

    if len(data) >= 7:
        data = []

    # ==========================
    # Tambah hari baru
    # ==========================

    hari = len(data) + 1

    data.append([
        str(hari),
        str(total)
    ])

    # ==========================
    # Simpan daily_summary.csv
    # ==========================

    with open(
        DAILY_FILE,
        "w",
        newline="",
        encoding="utf-8"
    ) as f:

        writer = csv.writer(f)

        writer.writerows(data)

    # ==========================
    # Update progress sidebar
    # ==========================

    jumlah = load_progress()

    progress_mingguan.configure(
    text=f"📅 Progress : {jumlah}/7 Hari"
)

    # ==========================
    # Reset tampilan hari ini
    # ==========================

    riwayat_harian.clear()
    riwayat_detail.clear()

    update_riwayat()

    kalori_label.configure(
        text="0 kcal"
    )

    progress.set(0)

    progress_label.configure(
        text="0%"
    )

    status_label.configure(
        text="KURANG ⚠️",
        text_color="#F5A623"
    )

    porsi_entry.delete(0, END)

    dropdown.set("")

    messagebox.showinfo(
        "Berhasil",
        f"Hari ke-{hari} berhasil disimpan!"
    )

def buka_grafik():

    if not os.path.exists(DAILY_FILE):

        messagebox.showinfo(
            "Grafik",
            "Belum ada data."
        )

        return

    hari = []
    kalori = []

    with open(
        DAILY_FILE,
        newline="",
        encoding="utf-8"
    ) as f:

        reader = csv.reader(f)

        for row in reader:

            if len(row) != 2:
                continue

            try:

                hari.append(
                    f"Hari {int(row[0])}"
                )

                kalori.append(
                    int(row[1])
                )

            except:
                continue

    if len(hari) == 0:

        messagebox.showinfo(
            "Grafik",
            "Belum ada data."
        )

        return

    plt.figure(figsize=(9,5))

    bars = plt.bar(
        hari,
        kalori
    )

    # angka di atas batang
    for bar in bars:

        tinggi = bar.get_height()

        plt.text(
            bar.get_x() + bar.get_width()/2,
            tinggi + 30,
            f"{int(tinggi)}",
            ha="center"
        )

    plt.axhline(
        TARGET_HARIAN,
        color="red",
        linestyle="--",
        label=f"Target ({TARGET_HARIAN} kcal)"
    )

    plt.title(
        "📈 Grafik Challenge 7 Hari"
    )

    plt.xlabel(
        "Hari"
    )

    plt.ylabel(
        "Kalori (kcal)"
    )

    plt.grid(
        axis="y",
        linestyle="--",
        alpha=0.3
    )

    plt.legend()

    plt.tight_layout()

    plt.show()

def rekap_mingguan():

    if not os.path.exists(DAILY_FILE):

        messagebox.showinfo(
            "Rekap",
            "Belum ada data."
        )

        return

    data = []

    with open(
        DAILY_FILE,
        newline="",
        encoding="utf-8"
    ) as f:

        reader = csv.reader(f)

        for row in reader:

            if len(row) != 2:
                continue

            try:

                hari = int(row[0])
                kalori = int(row[1])

                data.append((hari, kalori))

            except:
                continue

    if len(data) == 0:

        messagebox.showinfo(
            "Rekap",
            "Belum ada data."
        )

        return

    total = sum(
        kal
        for _, kal in data
    )

    rata = total / len(data)

    tertinggi = max(
        kal
        for _, kal in data
    )

    terendah = min(
        kal
        for _, kal in data
    )

    hari_tertinggi = max(
        data,
        key=lambda x: x[1]
    )[0]

    hari_terendah = min(
        data,
        key=lambda x: x[1]
    )[0]

    target = sum(
        1
        for _, kal in data
        if kal <= TARGET_HARIAN
    )

    persentase = (
        target / len(data)
    ) * 100

    hasil = f"""
📊 REKAP 7 HARI

Progress :
{len(data)}/7 Hari

Total Kalori :
{total} kcal

Rata-rata :
{rata:.1f} kcal

Kalori Tertinggi :
{tertinggi} kcal
(Hari {hari_tertinggi})

Kalori Terendah :
{terendah} kcal
(Hari {hari_terendah})

Target Tercapai :
{target}/7 Hari

Persentase :
{persentase:.1f}%
"""

    messagebox.showinfo(
        "Rekap Mingguan",
        hasil
    )

def splash_screen():

    splash = ctk.CTk()

    splash.geometry("500x300")
    splash.title("SmartCal Tracker")
    splash.resizable(False, False)

    ctk.CTkLabel(
        splash,
        text="🍎",
        font=("Arial", 60)
    ).pack(pady=(40,10))

    ctk.CTkLabel(
        splash,
        text="SmartCal Tracker",
        font=("Arial", 26, "bold")
    ).pack()

    ctk.CTkLabel(
        splash,
        text="Calorie Tracking Application",
        font=("Arial", 15)
    ).pack(pady=5)

    progress = ctk.CTkProgressBar(
        splash,
        width=300
    )

    progress.pack(
        pady=25
    )

    progress.set(0)

    splash.update()

    for i in range(101):

        progress.set(i/100)

        splash.update()

        time.sleep(0.015)

    splash.destroy()
splash_screen()

app = ctk.CTk()
app.title("🍎 SmartCal Tracker")
app.geometry("1400x850")

BACKGROUND = "#DFF4FF"
SIDEBAR = "#BFA2FF"
CARD = "#FFFFFF"

app.configure(fg_color=BACKGROUND)

sidebar = ctk.CTkFrame(app, width=220, fg_color=SIDEBAR, corner_radius=0)
sidebar.pack(side="left", fill="y")

logo = ctk.CTkLabel(
    sidebar,
    text="🍎\nSmartCal\nTracker",
    font=("Arial", 30, "bold"),
    text_color="white"
)
logo.pack(pady=35)

ctk.CTkLabel(
    sidebar,
    text="Stay Healthy ✨",
    text_color="white"
).pack()

ctk.CTkButton(
    sidebar,
    text="💾 Simpan Hari Ini",
    command=simpan_hari_ini
).pack(
    fill="x",
    padx=15,
    pady=8
)

# ==========================
# LABEL PROGRESS MINGGUAN
# ==========================
progress_mingguan = ctk.CTkLabel(
    sidebar,
    text="📅 Progress : 0/7 Hari",
    font=("Arial", 14, "bold"),
    text_color="white"
)

progress_mingguan.pack(
    pady=8
)

ctk.CTkButton(
    sidebar,
    text="📈 Lihat Grafik",
    command=buka_grafik
).pack(
    fill="x",
    padx=15,
    pady=8
)

ctk.CTkButton(
    sidebar,
    text="📊 Rekap Mingguan",
    command=rekap_mingguan
).pack(
    fill="x",
    padx=15,
    pady=8
)


main = ctk.CTkFrame(app, fg_color=BACKGROUND)
main.pack(side="right", fill="both", expand=True)

header = ctk.CTkLabel(
    main,
    text="👋 Hai! Selamat Datang di SmartCal Tracker",
    font=("Arial", 28, "bold"),
    text_color="black"
)
header.pack(anchor="w", padx=25, pady=(25, 5))

sub = ctk.CTkLabel(
    main,
    text="Pantau kalori harianmu dengan lebih mudah 💜",
    font=("Arial", 16),
    text_color="black"
)
sub.pack(anchor="w", padx=25)

card_frame = ctk.CTkFrame(main, fg_color=BACKGROUND)
card_frame.pack(fill="x", padx=20, pady=20)

def create_card(parent, title, value, color):
    card = ctk.CTkFrame(parent, width=250, height=170, fg_color=CARD)
    card.pack(side="left", padx=10)
    card.pack_propagate(False)

    ctk.CTkLabel(
    card,
    text=title,
    font=("Arial", 18, "bold"),
    text_color="black"
).pack(pady=15)
    
    lbl = ctk.CTkLabel(card, text=value, font=("Arial", 28, "bold"), text_color=color)
    lbl.pack()

    return card, lbl

card1, kalori_label = create_card(card_frame, "🔥 Kalori Hari Ini", "0 kcal", "#4A90E2")
card2, _ = create_card(card_frame, "🎯 Target Harian", f"{TARGET_HARIAN} kcal", "#A66CFF")

card3 = ctk.CTkFrame(card_frame, width=250, height=170, fg_color=CARD)
card3.pack(side="left", padx=10)
card3.pack_propagate(False)

ctk.CTkLabel(card3, text="⭐ Progress", font=("Arial", 18, "bold"),text_color="black").pack(anchor="w", padx=20, pady=15)

progress = ctk.CTkProgressBar(card3, width=180)
progress.pack(pady=10)
progress.set(0)

progress_label = ctk.CTkLabel(
    card3,
    text="0%",
    font=("Arial", 18, "bold"),
    text_color="#2E86DE"
)
progress_label.pack()

card4 = ctk.CTkFrame(card_frame, width=250, height=170, fg_color=CARD)
card4.pack(side="left", padx=10)
card4.pack_propagate(False)

ctk.CTkLabel(
    card4,
    text="💚 Status",
    font=("Arial", 18, "bold"),
    text_color="black"
).pack(pady=15)

status_label = ctk.CTkLabel(
    card4,
    text="KURANG ⚠️",
    font=("Arial", 24, "bold"),
    text_color="#F5A623"
)
status_label.pack()

content = ctk.CTkFrame(main, fg_color=CARD)
content.pack(fill="both", expand=True, padx=25, pady=15)

ctk.CTkLabel(content, text="🍔 Konsumsi Makanan", font=("Arial", 24, "bold"),text_color="black").pack(anchor="w", padx=20, pady=15)

makanan_var = ctk.StringVar()

dropdown = ctk.CTkComboBox(
    content,
    values=list(food_db.keys()),
    variable=makanan_var,
    width=250,
    fg_color="white",
    text_color="black"
)
dropdown.pack(anchor="w", padx=20, pady=10)

porsi_entry = ctk.CTkEntry(
    content,
    placeholder_text="Jumlah Porsi",
    fg_color="white",
    text_color="black"
)
porsi_entry.pack(
    anchor="w",
    padx=20,
    pady=10
)

ctk.CTkButton(
    content,
    text="➕ Tambah Konsumsi",
    command=tambah_konsumsi
).pack(anchor="w", padx=20, pady=10)
ctk.CTkButton(
    content,
    text="🍜 Tambah Makanan Baru",
    command=tambah_makanan_baru
).pack(anchor="w", padx=20, pady=5)

ctk.CTkLabel(
    content,
    text="📋 Riwayat Konsumsi",
    font=("Arial", 20, "bold"),
    text_color="black"
).pack(anchor="w", padx=20, pady=(20,10))

riwayat_box = ctk.CTkTextbox(
    content,
    height=180,
    fg_color="white",
    text_color="black"
)

riwayat_box.pack(
    fill="x",
    padx=20,
    pady=10
)

load_makanan()

load_csv()

# ==========================
# Update progress challenge
# ==========================
jumlah = load_progress()

progress_mingguan.configure(
    text=f"📅 Progress : {jumlah}/7 Hari"
)

update_riwayat()

app.mainloop()