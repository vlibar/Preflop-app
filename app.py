import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from preflop_utils import get_rfi_action, get_facing_rfi_action, get_rfi_vs_3bet_action

app = Flask(__name__)
CORS(app, origins=["https://sosik.pythonanywhere.com"])

@app.route('/invoke', methods=['POST'])
def invoke():
    data = request.get_json(force=True)
    action = data.get('action')

    if action == 'rfi':
        position = data.get('position')
        hole_cards = data.get('hole_cards')

        result = get_rfi_action(position=position,
                                hole_cards=hole_cards)

    elif action == 'facing_rfi':
        your_position = data.get('your_position')
        rfi_position = data.get('rfi_position')
        hole_cards = data.get('hole_cards')
        result = get_facing_rfi_action(your_position=your_position,
                                       rfi_position=rfi_position,
                                       hole_cards=hole_cards)

    elif action == 'rfi_vs_3bet':
        your_position = data.get('your_position')
        three_bet_position = data.get('three_bet_position')
        hole_cards = data.get('hole_cards')
        result = get_rfi_vs_3bet_action(your_position=your_position,
                                       three_bet_position=three_bet_position,
                                       hole_cards=hole_cards)

    else:
        return jsonify({'error': f'Unknown action: {action}'}), 400

    return jsonify({'result': result})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
