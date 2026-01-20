import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QTabWidget
from PySide6.QtCore import QTimer
from PySide6.QtGui import QIcon

# ---IMPORT UTILITAS ---
# resource_path : untuk mengambil path file (icon, qss) secara aman
# load_qss      : untuk memuat style aplikasi
from utils import resource_path, load_qss

# ---IMPORT TAB APLIKASI ---
# Setiap tab dipisahkan ke file masing-masing
from tabs.kamar_tab import KamarTab
from tabs.penghuni_tab import PenghuniTab
from tabs.pembayaran_tab import PembayaranTab


# --- CLASS UTAMA APLIKASI ---
# MainWindow mewarisi QWidget dan ketiga Tab
# sehingga semua method tab bisa langsung dipanggil
class MainWindow(QWidget, KamarTab,PenghuniTab,PembayaranTab):
    def __init__(self): # Inisialisasi window, tab, dan data awal
        super().__init__()

        # Judul dan ukuran window aplikasi
        self.setWindowTitle("Monitoring Operasional Kos")
        self.resize(1050, 650)

        # --- PENYIMPANAN DATA ---
        # Data disimpan di memori agar bisa dipakai antar tab
        self.data_penghuni = []
        self.data_bayar = []
        self.data_kamar = []

        # --- TAB UTAMA ---
        # QTabWidget sebagai wadah seluruh tab
        self.tabs = QTabWidget()

        # Layout utama window
        layout = QVBoxLayout(self)
        layout.addWidget(self.tabs)

        # Inisialisasi tab Kamar, Penghuni, dan Pembayaran
        self.init_tab_kamar()
        self.init_tab_penghuni()
        self.init_tab_pembayaran()

        # popup reminder setelah window tampil
        QTimer.singleShot(300, self.reminder_telat_bayar)
    
# TAB KAMAR: CRUD, filter, dan informasi status kamar
        
# TAB PENGHUNI: tambah, hapus, dan pencarian data
    
# TAB PEMBAYARAN: kelola status pembayaran dan reminder
    
# RUN PROGRAM
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(resource_path("/icons/KOSMON.ico")))
    load_qss(app)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
