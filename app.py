import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import ezdxf
import io

# --- MİMARİ PLANLAMA MANTIĞI ---
def plan_olustur(en, boy):
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
    # Yeni bir DXF dökümanı oluştur (R2010 formatı en uyumludur)
    doc = ezdxf.new('R2010')
    msp = doc.modelspace()
    
    for ad, veri in plan.items():
        x, y, w, h = veri["box"]
        # Odaları kapalı çizgi (Polyline) olarak ekle
        msp.add_lwpolyline([(x, y), (x+w, y), (x+w, y+h), (x, y+h), (x, y)], close=True)
        # Oda ismini AutoCAD'e metin olarak ekle
        msp.add_text(ad, dxfattribs={'height': 0.3}).set_placement((x+0.2, y+0.2))
    
    # HATAYI ÇÖZEN KISIM: StringIO yerine BytesIO kullanarak ham veri akışı sağlıyoruz
    out = io.BytesIO()
    doc.write(out)
    return out.getvalue()

# --- STREAMLIT ARAYÜZÜ ---
st.set_page_config(page_title="Mimar AI Pro v5", layout="wide")
st.title("🏗️ Profesyonel Mimari Planlama & DXF Export")

with st.sidebar:
    st.header("📐 Proje Parametreleri")
    en = st.slider("Daire Eni (m)", 8, 20, 12)
    boy = st.slider("Daire Boyu (m)", 8, 20, 12)
    st.divider()
    st.write("Mimar: **inanntug-blip**")

plan_verisi = plan_olustur(en, boy)

col1, col2 = st.columns([2, 1]) 

with col1:
    st.subheader("📍 2D Teknik Kat Planı (Önizleme)")
    fig, ax = plt.subplots(figsize=(10, 8))
    for ad, veri in plan_verisi.items():
        x, y, w, h = veri["box"]
        # Odalar (Dikdörtgenler)
        rect = patches.Rectangle((x, y), w, h, linewidth=3, edgecolor='#333333', facecolor=veri["renk"], alpha=0.6)
        ax.add_patch(rect)
        # Oda isimleri ve m2
        plt.text(x + w/2, y + h/2, f"{ad}\n{w*h:.1f} m²", ha='center', va='center', weight='bold')
        # Mimari pencere detayları (Mavi çizgiler)
        if y + h >= boy: # Üst cephe pencereleri
            ax.plot([x+w*0.2, x+w*0.8], [y+h, y+h], color='blue', lw=5)

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
    # DXF Export Butonu (Yeni hata korumalı yöntem)
    try:
        dxf_bytes = dxf_disa_aktar(plan_verisi)
        st.download_button(
            label="📁 AutoCAD (DXF) Dosyasını İndir",
            data=dxf_bytes,
            file_name="mimari_proje_v5.dxf",
            mime="application/dxf"
        )
        st.success("✅ Teknik çizim hazır!")
    except Exception as e:
        st.error(f"DXF Hatası oluştu. Lütfen tekrar deneyin.")

    st.info("💡 İndirdiğiniz DXF dosyasını AutoCAD veya SketchUp içine sürükleyerek profesyonel çizime devam edebilirsiniz.")
