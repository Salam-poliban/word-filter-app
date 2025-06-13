import streamlit as st
import pandas as pd

# Load data kata
df = pd.read_csv("five_letter_words_new.csv")
words = df["Word"].dropna().astype(str).str.lower().unique()

st.set_page_config(page_title="Wordle Assistant", layout="centered")
st.title("🔤 Wordle Assistant")

st.markdown("Masukkan huruf dan status warna seperti Wordle (⬛ 🟨 🟩):")

# Mapping warna
warna_opsi = {
    "gray": "⬛",
    "yellow": "🟨",
    "green": "🟩"
}
warna_keys = list(warna_opsi.keys())

inputs = []
statuses = []

# Form input posisi 1–5
for i in range(5):
    col1, col2 = st.columns([1, 1.5])
    with col1:
        huruf = st.text_input(f" ", max_chars=1, key=f"huruf_{i}", placeholder=f"Huruf {i+1}")
        inputs.append(huruf.lower())
    with col2:
        status = st.radio(
            label=" ",
            options=warna_keys,
            format_func=lambda x: warna_opsi[x],
            key=f"status_{i}",
            horizontal=True
        )
        statuses.append(status)

# Form tambahan
gray_extra = st.text_input("Huruf-huruf yang sudah dicoba dan abu-abu (⬛):", max_chars=10, placeholder="misal: tqxz")
optional_letters = st.text_input("Huruf-huruf yang boleh ada di dalam kata (opsional):", max_chars=10, placeholder="misal: ab")

# === Fungsi filter
def wordle_filter(word_list, inputs, statuses, extra_gray_letters, optional_letters):
    contains = set(optional_letters) if optional_letters else set()
    must_not_contain = set(extra_gray_letters) if extra_gray_letters else set()
    must_be_at_pos = {}
    not_at_pos = {}

    for i, (ch, status) in enumerate(zip(inputs, statuses)):
        if not ch:
            continue
        if status == "green":
            must_be_at_pos[i] = ch
            contains.add(ch)
        elif status == "yellow":
            not_at_pos[i] = ch
            contains.add(ch)
        elif status == "gray":
            must_not_contain.add(ch)

    result = []
    for word in word_list:
        valid = True

        # Posisi hijau
        for i, ch in must_be_at_pos.items():
            if word[i] != ch:
                valid = False
                break

        # Posisi kuning
        for i, ch in not_at_pos.items():
            if ch not in word or word[i] == ch:
                valid = False
                break

        # Harus mengandung semua huruf
        if not contains.issubset(set(word)):
            valid = False

        # Tidak boleh mengandung huruf abu-abu (kecuali sudah dianggap kuning/hijau/opsional)
        if any(ch in word for ch in must_not_contain - contains):
            valid = False

        if valid:
            result.append(word)

    return result

# Tombol pencarian
if st.button("🔍 Cari Kata"):
    hasil = wordle_filter(words, inputs, statuses, gray_extra.lower(), optional_letters.lower())
    st.success(f"Ditemukan {len(hasil)} kata:")
    st.write(hasil)
