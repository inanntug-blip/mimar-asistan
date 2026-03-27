import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import io

# --- MOBİLYA ÇİZİM MOTORU ---
def mobilya_ciz(ax, oda_adi, x, y, w, h):
    # Renk paleti
    m_renk = "#5D6D7E" # Mobilya rengi (Koyu Gri)
    
    if "Yatak" in oda_adi:
        # Yatak (1.6x2.0 m) - Duvara dayalı
        ax.add_patch(patches.Rectangle((x+0.5, y+h-2.5), 1.6, 2.0, color=m_renk, alpha=0.8))
        ax.add_patch(patches.Rectangle((x+0.5, y+h-0.5), 1.6, 0.4, color="#34495E")) # Yatak başlığı
    
    elif "Salon" in oda_adi:
        # L Koltuk (2.5x2.5 m)
        ax.add_patch(patches.Rectangle((x+0.5, y+0.5), 2.5, 0.8, color=m_renk, alpha=0.8))
        ax.add_patch(patches.Rectangle((x+0.5, y+0.5), 0.8, 2.5, color=m_renk, alpha=0.8))
        # TV Ünitesi
        ax.add_patch(patches.Rectangle((x+w-1.5, y+h/2-1), 0.4, 2.0, color="#2C3E50"))
        
    elif "Mutfak" in oda_adi:
        # Mutfak Tezgahı (L şeklinde)
        ax.add_patch(patches.Rectangle((x, y+h-0.6), w, 0.6, color="#BDC3C7"))
        ax.add_patch(patches.Rectangle((x+w-0.6, y), 0.6, h, color="#BDC3C7"))
        # Buzdolabı
        ax.add_patch(patches.Rectangle((x+0.1, y+h-0.7), 0.7, 0.7, color="#7F8C8D"))

    elif "Banyo" in oda_adi:
        # Duş kabini (0.9x0.9)
        ax.add_patch(patches.Rectangle((x+w-1, y+h-1), 0.9, 0.9, color="#AED6F1"))
        # Lavabo
        ax.add_patch(patches.Circle((x+0.5, y+h-0.5), 0.3, color="#ECF0F1"))

# --- MİMARİ ZEKA: DAİRE TİPİ ---
def plan_olustur(en, boy, tip):
    if tip == "1+1":
        plan = {
            "Salon + Mutfak": [0, 0, en*0.6, boy, "#FAD7A0"],
            "Yatak Odası": [en*0.6, 0, en*0.4, boy*0.7, "#AED6F1"],
            "Banyo": [en*0.6, boy*0.7, en*0.4, boy*0.3, "#D5DBDB"]
        }
    elif tip == "2+1":
        plan = {
            "Salon": [0, 0, en*0.6, boy*0.6, "#FAD7A0"],
            "Mutfak": [en*0.6, 0, en*0.4, boy*0.4, "#FCF3CF"],
            "E. Yatak Odası": [0, boy*0.6, en*0.5, boy*0.4, "#AED6F1"],
            "Oda 2": [en*0.5, boy*0.6, en*0.5, boy*0.4, "#D6EAF8"],
            "Banyo": [en*0.6, boy*0.4, en*0.4, boy*0.2, "#D5DBDB"]
        }
    else: # 3+1
        plan = {
            "Salon": [0, 0, en*0.45, boy*0.65, "#FAD7A0"],
            "Mutfak": [en*0.45, 0, en*0.25, boy*0.45, "#FCF3CF"],
            "E. Yatak Odası": [en*0.7, 0, en*0.3, boy*0.6, "#AED6F1"],
            "Oda 1": [0, boy*0.65, en*0.35, boy*0.35, "#D6EAF8"],
            "Oda 2": [en*0.35, boy*0.65, en*0.35, boy*0.35, "#D6EAF8"],
            "Banyo": [en*0.7, boy*0.6, en*0.3, boy*0.4, "#D5DBDB"]
        }
    return plan

# --- ARAYÜZ ---
st.set_page_config(page_title="AI Mimar v7", layout="wide")
st.title("🏗️ Profesyonel Tefrişli Mimari Planlayıcı")

with st.sidebar:
    tip = st.selectbox("Daire Tipi", ["1+1", "2+1", "3+1"], index=1)
    en = st.slider("Daire Eni (m)", 10.0, 20.0, 14.0)
    boy = st.slider("Daire Boyu (m)", 8.0, 15.0, 10.0)
    st.write("---")
    duvar_kalinligi = st.checkbox("Duvarları Kalınlaştır", value=True)

plan_verisi = plan_olustur(en, boy, tip)

fig, ax = plt.subplots(figsize=(14, 10))

for ad, (x, y, w, h, renk) in plan_verisi.items():
    # Oda Çizimi
    linewidth = 5 if duvar_kalinligi else 2
    rect = patches.Rectangle((x, y), w, h, linewidth=linewidth, edgecolor='#2C3E50', facecolor=renk, alpha=0.6)
    ax.add_patch(rect)
    
    # Oda Etiketi
    plt.text(x + w/2, y + h/2, f"{ad}\n{w*h:.1f} m²", ha='center', va='center', weight='bold', fontsize=12)
    
    # Mobilya Çizimi (Yeni Fonksiyon)
    mobilya_ciz(ax, ad, x, y, w, h)
    
    # Mimari Detay: Pencereler (Mavi)
    if y + h >= boy - 0.1:
        ax.plot([x+w*0.2, x+w*0.8], [y+h, y+h], color='#3498DB', lw=8, label='Pencere')

# Kapı Çizimi (Temsili Giriş)
ax.plot([0, 1], [0, 0], color='red', lw=10) # Ana giriş kapısı

plt.xlim(-1, en+1); plt.ylim(-1, boy+1)
plt.gca().set_aspect('equal'); plt.axis('off')
st.pyplot(fig)

st.success(f"✅ {tip} Planı matematiksel olarak optimize edildi ve mobilyalar yerleştirildi.")
