import os
import sys

# UTILITIES
# File ini berisi fungsi-fungsi bantuan (helper)
# yang digunakan oleh berbagai bagian aplikasi

# Menyesuaikan path resource (icon, qss, dll)
# Agar tetap bisa diakses saat aplikasi dijalankan
# sebagai file .exe (PyInstaller) maupun mode biasa

def resource_path(relative_path):
    """
    Mengembalikan path absolut ke file resource
    (icon, gambar, QSS, dll).

    Parameter:
    - relative_path (str): path relatif file resource
    """
    try:
        # Jika aplikasi dijalankan sebagai .exe PyInstaller
        base_path = sys._MEIPASS
    except Exception:
        # Jika dijalankan sebagai script Python biasa
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)



# Memuat file stylesheet (QSS) ke aplikasi
def load_qss(app, filename="styleKOSMON.qss"):
    """
    Memuat file QSS (Qt Style Sheet) ke aplikasi.

    Parameter:
    - app : objek QApplication
    - filename (str): nama file QSS
    """
    try:
        qss_path = resource_path(filename)
        with open(qss_path, "r", encoding="utf-8") as f:
            app.setStyleSheet(f.read())
    except Exception as e:
        # Jika file tidak ditemukan atau gagal dibaca
        print("Gagal load QSS:", e)
