import eval7
# from itertools import combinations


def calculate_equity_multi(hole_cards, board_cards, num_opponents, simulations=10000):
    """
    Monte Carlo-симуляция equity против num_opponents соперников,
    с оценкой силы рук через eval7.evaluate().

    :param hole_cards: list[str], например ['Ah','Kd']
    :param board_cards: list[str], например ['Qs','Jh','2c']
    :param num_opponents: int — число оппонентов
    :param simulations: int — число раундов Monte Carlo
    :return: float — equity (0.0–1.0)
    """
    # 1. Преобразуем входные строки в объекты Card
    hero = [eval7.Card(c) for c in hole_cards]  # :contentReference[oaicite:1]{index=1}
    board = [eval7.Card(c) for c in board_cards]  # :contentReference[oaicite:2]{index=2}

    wins = ties = 0

    for _ in range(simulations):
        # 2. Готовим свежую колоду и убираем известные карты
        deck = eval7.Deck()  # :contentReference[oaicite:3]{index=3}
        for card in hero + board:
            deck.cards.remove(card)

        deck.shuffle()

        # 3. Раздаём n оппонентам по 2 карты
        opponents = [deck.deal(2) for _ in range(num_opponents)]

        # 4. Досдаём борд до 5 карт
        sim_board = board + deck.deal(5 - len(board))

        # 5. Собираем полные руки и оцениваем их
        hero_score = eval7.evaluate(hero + sim_board)  # :contentReference[oaicite:4]{index=4}
        opp_scores = [eval7.evaluate(opp + sim_board) for opp in opponents]  # :contentReference[oaicite:5]{index=5}

        # 6. Считаем, выиграли ли мы
        best = max([hero_score] + opp_scores)
        if hero_score == best:
            # Если есть ровно один минимальный скор — чистая победа
            if ([hero_score] + opp_scores).count(best) == 1:
                wins += 1
            else:
                ties += 1

    # 7. Equity по определению
    return (wins + 0.5 * ties) / simulations
