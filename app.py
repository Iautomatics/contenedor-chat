from flask import Flask, render_template, request, jsonify, session
from openai import OpenAI
import os

app = Flask(__name__)
app.secret_key = "clave-secreta-super-segura"  # ✅ necesaria para manejar sesiones

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

    # ✅ Inicializar historial en la sesión si no existe
    if "history" not in session:
        session["history"] = []

    try:
        # Agregar mensaje del usuario al historial
        session["history"].append({"role": "user", "content": user_input})

        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": (
                    "Eres Robotik IA, un asistente virtual amigable y profesional. "
                    "Siempre respondes en español, con claridad y empatía, eres muy carismatico, usas emojis cuando te expresas. "
                    "Tu estilo es cercano pero respetuoso, y ayudas al usuario"
                    "con explicaciones concretas pero cuando se necesita ampliar, completas el tema y usas ejemplos cuando es útil."
                )}
            ] + session["history"].append({"role": "user", "content": user_input})
                session["history"].append({"role": "assistant", "content": ai_text})

        )

        ai_text = completion.choices[0].message.content
        # Agregar respuesta de la IA al historial
        session["history"].append({"role": "assistant", "content": ai_text})

        return jsonify({"response": ai_text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
# ✅ Aquí agregas la nueva ruta para reiniciar conversación
@app.route("/reset", methods=["POST"])
def reset():
    session["history"] = []  # limpiar historial de la sesión
    return jsonify({"message": "Conversación reiniciada"})
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

