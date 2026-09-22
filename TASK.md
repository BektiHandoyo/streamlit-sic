---
## 11. 📝 Tugas Mandiri

Selamat! Kamu sudah memiliki semua bekal untuk membangun proyekmu sendiri. Sekarang saatnya praktik mandiri sebagai proyek akhir (capstone) kelas ini.

### Pilih salah satu opsi di bawah ini:

**Opsi A — Kembangkan Aplikasi Pencatat Nilai Siswa**
Tambahkan minimal **2 fitur baru** ke aplikasi yang sudah dibuat di Bagian 9, misalnya:
- Menghitung dan menampilkan rata-rata nilai seluruh siswa (`st.write` / `st.metric`).
- Fitur pencarian siswa berdasarkan nama (`st.text_input` sebagai filter).
- Tombol untuk menghapus/reset seluruh data.
- Grafik sederhana jumlah siswa Lulus vs Belum Lulus (`st.bar_chart`).

**Opsi B — Buat Aplikasi Baru dari Nol (end-to-end)**
Pilih salah satu ide berikut, lalu bangun end-to-end (Streamlit + logika + CSV) seperti yang sudah dipelajari:
- **To-Do List**: input tugas baru, tandai selesai, simpan ke CSV, tampilkan daftar tugas.
- **Kalkulator BMI**: input berat & tinggi badan, hitung BMI dengan fungsi, tentukan kategori dengan if-else, simpan riwayat ke CSV, tampilkan riwayat dengan `st.dataframe`.

### ✅ Kriteria Penilaian (Checklist)
Pastikan proyekmu memenuhi semua poin berikut:
- [ ] Menggunakan minimal 1 **fungsi** (`def ...`)
- [ ] Menggunakan minimal 1 **percabangan** (`if-else`)
- [ ] Menggunakan minimal 1 **perulangan** (`for`/`while`) *(boleh implisit lewat pembacaan banyak baris CSV)*
- [ ] Menyimpan data ke file **CSV**
- [ ] Menampilkan data kembali di **Streamlit** (`st.write`, `st.dataframe`, dsb.)
- [ ] Aplikasi berhasil dijalankan dan diakses lewat link LocalTunnel
- [ ] Dokumentasi singkat (isi ulang template di Bagian 10 untuk proyekmu sendiri)

### 🚀 Kerjakan di sini

Tulis kode aplikasi Tugas Mandiri-mu pada sel `%%writefile tugas_mandiri.py` di bawah ini (ganti seluruh isi contoh kerangka dengan kodemu sendiri), lalu jalankan sel-sel setelahnya untuk mencobanya.