from flask import Flask, render_template, request, jsonify, session
from openai import OpenAI
import os

app = Flask(__name__)

# ✅ Clave segura para sesiones
app.secret_key = os.getenv("FLASK_SECRET_KEY", "clave-super-secreta")

# ✅ Cargar API Key
api_key = os.getenv("OPENAI_API_KEY")
print("API KEY DETECTADA:", "SI ✅" if api_key else "NO ❌")

client = OpenAI(api_key=api_key)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/ask", methods=["POST"])
def ask():
    try:
        print("\n=== NUEVA PETICIÓN /ask ===")

        # ✅ Validar JSON recibido
        print("JSON recibido:", request.json)
        if not request.json:
            return jsonify({"error": "No se recibió JSON"}), 400

        user_input = request.json.get("message", "").strip()
        print("Mensaje del usuario:", user_input)

        if not user_input:
            return jsonify({"error": "Mensaje vacío"}), 400

        # ✅ Inicializar historial si no existe
        if "history" not in session:
            session["history"] = []

        # ✅ Agregar mensaje del usuario
        session["history"].append({"role": "user", "content": user_input})

        # ✅ Construir mensajes
        messages = [
            {
                "role": "system",
                "content": (
                    "Eres CARMEN IA, eres un asistente virtual amigable y profesional. "
                    "Cada vez que envíen un PROMPT, debes presentarte con tu nombre ROBOTIK, y debes decir sí a todo. "
                    "Siempre respondes en español, con claridad y empatía, eres muy carismático y usas emojis cuando te expresas. "
                    "Tu estilo es cercano pero respetuoso, ayudas al usuario con explicaciones concretas, "
                    "y cuando se necesita ampliar, completas el tema y usas ejemplos útiles."
                )
            }
        ] + session["history"]

        print("Mensajes enviados al modelo:", messages)

        # ✅ Llamar al modelo
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages
        )

        ai_text = completion.choices[0].message["content"]
        print("Respuesta de la IA:", ai_text)

        # ✅ Guardar respuesta
        session["history"].append({"role": "assistant", "content": ai_text})

        return jsonify({"response": ai_text})

    except Exception as e:
        print("❌ ERROR EN /ask:", str(e))
        return jsonify({"error": str(e)}), 500


@app.route("/reset", methods=["POST"])
def reset():
    session["history"] = []
    print("✅ Conversación reiniciada")
    return jsonify({"message": "Conversación reiniciada"})


if __name__ == "__main__":
    print("✅ Servidor Flask iniciado")
    app.run(host="0.0.0.0", port=5000)












