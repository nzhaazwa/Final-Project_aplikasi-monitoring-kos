from datetime import date, datetime
import requests

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QTableWidget, QTableWidgetItem,
    QPushButton, QLineEdit, QComboBox,
    QMessageBox, QLabel, QDateEdit
)
from PySide6.QtCore import QDate, Qt
from PySide6.QtGui import QColor, QIcon
from PySide6.QtWidgets import QHeaderView

from utils import resource_path
from config import API_BASE_URL, HEADERS


# Class ini mengelola tampilan dan logika
# tab Pembayaran pada aplikasi Monitoring Kos
class PembayaranTab:
    """
    Membuat dan menginisialisasi seluruh
    komponen UI tab Pembayaran
    """
    def init_tab_pembayaran(self):
        # Container tab dan layout utama
        tab = QWidget() 
        main = QVBoxLayout(tab)

        # Judul tab pembayaran
        title = QLabel("DAFTAR PEMBAYARAN")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignCenter)
        main.addWidget(title)
        # Teks petunjuk penggunaan
        hint = QLabel("*Silahkan isi form atau pilih data dari tabel untuk mengelola")
        hint.setAlignment(Qt.AlignCenter)
        hint.setStyleSheet("color:#6b7280; font-size:12px; font-style: italic;")
        main.addWidget(hint)

        # INPUT DATA PEMBAYARAN
        input_row = QHBoxLayout()
        input_row.addStretch()

        self.b_nama = QLineEdit()
        self.b_nama.setPlaceholderText("Nama Penghuni")

        self.b_tgl = QDateEdit()
        self.b_tgl.setCalendarPopup(True)
        self.b_tgl.setDate(QDate.currentDate())
        self.b_tgl.setDisplayFormat("dd/MM/yyyy")

        self.b_status = QComboBox()
        self.b_status.addItems(["Belum Lunas", "Lunas"])

        self.b_ket = QLineEdit()
        self.b_ket.setPlaceholderText("Keterangan")

        input_row.addWidget(self.b_nama)
        input_row.addWidget(self.b_tgl)
        input_row.addWidget(self.b_status)
        input_row.addWidget(self.b_ket)
        input_row.addStretch()
        main.addLayout(input_row)

        btn_row = QHBoxLayout()
        btn_row.addStretch()

        self.btn_add_bayar = QPushButton("Tambah")
        self.btn_add_bayar.setObjectName("add")
        self.btn_add_bayar.clicked.connect(self.tambah_pembayaran)

        self.btn_update_bayar = QPushButton("Perbarui Status")
        self.btn_update_bayar.setObjectName("update")
        self.btn_update_bayar.setEnabled(True)
        self.btn_update_bayar.clicked.connect(self.update_pembayaran)

        self.btn_delete_bayar = QPushButton("Hapus")
        self.btn_delete_bayar.setObjectName("delete")
        self.btn_delete_bayar.setEnabled(True)
        self.btn_delete_bayar.clicked.connect(self.hapus_pembayaran)

        btn_row.addWidget(self.btn_add_bayar)
        btn_row.addWidget(self.btn_update_bayar)
        btn_row.addWidget(self.btn_delete_bayar)
        btn_row.addStretch()
        main.addLayout(btn_row)

        filter_row = QHBoxLayout()
        filter_row.addStretch()

        self.filter_bayar = QComboBox()
        self.filter_bayar.addItems([
            "Semua",
            "Belum Lunas",
            "Lunas"
        ])
        self.filter_bayar.currentTextChanged.connect(self.filter_pembayaran)

        filter_row.addWidget(QLabel("Filter Status Pembayaran:"))
        filter_row.addWidget(self.filter_bayar)
        filter_row.addStretch()

        # INFO TOTAL PEMBAYARAN
        self.lbl_info_bayar = QLabel()
        self.lbl_info_bayar.setAlignment(Qt.AlignCenter)
        self.lbl_info_bayar.setStyleSheet("""
            font-size: 12px;
            font-style: italic;
            color: #6b7280;
        """)
        main.addLayout(filter_row)

        # TABEL DATA PEMBAYARAN
        self.table_bayar = QTableWidget(0, 6)
        self.table_bayar.setHorizontalHeaderLabels(
            ["ID", "Nama", "Jatuh Tempo", "Status", "Keterangan", "Bulan"]
        )
        self.table_bayar.setColumnHidden(0, True)
        self.table_bayar.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_bayar.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table_bayar.cellClicked.connect(self.isi_form_pembayaran)
        self.table_bayar.setStyleSheet("QTableWidget::item { padding-left: 0px; padding-right: 0px; }")
        main.addWidget(self.table_bayar)
 

        # Menambahkan tab pembayaran ke QTabWidget
        self.tabs.addTab(tab,QIcon(resource_path("icons/payment.png")), "Pembayaran")
        main.addWidget(self.lbl_info_bayar)
        self.load_pembayaran()  # Memuat data pembayaran dari database

    def update_info_pembayaran(self, data):
        # Menampilkan informasi jumlah pembayaran lunas dan belum lunas
        total_lunas = sum(1 for d in data if d["status"] == "Lunas")
        total_belum = sum(1 for d in data if d["status"] == "Belum Lunas")

        self.lbl_info_bayar.setText(
            f"Total belum lunas: {total_belum} | Total lunas: {total_lunas}"
        )

    def isi_form_pembayaran(self, row, col):
        # Mengisi form pembayaran berdasarkan data yang dipilih pada tabel
        self.b_nama.setText(self.table_bayar.item(row, 1).text())

        tgl = QDate.fromString( # Konversi tanggal jatuh tempo ke QDate
            self.table_bayar.item(row, 2).text(), "dd/MM/yyyy"
        )
        self.b_tgl.setDate(tgl)

        self.b_status.setCurrentText(
            self.table_bayar.item(row, 3).text()
        )

        self.b_ket.setText(
            self.table_bayar.item(row, 4).text()
        )

        self.btn_update_bayar.setEnabled(True)
        self.btn_delete_bayar.setEnabled(True)

    def load_pembayaran(self):
        # Mengambil data pembayaran dari database dan menyimpannya ke memori aplikasi
        res = requests.get(f"{API_BASE_URL}/pembayaran?select=*", headers=HEADERS)
        if res.status_code != 200:
            return

        self.data_bayar = res.json()
        self.tampilkan_pembayaran(self.data_bayar)  # ✅ SATU-SATUNYA PENGISI TABEL

    # Menambahkan data pembayaran baru
    def tambah_pembayaran(self):
        if not self.b_nama.text():   # Validasi input nama penghuni
            QMessageBox.warning(self, "Peringatan", "Nama penghuni wajib diisi")
            return

        jatuh = self.b_tgl.date().toPython() # Ambil tanggal jatuh tempo

        res = requests.post(  # Request tambah data pembayaran
            f"{API_BASE_URL}/pembayaran",
            headers=HEADERS,
            json={
                "nama_penghuni": self.b_nama.text(),
                "jatuh_tempo": jatuh.strftime("%Y-%m-%d"),
                "status": self.b_status.currentText(),
                "keterangan": self.b_ket.text(),
                "bulan": jatuh.strftime("%B %Y")
            }
        )

        if res.status_code in (200, 201):
            QMessageBox.information(
                self, "Berhasil", "Data pembayaran berhasil ditambahkan."
            )
            self.load_pembayaran()
        else:
            QMessageBox.critical(
                self, "Gagal", "Data pembayaran gagal ditambahkan."
            )

    # Memperbarui status pembayaran
    def update_pembayaran(self):
        # Validasi baris tabel terpilih
        row = self.table_bayar.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Peringatan", "Pilih data pembayaran terlebih dahulu.")
            return

        id_bayar = self.table_bayar.item(row, 0).text()

        res = requests.patch( # Request update data pembayaran
            f"{API_BASE_URL}/pembayaran?id=eq.{id_bayar}",
            headers=HEADERS,
            json={
                "status": self.b_status.currentText(),
                "keterangan": self.b_ket.text()
            }
        )
        if res.status_code in (200, 204):
            QMessageBox.information(
                self, "Berhasil", "Status pembayaran berhasil diperbarui."
            )
            self.load_pembayaran()
        else:
            QMessageBox.critical(
                self, "Gagal", "Gagal memperbarui status pembayaran."
            )

    # Menghapus data pembayaran terpilih
    def hapus_pembayaran(self):
        row = self.table_bayar.currentRow()
        if row < 0:  # Validasi baris tabel terpilih
            QMessageBox.warning(self, "Peringatan", "Pilih data pembayaran terlebih dahulu.")
            return

        confirm = QMessageBox.question(
            self,
            "Konfirmasi",
            "Apakah Anda yakin ingin menghapus data pembayaran ini?",
            QMessageBox.Yes | QMessageBox.No
        )

        if confirm != QMessageBox.Yes:   # Konfirmasi penghapusan data
            return

        id_bayar = self.table_bayar.item(row, 0).text()

        res = requests.delete( # Request hapus data pembayaran
            f"{API_BASE_URL}/pembayaran?id=eq.{id_bayar}",
            headers=HEADERS
        )

        if res.status_code in (200, 204):
            QMessageBox.information(
                self, "Berhasil", "Data pembayaran berhasil dihapus."
            )
            self.load_pembayaran()
        else:
            QMessageBox.critical(
                self, "Gagal", "Data pembayaran gagal dihapus."
            )

    def tampilkan_pembayaran(self, data):
        #  Menampilkan data pembayaran ke tabel dan memperbarui informasi total
        self.table_bayar.setRowCount(len(data))
        self.table_bayar.setAlternatingRowColors(True)
        self.update_info_pembayaran(data)

        for r, d in enumerate(data):
            # ID
            self.table_bayar.setItem(r, 0, QTableWidgetItem(str(d["id"])))

            # Nama → kiri
            nama = QTableWidgetItem(d["nama_penghuni"])
            nama.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            self.table_bayar.setItem(r, 1, nama)

            # Jatuh tempo → tengah ✅
            jt = datetime.strptime(d["jatuh_tempo"], "%Y-%m-%d").strftime("%d/%m/%Y")
            self.table_bayar.setItem(r, 2, QTableWidgetItem(jt))
            self.table_bayar.item(r, 2).setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)

           # Status Pembayaran → badge pill
            status_item = QTableWidgetItem(d["status"])
            status_item.setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)

            if d["status"] == "Lunas":
                status_item.setForeground(QColor("#16A34A"))   # hijau
            else:
                status_item.setForeground(QColor("#DC2626"))   # merah

            self.table_bayar.setItem(r, 3, status_item)

            # Keterangan → kiri
            ket = QTableWidgetItem(d.get("keterangan", ""))
            ket.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            self.table_bayar.setItem(r, 4, ket)

            # Bulan → tengah ✅
            self.table_bayar.setItem(r, 5, QTableWidgetItem(d["bulan"]))
            self.table_bayar.item(r, 5).setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)

    def filter_pembayaran(self, pilihan):
        # Menyaring data pembayaran berdasarkan status
        today = date.today()

        if pilihan == "Semua":
            data = self.data_bayar

        elif pilihan == "Belum Lunas":
            data = [d for d in self.data_bayar if d["status"] == "Belum Lunas"]

        elif pilihan == "Lunas":
            data = [d for d in self.data_bayar if d["status"] == "Lunas"]

        elif pilihan == "Telat ≥ 3 Hari":  # Menampilkan pembayaran belum lunas yang terlambat ≥ 3 hari
            data = []
            for d in self.data_bayar:
                if d["status"] == "Belum Lunas":
                    jt = date.fromisoformat(d["jatuh_tempo"])
                    if (today - jt).days >= 3:
                        data.append(d)
        self.tampilkan_pembayaran(data)

    # POPUP REMINDER PEMBAYARAN
    def reminder_telat_bayar(self):
        today = date.today() # Menampilkan pengingat pembayaran yang terlambat ≥ 3 hari
        res = requests.get(   # Mengambil data pembayaran yang belum lunas
            f"{API_BASE_URL}/pembayaran?status=eq.Belum Lunas",
            headers=HEADERS
        )
        if res.status_code != 200:
            return

        telat = []
        for d in res.json():
            jt = date.fromisoformat(d["jatuh_tempo"])
            selisih = (today - jt).days
            if selisih >= 3:
                telat.append(
                    f"Nama        : {d['nama_penghuni']}\n"
                    f"Jatuh Tempo : {jt.strftime('%d/%m/%Y')}\n"
                    f"Telat       : {selisih} hari\n"
                )

        if telat: # Menampilkan popup jika ada pembayaran terlambat
            QMessageBox.warning(
                self,
                "Pembayaran Terlambat",
                "<pre>" + "\n".join(telat) + "</pre>"
            )
