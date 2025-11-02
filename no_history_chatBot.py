import json
from openai import OpenAI
from dotenv import load_dotenv  # mengimport smua api key dari env
import os

# --- Setup Awal ---
load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

SYSTEM_PROMPT = "You are a helpful assistant."
# 12 pasang (user/assistant) = 24 pesan, ditambah 1 system prompt
MAX_HISTORY = 12 * 2 + 1

history = [
    {"role": "system", "content": SYSTEM_PROMPT}
]

# Variabel baru untuk menyimpan status streaming
streaming_enabled = True

# --- Fungsi Bantuan ---
def print_welcome_message():
    """Mencetak pesan selamat datang dan daftar perintah."""
    print("--- Chatbot AI Terminal (OpenAI) ---")
    print("Commands:")
    print("  /stream on  -> Aktifkan streaming mode (default)")
    print("  /stream off -> Matikan streaming mode (jawab langsung)")
    print("  /save       -> Simpan riwayat chat ke chat_history.json")
    print("  /exit       -> Keluar dari program")
    print("---------------------------------------")

def save_chat_history():
    """Menyimpan list 'history' ke file JSON."""
    try:
        with open("chat_history.json", "w", encoding="utf-8") as f:
            json.dump(history, f, indent=4, ensure_ascii=False)
        print("Bot: Riwayat chat berhasil disimpan ke chat_history.json")
    except Exception as e:
        print(f"Bot: Gagal menyimpan riwayat: {e}")

def trim_history():
    """
    Memangkas riwayat jika melebihi MAX_HISTORY.
    Ini mempertahankan prompt sistem dan (MAX_HISTORY - 1) pesan terbaru.
    """
    global history
    if len(history) > MAX_HISTORY:
        # history[0] adalah system prompt
        # history[-(MAX_HISTORY - 1):] adalah X pesan terbaru
        history = [history[0]] + history[-(MAX_HISTORY - 1):]
        print("\n(Bot: Riwayat chat dipangkas untuk menghemat token.)")

# --- Loop Utama Program ---
def main():
    global streaming_enabled
    global history

    print_welcome_message()

    try:
        while True:
            user_input = input('You: ').strip()

            if not user_input:
                continue

            # --- 1. Penanganan Perintah (Commands) ---
            if user_input.startswith('/'):
                if user_input == '/exit':
                    print("Bot: Sampai jumpa!")
                    break  # Keluar dari loop while

                elif user_input == '/stream on':
                    streaming_enabled = True
                    print("Bot: Streaming mode diaktifkan.")
                    continue  # Kembali ke awal loop

                elif user_input == '/stream off':
                    streaming_enabled = False
                    print("Bot: Streaming mode dimatikan.")
                    continue

                elif user_input == '/save':
                    save_chat_history()
                    continue

                else:
                    print(f"Bot: Perintah '{user_input}' tidak dikenali.")
                    continue

            # --- 2. Jika Bukan Perintah, Proses sebagai Chat ---
            history.append({"role": "user", "content": user_input})

            try:
                # --- Mode Streaming (Default) ---
                if streaming_enabled:
                    print("AI: ", end="", flush=True)
                    
                    # Memanggil API dengan mode streaming
                    response_stream = client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=history,
                        stream=True
                    )

                    full_ai_response = ""
                    for chunk in response_stream:
                        # Dapatkan konten dari 'delta'
                        content = chunk.choices[0].delta.content or ""
                        if content:
                            print(content, end="", flush=True)
                            full_ai_response += content
                    
                    print() # Pindah baris baru setelah selesai stream
                    
                    # Simpan respons lengkap ke riwayat
                    history.append({"role": "assistant", "content": full_ai_response})

                # --- Mode Non-Streaming ---
                else:
                    response = client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=history,
                        stream=False # Eksplisit non-stream
                    )
                    
                    ai_response = response.choices[0].message.content
                    print(f"AI: {ai_response}")
                    
                    # Simpan respons ke riwayat
                    history.append({"role": "assistant", "content": ai_response})

                # --- 3. Manajemen Riwayat ---
                # Panggil fungsi trim SETELAH menambahkan respons AI
                trim_history()

            except Exception as e:
                print(f"\nBot: Terjadi error saat memanggil OpenAI: {e}")
                # Hapus prompt pengguna terakhir jika AI gagal merespons
                if history[-1]["role"] == "user":
                    history.pop()

    except KeyboardInterrupt:
        print("\nBot: Program dihentikan. Sampai jumpa!")

# Menjalankan program
if __name__ == "__main__":
    main()