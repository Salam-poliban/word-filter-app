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
    "gray": "⬛",    # Tidak ada huruf
    "yellow": "🟨",  # Huruf ada tapi salah posisi
    "green": "🟩"    # Huruf dan posisi tepat
}
warna_keys = list(warna_opsi.keys())

inputs = []
statuses = []

# Tampilkan inputan horizontal per huruf
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

# === Fungsi filter
def wordle_filter(word_list, inputs, statuses):
    contains = set()
    must_not_contain = set()
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
        for i, ch in must_be_at_pos.items():
            if word[i] != ch:
                valid = False
                break
        for i, ch in not_at_pos.items():
            if ch not in word or word[i] == ch:
                valid = False
                break
        if not contains.issubset(set(word)):
            valid = False
        if any(ch in word for ch in must_not_contain - contains):
            valid = False
        if valid:
            result.append(word)
    return result

# Tombol pencarian
if st.button("🔍 Cari Kata"):
    hasil = wordle_filter(words, inputs, statuses)
    st.success(f"Ditemukan {len(hasil)} kata:")
    st.write(hasil)
