import pandas as pd
import streamlit as st

# App Header & Creator Info
st.title("📚 Minaaree Sadarkaa 1ffaa - Bara 2019")
st.markdown("*Appii Qoodinsa Qabxii Barattootaa*")
st.sidebar.info("Creator: **Kitesa Negasa (KN)**")

# 1. Daataa galchuuf (Manual entry ykn CSV upload)
option = st.sidebar.radio(
    "Filannoo Galtee:", ("Galchee Dhuunfaa (Manual)", "Faayilii CSV Fe'uu")
)

if option == "Galchee Dhuunfaa (Manual)":
  st.subheader("Odeeffannoo Barataa Galchi")

  col1, col2 = st.columns(2)
  with col1:
    name = st.text_input("Maqaa Barataa")
    gender = st.selectbox("Koorniyaa", ("Dhiira (M)", "Dhalaa (F)"))
  with col2:
    grade_section = st.text_input("Kutaa fi Daree (Fkn: Kutaa 5ffaa A)")
    score = st.number_input("Qabxii (Dhibbeentaa - %)", min_value=0.0, max_value=100.0)

  if st.button("Ramadi fi Galmeessi"):
    if name and grade_section:
      # Sadarkaa irratti hundaa'uun qooduu
      if score >= 80:
        category = "🌟 Ciccimoo (High Achievers)"
        st.success(
            f"Barataa: {name} | Koorniyaa: {gender} | Kutaa: {grade_section} |"
            f" Qabxii: {score}% -> {category}"
        )
      elif score >= 50:
        category = "📊 Giddu-galeeyyii (Average)"
        st.info(
            f"Barataa: {name} | Koorniyaa: {gender} | Kutaa: {grade_section} |"
            f" Qabxii: {score}% -> {category}"
        )
      else:
        category = "⚠️ Suuta Barattoota (Needs Support)"
        st.warning(
            f"Barataa: {name} | Koorniyaa: {gender} | Kutaa: {grade_section} |"
            f" Qabxii: {score}% -> {category}"
        )
    else:
      st.error("Maaloo maqaa barataa fi kutaa guutaa!")

else:
  st.subheader("Faayilii Qabxii (CSV) Mana Barumsichaa Fe'aa")
  uploaded_file = st.file_uploader(
      "Faayilii CSV (Maqaa, Koorniyaa, Kutaa, Qabxii qabu) filadhu", type=["csv"]
  )

  if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.write("Daataa Galfame:")
    st.dataframe(df)

    # Kolonni barbaachisoo jiraachuu isaanii mirkaneessuu
    required_cols = ["Maqaa", "Koorniyaa", "Kutaa", "Qabxii"]
    if all(col in df.columns for col in required_cols):

      def classify(score):
        if score >= 80:
          return "Ciccimoo"
        elif score >= 50:
          return "Giddu-galeeyyii"
        else:
          return "Suuta Barattoota"

      df["Garee (Category)"] = df["Qabxii"].apply(classify)

      st.subheader("Bu'aa Ramaddii Barattootaa - Minaaree S.1ffaa (2019):")
      st.dataframe(df)

      # Gabaasa gabaabaa (Summary)
      st.subheader("Gabaasa Waliigalaa Gareetiin")
      st.write(df["Garee (Category)"].value_counts())
    else:
      st.error(
          f"Faayilin kee kolonoota armaan gadii qabaachuu qaba:"
          f" {required_cols}"
      )

# Footer info
st.markdown("---")
st.text("Designed & Developed by KN (Kitesa Negasa)")
