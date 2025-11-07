import os
import json
import re
from openai import OpenAI
from dotenv import load_dotenv

# 1. SETUP: Muat .env dan siapkan Klien OpenAI
# ----------------------------------------------------
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY") 

if not OPENAI_API_KEY:
    print("Error: OPENAI_API_KEY tidak ditemukan di .env")
    exit()

client = OpenAI(
    api_key=OPENAI_API_KEY
)

# 2. DEFINISI ALAT (TOOL): Fungsi Kalkulator
# ----------------------------------------------------
def safe_calculate(expression: str):
    """
    Mengevaluasi ekspresi matematika sederhana dengan aman.
    """
    print(f"\n--- Memanggil Alat Kalkulator: safe_calculate('{expression}') ---")
    
    if not re.fullmatch(r"^[0-9\s\+\-\*\/\(\)\.]*$", expression):
        return "Error: Ekspresi mengandung karakter tidak valid."
        
    try:
        result = eval(expression)
        return str(result)
    except ZeroDivisionError:
        return "Error: Tidak bisa membagi dengan nol."
    except Exception as e:
        return f"Error: Ekspresi matematika tidak valid ({e})."

# 3. SKEMA ALAT: 'Resep' untuk AI
# ----------------------------------------------------
tools_list = [
    {
        "type": "function",
        "function": {
            "name": "safe_calculate",
            "description": "Menjalankan kalkulator untuk mengevaluasi ekspresi matematika. Gunakan ini untuk semua perhitungan aritmetika.",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "Ekspresi matematika yang akan dievaluasi, cth: '5 * (10 / 2)'"
                    }
                },
                "required": ["expression"]
            }
        }
    }
]

# 4. LOGIKA UTAMA AGENT
# ----------------------------------------------------
def calculator_agent(user_prompt: str):
    """
    Agen yang dapat memutuskan apakah akan menggunakan kalkulator atau tidak.
    """
    print(f"\n👤 PROMPT PENGGUNA: '{user_prompt}'")
    
    MODEL_AGENT = "gpt-4o-mini" 
    
    messages = [{"role": "user", "content": user_prompt}]
    
    try:
        # === PANGGILAN API PERTAMA ===
        print("🤖 Meminta keputusan dari AI...")
        response = client.chat.completions.create(
            model=MODEL_AGENT,
            messages=messages,
            tools=tools_list,
            tool_choice="auto" 
        )
        
        response_message = response.choices[0].message

        # === EVALUASI KEPUTUSAN AI ===

        # KASUS 1: AI memutuskan untuk memanggil alat
        if response_message.tool_calls:
            print("🤖 Keputusan: Perlu menggunakan kalkulator.")
            
            messages.append(response_message)
            
            for tool_call in response_message.tool_calls:
                function_name = tool_call.function.name
                
                if function_name == "safe_calculate":
                    args = json.loads(tool_call.function.arguments)
                    expression = args.get("expression")
                    
                    tool_result = safe_calculate(expression)
                    
                    messages.append({
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "name": function_name,
                        "content": tool_result
                    })
            
            # === PANGGILAN API KEDUA ===
            print("🤖 Mengirim hasil kalkulator kembali ke AI...")
            final_response = client.chat.completions.create(
                model=MODEL_AGENT,
                messages=messages
            )
            return final_response.choices[0].message.content
        
        # KASUS 2: AI tidak perlu alat (hanya ngobrol)
        else:
            print("🤖 Keputusan: Tidak perlu alat (hanya ngobrol).")
            return response_message.content

    except Exception as e:
        return f"Terjadi error pada API: {e}"

# --- 5. LOOP INTERAKTIF ---
# INI BAGIAN YANG DIUBAH
if __name__ == "__main__":
    print("="*50)
    print("🤖 Selamat Datang di Calculator Agent (Model: gpt-4o-mini)")
    print("Ketik 'exit' atau 'keluar' untuk berhenti.")
    print("="*50)
    
    # Memulai loop tak terbatas untuk chat
    while True:
        # Meminta input dari pengguna
        user_prompt = input("\n👤 Anda: ")
        
        # Opsi untuk keluar dari program
        if user_prompt.lower() in ['exit', 'keluar', 'q']:
            print("🤖 Asisten: Sampai jumpa!")
            break
            
        # Panggil agent dengan input pengguna
        jawaban = calculator_agent(user_prompt)
        
        # Cetak jawaban akhir dari agent
        print(f"\n✅ JAWABAN AKHIR:\n{jawaban}")
        