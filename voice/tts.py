# voice/tts.py
import subprocess
import edge_tts
from core.config import AsistenteConfig

class VozSerena:
    def __init__(self):
        config = AsistenteConfig()
        self.ruta_audio = config.ruta_audio
        self.voz = "es-MX-DaliaNeural"
    
    async def texto_a_audio(self, texto, nombre="respuesta.mp3"):
        """Versión async compatible con Discord"""
        ruta = self.ruta_audio / nombre
        comunicar = edge_tts.Communicate(texto, self.voz)
        await comunicar.save(str(ruta))
        return ruta