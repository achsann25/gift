import streamlit as st
import json
import os
from datetime import datetime

# 1. DATABASE LOKAL (MENGGUNAKAN JSON)
DB_FILE = "vouchers.json"

# Master Data: 16 Kode Unik (Cetak di kertas) & Hadiahnya (Muncul di Web)
VOUCHER_DICT = {
    "ofslfs": "kamu dapet es krim mcd sayangg, selamat ya",
    "ujwsmf": "asekk dapet es krim walls",
    "rjwfxf": "selamat kamu mendapatkan voucher makan mie ayam",
    "xjsinwn": "kali ini doang nih aku ngasi kretek ke kamu",
    "fpzofson": "selamat, kamu mendapatkan voucher jajan di dadaha, hayuu support umkm",
    "fpzfif": "Selamat kamu mendapatkan kesempatan foto dengan orang keren dan ganteng (aku)",
    "inxnsi": "asekk dapet es krim walls",
    "xfrf": "burger paling enak sejagat dunia raya(lazatto) free for you",
    "pfrz": "WAHHH anda mendapatkan kesempatan untuk video call sama orang keren dan ganteng (aku) ",
    "xjqfrfstd": "SILVERQUEEN FREE FOR YOU"
}

def load_data():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

def save_data(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)

# Inisialisasi State Streamlit
if 'vouchers' not in st.session_state:
    st.session_state.vouchers = load_data()

# 2. KONFIGURASI HALAMAN UTAMA WEB
st.set_page_config(page_title="Semhas Reward Gacha", page_icon="🪙", layout="centered")
st.title("🪙 Seporsi Reward buat pacar tercintah")
st.write("Masukkan kode uniknya di sini bebb biar tau kamu dapet apa, hehehe")

# Membuat Tab Navigasi
tab1, tab2 = st.tabs(["🎁 Redeem Voucher", "🛠️ Dashboard Panitia"])


# --- TAB 1: HALAMAN PACAR (USER) ---
with tab1:
    st.header("Redeem Kode Disini")
    
    with st.form(key="redeem_form", clear_on_submit=True):
        input_code = st.text_input("Masukkan Kode Unik :").strip().lower()
        
        # Di sini kolom tanggal kita buat otomatis menampilkan tanggal hari ini dan dikunci (disabled)
        hari_ini = datetime.today()
        st.date_input("Tanggal Redeem (Otomatis Terkunci):", value=hari_ini, disabled=True)
        
        notes = st.text_area("Catatan Tambahan untuk Pacarmu yang ganteng ini (Opsional):", placeholder="contoh : aku sayang kamu banget banget tapi suka malu mau bilang langsung, jadi ngetik disini aja")
        
        submit_button = st.form_submit_button(label="GASSSS 🚀")
        
        if submit_button:
            # Validasi kode di kamus master data
            if input_code in VOUCHER_DICT:
                # Validasi apakah sudah pernah di-redeem sebelumnya
                already_claimed = any(v["kode_unik"] == input_code for v in st.session_state.vouchers)
                
                if already_claimed:
                    st.error("Yah, kode unik ini sudah pernah kamu klaim sebelumnya! Coba gacha kode lain di toples. 😜")
                else:
                    hadiah_terungkap = VOUCHER_DICT[input_code]
                    waktu_sekarang = datetime.now().strftime("%Y-%m-%d %H:%M")
                    tanggal_saja = datetime.now().strftime("%Y-%m-%d")
                    
                    new_claim = {
                        "id": len(st.session_state.vouchers) + 1,
                        "kode_unik": input_code,
                        "nama_voucher": hadiah_terungkap,
                        "tanggal_rencana": tanggal_saja, # Otomatis mencatat tanggal redeem saat tombol diklik
                        "catatan": notes,
                        "status": "⌛ Pending (Menunggu Ketemu)",
                        "waktu_klaim": waktu_sekarang
                    }
                    
                    st.session_state.vouchers.append(new_claim)
                    save_data(st.session_state.vouchers)
                    
                    # Efek Selebrasi Balon
                    st.balloons()
                    st.success(f"🎉 KODE VALID! : **{hadiah_terungkap}**")
                    st.info("Hadiah sudah otomatis masuk ke daftar antrian, nanti diwujudin pas ketemu!")
            else:
                st.error("Kodenya salah atau gak terdaftar nih. Coba periksa typo atau tulisan di kertasnya lagi !")

    # Tampilkan Riwayat Buku Tabungan Voucher Milik Pacar
    st.subheader("📋 Buku Tabungan Vouchermu")
    if not st.session_state.vouchers:
        st.info("Belum ada voucher yang berhasil di-redeem. Yuk buruan ngerogoh burung hantunya!")
    else:
        for v in st.session_state.vouchers:
            is_pending = "Pending" in v["status"]
            status_color = "orange" if is_pending else "green"
            
            st.markdown(f"""
            ### 🎁 {v['nama_voucher']}
            * **Kode Unik:** `{v['kode_unik']}`
            * **Status Antrean:** :{status_color}[{v['status']}]
            * **Tanggal Di-redeem:** `{v['tanggal_rencana']}`
            * **Catatanmu:** *"{v['catatan'] or '-'}"*
            """)
            st.divider()


# --- TAB 2: HALAMAN ACHSANN (ADMIN) ---
with tab2:
    st.header("(jangan coba-coba masuk disini ya, gabakal bisa juga yee)")
    password = st.text_input("Masukkan Password Panitia:", type="password")
    
    if password == "ajengforlife":
        st.success("Akses diterima! Silakan kelola janji kencanmu, Achsann.")
        
        pending_vouchers = [v for v in st.session_state.vouchers if "Pending" in v["status"]]
        
        st.subheader("📥 Daftar Voucher Menunggu Ketemu")
        if not pending_vouchers:
            st.info("Aman! Semua hutang kencan dan voucher sudah lunas ditunaikan.")
        else:
            for v in pending_vouchers:
                st.write(f"**ID {v['id']} ({v['kode_unik']}):** {v['nama_voucher']}")
                st.write(f"📅 Tanggal Doi Redeem: `{v['tanggal_rencana']}`")
                st.write(f"💬 Catatan doi: *\"{v['catatan'] or '-'}\"*")
                
                # Tombol Aksi Update Status
                if st.button(f"Tandai Selesai (ID {v['id']})", key=f"btn_done_{v['id']}_{v['kode_unik']}"):
                    for index, item in enumerate(st.session_state.vouchers):
                        if item["id"] == v["id"]:
                            st.session_state.vouchers[index]["status"] = "✅ Selesai (Sudah Ketemu)"
                    save_data(st.session_state.vouchers)
                    st.toast(f"Mantap, voucher ID {v['id']} resmi lunas!")
                    st.rerun()
                st.divider()
    elif password != "":
        st.error("Password salah sayanggg! Jangan coba-coba masuk ke sistem akuu. hahahah 🤫")