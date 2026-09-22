# 📄 Dokumentasi Proyek: Weekly Routine To-Do List

Aplikasi pencatat dan pemantau jadwal rutin mingguan berbasis web interaktif yang dibangun menggunakan **Python**, **Streamlit**, dan **Pandas** dengan penyimpanan basis data lokal berbasis file **CSV**.

---

## 1. Tujuan Aplikasi
Aplikasi ini dibuat untuk membantu pengguna mengelola, mencatat, dan memantau jadwal kegiatan rutin mingguan yang berulang secara terstruktur. 

**Masalah yang diselesaikan:**
- Ketidakpraktisan dalam mencatat rutinitas harian yang sifatnya berulang.
- Kesulitan memantau progres penyelesaian tugas harian maupun akumulasi mingguan.
- Menghindari kerepotan membuat ulang daftar tugas baru setiap kali minggu baru dimulai.

---

## 2. Fitur Utama
- **Penambahan Tugas Rutin (Sidebar Form):** Form untuk menginput nama tugas, deskripsi detail, serta menentukan hari pelaksanaan (Senin–Minggu).
- **Tampilan Terstruktur Per Hari (Expander & Data Editor):** Daftar tugas dikelompokkan berdasarkan hari dalam bentuk *accordion/dropdown* dan ditampilkan menggunakan tabel interaktif (`st.data_editor`).
- **Pencentangan & Penghapusan Interaktif:** Fitur *checkbox* langsung di dalam tabel untuk menandai status selesai serta opsi hapus baris tugas secara dinamis.
- **Indikator Progres Visual (Progress Bar & Metrics):** Tampilan grafik persentase penyelesaian tugas secara *real-time* khusus untuk hari ini dan total akumulasi seminggu.
- **Penyimpanan Permanen (CSV Storage):** Setiap perubahan data otomatis tersimpan ke file `todo_routine.csv` tanpa memerlukan *database server* terpisah.
- **Reset Status Mingguan:** Tombol pemeliharaan di *sidebar* untuk mengembalikan seluruh status tugas menjadi *pending* (belum selesai) saat memasuki minggu baru.

---

## 3. Alur Program

```Text
[Input Pengguna] ──> [Diproses Streamlit & Pandas] ──> [Auto-Sync CSV] ──> [Update Tampilan UI]
```
1) Inisialisasi (Startup): Aplikasi mengecek keberadaan file todo_routine.csv. Jika belum ada, sistem akan membuat file CSV baru dengan header default. Data kemudian dimuat ke st.session_state.
2) Input Data Baru: Pengguna mengisi form tugas di sidebar. Saat diklik Simpan, sistem membuat ID unik berbasis timestamp, menambahkannya ke DataFrame, dan menyimpan perubahan ke CSV.
3) Interaksi Tabel: Pengguna dapat mencentang status tugas atau menghapus tugas dari tabel interaktif harian.
4) Pemrosesan & Penyimpanan: Setiap interaksi di tabel memicu fungsi sinkronisasi yang secara otomatis memperbarui DataFrame dan file CSV.
5) Kalkulasi & Output Visual: Sistem menghitung persentase penyelesaian tugas secara otomatis dan memperbarui progress bar serta metrik di bagian atas halaman.

---

## 4. Struktur Kode
Aplikasi dibangun menggunakan arsitektur modular yang terbagi menjadi beberapa file:
```Text
todo_app/
│
├── database.py       # Data Access Layer (Operasi I/O File CSV)
├── helpers.py        # Business Logic & Utility (Waktu, Kalkulasi Progress)
├── ui_components.py  # Presentation Layer (Form Sidebar, Tabel, Metrics, Expander)
└── app.py            # Main Entry Point (Inisialisasi & Pengatur Layout UI)
```
### Rincian Modul & Fungsi:
`database.py`

Mengatur seluruh interaksi baca dan tulis data ke file CSV.
- load_data(): Membaca file CSV atau membuat DataFrame kosong baru jika file belum ada.
- save_data(df): Menyimpan data DataFrame ke file todo_routine.csv.
- add_task(df, new_task): Menambahkan baris tugas baru ke dalam DataFrame.
- update_task_status(df, task_id, status): Memperbarui kolom is_completed berdasarkan ID tugas.
- delete_task(df, task_id): Menghapus tugas dari DataFrame berdasarkan ID.
- reset_weekly_tasks(df): Mengembalikan seluruh nilai is_completed menjadi False.

`helpers.py`

Mengelola logika bantuan non-UI dan konstanta aplikasi.
- get_today_name(): Mengembalikan nama hari ini dalam Bahasa Indonesia berdasarkan waktu sistem.
- calculate_progress(df): Menghitung total tugas, jumlah tugas selesai, dan persentase progres.

`ui_components.py`

Mengelola tampilan antarmuka dan komponen interaktif Streamlit.
- render_sidebar_form(): Menampilkan form tambah tugas dan tombol reset mingguan di sidebar.
- render_dashboard_metrics(): Menampilkan progress bar dan angka metrik penyelesaian tugas.
- render_today_tasks(): Menampilkan tabel interaktif khusus untuk jadwal tugas hari ini.
- render_weekly_schedule(): Menampilkan daftar tugas seminggu penuh dalam bentuk expander dan tabel.
- _sync_table_changes(original_df, edited_df): Helper internal untuk membandingkan perubahan data pada tabel dan menyinkronkannya ke basis data.

`tugas_mandiri.py`

File utama yang dijalankan oleh Streamlit (`streamlit run tugas_mandiri.py`).
- Mengatur konfigurasi halaman (st.set_page_config).
- Memuat session state saat aplikasi pertama kali diakses.
- Memanggil fungsi-fungsi render dari ui_components.py untuk menyusun tata letak aplikasi.

---

## 5. Cara Menjalankan Aplikasi (Google Colab)

Aplikasi ini dirancang agar dapat dijalankan langsung di environment **Google Colab** menggunakan bantuan `pyngrok` untuk membuat *tunneling* URL publik.

### Langkah-Langkah Penyiapan & Pengadaan Server

1. Pastikan seluruh file modul (`database.py`, `helpers.py`, `ui_components.py`) dan file utama `tugas_mandiri.py` sudah dibuat di dalam direktori Google Colab dengan menjalankan blok `%%writefile <nama_file>.py`
2. Buat file `NGROK_TOKEN` pada bagian **Secrets** (ikon kunci di sidebar kiri Colab) dan masukkan Authtoken ngrok milikmu.
3. Jalankan sel kode berikut untuk menginstal dependensi, mematikan proses lama, dan menjalankan aplikasi Streamlit:

```python
# Part 1 : Start App Streamlit
# Matikan proses lama, jalankan Tugas Mandiri
!pkill -f streamlit
!streamlit run tugas_mandiri.py &>/content/logs.txt &
```
```python
# Part 2 : Install Dependensi
!pip install pyngrok
```
```python
# Start tunnel ngrok
# Menggunakan ngrok sebagai alternatif LocalTunnel agar koneksi lebih stabil
from google.colab import userdata
from pyngrok import ngrok

ngrok.set_auth_token(userdata.get("NGROK_TOKEN"))

# Disconnect tunnel lama jika ada
tunnels = ngrok.get_tunnels()
for tunnel in tunnels:
    ngrok.disconnect(tunnel.public_url)

# Connect ke port Streamlit (8501)
public_url = ngrok.connect(8501).public_url
print("Streamlit URL:", public_url)
```