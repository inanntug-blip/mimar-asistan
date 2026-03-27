import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import ezdxf
from io import BytesIO

# --- MİMARİ MANTIK FONKSİYONLARI ---

def plan_olustur(en, boy, daire_tipi):
    # Basit bir 2+1 yerleşim mantığı (Örnek geometrik bölme)
    plan = {
        "Salon": [0, 0, en*0.5, boy*0.6, "orange"],
        "Mutfak": [en*0.5, 0, en*0.5, boy*0.4, "yellow"],
        "Yatak Odası 1": [0, boy*0.6, en*0.4, boy*0.4, "lightblue"],
        "Yatak Odası 2": [en*0.4, boy*0.6, en*0.3, boy*0.4, "cyan"],
        "Banyo/WC": [en*0.7, boy*0.4, en*0.3, boy*0.4, "lightgrey"],
        "Antre": [en*0.5, boy*0.4, en*0.2, boy*0.2, "white"]
    }
    return plan

def dxf_disa_aktar(plan):
    doc = ezdxf.new()
    msp = doc.modelspace()
    for ad, (x, y, w, h, _) in plan.items():
        # Oda sınırlarını çiz
        msp.add_lwpolyline([(x, y), (x+w, y), (x+w, y+h), (x, y+h), (x, y)], close=True)
        # Oda ismini yaz
        msp.add_text(f"{ad}", dxfattribs={'height': 0.5}).set_placement((x+0.5, y+0.5))
    
    out = BytesIO()
    doc.save_to_stream(out)
    return out.getvalue()

# --- STREAMLIT ARAYÜZÜ ---

st.set_page_config(page_title="AI Mimar Asistanı", layout="wide")
st.title("🏗️ Yapay Zeka Destekli Mimari Planlama")

with st.sidebar:
    st.header("Proje Girdileri")
    en = st.number_input("Daire Eni (m)", value=10)
    boy = st.number_input("Daire Boyu (m)", value=12)
    tip = st.selectbox("Daire Tipi", ["1+1", "2+1", "3+1"])
    hesapla = st.button("Planı Oluştur ve Optimize Et")

if hesapla:
    plan_verisi = plan_olustur(en, boy, tip)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Matematiksel Yerleşim ve Tefriş Şeması")
        fig, ax = plt.subplots(figsize=(10, 8))
        for oda, (x, y, w, h, renk) in plan_verisi.items():
            rect = patches.Rectangle((x, y), w, h, linewidth=2, edgecolor='black', facecolor=renk, alpha=0.5)
            ax.add_patch(rect)
            plt.text(x + w/2, y + h/2, f"{oda}\n{w*h:.1f} m2", ha='center', va='center', weight='bold')
        
        plt.xlim(-1, en+1)
        plt.ylim(-1, boy+1)
        plt.gca().set_aspect('equal', adjustable='box')
        st.pyplot(fig)

    with col2:
        st.subheader("Verimlilik Raporu")
        toplam_alan = en * boy
        kullanilan_alan = sum(w*h for _, _, w, h, _ in plan_verisi.values())
        st.metric("Toplam Alan", f"{toplam_alan} m2")
        st.metric("Kullanılabilir Alan", f"{kullanilan_alan:.1f} m2")
        st.metric("Verimlilik Skoru", f"%{(kullanilan_alan/toplam_alan)*100:.1f}")
        
        dxf_data = dxf_disa_aktar(plan_verisi)
        st.download_button("AutoCAD (DXF) Olarak İndir", data=dxf_data, file_name="proje_taslak.dxf")

st.info("Bu prototip, matematiksel oran-orantı ve mimari yerleşim kurallarını baz alarak saniyeler içinde taslak üretir.")
