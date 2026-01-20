import requests
from config import API_BASE_URL, HEADERS

# SERVICE LAYER
# File ini berisi fungsi-fungsi untuk komunikasi
# antara aplikasi dan database Supabase (REST API)

# --- KAMAR ---

def get_kamar():
    # Mengambil seluruh data kamar dari database
    return requests.get(
        f"{API_BASE_URL}/kamar?select=*",
        headers=HEADERS
    )


def tambah_kamar(data):
    # Menambahkan data kamar baru
    return requests.post(
        f"{API_BASE_URL}/kamar",
        headers=HEADERS,
        json=data
    )


def update_kamar(nomor, status):
    # Memperbarui status kamar berdasarkan nomor kamar
    return requests.patch(
        f"{API_BASE_URL}/kamar?nomor_kamar=eq.{nomor}",
        headers=HEADERS,
        json={"status": status}
    )


def hapus_kamar(nomor):
    # Menghapus data kamar berdasarkan nomor kamar
    return requests.delete(
        f"{API_BASE_URL}/kamar?nomor_kamar=eq.{nomor}",
        headers=HEADERS
    )


# ---  PENGHUNI ---
def get_penghuni():
    # Mengambil seluruh data penghuni
    return requests.get(
        f"{API_BASE_URL}/penghuni?select=*",
        headers=HEADERS
    )


def tambah_penghuni(data):
    # Menambahkan data penghuni baru
    return requests.post(
        f"{API_BASE_URL}/penghuni",
        headers=HEADERS,
        json=data
    )


def hapus_penghuni(nama):
    # Menghapus data penghuni berdasarkan nama
    return requests.delete(
        f"{API_BASE_URL}/penghuni?nama=eq.{nama}",
        headers=HEADERS
    )


# --- PEMBAYARAN ---

def get_pembayaran():
    # Mengambil seluruh data pembayaran
    return requests.get(
        f"{API_BASE_URL}/pembayaran?select=*",
        headers=HEADERS
    )


def tambah_pembayaran(data):
    # Menambahkan data pembayaran baru
    return requests.post(
        f"{API_BASE_URL}/pembayaran",
        headers=HEADERS,
        json=data
    )


def update_pembayaran(id_bayar, data):
    # Memperbarui status atau keterangan pembayaran
    return requests.patch(
        f"{API_BASE_URL}/pembayaran?id=eq.{id_bayar}",
        headers=HEADERS,
        json=data
    )


def hapus_pembayaran(id_bayar):
    # Menghapus data pembayaran berdasarkan ID
    return requests.delete(
        f"{API_BASE_URL}/pembayaran?id=eq.{id_bayar}",
        headers=HEADERS
    )
