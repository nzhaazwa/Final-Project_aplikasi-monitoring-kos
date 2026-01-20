from datetime import datetime
import requests

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QTableWidget, QTableWidgetItem,
    QPushButton, QLineEdit, QMessageBox, QLabel, QDateEdit
)
from PySide6.QtCore import QDate, Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QHeaderView

from utils import resource_path
from config import API_BASE_URL, HEADERS


# Class ini mengelola seluruh tampilan dan
#logika tab Penghuni pada aplikasi
class PenghuniTab:
    """ 
    Menginisialisasi tampilan tab Penghuni,
    termasuk form input, tabel, dan tombol aksi
    """
    def init_tab_penghuni(self):
        tab = QWidget() # Container tab dan layout utama
        main = QVBoxLayout(tab)
        
        # Judul tab penghuni
        title = QLabel("DAFTAR PENGHUNI")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignCenter)
        main.addWidget(title)
        # Teks petunjuk penggunaan
        hint = QLabel("*Silahkan isi form atau pilih data dari tabel untuk menghapus")
        hint.setAlignment(Qt.AlignCenter)
        hint.setStyleSheet("color:#6b7280; font-size:12px; font-style: italic;")
        main.addWidget(hint)

        # INPUT
        input_row = QHBoxLayout()
        input_row.addStretch()

        self.p_nama = QLineEdit()
        self.p_nama.setPlaceholderText("Nama Penghuni")

        self.p_kamar = QLineEdit()
        self.p_kamar.setPlaceholderText("Nomor Kamar")

        self.p_tgl = QDateEdit()
        self.p_tgl.setCalendarPopup(True)
        self.p_tgl.setDate(QDate.currentDate())
        self.p_tgl.setDisplayFormat("dd/MM/yyyy")

        self.p_kontak = QLineEdit()
        self.p_kontak.setPlaceholderText("Kontak")

        input_row.addWidget(self.p_nama)
        input_row.addWidget(self.p_kamar)
        input_row.addWidget(self.p_tgl)
        input_row.addWidget(self.p_kontak)
        input_row.addStretch()
        main.addLayout(input_row)

        # BUTTON AKSI
        btn_row = QHBoxLayout()
        btn_row.addStretch()

        self.btn_add_penghuni = QPushButton("Tambah")
        self.btn_add_penghuni.setObjectName("add")
        self.btn_add_penghuni.clicked.connect(self.tambah_penghuni)

        self.btn_delete_penghuni = QPushButton("Hapus")
        self.btn_delete_penghuni.setObjectName("delete")
        self.btn_delete_penghuni.setEnabled(True)
        self.btn_delete_penghuni.clicked.connect(self.hapus_penghuni)

        btn_row.addWidget(self.btn_add_penghuni)
        btn_row.addWidget(self.btn_delete_penghuni)
        btn_row.addStretch()
        main.addLayout(btn_row)

        # PENCARIAN DATA PENGHUNI
        search_row = QHBoxLayout()
        search_row.addStretch()

        self.p_search = QLineEdit()
        self.p_search.setPlaceholderText("Cari nama atau nomor kamar...")
        self.p_search.setFixedWidth(350)
        self.p_search.textChanged.connect(self.filter_penghuni)

        search_row.addWidget(self.p_search)
        search_row.addStretch()
        main.addLayout(search_row)

        # TABEL DATA PENGHUNI
        self.table_penghuni = QTableWidget(0, 4)
        self.table_penghuni.setHorizontalHeaderLabels(
            ["Nama", "Kamar", "Tanggal Masuk", "Kontak"]
        )
        self.table_penghuni.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_penghuni.setEditTriggers(QTableWidget.NoEditTriggers)
        # Aktifkan tombol hapus saat baris dipilih
        self.table_penghuni.cellClicked.connect(
        lambda r, c: self.btn_delete_penghuni.setEnabled(True)
    )
        main.addWidget(self.table_penghuni)
        # Menambahkan tab penghuni ke QTabWidget
        self.tabs.addTab(tab, QIcon(resource_path("icons/penghuni.png")), "Penghuni")
        # Mengisi form saat data tabel diklik
        self.table_penghuni.cellClicked.connect(self.isi_form_penghuni)
        self.load_penghuni()    # Memuat data penghuni dari database

    def isi_form_penghuni(self, row, col):
        # Mengisi form penghuni berdasarkan data yang dipilih pada tabel
        self.p_nama.setText(self.table_penghuni.item(row, 0).text())
        self.p_kamar.setText(self.table_penghuni.item(row, 1).text())

        tgl = QDate.fromString(  # Konversi tanggal masuk ke format QDate
            self.table_penghuni.item(row, 2).text(),
            "dd/MM/yyyy"
        )
        self.p_tgl.setDate(tgl)

        self.p_kontak.setText(self.table_penghuni.item(row, 3).text())

    def load_penghuni(self): # Mengambil dan menampilkan data penghuni dari database.
        res = requests.get(f"{API_BASE_URL}/penghuni?select=*", headers=HEADERS)
        if res.status_code != 200:
            return
        self.data_penghuni = res.json()
        self.tampilkan_penghuni(self.data_penghuni)

    def tampilkan_penghuni(self, data):  # Menampilkan data penghuni ke dalam tabel
        self.table_penghuni.setRowCount(len(data))
        self.table_penghuni.setAlternatingRowColors(True)
        for r, d in enumerate(data):
            tgl = datetime.strptime(
                d["tanggal_masuk"], "%Y-%m-%d"
            ).strftime("%d/%m/%Y")

            # Nama → kiri (default)
            nama = QTableWidgetItem(d["nama"])
            nama.setTextAlignment(Qt.AlignVCenter)
            self.table_penghuni.setItem(r, 0, nama)

            # Nomor kamar → tengah
            kamar = QTableWidgetItem(d["nomor_kamar"])
            kamar.setTextAlignment(Qt.AlignCenter)
            self.table_penghuni.setItem(r, 1, kamar)

            # Tanggal masuk → tengah
            item_tgl = QTableWidgetItem(tgl)
            item_tgl.setTextAlignment(Qt.AlignCenter)
            self.table_penghuni.setItem(r, 2, item_tgl)

            # Kontak → kiri (default)
            kontak = QTableWidgetItem(d["kontak"])
            kontak.setTextAlignment(Qt.AlignVCenter)
            self.table_penghuni.setItem(r, 3, kontak)

    def filter_penghuni(self, text): # Menyaring data penghuni berdasarkan nama atau nomor kamar
        text = text.lower()
        hasil = [
            d for d in self.data_penghuni
            if text in d["nama"].lower()
            or text in d["nomor_kamar"].lower()
        ]
        self.tampilkan_penghuni(hasil)

    # Menambahkan data penghuni baru dan otomatis mengubah status kamar menjadi 'Terisi'
    def tambah_penghuni(self): 
        if not self.p_nama.text() or not self.p_kamar.text():
            QMessageBox.warning(self, "Peringatan", "Nama dan kamar wajib diisi")
            return
        res = requests.post(  # Request tambah data penghuni ke database
            f"{API_BASE_URL}/penghuni",
            headers=HEADERS,
            json={
                "nama": self.p_nama.text(),
                "nomor_kamar": self.p_kamar.text(),
                "tanggal_masuk": self.p_tgl.date().toString("yyyy-MM-dd"),
                "kontak": self.p_kontak.text()
            }
        )

        if res.status_code in (200, 201): # Otomatis ubah status kamar menjadi "Terisi"
            # AUTO UBAH STATUS KAMAR)
            requests.patch(
                f"{API_BASE_URL}/kamar?nomor_kamar=eq.{self.p_kamar.text()}",
                headers=HEADERS,
                json={"status": "Terisi"}
            )

            QMessageBox.information(
                self, "Berhasil", "Data penghuni berhasil ditambahkan."
            )
            self.load_penghuni()
            self.load_kamar()    
        else:
            QMessageBox.critical(
                self, "Gagal", "Data penghuni gagal ditambahkan."
            )

    #  Menghapus data penghuni dan otomatis mengubah status kamar menjadi 'Kosong'
    def hapus_penghuni(self): 
        row = self.table_penghuni.currentRow()  # Validasi baris tabel terpilih
        if row < 0:
            QMessageBox.warning(self, "Peringatan", "Pilih data penghuni terlebih dahulu.")
            return

        # SIMPAN NOMOR KAMAR SEBELUM DIHAPUS
        kamar = self.table_penghuni.item(row, 1).text()
        confirm = QMessageBox.question(   # Konfirmasi penghapusan data
            self,
            "Konfirmasi",
            "Apakah Anda yakin ingin menghapus data penghuni ini?",
            QMessageBox.Yes | QMessageBox.No
        )

        if confirm != QMessageBox.Yes:
            return

        nama = self.table_penghuni.item(row, 0).text()

        res = requests.delete(  # Request hapus data penghuni
            f"{API_BASE_URL}/penghuni?nama=eq.{nama}",
            headers=HEADERS
        )

        if res.status_code in (200, 204): 
            # AUTO UBAH STATUS KAMAR MENJADI KOSONG
            requests.patch(
                f"{API_BASE_URL}/kamar?nomor_kamar=eq.{kamar}",
                headers=HEADERS,
                json={"status": "Kosong"}
            )

            QMessageBox.information(
                self, "Berhasil", "Data penghuni berhasil dihapus."
            )

            self.load_penghuni()   # refresh tabel penghuni
            self.load_kamar()      # refresh kamar
        else:
            QMessageBox.critical(
                self, "Gagal", "Data penghuni gagal dihapus."
            )
