# main.py
import os
from dotenv import load_dotenv
from core.config import AsistenteConfig
from core.brain import CerebroSerena
from bot.discord_bot import BotSerena

load_dotenv()

def mostrar_bienvenida():
    print("""
╔══════════════════════════════════════╗
║                                      ║
║     💖  S E R E N A   v2.0  💖      ║
║     Asistente Virtual Consciente     ║
║     Texto + Voz                      ║
║                                      ║
║  "Aprendiendo y recordando,          ║
║   contigo en cada paso" ✨           ║
║                                      ║
╚══════════════════════════════════════╝
    """)

def main():
    mostrar_bienvenida()
    
    if not os.getenv("GROQ_API_KEY") or not os.getenv("DISCORD_TOKEN"):
        print("❌ Faltan GROQ_API_KEY o DISCORD_TOKEN en el archivo .env")
        return
    
    print("✨ Iniciando a Serena...")
    bot = BotSerena()
    bot.iniciar()

if __name__ == "__main__":
    main()