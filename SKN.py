import pandas as pd
import streamlit as st

# App Configuration
st.set_page_config(
    page_title="Appii Qoodinsa Qabxii Barattootaa (Kutaa 1-12)",
    page_icon="📚",
    layout="wide",
)

# Header & Creator Info
st.title("🏫 Appii Qoodinsa Qabxii Barattootaa Gosa Barnootaan")
st.markdown(
    "### Kutaa 1 hanga 12 - Qabxii Barattootaa Gara Gareetti Qooduu"
)
st.sidebar.info("Designed & Developed by **KN (Kitesa Negasa)**")

# Kutaa filachiisuu
grade_level = st.sidebar.selectbox(
    "Kutaa Barumsaa Filadhu:",
    [
        "Kutaa 1ffaa",
        "Kutaa 2ffaa",
        "Kutaa 3ffaa",
        "Kutaa 4ffaa",
        "Kutaa 5ffaa",
        "Kutaa 6ffaa",
        "Kutaa 7ffaa",
        "Kutaa 8ffaa",
        "Kutaa 9ffaa",
        "Kutaa 10ffaa",
        "Kutaa 11ffaa",
        "Kutaa 12ffaa",
    ],
)

st.sidebar.markdown(f"**Kutaa Filatame:** {grade_level}")
st.sidebar.markdown("---")

# Faayilii Excel/CSV Fe'uu (Upload)
st.subheader("📂 Faayilii Qabxii Barattootaa (Excel/CSV) Fe'aa")
uploaded_file = st.file_uploader(
    "Faayilii Qabxii barattootaa (Maqaa fi Gosa barnootaa kan qabate) filadhu",
    type=["csv", "xlsx"],
)

if uploaded_file is not None:
  # Faayilii dubbisuu (CSV ykn Excel)
  if uploaded_file.name.endswith(".csv"):
    df = pd.read_csv(uploaded_file)
  else:
    xls = pd.ExcelFile(uploaded_file)
    sheet_name = st.selectbox("Sheet Excel filadhu:", xls.sheet_names)
    skip = st.number_input(
        "Sarara irraa kaafamu (Header Row Index, yoo barbaachise):",
        min_value=0,
        max_value=10,
        value=0,
    )
    df = pd.read_excel(uploaded_file, sheet_name=sheet_name, skiprows=skip)

  st.success("Faayiliin milkaa'inaan fe'ameera!")
  st.subheader("Daataa Jalqabaa (Raw Data Preview)")
  st.dataframe(df.head(), use_container_width=True)

  # Kolonoota gosa barnootaa filachiisuu
  st.subheader("⚙️ Qindaa'ina Gosa Barnootaa")
  all_columns = df.columns.tolist()

  name_col = st.selectbox(
      "Kolonii Maqaa Barataa:",
      all_columns,
      index=1 if len(all_columns) > 1 else 0,
  )

  subject_cols = st.multiselect(
      "Kolonoota Gosa Barnootaa (Qabxii qaban) filadhu:",
      [col for col in all_columns if col != name_col],
  )

  if subject_cols:
    st.markdown("---")
    st.subheader(f"📊 Bu'aa Qoodinsa {grade_level} - Gosa Barnootaan")

    for subj in subject_cols:
      st.markdown(f"### 📖 Gosa Barnootaa: **{subj}**")

      scores = pd.to_numeric(df[subj], errors="coerce")

      ciccimoo = df[scores >= 80]
      giddu = df[(scores >= 50) & (scores < 80)]
      suuta = df[(scores < 50) & (scores.notna())]

      col1, col2, col3 = st.columns(3)
      with col1:
        st.metric(
            label="🌟 Ciccimoo (≥ 80%)", value=f"{len(ciccimoo)} Barattoota"
        )
        if not ciccimoo.empty:
          st.dataframe(
              ciccimoo[[name_col, subj]], use_container_width=True, hide_index=True
          )

      with col2:
        st.metric(
            label="📊 Giddu-galeeyyii (50-79.9%)",
            value=f"{len(giddu)} Barattoota",
        )
        if not giddu.empty:
          st.dataframe(
              giddu[[name_col, subj]], use_container_width=True, hide_index=True
          )

      with col3:
        st.metric(
            label="⚠️ Suuta Barattoota (< 50%)",
            value=f"{len(suuta)} Barattoota",
        )
        if not suuta.empty:
          st.dataframe(
              suuta[[name_col, subj]], use_container_width=True, hide_index=True
          )

      st.markdown("---")

else:
  st.info(
      "Maaloo jalqabaaf faayilii kee (Excel ykn CSV) fe'i, itti aansees"
      " kolonoota gosa barnootaa filadhu."
  )

# Footer
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: gray;'>Created with ❤️ by KN (Kitesa"
    " Negasa) | Educational Analytics App</p>",
    unsafe_allow_html=True,
)
