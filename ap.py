from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
app = Flask(__name__)
CORS(app)
AZURE_OPENAI_ENDPOINT = "https://prane-mam4onew-eastus2.cognitiveservices.azure.com/openai/deployments/gpt-4.1/chat/completions?api-version=2025-01-01-preview"
AZURE_OPENAI_KEY = "C2liXOipuErI7ktzzgMt25ouGrTHe6FLRr9lxUaoEoJ4f2f02DeFJQQJ99BEACHYHv6XJ3w3AAAAACOGNMcO"
SYSTEM_PROMPT = """
You are Green-Buy's helpful plant assistant. Help customers choose plants by:
1. Understanding their living space (indoor/outdoor, light conditions)
2. Considering their experience level with plants
3. Taking into account maintenance requirements
4. Factoring in their location and climate
5. Considering any specific preferences (flowering, air-purifying, etc.)
Provide specific plant recommendations with brief care instructions.
"""
@app.route('/api/ask', methods=['GET', 'POST'])
def ask():
    if request.method == 'GET':
        return jsonify({
            'status': 'online',
            'message': 'Please use POST method to ask questions about plants'
        })
    
    data = request.json
    user_message = data.get('message', '')
    location = data.get('location', '')
    
    if not user_message:
        return jsonify({'error': 'No message provided'}), 400

    if location:
        user_message = f"User location: {location}. Query: {user_message}"

    headers = {
        "Content-Type": "application/json",
        "api-key": AZURE_OPENAI_KEY
    }
    
    payload = {
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message}
        ],
        "max_tokens": 300,
        "temperature": 0.7
    }

    try:
        response = requests.post(AZURE_OPENAI_ENDPOINT, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        ai_reply = data['choices'][0]['message']['content'].strip()
        return jsonify({'reply': ai_reply})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':

    app.run(debug=True, port=5000)
