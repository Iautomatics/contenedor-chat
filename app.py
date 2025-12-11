from flask import Flask, render_template, request, jsonify, session
from openai import OpenAI
import os

app = Flask(__name__)
app.secret_key = "clave-super-secreta"   # necesaria para manejar sesiones

# Configura tu API key desde variables de entorno
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    user_input = request.json.get("message", "").strip()

    if not user_input:
        return jsonify({"error": "Mensaje vacío"}), 400

    # Inicializar historial si no existe
    if "history" not in session:
        session["history"] = []

    try:
        # ✅ Agregar mensaje del usuario al historial
        session["history"].append({"role": "user", "content": user_input})

        # ✅ Construir mensajes para el modelo
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

        # ✅ Llamar al modelo
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages
        )

        # ✅ Obtener texto de la IA
        ai_text = completion.choices[0].message["content"]

        # ✅ Guardar respuesta en el historial
        session["history"].append({"role": "assistant", "content": ai_text})

        return jsonify({"response": ai_text})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ✅ Ruta para reiniciar conversación
@app.route("/reset", methods=["POST"])
def reset():
    session["history"] = []
    return jsonify({"message": "Conversación reiniciada"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)






