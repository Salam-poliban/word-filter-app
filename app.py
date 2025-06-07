import streamlit as st
import pandas as pd

# === Load data ===
df = pd.read_csv("five_letter_words_new.csv")
words = df["Word"].dropna().astype(str).str.lower().unique()

# === Filter kata berdasarkan huruf ===
def filter_words_by_letters(word_list, required_letters):
    required_letters = set(letter.lower() for letter in required_letters)
    return [word for word in word_list if required_letters.issubset(set(word.lower()))]

# === Filter kata berdasarkan posisi ===
def filter_words_by_positions(word_list, position_dict):
    result = []
    for word in word_list:
        match = True
        for pos, char in position_dict.items():
            if len(word) <= pos or word[pos].lower() != char.lower():
                match = False
                break
        if match:
            result.append(word)
    return result

# === UI ===
st.set_page_config(page_title="Word Finder", layout="centered")
st.title("🔤 5-Letter Word Filter")

st.markdown("Masukkan huruf pada posisi tertentu (boleh dikosongkan):")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    h1 = st.text_input("Huruf ke-1", max_chars=1)
with col2:
    h2 = st.text_input("Huruf ke-2", max_chars=1)
with col3:
    h3 = st.text_input("Huruf ke-3", max_chars=1)
with col4:
    h4 = st.text_input("Huruf ke-4", max_chars=1)
with col5:
    h5 = st.text_input("Huruf ke-5", max_chars=1)

huruf_bebas = st.text_input("Huruf tambahan (bebas)", max_chars=5)

# === Proses pencarian ===
if st.button("🔍 Cari Kata"):

    # Buat dict posisi
    posisi = {}
    if h1: posisi[0] = h1
    if h2: posisi[1] = h2
    if h3: posisi[2] = h3
    if h4: posisi[3] = h4
    if h5: posisi[4] = h5

    # Filter berdasarkan posisi
    hasil = filter_words_by_positions(words, posisi)

    # Gabungkan semua huruf yang harus ada
    required_letters = list(huruf_bebas.lower())
    required_letters += [c for c in [h1, h2, h3, h4, h5] if c]

    # Filter berdasarkan huruf yang terkandung
    hasil = filter_words_by_letters(hasil, required_letters)

    st.markdown(f"### ✨ Ditemukan {len(hasil)} kata:")
    st.write(sorted(hasil))
