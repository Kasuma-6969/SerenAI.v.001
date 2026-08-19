# memory/mcp.py
from collections import deque
import json
from pathlib import Path
from datetime import datetime

class MemoriaCortoPlazo:
    def __init__(self, max_interacciones=20, ruta_guardado=None):
        self.max = max_interacciones
        self.ruta = ruta_guardado
        self.memoria = deque(maxlen=self.max)
        self.cargar()

    def agregar(self, rol, contenido):
        self.memoria.append({
            "rol": rol, 
            "contenido": contenido, 
            "timestamp": datetime.now().isoformat()
        })
        self.guardar()

    def obtener_contexto(self):
        return list(self.memoria)
    
    def obtener_contexto_texto(self):
        if not self.memoria:
            return "(No se había mencionado nada aún)"
        lineas = []
        for m in self.memoria:
            nombre = "Tú" if m['rol'] == 'usuario' else "Serena"
            lineas.append(f"{nombre}: {m['contenido']}")
        return "\n".join(lineas)

    def guardar(self):
        if self.ruta:
            with open(self.ruta, 'w', encoding='utf-8') as f:
                json.dump(list(self.memoria), f, indent=2, ensure_ascii=False)

    def cargar(self):
        if self.ruta and self.ruta.exists():
            with open(self.ruta, 'r', encoding='utf-8') as f:
                datos = json.load(f)
                self.memoria = deque(datos, maxlen=self.max)