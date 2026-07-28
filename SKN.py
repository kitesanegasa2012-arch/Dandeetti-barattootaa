import pandas as pd
import streamlit as st

# App Header & Creator Info
st.set_page_config(
    page_title="Minaaree S.1ffaa - Offline App", page_icon="📚", layout="wide"
)

st.title("🏫 Mana Barumsaa Minaaree Sadarkaa 1ffaa")
st.markdown("### Roostera Cuunfaa Barattootaa (Bara 2018/2019)")
st.sidebar.info("Designed & Developed by **KN (Kitesa Negasa)**")

# Daataa Roostera Cuunfaa Kallattiidhaan Koodii Keessatti Qabsiifame (Embedded Data)
# Faayilii alaa malee intarneetii odoo hin gaafatin akka hojjetu godha.
data = {
    "LAKK": [
        1,
        2,
        3,
        4,
        5,
        6,
        7,
        8,
        9,
        10,
        11,
        12,
        13,
        14,
        15,
        16,
        17,
        18,
        19,
        20,
    ],
    "Maqaa Barattootaa": [
        "Abdataa katamaa Fayisaa",
        "Abdiisaa Garramaa kabbabaa",
        "Abdiisaa Masfinee Kabbuu",
        "Addisuu Girmaa Dhugoo",
        "Addisuu Girmaa Naggasaa",
        "Arjummaa Dassaalenyi Qana'aa",
        "Asheetuu Abdataa Addunyaa",
        "Baqqalaa Asaffaa Mokonnon",
        "Biiniyaam Dirribsaa Damee",
        "Bokii Abarraa Addunyaa",
        "Boontuu Asaffaa Birruu",
        "Boontuu Biraanuu Abarraa",
        "Boontuu Lammii Mul,isaa",
        "BurteeSisuu Baqqalaa",
        "BurteeTufaa caalaa",
        "Burtukaan Abdataa Gaaddisaa",
        "Caalii Fiqaaduu Addunyaa",
        "Caaltuu Caalaa Qananii",
        "Daamxoo Geetaachoo shifarraa",
        "Daawwit Fiqaaduu Addunyaa",
    ],
    "Saala": [
        "Dhi",
        "Dhi",
        "Dhi",
        "Dhi",
        "Dha",
        "Dhi",
        "Dhi",
        "Dhi",
        "Dhi",
        "Dhi",
        "Dha",
        "Dha",
        "Dha",
        "Dha",
        "Dha",
        "Dha",
        "Dha",
        "Dha",
        "Dhi",
        "Dhi",
    ],
    "Afaan_Oromoo": [
        67,
        22,
        52,
        66.5,
        20,
        62.5,
        81,
        0,
        58.5,
        27.5,
        56.5,
        73,
        65.5,
        0,
        20.5,
        70.5,
        23.5,
        61.5,
        55,
        48,
    ],
    "Herrega": [
        49.5,
        18,
        43.5,
        46,
        17,
        44,
        69.5,
        0,
        51.5,
        17.5,
        52,
        50,
        48.5,
        0,
        19.5,
        67,
        24,
        53.5,
        41,
        36,
    ],
    "Ida'ama": [
        551,
        209,
        503,
        566,
        233,
        514.5,
        663.5,
        0,
        539,
        233.5,
        546,
        591.5,
        584.5,
        0,
        232.5,
        575,
        256.5,
        553.5,
        505,
        448,
    ],
    "Av_Qabxii": [
        61.22,
        23.22,
        55.89,
        62.89,
        25.89,
        57.17,
        73.72,
        0.0,
        59.89,
        25.94,
        60.67,
        65.72,
        64.94,
        0.0,
        25.83,
        63.89,
        28.5,
        61.5,
        56.11,
        49.78,
    ],
    "Yaada": [
        "Darbee",
        "Hin Darbine",
        "Darbee",
        "Darbee",
        "Hin Darbine",
        "Darbee",
        "Darbee",
        "Hin Darbine",
        "Darbee",
        "Hin Darbine",
        "Darbitee",
        "Darbitee",
        "Darbitee",
        "Hin Darbine",
        "Hin Darbine",
        "Darbitee",
        "Hin Darbine",
        "Darbitee",
        "Darbee",
        "Darbee",
    ],
}

df = pd.DataFrame(data)

# Sidebar Filter (Barbaacha Maqaa ykn Yaada)
st.sidebar.header("Filannoo fi Barbaacha")
search_name = st.sidebar.text_input("Maqaan Barataa Barbaadi:")
status_filter = st.sidebar.selectbox(
    "Haala Darbiinsaa (Status):",
    ("Hunda", "Darbee / Darbitee", "Hin Darbine"),
)

# Filtarrii hojiirra oolchuu
filtered_df = df.copy()
if search_name:
  filtered_df = filtered_df[
      filtered_df["Maqaa Barattootaa"].str.contains(search_name, case=False)
  ]

if status_filter == "Darbee / Darbitee":
  filtered_df = filtered_df[filtered_df["Yaada"].isin(["Darbee", "Darbitee"])]
elif status_filter == "Hin Darbine":
  filtered_df = filtered_df[filtered_df["Yaada"] == "Hin Darbine"]

# Argisiisa Gabatee Daataa (DataFrame Display)
st.subheader("Gabatee Qabxii Barattootaa")
st.dataframe(filtered_df, use_container_width=True)

# Gabaasa Gabaabaa (Summary Statistics)
st.markdown("---")
st.subheader("📊 Gabaasa Gabaabaa (Summary)")
col1, col2, col3 = st.columns(3)

with col1:
  st.metric(label="Waliigala Barattoota Argaman", value=len(df))
with col2:
  passed_count = len(df[df["Yaada"].isin(["Darbee", "Darbitee"])])
  st.metric(label="Barattoota Darban", value=passed_count)
with col3:
  failed_count = len(df[df["Yaada"] == "Hin Darbine"])
  st.metric(label="Barattoota Hin Darbinne", value=failed_count)

# Footer
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: gray;'>Created with ❤️ by KN (Kitesa"
    " Negasa) | Minaaree Primary School</p>",
    unsafe_allow_html=True,
)
