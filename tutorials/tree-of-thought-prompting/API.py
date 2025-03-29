# @Author: Bertan Berker
# @Language: Python 3.11.9
# @Description: This is a Flask API implementation for using the tree of thought reasoning

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
from DFS import dfs_reasoning_solver_full_tree

# Initialize Flask app
app = Flask(__name__)

# Enable CORS with more permissive settings for development
CORS(app, 
     resources={r"/api/*": {
         "origins": ["http://localhost:3000"],
         "methods": ["POST", "OPTIONS"],
         "allow_headers": ["Content-Type"],
         "supports_credentials": True
     }})

# Load environment variables
load_dotenv()

@app.route('/api/chat', methods=['POST', 'OPTIONS'])
def chat():
    # Handle preflight requests
    if request.method == 'OPTIONS':
        response = jsonify({'status': 'ok'})
        response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'POST')
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        return response

    try:
        data = request.json
        reasoning_prompt = data.get('message')
        
        if not reasoning_prompt:
            return jsonify({'error': 'No message provided'}), 400

        answer = dfs_reasoning_solver_full_tree(reasoning_prompt)

        response = jsonify({
            'message': answer
        })
        
        # Add CORS headers to the response
        response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        return response, 200

    except Exception as e:
        print(f"Error in /api/chat: {str(e)}")
        error_response = jsonify({'error': str(e)})
        error_response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
        error_response.headers.add('Access-Control-Allow-Credentials', 'true')
        return error_response, 500


if __name__ == '__main__':
    print("Server starting on http://localhost:8000")
    app.run(debug=True, port=8000)