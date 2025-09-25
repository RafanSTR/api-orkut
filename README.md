# API Mutasi QRIS OrderKuota

Sebuah API sederhana berbasis **Flask (Python)** untuk mengambil data mutasi QRIS dari OrderKuota.  
⚠️ **Catatan penting**:  
- Jangan mengubah nama creator. Yang mengubah nama creator semoga mandul 7 turunan.  
- Gunakan dengan bijak.  
- Jika ada error hubungi: [t.me/RafanSTR](https://t.me/RafanSTR)  

---

## 🚀 Fitur
- Mendapatkan riwayat mutasi QRIS (masuk/keluar).
- Format response JSON rapi dengan informasi transaksi.
- Signature API otomatis sesuai aturan OrderKuota.
- Mudah dijalankan dengan Python/Flask.

---

## 📦 Instalasi

Ikuti langkah-langkah berikut untuk menjalankan API ini:

### 1. Clone repository
```bash
git clone https://github.com/username/reponame.git
cd reponame
```

### 2. Buat virtual environment (opsional tapi direkomendasikan)
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

Jika file `requirements.txt` belum ada, buat dengan isi berikut:
```
Flask
requests
```

### 4. Jalankan API
```bash
python app.py
```

Secara default, API akan berjalan di:
```
http://0.0.0.0:5000
```

---

## 📡 Endpoint

### `POST /mutasi`

#### Request Body (JSON)
```json
{
  "username": "isi_username_orderkuota",
  "token": "merchantId:apiKey"
}
```

#### Response Berhasil
```json
{
    "status": "success",
    "data": [
        {
            "date": "2025-09-25 12:30:00",
            "amount": 10000,
            "type": "CR",
            "qris": "ShopeePay",
            "brand_name": "ShopeePay",
            "issuer_reff": "id123456",
            "buyer_reff": "Bayar order #123",
            "balance": 250000
        }
    ],
    "creator": "t.me/RafanSTR"
}
```

#### Response Gagal
```json
{
    "status": "failed",
    "message": "username dan token wajib diisi",
    "creator": "t.me/RafanSTR"
}
```

---

## 🔧 Cara Pakai
1. Jalankan server dengan `python app.py`.
2. Kirim request `POST` ke endpoint `/mutasi` menggunakan **Postman**, **cURL**, atau integrasikan ke aplikasi lain.
3. Pastikan `username` dan `token` sesuai dengan akun OrderKuota Anda.

Contoh menggunakan `cURL`:
```bash
curl -X POST http://localhost:5000/mutasi      -H "Content-Type: application/json"      -d '{
           "username": "demo_user",
           "token": "12345:abcdeFGHIJK"
         }'
```

---

## 👨‍💻 Creator
- Telegram: [t.me/RafanSTR](https://t.me/RafanSTR)  

🙏 Mohon gunakan script ini dengan bijak.  
