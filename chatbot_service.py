from flask import Flask, request, jsonify
import google.generativeai as genai

app = Flask(__name__)

# ✅ Configure Gemini API key
genai.configure(api_key="AIzaSyDTAdsQoLdl0IqnrFLU5PrWMTXRdQz3Pj8")

# ✅ Use a supported and stable model
MODEL_NAME = "models/gemini-2.5-flash"

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")

    if not user_message:
        return jsonify({"response": "Please type something."})

    try:
        model = genai.GenerativeModel(MODEL_NAME)
        response = model.generate_content(user_message)

        reply = response.text.strip() if response.text else "No response from model."
        print("Gemini Reply:", reply)

    except Exception as e:
        print("Gemini error:", e)
        reply = f"Sorry, Gemini service encountered an issue: {e}"

    return jsonify({"response": reply})


if __name__ == "__main__":
    app.run(port=5001)
