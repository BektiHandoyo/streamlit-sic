import streamlit as st
import csv
import os

st.title("Aplikasi Pencatat Nilai Siswa")
st.write("Selamat datang! Silakan isi data siswa di bawah ini.")

nama = st.text_input("Nama siswa")
nilai = st.number_input("Nilai", min_value=0, max_value=100, step=1)

FILE_CSV = "nilai_siswa_app.csv"

if st.button("Simpan"):
    status = "Lulus" if nilai >= 75 else "Belum Lulus"
    with open(FILE_CSV, mode="a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([nama, nilai, status])
    st.success(f"Data {nama} berhasil disimpan dengan status: {status}")

st.subheader("Riwayat Data Siswa")
if os.path.exists(FILE_CSV):
    with open(FILE_CSV) as f:
        data = list(csv.reader(f))
    st.dataframe(data, use_container_width=True)
else:
    st.info("Belum ada data yang disimpan.")    