import os
from flask import Flask, request, jsonify
from preflop_utils import get_rfi_action, get_facing_rfi_action, get_rfi_vs_3bet_action

app = Flask(__name__)

@app.route('/invoke', methods=['POST'])
def invoke():
    data = request.get_json(force=True)
    result = get_rfi_action(**data)
    return jsonify({'result': result})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
