def get_rfi_action(position: str, hole_cards: str) -> str:
    """
    Функция принимает:
        position   — одно из: 'UTG', 'Hijack', 'Cutoff', 'Button', 'SB' или 'BB'.
        hole_cards — строку вида 'AKs', 'AKo', '87s', 'JJ' и т.д.

    Возвращает:
        'Raise' — если рука входит в диапазон открытия (Raise First In) 
                  для данной позиции.
        'Limp'  — (в SB, если рука помечена зелёным).
        'Fold'  — если рука не входит ни в один из диапазонов выше.
    """

    RAISE = {
        'UTG': {
            # Pairs 66+
            'AA','KK','QQ','JJ','TT','99','88','77','66',
            # Suited
            'AKs','AQs','AJs','ATs','A9s','KQs','KJs','KTs',
            'QJs','QTs','JTs','T9s','98s',
            # Offsuit
            'AKo','AQo'
        },
        'HJ': {
            # Pairs 22+
            'AA','KK','QQ','JJ','TT','99','88','77','66','55','44','33','22',
            # Suited
            'AKs','AQs','AJs','ATs','A9s','A8s','A7s','A6s','A5s',
            'A4s','A3s','A2s','KQs','KJs','KTs','K9s','K8s','QJs',
            'QTs','Q9s','JTs','J9s','T9s','T8s','98s','97s','87s',
            '76s','65s','54s',
            # Offsuit
            'AKo','AQo','KQo','AJo','KJo','QJo','ATo'    
        },
        'CO': {
            # Pairs 22+
            'AA','KK','QQ','JJ','TT','99','88','77','66','55','44','33','22',
            # Suited
            'AKs','AQs','AJs','ATs','A9s','A8s','A7s','A6s','A5s',
            'A4s','A3s','A2s','KQs','KJs','KTs','K9s','K8s','K7s',
            'QJs','QTs','Q9s','Q8s','JTs','J9s','J8s','T9s','T8s',
            '98s','97s','87s','86s','76s','75s','65s','64s','54s','43s',
            # Offsuit
            'AKo','AQo','KQo','AJo','KJo','QJo','ATo','KTo','QTo','JTo','A9o'  
        },
        'BTN': {
            # Pairs
            'AA','KK','QQ','JJ','TT','99','88','77','66','55','44','33','22',
            # Suited A
            'AKs','AQs','AJs','ATs','A9s','A8s','A7s','A6s','A5s','A4s','A3s','A2s',
            # Suited K
            'KQs','KJs','KTs','K9s','K8s','K7s','K6s','K5s','K4s','K3s','K2s',
            # Suited Q
            'QJs','QTs','Q9s','Q8s','Q7s','Q6s','Q5s','Q4s','Q3s','Q2s',
            # Suited J
            'JTs','J9s','J8s','J7s','J6s',
            # Suited разное (коннекторы, гапперы и т.д.)
            'T9s','T8s','T7s','T6s','98s','97s','96s','87s','86s','85s',
            '76s','75s','74s','65s','64s','54s','53s','43s','32s',
            # Offsuit Broadways
            'AKo','AQo','AJo','ATo','KQo','KJo','KTo','QJo','QTo','JTo',
            # Другие Offsuit Ax, Kx и коннекторы
            'A9o','A8o','A7o','A6o','A5o','A4o','A3o','A2o',
            'K9o','K8o','K7o','Q9o','Q8o','J9o','J8o','T8o',
            '98o','97o','87o','76o'   
        },
        'SB': {
            'QQ','JJ','TT','99','88','AKs','AQs','AJs','ATs',
            'KQs','KJs','QJs','AQo','AJo','ATo','KQo','KJo',
            # Небольшая часть "блефовых" рук из синих клеток:
            'K3o','K2o','Q5o','Q4o','Q3o','Q2o','J6o','T6o',
            '96o','86o','T5s','95s','85s','J4s','T4s','94s',
            '84s','74s','J3s','63s','53s','43s','J2s' 
        }
    }

    SB_LIMP = {
        # Pairs
        'AA','KK','77','66','55','44','33','22',
        # Suited
        'A9s','A8s','A7s','A6s','A5s','A4s','A3s','A2s',
        'KTs','K9s','K8s','K7s','K6s','K5s','K4s','K3s','K2s',
        'QTs','Q9s','Q8s','Q7s','Q6s','Q5s','Q4s','Q3s','Q2s',
        'JTs','J9s','J8s','J7s','J6s','J5s','T9s','T8s','T7s',
        'T6s','98s','97s','96s','87s','86s','76s','75s','65s',
        '64s','54s','32s',
        # Offsuit
        'AKo','A9o','A8o','A7o','A6o','A5o','A4o','A3o','A2o',
        'KTo','K9o','K8o','K7o','K6o','K5o','K4o',
        'QJo','QTo','Q9o','Q8o','Q7o','Q6o',
        'JTo','J9o','J8o','J7o','T9o','T8o','T7o',
        '98o','97o','87o','76o','65o'
    }

    if hole_cards in RAISE[position]:
            return 'Raise'
    elif position == 'SB' and hole_cards in SB_LIMP:
        return 'Limp'
    else:
        return 'Fold'


def get_facing_rfi_action(your_position: str, rfi_position: str, hole_cards: str) -> str:
    """
    Функция принимает:
        your_position   — одно из: 'Hijack', 'Cutoff', 'Button', 'SB' или 'BB'.
        rfi_position   — одно из: 'UTG', 'Hijack', 'Cutoff', 'Button' или 'SB'
        hole_cards — строку вида 'AKs', 'AKo', '87s', 'JJ' и т.д.

    Возвращает:
        'Raise'
        'Limp'
        'Fold'
    """

    COUNTER_BET = {
        'HJ': {
            'UTG': {
                'AA', 'KK', 'QQ',
                'AKs', 'ATs', 'A5s', 'KJs',
                'AKo', 'AQo'
            }
        },
        'CO': {
            'UTG': {
                'AA', 'KK', 'QQ',
                'AKs', 'AQs', 'A5s', 'A4s',
                'AKo', 'AQo', 'AJo'
            },
            'HJ': {
                'AA', 'KK', 'QQ',
                'AKs', 'AQs', 'AJs', 'A9s', 'A8s', 'A7s', 'A6s', 'A5s',
                'A4s', 'A3s', 'A2s', 'KQs', 'K9s', 'Q9s', 'J9s', '76s',
                '65s', '54s',
                'AKo', 'AQo', 'AJo', 'KQo'
            }
        },
        'BTN': {
            'UTG': {
                'AA', 'KK', 'QQ',
                'AKs', 'A5s', 'A4s', '76s',
                'AKo', 'AQo', 'AJo', 'KQo'
            },
            'HJ': {
                'AA', 'KK', 'QQ',
                'AKs', 'AQs', 'AJs', 'A8s', 'A7s', 'A6s', 'A5s',
                'A4s', 'A3s', 'A2s', '86s', '75s', '65s', '54s',
                'AKo', 'AQo', 'ATo', 'KJo'
            },
            'CO': {
                'AA', 'KK', 'QQ',
                'AKs', 'AQs', 'AJs', 'A8s', 'A7s', 'A6s', 'A3s',
                'A2s', 'K8s', 'Q8s', 'J8s'
                                     '86s', '75s', '65s', '64s', '54s', '43s'
                                                                        'AKo', 'AQo', 'A9o', 'KTo', 'QJo'
            }
        },
        'SB': {
            'UTG': {
                'AA', 'KK', 'QQ', 'AKs', 'A5s', '98s', '87s'
            },
            'HJ': {
                'AA', 'KK', 'QQ', 'AKs', 'AQs', 'A9s', 'A5s',
                'A4s', 'A3s', '76s', '65s', '54s',
                'AKo', 'AJo'
            },
            'CO': {
                'AA', 'KK', 'QQ', 'JJ', 'TT', '99', '88', '77',
                '66', '55', '44', 'AKs', 'AQs', 'AJs', 'ATs',
                'A9s', 'A8s', 'A7s', 'A6s', 'A5s', 'A4s', 'A3s',
                'A2s', 'KQs', 'KJs', 'KTs', 'K9s',
                'QJs', 'QTs', 'Q9s', 'JTs', 'J9s',
                'T9s', '98s', '87s', '76s', '65s', '54s',
                'AKo', 'AQo', 'AJo', 'KQo'
            },
            'BTN': {
                'AA', 'KK', 'QQ', 'JJ', 'TT', '99', '88', '77',
                '66', '55', '44', '33', '22', 'AKs', 'AQs', 'AJs', 'ATs',
                'A9s', 'A8s', 'A7s', 'A6s', 'A5s', 'A4s', 'A3s', 'A2s',
                'KQs', 'KJs', 'KTs', 'K9s', 'QJs', 'QTs', 'Q9s', 'JTs',
                'J9s', 'T9s', 'T8s', '98s', '97s', '87s', '86s', '76s',
                '65s', '54s',
                'AKo', 'AQo', 'AJo', 'ATo', 'KQo', 'KJo', 'QJo'
            }
        },
        'BB': {
            'UTG': {
                'AA', 'KK', 'QQ', 'AKs', 'AQs',
                '86s', '76s', '75s', '65s', '64s', '54s', '43s'
            },
            'HJ': {
                'AA', 'KK', 'QQ', 'JJ', 'TT',
                'AKs', 'AQs', 'AJs', 'KQs',
                '76s', '85s', '75s', '65s', '74s', '64s', '54s',
                '63s', '53s', '43s', '32s',
                'AKo', 'AQo', 'A9o'
            },
            'CO': {
                'AA', 'KK', 'QQ', 'JJ', 'TT',
                'AKs', 'AQs', 'AJs', 'ATs', 'KQs', 'KJs', 'QJs',
                '76s', '85s', '75s', '65s', '84s', '74s', '64s', '54s',
                '73s', '63s', '53s', '43s', '52s', '42s', '32s',
                'AKo', 'AQo', 'AJo', 'KQo', 'A4o', 'A3o'
            },
            'BTN': {
                'AA', 'KK', 'QQ', 'JJ', 'TT', '99',
                'AKs', 'AQs', 'AJs', 'ATs', 'KQs', 'KJs', 'KTs',
                'QJs', 'QTs', 'JTs',
                '76s', '75s', '65s', '74s', '64s', '54s',
                '73s', '63s', '53s', '43s', '52s', '42s', '32s',
                'AKo', 'AQo', 'AJo', 'A3o', 'A2o',
                'KQo', 'K5o', 'K4o', 'K3o', 'K2o', 'Q6o', 'Q5o', '75o', '65o'
            },
            'SB': {
                'AA', 'KK', 'QQ', 'JJ', 'TT', '99',
                'AKs', 'AQs', 'AJs', 'ATs', 'KQs', 'KJs', 'KTs',
                'QJs', 'QTs', 'JTs', 'J9s', 'T9s', 'T8s',
                '98s', '87s', '76s', '65s', '54s',
                'AKo', 'AQo', 'AJo', 'A2o', 'KQo', 'K3o', 'K2o',
                'Q4o', 'Q3o', 'Q2o', 'J5o', 'T5o', '76o', '75o',
                '65o', '64o', '54o'
            }
        }
    }

    CALL = {
        'HJ': {
            'UTG': {
                'JJ', 'TT', '99', '88', '77',
                'AQs', 'AJs', 'KQs', 'QJs', 'JTs', 'T9s'
            }
        },
        'CO': {
            'UTG': {
                'JJ', 'TT', '99', '88', '77', '66',
                'AJs', 'ATs', 'KQs', 'KJs', 'KTs', 'QJs', 'QTs',
                'JTs', 'T9s', '98s'
            },
            'HJ': {
                'JJ', 'TT', '99', '88', '77', '66', '55', '44'
                                                          'ATs', 'KJs', 'KTs', 'QJs', 'QTs', 'JTs', 'T9s',
                '98s', '87s'
            }
        },
        'BTN': {
            'UTG': {
                'JJ', 'TT', '99', '88', '77', '66', '55', '44', '33', '22',
                'AQs', 'AJs', 'ATs', 'KQs', 'KJs', 'KTs', 'QJs', 'QTs',
                'JTs', 'T9s', '98s', '87s'
            },
            'HJ': {
                'JJ', 'TT', '99', '88', '77', '66', '55', '44', '33', '22',
                'ATs', 'A9s', 'KQs', 'KJs', 'KTs', 'K9s', 'QJs', 'QTs', 'Q9s',
                'JTs', 'J9s', 'T9s', 'T8s', '98s', '97s', '87s', '76s', 'AJo'
            },
            'CO': {
                'JJ', 'TT', '99', '88', '77', '66', '55', '44', '33', '22',
                'ATs', 'A9s', 'A5s', 'A4s', 'KQs', 'KJs', 'KTs', 'K9s',
                'QJs', 'QTs', 'Q9s', 'JTs', 'J9s', 'T9s', 'T8s', '98s', '97s', '87s', '76s',
                'AJo', 'ATo', 'KQo', 'KJo'
            }
        },
        'SB': {
            'UTG': {
                'JJ', 'TT', '99', '88', '77',
                'AQs', 'AJs', 'ATs', 'KQs', 'KJs', 'QJs',
                'JTs', 'T9s', 'AKo', 'AQo'
            },
            'HJ': {
                'JJ', 'TT', '99', '88', '77', '66', '55', '44',
                'AJs', 'ATs', 'KQs', 'KJs', 'KTs', 'QJs', 'QTs',
                'JTs', 'T9s', '98s', '87s', 'AQo'
            },
            'CO': {},
            'BTN': {}
        },
        'BB': {
            'UTG': {
                # Pairs
                'JJ', 'TT', '99', '88', '77', '66', '55', '44', '33', '22',
                # Suited
                'AJs', 'ATs', 'A9s', 'A8s', 'A7s', 'A6s', 'A5s', 'A4s', 'A3s', 'A2s',
                'KQs', 'KJs', 'KTs', 'K9s', 'K8s', 'K7s', 'K6s', 'K5s',
                'QJs', 'QTs', 'Q9s', 'Q8s', 'Q7s', 'JTs', 'J9s', 'J8s', 'J7s',
                'T9s', 'T8s', 'T7s', '98s', '97s', '96s', '87s',
                # Offsuit
                'AKo', 'AQo', 'AJo', 'ATo',
                'KQo', 'KJo', 'KTo', 'QJo', 'QTo', 'JTo'
            },
            'HJ': {
                # Pairs
                '99', '88', '77', '66', '55', '44', '33', '22',
                # Suited
                'ATs', 'A9s', 'A8s', 'A7s', 'A6s', 'A5s', 'A4s', 'A3s', 'A2s',
                'KJs', 'KTs', 'K9s', 'K8s', 'K7s', 'K6s', 'K5s', 'K4s', 'K4s', 'K3s', 'K2s',
                'QJs', 'QTs', 'Q9s', 'Q8s', 'Q7s', 'Q6s', 'Q5s', 'Q4s',
                'JTs', 'J9s', 'J8s', 'J7s', 'J6s', 'J5s', 'T9s', 'T8s',
                'T7s', 'T6s', 'T5s', '98s', '97s', '96s', '95s', '87s', '86s'
                # Offsuit
                                                                        'AJo', 'ATo', 'KQo', 'KJo', 'KTo', 'QJo', 'QTo',
                'JTo'
            },
            'CO': {
                # Pairs
                '99', '88', '77', '66', '55', '44', '33', '22',
                # Suited
                'A9s', 'A8s', 'A7s', 'A6s', 'A5s', 'A4s', 'A3s', 'A2s',
                'KTs', 'K9s', 'K8s', 'K7s', 'K6s', 'K5s', 'K4s', 'K3s', 'K2s',
                'QTs', 'Q9s', 'Q8s', 'Q7s', 'Q6s', 'Q5s', 'Q4s',
                'JTs', 'J9s', 'J8s', 'J7s', 'J6s', 'J5s', 'J4s',
                'T9s', 'T8s', 'T7s', 'T6s', 'T5s', 'T4s',
                '98s', '97s', '96s', '95s', '94s', '87s', '86s',
                # Offsuit
                'ATo', 'A9o', 'A8o', 'A5o', 'KJo', 'KTo', 'K9o',
                'QJo', 'QTo', 'Q9o', 'JTo', 'J9o', 'T9o', '98o'
            },
            'BTN': {
                # Pairs
                '88', '77', '66', '55', '44', '33', '22',
                # Suited
                'A9s', 'A8s', 'A7s', 'A6s', 'A5s', 'A4s', 'A3s', 'A2s',
                'K9s', 'K8s', 'K7s', 'K6s', 'K5s', 'K4s', 'K3s', 'K2s',
                'Q9s', 'Q8s', 'Q7s', 'Q6s', 'Q5s', 'Q4s', 'Q3s', 'Q2s',
                'J9s', 'J8s', 'J7s', 'J6s', 'J5s', 'J4s', 'J3s', 'J2s',
                'T9s', 'T8s', 'T7s', 'T6s', 'T5s', 'T4s', 'T3s', 'T2s',
                '98s', '97s', '96s', '95s', '94s', '93s', '92s'
                                                          '87s', '86s', '85s', '84s', '83s', '82s', '72s', '62s',
                # Offsuit
                'ATo', 'A9o', 'A8o', 'A7o', 'A6o', 'A5o', 'A4o',
                'KJo', 'KTo', 'K9o', 'K8o', 'K7o', 'K6o',
                'QJo', 'QTo', 'Q9o', 'Q8o', 'Q7o',
                'JTo', 'J9o', 'J8o', 'J7o', 'J6o',
                'T9o', 'T8o', 'T7o', 'T6o',
                '98o', '97o', '96o', '87o', '86o', '76o'
            },
            'SB': {
                # Pairs
                '88', '77', '66', '55', '44', '33', '22',
                # Suited
                'A9s', 'A8s', 'A7s', 'A6s', 'A5s', 'A4s', 'A3s', 'A2s',
                'K9s', 'K8s', 'K7s', 'K6s', 'K5s', 'K4s', 'K3s', 'K2s',
                'Q9s', 'Q8s', 'Q7s', 'Q6s', 'Q5s', 'Q4s', 'Q3s', 'Q2s',
                'J8s', 'J7s', 'J6s', 'J5s', 'J4s', 'J3s', 'J2s',
                'T7s', 'T6s', 'T5s', 'T4s', 'T3s', 'T2s',
                '97s', '96s', '95s', '94s', '93s', '92s', '86s',
                '85s', '84s', '83s', '82s', '75s', '74s', '73s',
                '72s', '64s', '63s', '62s', '53s', '52s', '43s', '42s', '32s'
                # Offsuit
                                                                        'ATo', 'A9o', 'A8o', 'A7o', 'A6o', 'A5o', 'A4o',
                'A3o',
                'KJo', 'KTo', 'K9o', 'K8o', 'K7o', 'K6o', 'K5o', 'K4o',
                'QJo', 'QTo', 'Q9o', 'Q8o', 'Q7o', 'Q6o', 'Q5o',
                'JTo', 'J9o', 'J8o', 'J7o', 'J6o', 'T9o', 'T8o', 'T7o', 'T6o',
                '98o', '97o', '96o', '87o', '86o'
            }
        }

    }

    if hole_cards in COUNTER_BET[your_position][rfi_position]:
        return 'Counter bet'
    elif hole_cards in CALL[your_position][rfi_position]:
        return 'Call'
    else:
        return 'Fold'


def get_rfi_vs_3bet_action(your_position: str, three_bet_position: str, hole_cards: str) -> str:
    """
    Функция принимает:
        your_position   — одно из: 'Hijack', 'Cutoff', 'Button', 'SB' или 'BB'.
        rfi_position   — одно из: 'UTG', 'Hijack', 'Cutoff', 'Button' или 'SB'
        hole_cards — строку вида 'AKs', 'AKo', '87s', 'JJ' и т.д.

    Возвращает:
        'Raise'
        'Limp'
        'Fold'
    """

    FOUR_BET = {
        'UTG': {
            'HJ': {
                'AA', 'KK', 'QQ',
                'AKs', 'ATs', 'A9s', 'A5s',
                'AKo', 'AQo'
            },
            'CO': {
                'AA', 'KK', 'QQ',
                'AKs', 'A9s', 'A5s', 'KTs', 'QTs', '98s',
                'AKo'
            },
            'BTN': {
                'AA', 'KK', 'QQ',
                'AKs', 'A9s', 'A5s', 'KTs', 'QTs', '98s',
                'AKo'
            },
            'SB': {
                'AA', 'KK', 'QQ',
                'AKs', 'A9s', 'A5s', 'KTs', 'QTs', '98s',
                'AKo'
            },
            'BB': {
                'AA', 'KK', 'QQ',
                'AKs', 'A9s', 'A5s', 'KTs', 'QTs', '98s',
                'AKo'
            }
        },
        'HJ': {
            'CO': {
                'AA', 'KK', 'QQ', 'JJ',
                'AKs', 'A9s', 'A8s', 'A7s', 'A6s',
                'A5s', 'A4s', 'A3s', 'A2s', '76s',
                'AKo', 'ATo', 'KJo'
            },
            'BTN': {
                'AA', 'KK', 'QQ', 'JJ',
                'AKs', 'A9s', 'A8s', 'A7s', 'A6s', 'A5s',
                'A4s', 'A3s', 'A2s', '76s', '65s', '54s',
                'AKo', 'ATo', 'KJo'
            },
            'SB': {
                'AA', 'KK', 'QQ', 'JJ',
                'AKs', 'A9s', 'A8s', 'A7s', 'A6s', 'A5s',
                'A4s', 'A3s', 'A2s', 'AKo', 'ATo', 'KJo'
            },
            'BB': {
                'AA', 'KK', 'QQ', 'JJ',
                'AKs', 'A9s', 'A8s', 'A7s', 'A6s', 'A5s',
                'A4s', 'A3s', 'A2s', 'AKo', 'AJo', 'KQo'
            }
        },
        'CO': {
            'BTN': {
                'AA', 'KK', 'QQ', 'JJ', 'TT',
                'AKs', 'A8s', 'A7s', 'A6s', 'A4s', 'A3s',
                'A2s', '97s', '86s', '75s', '54s',
                'AKo', 'ATo', 'KJo'
            },
            'SB': {
                'AA', 'KK', 'QQ', 'JJ', 'TT',
                'AKs', 'A8s', 'A7s', 'A6s', 'A4s', 'A3s',
                'A2s', '97s', '86s', '75s', '54s',
                'AKo', 'ATo', 'KJo'
            },
            'BB': {
                'AA', 'KK', 'QQ', 'JJ', 'TT',
                'AKs', 'A8s', 'A4s', 'A3s', 'A2s',
                'T8s', '97s', '65s', '54s',
                'AKo', 'ATo', 'KJo'
            }
        },
        'BTN': {
            'SB': {
                'AA', 'KK', 'QQ', 'JJ', 'TT', '99',
                'AKs', 'AQs', 'AJs', 'K6s', 'K5s', 'K4s', 'Q7s',
                'J7s', '86s', '75s', '64s', '54s', '43s', 'AKo',
                'AQo', 'A8o', 'A5o', 'A4o', 'A3o', 'K9o', 'QTo', 'JTo'
            },
            'BB': {
                'AA', 'KK', 'QQ', 'JJ', 'TT', '99',
                'AKs', 'AQs', 'AJs', 'K6s', 'K5s', 'K4s', 'Q7s',
                'J7s', '86s', '75s', '64s', '54s', '43s', 'AKo',
                'AQo', 'A8o', 'A5o', 'A4o', 'A3o', 'K9o', 'QTo', 'JTo'
            }
        },
        'SB': {
            'BB': {
                'AA', 'KK', 'QQ', 'JJ',
                'AKs', 'AQs', 'AJs', 'J4s', 'AKo', 'AQo',
                'A3o', 'A2o', 'K6o', 'K5o', 'K3o', 'K2o',
                'Q7o', 'Q5o', 'Q4o'
            }
        }
    }

    CALL = {
        'UTG': {
            'HJ': {
                'JJ', 'TT', '99', '88', '77',
                'AQs', 'AJs', 'KQs', 'KJs', 'QJs', 'JTs', 'T9s'
            },
            'CO': {
                'JJ', 'TT', '99', '88', '77',
                'AQs', 'AJs', 'ATs', 'KQs', 'KJs', 'QJs', 'JTs', 'T9s', 'AQo'
            },
            'BTN': {
                'JJ', 'TT', '99', '88', '77',
                'AQs', 'AJs', 'ATs', 'KQs', 'KJs', 'QJs', 'JTs', 'T9s', 'AQo'
            },
            'SB': {
                'JJ', 'TT', '99', '88', '77', '66',
                'AQs', 'AJs', 'ATs', 'KQs', 'KJs', 'QJs', 'JTs', 'T9s', 'AQo'
            },
            'BB': {
                'JJ', 'TT', '99', '88', '77', '66',
                'AQs', 'AJs', 'ATs', 'KQs', 'KJs', 'QJs', 'JTs', 'T9s', 'AQo'
            }
        },
        'HJ': {
            'CO': {
                'TT', '99', '88', '77', '66', '55',
                'AQs', 'AJs', 'ATs', 'KQs', 'KJs', 'KTs', 'K9s',
                'QJs', 'QTs', 'Q9s', 'JTs', 'J9s', 'T9s', '98s', '87s',
                'AQo', 'KQo', 'AJo'
            },
            'BTN': {
                'TT', '99', '88', '77', '66', '55', '44',
                'AQs', 'AJs', 'ATs', 'KQs', 'KJs', 'KTs', 'K9s',
                'QJs', 'QTs', 'Q9s', 'JTs', 'J9s', 'T9s', '98s', '87s',
                'AQo', 'KQo', 'AJo'
            },
            'SB': {
                'TT', '99', '88', '77', '66', '55', '44',
                'AQs', 'AJs', 'ATs', 'KQs', 'KJs', 'KTs',
                'K9s', 'QJs', 'QTs', 'Q9s', 'JTs', 'J9s',
                'T9s', '98s', '87s', 'AQo', 'KQo', 'AJo'
            },
            'BB': {
                'TT', '99', '88', '77', '66', '55', '44',
                'AQs', 'AJs', 'ATs', 'KQs', 'KJs', 'KTs',
                'QJs', 'QTs', 'JTs', 'T9s', '98s', '87s', '76s',
                'AQo'
            }
        },
        'CO': {
            'BTN': {
                '99', '88', '77', '66', '55', '44', 'AQs', 'AJs',
                'ATs', 'A9s', 'A5s', 'KQs', 'KJs', 'KTs', 'K9s',
                'QJs', 'QTs', 'Q9s', 'JTs', 'J9s', 'T9s', 'T8s',
                '98s', '87s', '76s', '65s', 'AQo', 'KQo', 'AJo'
            },
            'SB': {
                '99', '88', '77', '66', '55', '44',
                'AQs', 'AJs', 'ATs', 'A9s', 'A5s', 'KQs', 'KJs',
                'KTs', 'K9s', 'QJs', 'QTs', 'Q9s', 'JTs', 'J9s',
                'T9s', 'T8s', '98s', '87s', '76s', '65s', 'AQo',
                'KQo', 'AJo'
            },
            'BB': {
                '99', '88', '77', '66', '55', '44',
                'AQs', 'AJs', 'ATs', 'A9s', 'A5s', 'KQs', 'KJs', 'KTs', 'K9s',
                'QJs', 'QTs', 'Q9s', 'JTs', 'J9s', 'T9s', '98s', '87s', '76s',
                'AQo', 'KQo', 'AJo'
            }
        },
        'BTN': {
            'SB': {
                '88', '77', '66', '55', '44', '33', '22',
                'ATs', 'A9s', 'A8s', 'A7s', 'A6s', 'A5s', 'A4s', 'A3s', 'A2s', 'KQs',
                'KJs', 'KTs', 'K9s', 'K8s', 'K7s', 'QJs', 'QTs', 'Q9s', 'Q8s', 'JTs',
                'J9s', 'J8s', 'T9s', 'T8s', 'T7s', '98s', '97s', '87s', '76s', '65s',
                'AJo', 'ATo', 'A9o', 'KQo', 'KJo', 'KTo', 'QJo'
            },
            'BB': {
                '88', '77', '66', '55', '44', '33', '22',
                'ATs', 'A9s', 'A8s', 'A7s', 'A6s', 'A5s', 'A4s', 'A3s', 'A2s',
                'KQs', 'KJs', 'KTs', 'K9s', 'K8s', 'K7s', 'QJs', 'QTs', 'Q9s',
                'Q8s', 'JTs', 'J9s', 'J8s', 'T9s', 'T8s', 'T7s', '98s', '97s',
                '87s', '76s', '65s', 'AJo', 'ATo', 'A9o', 'KQo', 'KJo', 'KTo', 'QJo'
            }
        },
        'SB': {
            'BB': {
                'TT', '99', '88', '77', '66', '55', '44', '33', '22',
                'ATs', 'A9s', 'A8s', 'A7s', 'A6s', 'A5s', 'A4s', 'A3s', 'A2s', 'KQs',
                'KJs', 'KTs', 'K9s', 'K8s', 'K7s', 'K6s', 'K5s', 'K4s', 'K3s', 'K2s',
                'QJs', 'QTs', 'Q9s', 'Q8s', 'Q7s', 'Q6s', 'Q5s', 'Q4s', 'Q3s', 'Q2s',
                'JTs', 'J9s', 'J8s', 'J7s', 'J6s', 'J5s', 'T9s', 'T8s', 'T7s', 'T6s',
                '98s', '97s', '96s', '95s', '87s', '86s', '85s', '76s', '75s', '74s',
                '65s', '64s', '54s', '43s', '32s', 'AJo', 'ATo', 'A9o', 'A8o', 'A7o',
                'A6o', 'A5o', 'A4o', 'KQo', 'KJo', 'KTo', 'K9o', 'K8o', 'K7o', 'QJo',
                'QTo', 'Q9o', 'Q8o', 'JTo', 'J9o', 'J8o', 'T9o', 'T8o', '98o', '97o',
                '87o', '76o'
            }
        }
    }

    if hole_cards in FOUR_BET[your_position][three_bet_position]:
        return 'Four bet'
    elif hole_cards in CALL[your_position][three_bet_position]:
        return 'Call'
    else:
        return 'Fold'