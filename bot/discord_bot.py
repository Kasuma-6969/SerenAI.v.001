# bot/discord_bot.py
import os
import asyncio
import discord
from discord.ext import commands
from core.brain import CerebroSerena
from core.config import AsistenteConfig

class BotSerena:
    def __init__(self):
        self.config = AsistenteConfig()
        self.cerebro = CerebroSerena(self.config)
        self.token = os.getenv("DISCORD_TOKEN")
        
        intents = discord.Intents.default()
        intents.message_content = True
        intents.voice_states = True
        intents.members = True
        
        self.bot = commands.Bot(command_prefix="!", intents=intents)
        self._configurar_eventos()
    
    def _configurar_eventos(self):
        @self.bot.event
        async def on_ready():
            print(f"✨ {self.config.nombre} lista como {self.bot.user}!")
            print("   📝 Texto y 🎤 Voz activos")
        
        @self.bot.event
        async def on_message(message):
            if message.author == self.bot.user:
                return
            
            texto_limpio = message.content
            for mention in message.mentions:
                texto_limpio = texto_limpio.replace(f"<@{mention.id}>", "").strip()
            
            nombres = ["serena", "serenita", "serenapi", "ser", "sere", "rena"]
            texto_lower = texto_limpio.lower()
            
            debe_responder = False
            es_voz = False
            
            # 1. Mención directa (@Serena)
            if self.bot.user in message.mentions:
                debe_responder = True
            
            # 2. Menciona su nombre (más flexible)
            elif any(nombre in texto_lower for nombre in nombres):
                debe_responder = True
            
            # 3. Es un DM
            elif isinstance(message.channel, discord.DMChannel):
                debe_responder = True
            
            # 4. El mensaje es respuesta a un mensaje de Serena
            elif message.reference and message.reference.message_id:
                try:
                    msg_ref = await message.channel.fetch_message(message.reference.message_id)
                    if msg_ref and msg_ref.author == self.bot.user:
                        debe_responder = True
                except:
                    pass
            
            # 5. Pregunta directa en canal pequeño (menos de 15 miembros)
            elif "?" in texto_limpio and message.guild and len(message.guild.members) <= 15:
                # Palabras que indican que buscan ayuda
                palabras_ayuda = ["alguien", "ayuda", "cómo", "donde", "cuál", "saben", "ideas", "opiniones"]
                if any(p in texto_lower for p in palabras_ayuda):
                    debe_responder = True
            
            palabras_voz = ["habla", "voz", "dime", "cuéntame", "háblame", "di algo"]
            # Solo activa voz si el usuario está en un canal de voz
            if debe_responder and any(p in texto_lower for p in palabras_voz) and message.guild and message.guild.get_member(message.author.id).voice:
                es_voz = True
            
            if debe_responder:
                async with message.channel.typing():
                    texto = texto_limpio
                    if not texto:
                        await message.reply("¡Hola! ✨ Soy Serena. ¿En qué puedo ayudarte? :3")
                        return
                    
                    respuesta = self.cerebro.pensar(texto, str(message.author.id), para_voz=es_voz)
                    
                    # Si es voz, hablar primero y luego enviar texto
                    if es_voz:
                        try:
                            canal = message.author.voice.channel
                            vc = await canal.connect()
                            audio = await self.cerebro.voz.texto_a_audio(respuesta)
                            
                            # Enviar texto breve avisando
                            await message.reply("🎤 *Hablando en voz...*")
                            
                            vc.play(discord.FFmpegPCMAudio(str(audio)))
                            while vc.is_playing():
                                await asyncio.sleep(1)
                            await vc.disconnect()
                            
                            # Enviar texto completo después de hablar
                            if len(respuesta) > 2000:
                                for i in range(0, len(respuesta), 2000):
                                    await message.reply(respuesta[i:i+2000])
                            else:
                                await message.reply(respuesta)
                        except Exception as e:
                            print(f"Error de voz: {e}")
                            # Si falla la voz, envía texto normalmente
                            if len(respuesta) > 2000:
                                for i in range(0, len(respuesta), 2000):
                                    await message.reply(respuesta[i:i+2000])
                            else:
                                await message.reply(respuesta)
                    else:
                        # Solo texto, sin voz
                        if len(respuesta) > 2000:
                            for i in range(0, len(respuesta), 2000):
                                await message.reply(respuesta[i:i+2000])
                        else:
                            await message.reply(respuesta)
        
        @self.bot.command(name="entrar")
        async def entrar(ctx):
            if ctx.author.voice:
                canal = ctx.author.voice.channel
                await canal.connect()
                await ctx.send(f"🎤 Me uní a **{canal.name}**")
            else:
                await ctx.send("Primero entra a un canal de voz :V")
        
        @self.bot.command(name="salir")
        async def salir(ctx):
            if ctx.voice_client:
                await ctx.voice_client.disconnect()
                await ctx.send("👋 ¡Hasta luego!")
            else:
                await ctx.send("No estoy en un canal de voz :^")
        
        @self.bot.command(name="di")
        async def di(ctx, *, texto):
            if ctx.author.voice:
                try:
                    canal = ctx.author.voice.channel
                    vc = await canal.connect()
                    audio = await self.cerebro.voz.texto_a_audio(texto)
                    vc.play(discord.FFmpegPCMAudio(str(audio)))
                    while vc.is_playing():
                        await asyncio.sleep(1)
                    await vc.disconnect()
                except Exception as e:
                    await ctx.send(f"Error: {e}")
            else:
                await ctx.send("Entra a un canal de voz primero :3")
        
        @self.bot.command(name="recuerdos")
        async def recuerdos(ctx, *, consulta=""):
            if not consulta:
                await ctx.send("¿Qué quieres que busque en mi memoria? 🔍")
                return
            resultados = self.cerebro.mlp.buscar_recuerdos(consulta, 5)
            if resultados:
                await ctx.send("🧠 **Recuerdos:**\n" + "\n".join([f"• {r}" for r in resultados]))
            else:
                await ctx.send("No encuentro nada... ¡cuéntame y lo recordaré! :3")
        
        @self.bot.command(name="reflexionar")
        async def reflexionar(ctx):
            async with ctx.typing():
                resultado = self.cerebro.consolidar()
            await ctx.send(f"🌙 {resultado}")
        
        @self.bot.command(name="ayuda")
        async def ayuda(ctx):
            await ctx.send(f"""
🌟 **{self.config.nombre} - Asistente Virtual**

**Texto:** Mencióname (@Serena) o di "Serena"
**Voz:** Agrega "dime", "háblame" o "voz"

**Comandos:**
`!entrar` - Me uno a tu canal de voz
`!salir` - Salgo del canal de voz
`!di <texto>` - Digo algo en voz
`!recuerdos <tema>` - Busco en mi memoria
`!reflexionar` - Reflexiono sobre el día
`!ayuda` - Muestro esto
            """)
    
    def iniciar(self):
        print(f"🚀 Iniciando {self.config.nombre}...")
        self.bot.run(self.token)