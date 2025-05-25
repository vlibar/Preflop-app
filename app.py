import os
import eval7
from flask import Flask, request, jsonify
from flask_cors import CORS
from preflop_utils import get_rfi_action, get_facing_rfi_action, get_rfi_vs_3bet_action
from flop_helper import calculate_equity_multi, generate_range

app = Flask(__name__)
CORS(app, origins=["https://sosik.pythonanywhere.com", "https://play.tonpoker.online"])

@app.route('/preflop', methods=['POST'])
def preflop():
    data = request.get_json(force=True)
    action = data.get('action')

    if action == 'rfi':
        your_position = data.get('your_position')
        hole_cards = data.get('hole_cards')

        result = get_rfi_action(position=your_position,
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
        three_bet_position = data.get('rfi_position')
        hole_cards = data.get('hole_cards')
        result = get_rfi_vs_3bet_action(your_position=your_position,
                                       three_bet_position=three_bet_position,
                                       hole_cards=hole_cards)

    else:
        return jsonify({'error': f'Unknown action: {action}'}), 400

    return jsonify({'result': result})


@app.route('/flop', methods=['POST'])
def flop():
    data = request.get_json(force=True)
    hole_cards = data.get('hole_cards')
    board_cards = data.get('board_cards')
    num_opponents = data.get('num_opponents')

    # 1. Собираем колоду и удаляем известные карты
    deck = eval7.Deck().cards
    for c in hole_cards + board_cards:
        try:
            deck.remove(eval7.Card(c))
        except ValueError:
            return jsonify({'result': 'Ошибка в переданных картах'})

    # 2. Определяем номинальный диапазон
    opponent_range = [
     '22','33','44','55','66','77','88','99','TT','JJ','QQ','KK','AA',
     'A2s','A3s','A4s','A5s','A6s','A7s','A8s','A9s','ATs','AJs','AQs','AKs',
     'K2s','K3s','K4s','K5s','K6s','K7s','K8s','K9s','KTs','KJs','KQs',
     'Q2s','Q3s','Q4s','Q5s','Q6s','Q7s','Q8s','Q9s','QTs','QJs',
     'J6s','J7s','J8s','J9s','JTs',
     'T6s','T7s','T8s','T9s',
     '96s','97s','98s',
     '85s','86s','87s',
     '74s','75s','76s',
     '64s','65s',
     '53s','54s',
     '43s',
     '32s',
     'A2o','A3o','A4o','A5o','A6o','A7o','A8o','A9o','ATo','AJo','AQo','AKo',
     'K7o','K8o','K9o','KTo','KJo','KQo',
     'Q8o','Q9o','QTo','QJo',
     'J8o','J9o','JTo',
     'T8o','T9o',
     '97o','98o',
     '87o',
     '76o'
    ]

    # 3. Генерируем все конкретные комбо в формате [['Ah','Ad'], …]
    opponent_combos = generate_range(deck, opponent_range)

    result = calculate_equity_multi(hero_cards=hole_cards,
                                    board_cards=board_cards,
                                    num_opponents=num_opponents,
                                    opponent_combos=opponent_combos
                                   )
    return jsonify({'result': result})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
