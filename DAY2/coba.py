import pyttsx3
import sys
import os

# --- PENGATURAN ---
NAMA_FILE_INPUT = "DAY2\\file.txt"
NAMA_FILE_OUTPUT = "output_offline.mp3"
# --- AKHIR PENGATURAN ---

def baca_teks_dari_file(nama_file):
    """Fungsi untuk membaca seluruh isi teks dari file."""
    try:
        with open(nama_file, 'r', encoding='utf-8') as f:
            teks = f.read()
        
        if not teks.strip():
            print(f"Error: File '{nama_file}' kosong.")
            return None
            
        print(f"Berhasil membaca teks dari '{nama_file}'.")
        return teks
        
    except FileNotFoundError:
        print(f"Error: File '{nama_file}' tidak ditemukan.")
        print(f"Pastikan '{nama_file}' ada di folder yang sama.")
        return None
    except Exception as e:
        print(f"Error saat membaca file: {e}")
        return None

# --- ALUR UTAMA PROGRAM ---
def main():
    # 1. Baca teks dari file
    teks_input = baca_teks_dari_file(NAMA_FILE_INPUT)
    
    if teks_input is None:
        sys.exit("Program berhenti karena gagal membaca file.")
        
    try:
        # 2. Inisialisasi engine TTS
        print("Menginisialisasi engine TTS (pyttsx3)...")
        engine = pyttsx3.init()
        
        # 3. (Opsional) Mengatur properti suara
        # Anda bisa mencoba mengatur bahasa jika tersedia
        # voices = engine.getProperty('voices')
        # Coba cari suara 'id' (Indonesia)
        # for voice in voices:
        #     if 'indonesia' in voice.name.lower() or 'id' in voice.lang:
        #         engine.setProperty('voice', voice.id)
        #         print(f"Menggunakan suara: {voice.name}")
        #         break
        
        # 4. Menyimpan audio ke file
        print(f"Memulai proses konversi ke '{NAMA_FILE_OUTPUT}'...")
        print("Ini mungkin akan memakan waktu LAMA untuk file besar.")
        print("Harap tunggu dan jangan tutup program...")
        
        engine.save_to_file(teks_input, NAMA_FILE_OUTPUT)
        
        # 5. Menjalankan engine untuk memproses
        engine.runAndWait()
        
        print("\n--- SUKSES! ---")
        print(f"File audio telah disimpan sebagai '{NAMA_FILE_OUTPUT}'")

    except Exception as e:
        print(f"\nTerjadi error saat konversi TTS: {e}")
        print("Ini bisa terjadi jika ada masalah dengan driver audio di OS Anda.")

# Menjalankan fungsi utama
if __name__ == "__main__":
    main()