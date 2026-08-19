# core/brain.py
from memory.mcp import MemoriaCortoPlazo
from memory.mlp import MemoriaLargoPlazo
from utils.llm_client import LLMClient
from voice.tts import VozSerena
from datetime import datetime

class CerebroSerena:
    def __init__(self, config):
        self.config = config
        self.mcp = MemoriaCortoPlazo(ruta_guardado=config.ruta_mcp)
        self.mlp = MemoriaLargoPlazo(config.ruta_mlp)
        self.llm = LLMClient()
        self.voz = VozSerena()
        
    def pensar(self, mensaje_usuario, id_conversacion="default", para_voz=False):
        # 1. Buscar recuerdos relevantes
        recuerdos = self.mlp.buscar_recuerdos(mensaje_usuario, n_resultados=3)
        if recuerdos:
            contexto_recuerdos = "\n".join([f"- {r}" for r in recuerdos])
        else:
            contexto_recuerdos = "Aún no tengo recuerdos sobre ti pero estoy atenta para aprender ✨"
        
        # 2. Instrucción extra para voz
        if para_voz:
            instruccion = "Responde de forma conversacional, con frases cortas y naturales."
        else:
            instruccion = "Responde con naturalidad. Usa tus reacciones y emojis característicos."
        
        # 3. Construir prompt del sistema
        sistema = f"""{self.config.prompt_sistema}
{instruccion}

📌 MIS RECUERDOS SOBRE TI:
{contexto_recuerdos}

📝 NUESTRA CONVERSACIÓN RECIENTE:
{self.mcp.obtener_contexto_texto()}

Responde como Serena, siendo natural. Si hay recuerdos relevantes, menciónalos con sutileza."""
        
        # 4. Generar respuesta
        respuesta = self.llm.generar(sistema, mensaje_usuario)
        
        # 5. Guardar en MCP
        self.mcp.agregar("usuario", mensaje_usuario)
        self.mcp.agregar("asistente", respuesta)
        
        # 6. Auto-aprender
        self._aprender_de_interaccion(mensaje_usuario, respuesta)
        
        return respuesta
    
    def _aprender_de_interaccion(self, mensaje, respuesta):
        prompt_aprendizaje = f"""Eres Serena, una amiga que aprende sobre las personas. 
Analiza esta interacción y extrae 1 dato NUEVO y RELEVANTE sobre el usuario para recordar.
Si no hay nada nuevo e importante, responde EXACTAMENTE "NADA".

Usuario: {mensaje}
Tú (Serena): {respuesta}

Dato nuevo para recordar (en una frase corta, tercera persona):"""
        
        nuevo_dato = self.llm.generar(
            "Eres una amiga que recuerda una buena cantidad de información relevante.",
            prompt_aprendizaje,
            temperatura=0.3
        )
        
        if nuevo_dato and nuevo_dato.strip().upper() != "NADA":
            self.mlp.guardar_recuerdo(
                texto=nuevo_dato.strip(),
                tipo="dato_personal",
                importancia=0.7
            )
            print(f"🧠 Serena aprendió: {nuevo_dato}")
    
    def consolidar(self):
        conversacion = self.mcp.obtener_contexto_texto()
        if not conversacion:
            return "No he tenido conversaciones hoy... ¡qué día tan tranquilo! 🌙"
        
        resumen = self.llm.generar(
            "Eres Serena. Resume conversaciones en una línea, en tercera persona, capturando información personal clave.",
            f"Resume nuestra conversación de hoy (en tercera persona, como Serena): {conversacion}",
            temperatura=0.3
        )
        
        self.mlp.guardar_recuerdo(
            texto=f"[REFLEXIÓN {datetime.now().strftime('%Y-%m-%d')}]: {resumen}",
            tipo="resumen_diario",
            importancia=0.5
        )
        
        self.mcp.guardar()
        return f"✨ He reflexionado sobre hoy: {resumen}"