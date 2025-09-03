# https://developers.deepgram.com/docs/live-streaming-audio
# pip install pyaudio
# pip install deepgram-sdk

"""
Basado en la documentación oficial de Deepgram
Adaptado para usar micrófono en lugar de stream remoto
"""

import pyaudio
import threading
from deepgram import (
    DeepgramClient,
    LiveTranscriptionEvents,
    LiveOptions,
)

API_KEY = "TU_API_KEY_AQUI"

def main():
    try:
        # Crear cliente con tu API Key
        if API_KEY == "TU_API_KEY_AQUI":
            print("❌ Necesitas tu API Key de Deepgram")
            return
            
        deepgram = DeepgramClient(API_KEY)
        
        # Crear conexión websocket
        dg_connection = deepgram.listen.websocket.v("1")
        
        # Función para manejar transcripciones
        def on_message(self, result, **kwargs):
            sentence = result.channel.alternatives[0].transcript
            if len(sentence) == 0:
                return
            if result.is_final:
                print(f"✅ FINAL: {sentence}")
            else:
                print(f"🔄 Parcial: {sentence}", end='\r')
        
        def on_open(self, open, **kwargs):
            print("🎤 ¡Conectado! Empezando a transcribir...")
        
        def on_error(self, error, **kwargs):
            print(f"❌ Error: {error}")
        
        # Registrar eventos
        dg_connection.on(LiveTranscriptionEvents.Transcript, on_message)
        dg_connection.on(LiveTranscriptionEvents.Open, on_open)
        dg_connection.on(LiveTranscriptionEvents.Error, on_error)
        
        # Opciones de transcripción
        options = LiveOptions(
            model="nova-2",
            language="es",
            smart_format=True,
            interim_results=True,
            encoding="linear16",
            sample_rate=16000,
            channels=1
        )
        
        print("🔄 Conectando a Deepgram...")
        print("Presiona Enter para parar la grabación...\n")
        
        # Iniciar conexión
        if dg_connection.start(options) is False:
            print("❌ Falló la conexión")
            return
        
        # Configuración del micrófono
        CHUNK = 1024 * 4
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 16000
        
        # Variables para controlar el hilo
        lock_exit = threading.Lock()
        exit_flag = False
        
        # Función del hilo del micrófono
        def microphone_thread():
            # Inicializar PyAudio
            p = pyaudio.PyAudio()
            
            # Abrir stream del micrófono
            stream = p.open(
                format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK
            )
            
            print("🎤 Micrófono iniciado. ¡Habla!")
            
            try:
                while True:
                    # Verificar si debemos salir
                    lock_exit.acquire()
                    should_exit = exit_flag
                    lock_exit.release()
                    
                    if should_exit:
                        break
                    
                    # Leer datos del micrófono
                    try:
                        data = stream.read(CHUNK, exception_on_overflow=False)
                        # Enviar datos a Deepgram
                        dg_connection.send(data)
                    except Exception as e:
                        print(f"Error leyendo micrófono: {e}")
                        break
                        
            finally:
                # Cerrar stream y PyAudio
                stream.stop_stream()
                stream.close()
                p.terminate()
                print("🔇 Micrófono cerrado")
        
        # Iniciar hilo del micrófono
        mic_thread = threading.Thread(target=microphone_thread)
        mic_thread.start()
        
        # Esperar a que el usuario presione Enter
        input("")
        
        # Señalar que debemos salir
        lock_exit.acquire()
        exit_flag = True
        lock_exit.release()
        
        # Esperar a que termine el hilo del micrófono
        mic_thread.join()
        
        # Cerrar conexión con Deepgram
        dg_connection.finish()
        
        print("✅ Finalizado correctamente")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return

if __name__ == "__main__":
    main()

"""
SÚPER SIMPLE: Transcribir tu archivo test.wav
"""

"""
from deepgram import DeepgramClient, PrerecordedOptions, FileSource

API_KEY = "TU_API_KEY_AQUI"

def transcribir_archivo():
    if API_KEY == "TU_API_KEY_AQUI":
        print("❌ Necesitas tu API Key de https://console.deepgram.com/")
        return

    try:
        print("🔄 Leyendo archivo test.wav...")
        
        # Leer tu archivo local
        with open("test.wav", "rb") as file:
            buffer_data = file.read()

        # Crear cliente Deepgram
        deepgram = DeepgramClient(API_KEY)
        
        # Configuración simple
        options = PrerecordedOptions(
            model="nova-2",      # Modelo más reciente
            language="es",       # Español
            smart_format=True,   # Puntuación automática
        )
        
        print("🔄 Enviando a Deepgram...")
        
        # Transcribir (versión actualizada sin warnings)
        response = deepgram.listen.rest.v("1").transcribe_file(
            {"buffer": buffer_data}, 
            options
        )
        
        # Extraer el texto
        transcript = response.results.channels[0].alternatives[0].transcript
        
        print("\n" + "="*50)
        print("✅ TRANSCRIPCIÓN DE test.wav:")
        print("="*50)
        print(f"📝 {transcript}")
        print("="*50)
        
        # Información adicional
        confidence = response.results.channels[0].alternatives[0].confidence
        print(f"🎯 Confianza: {confidence:.2%}")
        
    except FileNotFoundError:
        print("❌ No encontré el archivo 'test.wav' en esta carpeta")
        print("📁 Archivos en la carpeta actual:")
        import os
        for archivo in os.listdir("."):
            if archivo.endswith((".wav", ".mp3", ".m4a", ".mp4")):
                print(f"   🎵 {archivo}")
                
    except Exception as e:
        print(f"❌ Error: {e}")
        print("💡 Verifica que:")
        print("   1. El archivo test.wav existe")
        print("   2. Tu API Key es correcta")
        print("   3. Tienes internet")

if __name__ == "__main__":
    transcribir_archivo()
"""