import eval7
import itertools
import random
from typing import List, Tuple

def generate_range(deck_cards: List[eval7.Card],
                        nominal_hands: List[str]) -> List[Tuple[str, str]]:
    """
    Генерирует все конкретные комбинации карт из колоды, соответствующие заданным номинальным рукам.

    :param deck_cards: список оставшихся карт (без карт игрока и борда)
    :param nominal_hands: список номиналов, например ['AA', 'AKs', 'AQo', ...]
    :return: список пар строковых представлений карт (e.g. [('Ah', 'Ad'), ('Ah', 'As'), ...])
    """
    combos: List[Tuple[str, str]] = []

    for c1, c2 in itertools.combinations(deck_cards, 2):
        r1, r2 = c1.rank, c2.rank
        s1, s2 = c1.suit, c2.suit

        # Определяем, какая карта старше
        if r1 > r2:
            high, low = c1, c2
        else:
            high, low = c2, c1
        suited = (high.suit == low.suit)

        nominal = str(high)[0] + str(low)[0] + ('s' if suited else 'o')
        if nominal in nominal_hands:
            combos.append((str(high), str(low)))
    return combos


def calculate_equity_multi(
    hero_cards: List[str],
    board_cards: List[str],
    num_opponents: int,
    opponent_combos: List[List[str]],
    simulations: int = 5000,
) -> float:
    """
    Оценивает equity героя против num_opponents оппонентов по Monte-Carlo.

    :param hero_cards: ['Ah', 'Kd']
    :param board_cards: ['Qs', 'Jh', '2c']
    :param num_opponents: число оппонентов
    :param opponent_combos: список всех допустимых рук оппонентов
    :param simulations: число симуляций
    :return: equity (0.0 - 1.0)
    """
    hero = [eval7.Card(c) for c in hero_cards]
    board = [eval7.Card(c) for c in board_cards]

    wins = ties = 0

    for _ in range(simulations):
        deck = eval7.Deck()
        # Удаляем сразу все известные карты
        to_remove = hero + board
        # Выбираем случайные руки оппонентов
        sampled = random.sample(opponent_combos, k=num_opponents)
        opponents = [[eval7.Card(c) for c in hand] for hand in sampled]
        # Добавляем карты оппонентов к списку удаления
        for opp in opponents:
            to_remove.extend(opp)

        # Фильтрация колоды
        deck.cards = [c for c in deck.cards if c not in to_remove]
        deck.shuffle()

        sim_board = board + deck.deal(5 - len(board))

        hero_score = eval7.evaluate(hero + sim_board)
        opp_scores = [eval7.evaluate(opp + sim_board) for opp in opponents]

        all_scores = [hero_score] + opp_scores
        max_score = max(all_scores)
        count_max = all_scores.count(max_score)
        if hero_score == max_score:
            if count_max == 1:
                wins += 1
            else:
                ties += 1
    return (wins + ties * 0.5) / simulations
