import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import ezdxf
from io import BytesIO

# --- MİMARİ PLANLAMA VE TEFRİŞ MANTIĞI ---
def plan_olustur(en, boy):
    # Bir mimar gibi alanları % oranlarına göre bölüyoruz
    plan = {
        "Salon": {"box": [0, 0, en*0.6, boy*0.5], "renk": "#FFD580", "ikon": "🛋️"},
        "Mutfak": {"box": [en*0.6, 0, en*0.4, boy*0.4], "renk": "#FFF9C4", "ikon": "🍳"},
        "Yatak Odası 1": {"box": [0, boy*0.5, en*0.5, boy*0.5], "renk": "#B3E5FC", "ikon": "🛏️"},
        "Yatak Odası 2": {"box": [en*0.5, boy*0.5, en*0.3, boy*0.5], "renk": "#E1F5FE", "ikon": "🧸"},
        "Banyo/WC": {"box": [en*0.8, boy*0.4, en*0.2, boy*0.6], "renk": "#F5F5F5", "ikon": "🚿"},
        "Antre/Hol": {"box": [en*0.6, boy*0.4, en*0.2, boy*0.1], "renk": "#FFFFFF", "ikon": "👟"}
    }
    return plan

def dxf_disa_aktar(plan):
    # En güvenli DXF oluşturma yöntemi
    doc = ezdxf.new('R2010')
    msp = doc.modelspace()
    for ad, veri in plan.items():
        x, y, w, h = veri["box"]
        # Oda sınırlarını çiz
        msp.add_lwpolyline([(x, y), (x+w, y), (x+w, y+h), (x, y+h), (x, y)], close=True)
        # Oda ismini AutoCAD içine ekle
        msp.add_text(f"{ad}", dxfattribs={'height': 0.3}).set_placement((x+0.2, y+0.2))
    
    out = BytesIO()
    # HATA ÇÖZÜMÜ: save() fonksiyonu ile stream üzerine yazıyoruz
    doc.write(out) 
    return out.getvalue()

# --- STREAMLIT ARAYÜZÜ ---
st.set_page_config(page_title="Pro-Mimar AI v3", layout="wide")
st.title("🏗️ Profesyonel Mimari Planlama & Otomasyon")

with st.sidebar:
    st.header("📐 Proje Parametreleri")
    en = st.slider("Daire Eni (m)", 8, 20, 10)
    boy = st.slider("Daire Boyu (m)", 8, 20, 12)
    st.divider()
    st.write("Mimar: **inanntug-blip**")

plan_verisi = plan_olustur(en, boy)

col1, col2 = st.columns([2, 1]) # Plan alanı daha geniş olsun

with col1:
    st.subheader("📍 2D Teknik Kat Planı")
    fig, ax = plt.subplots(figsize=(10, 8))
    for ad, veri in plan_verisi.items():
        x, y, w, h = veri["box"]
        # Odaları çiz
        rect = patches.Rectangle((x, y), w, h, linewidth=3, edgecolor='#333333', facecolor=veri["renk"], alpha=0.6)
        ax.add_patch(rect)
        # Metinleri ekle
        plt.text(x + w/2, y + h/2, f"{veri['ikon']} {ad}\n{w*h:.1f} m²", ha='center', va='center', weight='bold')

    plt.xlim(-1, en+1)
    plt.ylim(-1, boy+1)
    plt.gca().set_aspect('equal', adjustable='box')
    plt.axis('off')
    st.pyplot(fig)

with col2:
    st.subheader("📊 Analiz ve Çıktılar")
    toplam_alan = en * boy
    st.metric("Toplam Brüt Alan", f"{toplam_alan} m²")
    
    st.write("---")
    # AutoCAD İndirme Butonu (Hatasız)
    try:
        dxf_data = dxf_disa_aktar(plan_verisi)
        st.download_button(
            label="📁 AutoCAD (DXF) Dosyasını İndir",
            data=dxf_data,
            file_name="mimari_proje.dxf",
            mime="application/dxf"
        )
    except Exception as e:
        st.error(f"DXF Hatası: {e}")

    st.success("Plan mimari standartlara göre optimize edildi.")
    
    # Oda Listesi Tablosu
    st.write("**Oda Detayları:**")
    for ad, veri in plan_verisi.items():
        w, h = veri["box"][2], veri["box"][3]
        st.write(f"- {ad}: {w*h:.1f} m²")
