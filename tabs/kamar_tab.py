# tabs/kamar_tab.py

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QTableWidget, QTableWidgetItem,
    QPushButton, QLineEdit, QComboBox, QMessageBox, QLabel
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QIcon
from PySide6.QtWidgets import QHeaderView

from utils import resource_path
import services

class KamarTab:
    # Membuat tampilan dan fitur tab kamar
    def init_tab_kamar(self):
        # Container tab dan layout utama
        tab = QWidget()
        main = QVBoxLayout(tab)

         # Judul tab kamar
        title = QLabel("DAFTAR KAMAR")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignCenter)
        main.addWidget(title)

        # Teks petunjuk penggunaan
        hint = QLabel("*Silahkan isi form atau pilih data dari tabel untuk mengelola")
        hint.setAlignment(Qt.AlignCenter)
        hint.setStyleSheet("color:#6b7280; font-size:12px; font-style: italic;")
        main.addWidget(hint)

        # Layout input data kamar
        input_row = QHBoxLayout()
        input_row.addStretch()

        # Input nomor kamar
        self.k_nomor = QLineEdit()
        self.k_nomor.setPlaceholderText("Nomor Kamar")

        # Input lantai kamar
        self.k_lantai = QLineEdit()
        self.k_lantai.setPlaceholderText("Lantai")

        # Pilihan status kamar
        self.k_status = QComboBox()
        self.k_status.addItems(["Kosong", "Terisi"])

        input_row.addWidget(self.k_nomor)
        input_row.addWidget(self.k_lantai)
        input_row.addWidget(self.k_status)
        input_row.addStretch()
        main.addLayout(input_row)

        # Layout tombol aksi
        btn_row = QHBoxLayout()
        btn_row.addStretch()

        # Tombol tambah kamar
        self.btn_add_kamar = QPushButton("Tambah")
        self.btn_add_kamar.setObjectName("add")
        self.btn_add_kamar.clicked.connect(self.tambah_kamar)

        # Tombol perbarui status kamar
        self.btn_update_kamar = QPushButton("Perbarui Status")
        self.btn_update_kamar.setObjectName("update")
        self.btn_update_kamar.setEnabled(True)
        self.btn_update_kamar.clicked.connect(self.update_kamar)

        self.btn_delete_kamar = QPushButton("Hapus")
        self.btn_delete_kamar.setObjectName("delete")
        self.btn_delete_kamar.setEnabled(True)
        self.btn_delete_kamar.clicked.connect(self.hapus_kamar)

        btn_row.addWidget(self.btn_add_kamar)
        btn_row.addWidget(self.btn_update_kamar)
        btn_row.addWidget(self.btn_delete_kamar)
        btn_row.addStretch()
        main.addLayout(btn_row)

        # FILTER KAMAR (berdasarkan status)
        filter_row = QHBoxLayout()
        filter_row.addStretch()

        # Label filter status kamar
        lbl_filter = QLabel("Filter Status Kamar:")
        lbl_filter.setAlignment(Qt.AlignVCenter)

        # ComboBox filter kamar
        self.filter_kamar = QComboBox()
        self.filter_kamar.addItems(["Semua", "Kosong", "Terisi"])
        self.filter_kamar.setFixedWidth(180)  
        self.filter_kamar.setEditable(False)
        self.filter_kamar.currentTextChanged.connect(self.filter_data_kamar)
        
        filter_row.addWidget(lbl_filter)
        filter_row.addSpacing(8)
        filter_row.addWidget(self.filter_kamar)

        filter_row.addStretch()
        main.addLayout(filter_row)

        # Tabel data kamar
        self.table_kamar = QTableWidget(0, 4)
        self.table_kamar.setAlternatingRowColors(True)
        self.table_kamar.setHorizontalHeaderLabels(
            ["Nomor", "Lantai", "Harga", "Status"]
        )
        self.table_kamar.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_kamar.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table_kamar.cellClicked.connect(self.isi_form_kamar)
        main.addWidget(self.table_kamar)

        # Menambahkan tab kamar ke QTabWidget
        self.tabs.addTab(tab, QIcon(resource_path("icons/room.png")), "Kamar") # icon kamar

        # INFO TOTAL KAMAR
        self.lbl_info_kamar = QLabel()
        self.lbl_info_kamar.setAlignment(Qt.AlignCenter)
        self.lbl_info_kamar.setStyleSheet("""
            font-size: 12px;
            font-style: italic;
            color: #6b7280;
        """)
        main.addWidget(self.lbl_info_kamar)
        self.load_kamar() # Memuat data kamar dari database

    def update_info_kamar(self, data):
        # Menampilkan informasi jumlah kamar kosong dan terisi
        total_kosong = sum(1 for d in data if d["status"] == "Kosong")
        total_terisi = sum(1 for d in data if d["status"] == "Terisi")

        self.lbl_info_kamar.setText(
            f"Total kamar kosong: {total_kosong} | "
            f"Total kamar terisi: {total_terisi}"
        )

    def isi_form_kamar(self, row, col):
        # Mengisi form kamar berdasarkan data yang dipilih pada tabel
        self.k_nomor.setText(self.table_kamar.item(row, 0).text())
        self.k_lantai.setText(self.table_kamar.item(row, 1).text())
        self.k_status.setCurrentText(self.table_kamar.item(row, 3).text())

        self.btn_update_kamar.setEnabled(True)
        self.btn_delete_kamar.setEnabled(True)

    def load_kamar(self):
        # Mengambil dan menampilkan data kamar dari database
        res = services.get_kamar()
        if res.status_code != 200:
            return

        # simpan data ke memori
        self.data_kamar = res.json()

        # SORT nomor kamar secara numerik
        self.data_kamar.sort(key=lambda x: int(x["nomor_kamar"]))
        self.tampilkan_kamar(self.data_kamar)

    # Menambahkan data kamar ke database
    def tambah_kamar(self):
        if not self.k_nomor.text() or not self.k_lantai.text():  # Validasi input wajib
            QMessageBox.warning(self, "Peringatan", "Nomor kamar dan lantai wajib diisi.")
            return
        try: # Validasi lantai harus berupa angka
            lantai = int(self.k_lantai.text())
        except ValueError:
            QMessageBox.warning(self, "Peringatan", "Lantai harus berupa angka.")
            return
        
        res = services.tambah_kamar({
            "nomor_kamar": self.k_nomor.text(),
            "lantai": lantai,
            "harga": 650000,
            "status": self.k_status.currentText()
        })


        if res.status_code in (200, 201):
            QMessageBox.information(self, "Berhasil", "Data kamar berhasil ditambahkan.")
            self.load_kamar()
        else:
            QMessageBox.critical(self, "Gagal", "Data kamar gagal ditambahkan.")

    # Memperbarui status kamar
    def update_kamar(self): # Validasi baris tabel terpilih
        row = self.table_kamar.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Peringatan", "Pilih data kamar terlebih dahulu.")
            return

        nomor = self.table_kamar.item(row, 0).text()

        res = services.update_kamar(nomor, self.k_status.currentText())


        if res.status_code in (200, 204):
            QMessageBox.information(self, "Berhasil", "Status kamar berhasil diperbarui.")
            self.load_kamar()

        else:
            QMessageBox.critical(self, "Gagal", "Gagal memperbarui status kamar.")

    # Menghapus data kamar terpilih
    def hapus_kamar(self):
        row = self.table_kamar.currentRow() # Validasi baris tabel terpilih
        if row < 0:
            QMessageBox.warning(self, "Peringatan", "Pilih data kamar terlebih dahulu.")
            return

        confirm = QMessageBox.question( # Konfirmasi penghapusan data
            self,
            "Konfirmasi",
            "Apakah Anda yakin ingin menghapus data kamar ini?",
            QMessageBox.Yes | QMessageBox.No
        )
        if confirm != QMessageBox.Yes:
            return

        nomor = self.table_kamar.item(row, 0).text()

        res = services.hapus_kamar(nomor)
        if res.status_code in (200, 204):
            QMessageBox.information(self, "Berhasil", "Data kamar berhasil dihapus.")
            self.load_kamar()
        else:
            QMessageBox.critical(self, "Gagal", "Data kamar gagal dihapus.")

    def tampilkan_kamar(self, data):
        self.table_kamar.setRowCount(len(data))

        for r, d in enumerate(data):
            # Nomor kamar → tengah
            item_nomor = QTableWidgetItem(d["nomor_kamar"])
            item_nomor.setTextAlignment(Qt.AlignCenter)
            self.table_kamar.setItem(r, 0, item_nomor)

            # Lantai → tengah
            item_lantai = QTableWidgetItem(str(d["lantai"]))
            item_lantai.setTextAlignment(Qt.AlignCenter)
            self.table_kamar.setItem(r, 1, item_lantai)

            # Format harga ke mata uang Rupiah (tetap kiri)
            harga = f"Rp {d['harga']:,}".replace(",", ".")
            self.table_kamar.setItem(r, 2, QTableWidgetItem(harga))

            # Pewarnaan status kamar → tengah
            status_item = QTableWidgetItem(d["status"])
            status_item.setTextAlignment(Qt.AlignCenter)
            status_item.setForeground(
                QColor("#2e7d32") if d["status"] == "Kosong" else QColor("#c62828")
            )
            self.table_kamar.setItem(r, 3, status_item)

        self.update_info_kamar(data)  # Perbarui informasi total kamar

    # Menyaring data kamar berdasarkan status
    def filter_data_kamar(self, status):
        if status == "Semua":
            data = self.data_kamar
        else:
            data = [d for d in self.data_kamar if d["status"] == status]

        self.tampilkan_kamar(data)