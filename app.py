# app.py
import os
import easyocr
import numpy as np
import pandas as pd
import streamlit as st
from PIL import Image

# Ensure folder for saved files
SAVE_DIR = "Kuusaa_Ragaa"
os.makedirs(SAVE_DIR, exist_ok=True)

# -- Page config
st.set_page_config(
    page_title="TRIAD",
    page_icon="📚",
    layout="wide"
)

# -- Load custom CSS
def local_css(file_name):
    if os.path.exists(file_name):
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css("styles.css")

# Header / Cover
st.markdown(
    """
    <div class="cover">
        <div style="display:flex; align-items:center; gap:20px;">
            <div style="flex:1">
                <h1>🏫 TRIAD APP</h1>
                <p style="margin:6px 0 0 0; font-size:16px; opacity:0.95;">
                    Appii Barattoota Daree Keessatti Dandeetti Sadiin Qoodu — Kalaqa KN (Kitesa Negasa)
                </p>
            </div>
            <div style="width:140px">
                <img src="qixxeessaa.jpg" class="profile-img" alt="Qixxeessaa" width="140"/>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.sidebar.info("Designed & Developed by **KN (Kitesa Negasa)**")
st.sidebar.markdown("---")
st.sidebar.subheader("👤 Suura Kalaqaa")

# Sidebar profile image (fallback)
profile_pic_path = "qixxeessaa.jpg"
if os.path.exists(profile_pic_path):
    st.sidebar.image(profile_pic_path, caption="Qixxeessaa Nagaasaa (KN)", use_container_width=True)
else:
    st.sidebar.warning("Suuraan 'qixxeessaa.jpg' hin argamne. Maaloo foldera koodii kana waliin kaa'i.")

# Sidebar texts (Oromo)
st.sidebar.markdown("### 📝 Seensa  (Introduction)")
st.sidebar.write(
    "Baga Nagaan Gara TRIAD appilikeeshiniikootti dhufte! Ani Kitesa Negasa (KN). TRIAD = Tracking Rates in Academic Development.\n\n"
    "Appiin kun barattoota dandeetti adda baasuun deggeruuf kan qophaa'e; kutaalee barnootaa fi sadarkaa adda addaa ni deeggara."
)

st.sidebar.markdown("### 🎯 Kaayyoo Appichaa")
st.sidebar.write(
    "Kaayyoon isaa: barattoota dandeetti isaanii adda baasuudhaan tajaajila barnootaa foyyeessuuf gorsa kennuufi."
)

st.sidebar.markdown("---")
st.sidebar.subheader("📖 Qajeelfama Itti Fayyadamaa")
st.sidebar.markdown(
    """
1. Faayilii Excel/CSV ykn Suuraa fe'uu.
2. 'Save' cuqaasi yoo barbaadde faayilii kuusuuf.
3. Kolonoota sirreessi (Maqaa, Saala, Gosa Barnootaa).
4. Bu'aa fi qoodinsa ilaali.
"""
)

# Cache OCR reader
@st.cache_resource
def load_ocr_reader():
    return easyocr.Reader(['en'])

st.sidebar.markdown("---")
st.sidebar.subheader("🗄️ Madda Ragaa Filadhu")
madda_ragaa = st.sidebar.radio("Filannoo kee:", ["📤 Ragaa Haaraa Fe'uu (Upload)", "📁 Ragaa Kuufame Fayyadamuu (Saved)"])

df = None
file_extension = ""
image_to_process = None

# Upload flow
if madda_ragaa == "📤 Ragaa Haaraa Fe'uu (Upload)":
    st.subheader("📂 Step 1: Faayilii (Excel/CSV) ykn Suuraa (Image) Fe'aa")
    uploaded_file = st.file_uploader("Faayilii ykn Suuraa filadhu", type=["csv","xlsx","png","jpg","jpeg"])
    if uploaded_file is not None:
        file_extension = uploaded_file.name.split('.')[-1].lower()
        # Save file
        if st.button("💾 Faayilii Kana Kuusi (Save File)"):
            file_path = os.path.join(SAVE_DIR, uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            st.success(f"Faayiliin '{uploaded_file.name}' kuufameera.")
        if file_extension == 'csv':
            df = pd.read_csv(uploaded_file)
            st.success("CSV milkaa'inaan fe'ameera!")
        elif file_extension == 'xlsx':
            xls = pd.ExcelFile(uploaded_file)
            sheet_name = st.selectbox("Sheet filadhu:", xls.sheet_names)
            skip = st.number_input("Sarara irraa kaafamu (Header Row Index):", min_value=0, max_value=50, value=0)
            df = pd.read_excel(uploaded_file, sheet_name=sheet_name, skiprows=skip)
            st.success("Excel milkaa'inaan fe'ameera!")
        else:
            image_to_process = Image.open(uploaded_file)
            st.image(image_to_process, caption="Suuraa Fe’ame", use_container_width=True)

# Saved files flow
else:
    st.subheader("📁 Faayiloota Kuufaman")
    saved_files = sorted(os.listdir(SAVE_DIR))
    if not saved_files:
        st.info("Kuusaa keessa ragaan hin jiru. Faayilii haaraa fe'i.")
    else:
        selected_file = st.selectbox("Faayilii filadhu:", saved_files)
        file_path = os.path.join(SAVE_DIR, selected_file)
        file_extension = selected_file.split('.')[-1].lower()
        if st.button("🗑️ Faayilii Kana Haqi (Delete)"):
            os.remove(file_path)
            st.success(f"Faayiliin '{selected_file}' haqameera!")
            st.experimental_rerun()
        if os.path.exists(file_path):
            if file_extension == 'csv':
                df = pd.read_csv(file_path)
            elif file_extension == 'xlsx':
                xls = pd.ExcelFile(file_path)
                sheet_name = st.selectbox("Sheet filadhu:", xls.sheet_names)
                skip = st.number_input("Sarara irraa kaafamu (Header Row Index):", min_value=0, max_value=50, value=0)
                df = pd.read_excel(file_path, sheet_name=sheet_name, skiprows=skip)
            else:
                image_to_process = Image.open(file_path)
                st.image(image_to_process, caption="Suuraa Kuufame", use_container_width=True)

# OCR processing
if image_to_process is not None:
    st.info("Suuraa irraa barreeffama dubbisa...")
    with st.spinner("OCR yeroo gabaabaa fudhata..."):
        image_np = np.array(image_to_process.convert('RGB'))
        reader = load_ocr_reader()
        results = reader.readtext(image_np)
        extracted_texts = [r[1] for r in results]
        if extracted_texts:
            st.success("Barreeffama suuraa irraa argameera.")
            for idx, t in enumerate(extracted_texts, start=1):
                st.write(f"{idx}. {t}")
        else:
            st.error("Barreeffama hin argamne.")

# Dataframe analytics
if df is not None:
    st.subheader("⚙️ Step 2 & 3: Qindaa'ina Kolonootaa fi Daataa")
    all_columns = df.columns.tolist()
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        name_col = st.selectbox("Kolonii Maqaa Barataa:", all_columns, index=0)
    with col_b:
        gender_col = st.selectbox("Kolonii Saala (Gender):", all_columns, index=1 if len(all_columns)>1 else 0)
    with col_c:
        subject_cols = st.multiselect("Kolonoota Gosa Barnootaa:", [c for c in all_columns if c not in [name_col, gender_col]])

    st.markdown("---")
    st.subheader("👀 Daataa Jalqabaa fi Baay'ina Barattoota")
    dhiira_total = len(df[df[gender_col].astype(str).str.contains("Dhi|M", case=False, na=False)])
    dhalaa_total = len(df[df[gender_col].astype(str).str.contains("Dha|F", case=False, na=False)])
    total_students = dhiira_total + dhalaa_total
    m_col1, m_col2, m_col3 = st.columns(3)
    m_col1.metric("👥 Waliigala Galmaa'an", f"{total_students}")
    m_col2.metric("👦 Dhiira", f"{dhiira_total}")
    m_col3.metric("👧 Dhalaa", f"{dhalaa_total}")
    st.dataframe(df.head(), use_container_width=True)

    # Scaling
    st.markdown("---")
    use_scaling = st.checkbox("Qabxii gara 100tti jijjiiru (Scale to 100%)")
    max_score_input = 100
    if use_scaling:
        max_score_input = st.number_input("Max Possible Score (e.g., 10,20):", min_value=1, value=10)

    if subject_cols and name_col and gender_col:
        st.markdown("---")
        st.subheader("🔍 Step 4: Qoodinsa Gosa Barnootaan")
        search_query = st.text_input("Maqaa Barataa Barbaadi:")
        filtered_main_df = df.copy()
        if search_query:
            filtered_main_df = filtered_main_df[filtered_main_df[name_col].astype(str).str.contains(search_query, case=False, na=False)]
            st.info(f"Bu'aa barbaacha: '{search_query}'")
            st.dataframe(filtered_main_df, use_container_width=True, hide_index=True)
            st.markdown("---")

        for subj in subject_cols:
            st.markdown(f"### 📖 Gosa Barnootaa: **{subj}**")
            scores = pd.to_numeric(df[subj], errors="coerce")
            if use_scaling and max_score_input > 0:
                scores = (scores / float(max_score_input)) * 100
            temp_df = df.copy()
            temp_df["Calculated_Score"] = scores
            ciccimoo = temp_df[temp_df["Calculated_Score"] >= 80]
            giddu = temp_df[(temp_df["Calculated_Score"] >= 50) & (temp_df["Calculated_Score"] < 80)]
            suuta = temp_df[(temp_df["Calculated_Score"] < 50) & (temp_df["Calculated_Score"].notna())]
            none_df = temp_df[temp_df["Calculated_Score"].isna()]
            dhiira_qoraman = len(pd.concat([ciccimoo, giddu, suuta])[pd.concat([ciccimoo, giddu, suuta])[gender_col].astype(str).str.contains("Dhi|M", case=False, na=False)])
            dhalaa_qoraman = len(pd.concat([ciccimoo, giddu, suuta])[pd.concat([ciccimoo, giddu, suuta])[gender_col].astype(str).str.contains("Dha|F", case=False, na=False)])
            waliigala_qoraman = dhiira_qoraman + dhalaa_qoraman
            dhiira_none = len(none_df[none_df[gender_col].astype(str).str.contains("Dhi|M", case=False, na=False)])
            dhalaa_none = len(none_df[none_df[gender_col].astype(str).str.contains("Dha|F", case=False, na=False)])
            waliigala_none = dhiira_none + dhalaa_none

            st.info(f"📊 Istaatistikaa {subj}:\n- Waliigala Qoraman: {waliigala_qoraman} (Dhiira: {dhiira_qoraman} | Dhalaa: {dhalaa_qoraman})\n- None: {waliigala_none} (Dhiira: {dhiira_none} | Dhalaa: {dhalaa_none})")

            display_cols = [name_col, gender_col, subj]
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("🌟 Ciccimoo (≥ 80%)", f"{len(ciccimoo)}")
                if not ciccimoo.empty:
                    st.dataframe(ciccimoo[display_cols], use_container_width=True, hide_index=True)
            with col2:
                st.metric("📊 Giddu-galeeyyii (50-79.9%)", f"{len(giddu)}")
                if not giddu.empty:
                    st.dataframe(giddu[display_cols], use_container_width=True, hide_index=True)
            with col3:
                st.metric("⚠️ Suuta (<50%)", f"{len(suuta)}")
                if not suuta.empty:
                    st.dataframe(suuta[display_cols], use_container_width=True, hide_index=True)
            st.markdown("---")
else:
    st.info("Faayilii fe'uu ykn filachuudhaan jalqabi.")

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center; color: gray;'>Created with ❤️ by KN (Kitesa Negasa) | Educational Analytics App</p>", unsafe_allow_html=True)
