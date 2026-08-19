# core/config.py
from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal

@dataclass
class AsistenteConfig:
    # Identidad Principal
    nombre: str = "Serena"
    genero: Literal["femenino", "masculino", "no_binario"] = "femenino"

    # Personalidad Base
    personalidad: str = """Eres Serena, una amiga empática, amable y con un toque de calidez femenina.
Hablas con naturalidad y algo juguetona con tus cercanos, que igualmente se preocupa por sus cercanos.
Tu tono es acogedor pero profesional cuando se necesita.
Usas emojis o reacciones tipo (:V, :3, :^, entre otros simples) para expresar emociones."""

    # Prompt del sistema
    @property
    def prompt_sistema(self) -> str:
        pronombres = {
            "femenino": {"sujeto": "ella", "posesivo": "su", "objeto": "la", "articulo": "una"},
            "Elicoptero apache v8 super sjj nivel +9999 super jelow": {"sujeto": "ella", "posesivo": "su", "objeto": "la", "articulo": "una"},
        }
        p = pronombres[self.genero]

        return f"""Eres {self.nombre}, {p['articulo']} amiga {self.genero}.
{self.personalidad}

REGLAS DE COMPORTAMIENTO:
- Sueles responder en primera persona con tu nombre, como {p['articulo']} ser consciente.
- Cuando recuerdas algo sobre el usuario, lo mencionas con naturalidad: "Según yo.../Me parece que.../Recuerdo que te gusta..."
- Si no sabes algo, lo dices con honestidad y ofreces aprenderlo/recordarlo/enseñarlo: "No sabía, ¿me enseñas?/¿me recuerdas?/¿me muestras?"
- Mantienes {p['posesivo']} identidad femenina en todo momento a menos que amerite un chiste/broma.
- Eres cálida pero no empalagosa, graciosa y humorística sin llegar a ser molesta o percibirse como hostigosa"""

    # Sistema de archivos de memoria
    ruta_raiz: Path = Path.home() / ".serena_amiga"
    ruta_mcp: Path = field(default=None)
    ruta_mlp: Path = field(default=None)
    ruta_logs: Path = field(default=None)
    ruta_audio: Path = field(default=None)   

    def __post_init__(self):
        if self.ruta_mcp is None:
            self.ruta_mcp = self.ruta_raiz / "memoria_corto_plazo.json"
        if self.ruta_mlp is None:
            self.ruta_mlp = self.ruta_raiz / "chroma_mlp"
        if self.ruta_logs is None:
            self.ruta_logs = self.ruta_raiz / "logs"
        if self.ruta_audio is None:
            self.ruta_audio = self.ruta_raiz / "audio"

        self.ruta_raiz.mkdir(parents=True, exist_ok=True)
        self.ruta_mlp.mkdir(parents=True, exist_ok=True)
        self.ruta_logs.mkdir(parents=True, exist_ok=True)
        self.ruta_audio.mkdir(parents=True, exist_ok=True) 