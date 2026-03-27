import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import ezdxf
import io

# --- MİMARİ ZEKA: DAİRE TİPİ VE TEFRİŞ MANTIĞI ---
def plan_olustur(en, boy, tip):
    # Daire tipine göre oda konfigürasyonları
    if tip == "1+1":
        plan = {
            "Salon + Mutfak": {"box": [0, 0, en*0.6, boy], "renk": "#FFD580", "tefris": ["🛋️", "🍽️", "🍳"]},
            "Yatak Odası": {"box": [en*0.6, 0, en*0.4, boy*0.7], "renk": "#B3E5FC", "tefris": ["🛏️", "👗"]},
            "Banyo/WC": {"box": [en*0.6, boy*0.7, en*0.4, boy*0.3], "renk": "#F5F5F5", "tefris": ["🚿", "🚽"]}
        }
    elif tip == "2+1":
        plan = {
            "Salon": {"box": [0, 0, en*0.5, boy*0.6], "renk": "#FFD580", "tefris": ["🛋️", "📺"]},
            "Mutfak": {"box": [en*0.5, 0, en*0.5, boy*0.4], "renk": "#FFF9C4", "tefris": ["🍳", "❄️"]},
            "Yatak Odası 1": {"box": [0, boy*0.6, en*0.5, boy*0.4], "renk": "#B3E5FC", "tefris": ["🛏️", "👗"]},
            "Yatak Odası 2": {"box": [en*0.5, boy*0.6, en*0.5, boy*0.4], "renk": "#E1F5FE", "tefris": ["🧸", "📚"]},
            "Banyo": {"box": [en*0.5, boy*0.4, en*0.25, boy*0.2], "renk": "#F5F5F5", "tefris": ["🚿"]},
            "Antre": {"box": [en*0.75, boy*0.4, en*0.25, boy*0.2], "renk": "#FFFFFF", "tefris": ["👟"]}
        }
    else: # 3+1
        plan = {
            "Salon": {"box": [0, 0, en*0.4, boy*0.7], "renk": "#FFD580", "tefris": ["🛋️", "🍽️"]},
            "Mutfak": {"box": [en*0.4, 0, en*0.3, boy*0.4], "renk": "#FFF9C4", "tefris": ["🍳"]},
            "E. Yatak Odası": {"box": [en*0.7, 0, en*0.3, boy*0.5], "renk": "#B3E5FC", "tefris": ["🛏️", "🚿"]},
            "Oda 1": {"box": [0, boy*0.7, en*0.35, boy*0.3], "renk": "#E1F5FE", "tefris": ["🧸"]},
            "Oda 2": {"box": [en*0.35, boy*0.7, en*0.35, boy*0.3], "renk": "#E1F5FE", "tefris": ["🧸"]},
            "Banyo/Antre": {"box": [en*0.7, boy*0.5, en*0.3, boy*0.5], "renk": "#F5F5F5", "tefris": ["🚽"]}
        }
    return plan

# --- DXF EXPORT (Hatasız Versiyon) ---
def dxf_disa_aktar(plan):
    doc = ezdxf.new('R2010')
    msp = doc.modelspace()
    for ad, veri in plan.items():
        x, y, w, h = veri["box"]
        msp.add_lwpolyline([(x, y), (x+w, y), (x+w, y+h), (x, y+h), (x, y)], close=True)
        msp.add_text(ad, dxfattribs={'height': 0.3}).set_placement((x+0.2, y+0.2))
    out = io.BytesIO()
    doc.write(out)
    return out.getvalue()

# --- ARAYÜZ ---
st.set_page_config(page_title="Mimar AI Pro v6", layout="wide")
st.title("🏗️ Profesyonel Mimari Tasarım & Tefriş Paneli")

with st.sidebar:
    st.header("📐 Proje Parametreleri")
    tip = st.selectbox("Daire Tipi", ["1+1", "2+1", "3+1"])
    en = st.slider("Daire Eni (m)", 8.0, 20.0, 12.0)
    boy = st.slider("Daire Boyu (m)", 8.0, 20.0, 10.0)
    st.divider()
    show_furniture = st.checkbox("Tefrişleri (Eşyalar) Göster", value=True)
    show_doors = st.checkbox("Kapı ve Pencereleri Göster", value=True)

plan_verisi = plan_olustur(en, boy, tip)

col1, col2 = st.columns([3, 1])

with col1:
    st.subheader(f"📍 {tip} Teknik Kat Planı")
    fig, ax = plt.subplots(figsize=(12, 9))
    for ad, veri in plan_verisi.items():
        x, y, w, h = veri["box"]
        # Odalar
        rect = patches.Rectangle((x, y), w, h, linewidth=3, edgecolor='#2C3E50', facecolor=veri["renk"], alpha=0.7)
        ax.add_patch(rect)
        # Oda Metni
        plt.text(x + w/2, y + h*0.8, f"{ad}\n{w*h:.1f} m²", ha='center', va='center', weight='bold', fontsize=10)
        
        # TEFRİŞLER
        if show_furniture:
            items = " ".join(veri["tefris"])
            plt.text(x + w/2, y + h*0.4, items, ha='center', va='center', fontsize=20)

        # KAPI VE PENCERE SEMBOLLERİ
        if show_doors:
            # Pencere (Mavi)
            if y + h >= boy - 0.1: ax.plot([x+w*0.2, x+w*0.8], [y+h, y+h], color='#3498DB', lw=6)
            # Kapı Sembolü (Çeyrek Daire - Temsili)
            ax.plot([x, x+0.9], [y, y], color='brown', lw=2) 
            arc = patches.Arc((x, y), 1.8, 1.8, angle=0, theta1=0, theta2=90, color='brown', ls='--')
            ax.add_patch(arc)

    plt.xlim(-1, en+1); plt.ylim(-1, boy+1)
    plt.gca().set_aspect('equal'); plt.axis('off')
    st.pyplot(fig)

with col2:
    st.subheader("📊 Analiz")
    st.metric("Toplam Alan", f"{en*boy:.1f} m²")
    st.write("**Oda Dağılımı:**")
    for ad, v in plan_verisi.items():
        st.write(f"- {ad}: {v['box'][2]*v['box'][3]:.1f} m²")
    
    st.divider()
    try:
        dxf_bytes = dxf_disa_aktar(plan_verisi)
        st.download_button("📁 AutoCAD (DXF) İndir", data=dxf_bytes, file_name=f"{tip}_proje.dxf")
        st.success("Çizim Hazır!")
    except:
        st.error("DXF oluşturulamadı.")

st.info("💡 Mimar Notu: Daire tipine göre ıslak hacimler ve yaşam alanları optimize edilmiştir.")
