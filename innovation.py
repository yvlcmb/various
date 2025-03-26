"""Innovation, based on the card game by Carl Chudyk.

code smells:
    stateful modifications in place

not yet implemented:
    dogma action
    end game score calculation
    remaining test functions

some naming conventions for functions:
   transfer_* functions are interactions between two players
   return_* functions are interactions between a player and the draw deck 
"""

import random
from collections import Counter, deque
from pprint import pprint


def create_player(num) -> dict:
    return {
        'number': num + 1,
        'hand': {},
        'board': {
            'red': {'cards': deque(), 'splay': 'none'},
            'yellow': {'cards': deque(), 'splay': 'none'},
            'green': {'cards': deque(), 'splay': 'none'},
            'blue': {'cards': deque(), 'splay': 'none'},
            'purple': {'cards': deque(), 'splay': 'none'},
        },
        'score_pile': [],
        'achievements': [],
    }


COLORS = tuple(create_player(0)['board'].keys())


def meld(player, card) -> bool:
    """meld!
    side effects: mutates player[board] and player[hand] dicts in place
    returns: boolean
         True if success, False if failure
    """
    print('meld!')
    yes = card in player['hand']
    if not yes:
        print(f'The player does not have {card} in hand\n.')
        return False
    card = player['hand'].pop(card)
    color = card.get('color')
    player['board'][color]['cards'].append(card)
    print(f"Player {player['number']} melded {card.get('name')} to their {color} stack\n")
    return True


def splay(player, color, direction) -> bool:
    """splay!
    side effects: mutates player[board] dict in place
    returns: boolean
             True if success, False if failure
    """
    print('splay!')
    board = player.get('board')
    if len(board[color].get('cards', [])) < 2:
        print('cannot splay a single card\n')
        return False
    board[color]['splay'] = direction
    print(f'{player[number]} splayed their {color} cards {direction}\n')
    return True


def tuck(player, cardname) -> bool:
    """tuck!
    side effects: mutates player[board] and player[hand] dicts in place
    returns: boolean
        True if success, False if failure
    """
    print('tuck!')
    if not cardname in player.get('hand'):
        print(f"{cardname} not found in Player {player['number']}'s hand\n")
        return False
    card = player['hand'].pop(cardname)
    color = card.get('color')
    print(color)
    player['board'][color]('cards').appendleft(card)
    print(f"Player {player['number']} tucked {card.get('name')} in their {card.get('color')} stack\n")
    return True


def draw(player, age) -> bool:
    """draw!
    side effects: mutates player[hand], decks dicts in place
    returns: boolean
        True if success, False if decks are empty
    """
    print('draw!')
    while age <= 10:
        if decks.get(age):
            card = decks[age].pop()
            player['hand'].update({card.get('name'): card})
            print(f"Player {player['number']} drew {card.get('name')}\n")
            return True
        else:
            age += 1
    print('Game over!\n')
    return False


def draw_and_score(player, deck) -> int:
    if not decks[deck]:
        return False
    player['score_pile'].append(decks[deck].pop())
    return True


def count_score(player) -> int:
    return sum([card['age'] for card in player['score_pile']])


def get_age(player, func=max) -> int:
    """Find the age on the player's board, defaults to max, can be used with min."""
    func = func or max
    non_empty_colors = [color for color in player['board'] if player['board'][color]['cards']]
    return func(
        (player['board'][color]['cards'][-1]['age'] for color in non_empty_colors), default=0
    )


def achieve(player, age) -> bool:
    """achieve!
    side effects: mutates player[hand], decks dicts in place
    returns: boolean
             True if success, False if failure
    """
    print('achieve!')
    score = count_score(player)
    max_age = get_age(player)
    if all((score >= (age * 5), achievements.get(age), max_age >= age)):
        card = achievements.pop(age)
        player['achievements'].append(card)
        print(f"Player {player['number']} achieved age {age}!\n")
        return True
    else:
        print(f"Player {player['number']} cannot achieve any cards at this time\n")
        return False


def count_icons(player) -> Counter:
    icon_count = Counter()

    for color, data in player['board'].items():
        cards = data.get('cards')
        if not cards:
            continue

        # Count icons from top card
        top_card_icons = [icon for icon in cards[-1]['icons'] if icon]
        icon_count.update(top_card_icons)

        # Handle splayed cards if present
        splay_positions = {'left': [3], 'right': [0, 1], 'up': [1, 2, 3]}.get(data.get('splay'))
        if splay_positions and len(cards) > 1:
            # count the rest of the icons skipping the top card
            # but first must cast the deque to a list b/c deques can't slice
            for card in list(cards)[:-1]:
                icon_count.update([card['icons'][pos] for pos in splay_positions])

    return icon_count


def score_handcard(player, card) -> bool:
    if card not in player['hand']:
        return False
    score = player['hand'].pop(card)
    player['score_pile'].append(score)
    return True


def transfer_handcard(source, target, cardname) -> bool:
    if cardname not in source['hand']:
        print(f"{card} not in player {source['number']}'s hand")
        return False
    card = source['hand'].pop(cardname)
    target['hand'].update({cardname: card})
    print(
        f"Player {source['number']} transfers {card} from their hand to {target['number']}'s hand."
    )
    return True


def top_cards(player) -> list:
    return [cards['cards'][-1] for color, cards in player['board'].items() if cards['cards']]


def transfer_topcard(src, tgt, color) -> bool:
    if not src['board'][color]:
        print(f"Player {src['number']} does not have a top {color} card.")
        return False
    card = src['board'][color]['cards'].pop()
    tgt['board'][color].update({card['name']: card})
    print(f"Player {src['number']} transfers {card} to player {tgt['number']}'s board")
    return True


def hand(player) -> dict:
    """helper function to quickly see what is in hand"""
    data = {color: [] for color in COLORS}
    for card in player['hand'].items():
        data[card[1]['color']].append(card[0])
    return data


def count_cards(plyr) -> dict:
    """helper function to count cards"""
    return Counter({color: len(cards['cards']) for color, cards in plyr['board'].items()})


def score_opponent_topcard(src, tgt, color) -> bool:
    """score an opponent's top card, good for engineering, skyscrapers, etc."""
    match = [card for card in top_cards(tgt) if card['color'] == color]
    if not match:
        print(f"Player {tgt['number']} has no top cards of that color")
        return False
    swipe = tgt['board'][color]['cards'].pop()
    src['score_pile'].append(swipe)
    print(f"Player {src['number']} scored {swipe['name']} from Player {tgt['number']}'s board!")
    return True


def show_dogmas(plyr) -> dict:
    """helper function to show available dogma actions"""
    cards = top_cards(plyr)
    return {card['color']: card['dogma_effects'] for card in cards}


def compare(p1, p2) -> dict:
    """helper function to compare two player's positions at any given game state"""
    p1 = {
        'score': count_score(p1),
        'achievements': len(p1['achievements']),
        'icon_count': count_icons(p1),
        'hand_size': len(p1['hand']),
        'max_age': get_age(p1),
        'stacks': dict(count_cards(p1)),
    }
    p2 = {
        'score': count_score(p2),
        'achievements': len(p2['achievements']),
        'icon_count': count_icons(p2),
        'hand_size': len(p2['hand']),
        'max_age': get_age(p2),
        'stacks': dict(count_cards(p2)),
    }
    return pprint({'player 1': p1, 'player 2': p2})


def transfer_scorecard_by_value(src, tgt, val) -> bool:
    vals = [(idx, crd) for idx, crd in enumerate(src['score_pile']) if crd['age'] == val]
    if not vals:
        return False
    idx, card = random.choice(vals)
    src['score_pile'].pop(idx)
    tgt['score_pile'].append(card)
    return True


def return_card_from_hand(player, card) -> bool:
    if card not in player['hand']:
        print('card not in hand')
        return False
    _card = player['hand'].pop(card)
    age = _card.get('age')
    decks[age].appendleft(_card)
    print(f"Player {player['number']} returns {card} from their hand")
    return True


def return_scored_card_by_age(player, age) -> bool:
    if not player['score_pile']:
        print(f"Player {player['number']} has no cards in their score pile.")
        return False
    choices = [i for i, d in enumerate(player['score_pile']) if d['age'] == age] 
    if not choices:
        print(f"Player {player['number']} has no scored cards from that age")
        return False
    card = player['score_pile'].pop(random.choice(choices))
    decks[age].appendleft(card)
    print(f"Player {player['number']} returned an age {age} card to the deck")
    return True


def return_many_scored_cards(player, card):
    pass


def return_card_from_board(player, card):
    pass


def make_decks():
    age1 = deque()
    age1.extend(
        (
            archery,
            metalworking,
            oars,
            domestication,
            agriculture,
            tools,
            writing,
            pottery,
            clothing,
            sailing,
            wheel,
            city_states,
            codeoflaws,
            mysticism,
        )
    )
    random.shuffle(age1)

    age2 = deque()
    age2.extend(
        (
            construction,
            road_building,
            canal_building,
            fermenting,
            currency,
            mapmaking,
            calendar,
            mathematics,
            monotheism,
            philosophy,
        )
    )
    random.shuffle(age2)

    age3 = deque()
    age3.extend(
        (
            engineering,
            optics,
            machinery,
            medicine,
            compass,
            paper,
            alchemy,
            translation,
            education,
            feudalism,
        )
    )
    random.shuffle(age3)

    age4 = deque()
    age4.extend(
        (
            colonialism,
            gunpowder,
            anatomy,
            invention,
            experimentation,
            printing_press,
            enterprise,
            perspective,
            navigation,
            reformation,
        )
    )
    random.shuffle(age4)

    age5 = deque()
    age5.extend(
        [
            coal,
            pirate_code,
            statistics,
            steam_engine,
            banking,
            measurement,
            chemistry,
            physics,
            astronomy,
            societies,
        ]
    )
    random.shuffle(age5)

    age6 = deque()
    age6.extend(
        (
            industrialization,
            machine_tools,
            canning,
            vaccination,
            classification,
            metric_system,
            atomic_theory,
            encyclopedia,
            democracy,
            emancipation,
        )
    )
    random.shuffle(age6)

    age7 = deque()
    age7.extend(
        (
            lighting,
            publications,
            railroad,
            evolution,
            electricity,
            bicycle,
            sanitation,
            refrigeration,
            explosives,
            combustion,
        )
    )
    random.shuffle(age7)

    age8 = deque()
    age8.extend(
        (
            flight,
            corporations,
            antibiotics,
            quantum_theory,
            mobility,
            empiricism,
            skyscrapers,
            mass_media,
            rocketry,
            socialism,
        )
    )
    random.shuffle(age8)

    age9 = deque()
    age9.extend(
        (
            specialization,
            services,
            genetics,
            computers,
            satellites,
            collaboration,
            suburbia,
            ecology,
            fission,
            composites,
        )
    )
    random.shuffle(age9)

    age10 = deque()
    age10.extend(
        (
            miniaturization,
            robotics,
            globalsization,
            stem_cells,
            databases,
            self_service,
            bioengineering,
            software,
            ai,
            the_internet,
        )
    )
    random.shuffle(age10)

    achievements = {
        1: age1.pop(),
        2: age2.pop(),
        3: age3.pop(),
        4: age4.pop(),
        5: age5.pop(),
        6: age6.pop(),
        7: age7.pop(),
        8: age8.pop(),
        9: age9.pop(),
    }
    decks = {
        1: age1,
        2: age2,
        3: age3,
        4: age4,
        5: age5,
        6: age6,
        7: age7,
        8: age8,
        9: age9,
        10: age10,
    }
    return decks, achievements


def init_two_player():
    players = [create_player(i) for i in range(2)]
    p1 = players[0]
    p2 = players[1]
    draw(p1, 1)
    draw(p2, 1)
    draw(p1, 1)
    draw(p2, 1)
    return p1, p2


# cards
archery = {
    'name': 'Archery',
    'age': 1,
    'color': 'red',
    'icons': ('castle', 'bulb', '', 'castle'),
    'dogma_effects': 'I *demand* you draw a 1. Then transfer the highest card in your hand to my hand!',
    'dogma_icon': 'castle',
}
metalworking = {
    'name': 'Metalworking',
    'age': 1,
    'color': 'red',
    'icons': ('castle', 'castle', '', 'castle'),
    'dogma_effects': ''.join(
        (
            'Draw and reveal a 1. If it has a castle icon, score it and repeat this dogma effect, ',
            'otherwise keep it',
        )
    ),
    'dogma_icon': 'castle',
}
oars = {
    'name': 'Oars',
    'age': 1,
    'color': 'red',
    'icons': ('castle', 'crown', '', 'castle'),
    'dogma_effects': ''.join(
        (
            '1. I *demand* you transfer a card with a crown from your hand to my score pile! ',
            'If you do, draw a 1! ',
            '2. If no cards were transferred due to this demand, draw a 1',
        )
    ),
    'dogma_icon': 'castle',
}
agriculture = {
    'name': 'Agriculture',
    'age': 1,
    'color': 'yellow',
    'icons': ('', 'leaf', 'leaf', 'leaf'),
    'dogma_effects': ''.join(
        (
            'You may return a card from your hand.',
            ' If you do, draw and score a card of value one higher than',
            ' the card you returned.',
        )
    ),
    'dogma_icon': 'leaf',
}
domestication = {
    'name': 'Domestication',
    'age': 1,
    'color': 'yellow',
    'icons': ('castle', 'crown', '', 'castle'),
    'dogma_effects': 'Meld the lowest card in your hand. Draw a 1',
    'dogma_icon': 'castle',
}
masonry = {
    'name': 'Masonry',
    'age': 1,
    'color': 'yellow',
    'icons': ('castle', '', 'castle', 'castle'),
    'dogma_effects': ''.join(
        (
            'You may meld any number of cards from your hand, each with a castle symbol. ',
            'If you melded four or more cards, claim the Monument achievement.',
        )
    ),
    'dogma_icon': 'castle',
}
clothing = {
    'name': 'Clothing',
    'age': 1,
    'color': 'green',
    'icons': ('', 'crown', 'leaf', 'leaf'),
    'dogma_effects': ''.join(
        (
            '1. Meld a card from your hand of a different color than any ',
            'color currently on your board. ',
            '2. Draw and score a 1 for each color present on your board ',
            "not present on any other player's board.",
        )
    ),
    'dogma_icon': 'leaf',
}
sailing = {
    'name': 'Sailing',
    'age': 1,
    'color': 'green',
    'icons': ('crown', 'crown', '', 'leaf'),
    'dogma_effects': 'Draw and meld a 1',
    'dogma_icon': 'crown',
}
wheel = {
    'name': 'The Wheel',
    'age': 1,
    'color': 'green',
    'icons': ('', 'castle', 'castle', 'castle'),
    'dogma_effects': 'Draw two 1s',
    'dogma_icon': 'castle',
}
pottery = {
    'name': 'Pottery',
    'age': 1,
    'color': 'blue',
    'icons': ('', 'leaf', 'leaf', 'leaf'),
    'dogma_effects': ''.join(
        (
            '1. You may return up to three cards from your hand ',
            'If you returned any cards, draw and score a card of value ',
            'equal to the number of cards you returned. ',
            '2. Draw a 1.',
        )
    ),
    'dogma_icon': 'leaf',
}
tools = {
    'name': 'Tools',
    'age': 1,
    'color': 'blue',
    'icons': ('', 'bulb', 'bulb', 'castle'),
    'dogma_effects': ''.join(
        (
            '1. You may return three cards from your hand, if you do draw and meld a 3',
            '2. You may return a 3 from your hand, if you do draw three 1s.',
        )
    ),
    'dogma_icon': 'bulb',
}
writing = {
    'name': 'Writing',
    'age': 1,
    'color': 'blue',
    'icons': ('', 'bulb', 'bulb', 'crown'),
    'dogma_effects': 'Draw a 2',
    'dogma_icon': 'bulb',
}
codeoflaws = {
    'name': 'Code of Laws',
    'age': 1,
    'color': 'purple',
    'icons': ('', 'crown', 'crown', 'leaf'),
    'dogma_effects': ''.join(
        (
            'You may tuck a card from your hand of any color matching a card on your board.',
            ' If you do, splay that color of your cards left',
        )
    ),
    'dogma_icon': 'crown',
}
city_states = {
    'name': 'City States',
    'age': 1,
    'color': 'purple',
    'icons': ('', 'crown', 'crown', 'castle'),
    'dogma_effects': ''.join(
        (
            'I *demand* you transfer a card with a crown on it from your hand to my score pile',
            'if you have at least four castle icons on your board!',
        )
    ),
    'dogma_icon': 'crown',
}
mysticism = {
    'name': 'Mysticism',
    'age': 1,
    'color': 'purple',
    'icons': ('', 'castle', 'castle', 'castle'),
    'dogma_effects': ''.join(
        ('Draw a 1. If it is the same color of any card on your board, meld it. ' 'Draw a 1',)
    ),
    'dogma_icon': 'castle',
}
construction = {
    'name': 'Construction',
    'age': 2,
    'color': 'red',
    'icons': ('castle', '', 'castle', 'castle'),
    'dogma_effects': ''.join(
        (
            '1. I *demand* you transfer two cards from your hand to my hand ',
            'then draw a 2! ',
            '2. If you are the only player with five top cards, claim the Empire achievement',
        )
    ),
    'dogma_icon': 'castle',
}
road_building = {
    'name': 'Road Building',
    'age': 2,
    'color': 'red',
    'icons': ('castle', 'castle', '', 'castle'),
    'dogma_effects': ''.join(
        (
            'Meld one or two cards from your hand. ',
            "If you melded two, you may transfer your top red card to another player's board. ",
            "If you do, transfer that player's top green card to your board.",
        )
    ),
    'dogma_icon': 'castle',
}
canal_building = {
    'name': 'Canal Building',
    'age': 2,
    'color': 'yellow',
    'icons': ('', 'crown', 'leaf', 'crown'),
    'dogma_effects': 'You may exchange all the highest cards in your hand with all the highest card in your score pile',
    'dogma_icon': 'crown',
}
fermenting = {
    'name': 'Fermenting',
    'age': 2,
    'color': 'yellow',
    'icons': ('leaf', 'leaf', '', 'castle'),
    'dogma_effects': 'Draw a 2 for every two leaf icons on your board',
    'dogma_icon': 'leaf',
}
currency = {
    'name': 'Currency',
    'age': 2,
    'color': 'green',
    'icons': ('leaf', 'crown', '', 'crown'),
    'dogma_effects': ''.join(
        (
            'You may return any number of cards from your hand. ',
            'If you do, draw and score a 2 for every different value of card you returned.',
        )
    ),
    'dogma_icon': 'crown',
}
mapmaking = {
    'name': 'Mapmaking',
    'age': 2,
    'color': 'green',
    'icons': ('', 'crown', 'crown', 'castle'),
    'dogma_effects': ''.join(
        (
            '1. I *demand* you transfer a 1 from your score pile, if it has any to my score pile!',
            '2. If any card was transferred due to the demand, draw and score a 1',
        )
    ),
    'dogma_icon': 'crown',
}
calendar = {
    'name': 'Calendar',
    'age': 2,
    'color': 'blue',
    'icons': ('', 'leaf', 'leaf', 'bulb'),
    'dogma_effects': 'If you have have more cards in your score pile than in your hand, draw two 3',
    'dogma_icon': 'leaf',
}
mathematics = {
    'name': 'Mathematics',
    'age': 2,
    'color': 'blue',
    'icons': ('', 'bulb', 'crown', 'bulb'),
    'dogma_effects': ''.join(
        (
            'You may return a card from your hand. ',
            'If you do, draw and meld a card of one value higher than the card you returned.',
        )
    ),
    'dogma_icon': 'bulb',
}
monotheism = {
    'name': 'Monotheism',
    'age': 2,
    'color': 'purple',
    'icons': ('', 'castle', 'castle', 'castle'),
    'dogma_effects': ''.join(
        (
            '1. I *demand* you transfer a top card on your board of a different color ',
            'from any color on my board to my score pile! ',
            '2. Draw and tuck a 1.',
        )
    ),
    'dogma_icon': 'castle',
}
philosophy = {
    'name': 'Philosophy',
    'age': 2,
    'color': 'purple',
    'icons': ('', 'bulb', 'bulb', 'bulb'),
    'dogma_effects': ''.join(
        (
            '1. You may splay left any one color of your cards. ',
            '2. You may score a card from your hand.',
        )
    ),
    'dogma_icon': 'bulb',
}
engineering = {
    'name': 'Engineering',
    'age': 3,
    'color': 'red',
    'icons': ('castle', '', 'bulb', 'castle'),
    'dogma_effects': ''.join(
        (
            '1. I *demand* you transfer all your top cards with a castle icon to my score pile!',
            '2. You may splay your red cards left.',
        )
    ),
    'dogma_icon': 'castle',
}
optics = {
    'name': 'Optics',
    'age': 3,
    'color': 'red',
    'icons': ('crown', 'crown', 'crown', ''),
    'dogma_effects': ''.join(
        (
            'Draw and meld a 3. If it has a crown icon draw and score a 4, ',
            'otherwise transfer a card from your score pile to the score pile of an opponent ',
            'who has fewer points than you',
        )
    ),
    'dogma_icon': 'crown',
}
machinery = {
    'name': 'Machinery',
    'age': 3,
    'color': 'yellow',
    'icons': ('leaf', 'leaf', '', 'castle'),
    'dogma_effects': ''.join(
        (
            '1. I *demand* you exchange all cards in your hand with the highest card in my hand!',
            '2. Score a card from your hand with a castle icon.',
            'You may splay your red cards left',
        )
    ),
    'dogma_icon': 'leaf',
}
medicine = {
    'name': 'Medicine',
    'age': 3,
    'color': 'yellow',
    'icons': ('crown', 'leaf', 'leaf', ''),
    'dogma_effects': ''.join(
        (
            'I *demand* you exchange the highest card in your score pile ',
            'with the lowest card in my score pile!',
        )
    ),
    'dogma_icon': 'leaf',
}
compass = {
    'name': 'Compass',
    'age': 3,
    'color': 'green',
    'icons': ('', 'crown', 'crown', 'leaf'),
    'dogma_effects': ''.join(
        (
            'I *demand* you transfer a top non-green card with leaf icon ',
            'from your board to my board, and then transfer a top card ',
            'wihtout a leaf icon from my board to your board!',
        )
    ),
    'dogma_icon': 'crown',
}
paper = {
    'name': 'Paper',
    'age': 3,
    'color': 'green',
    'icons': ('', 'bulb', 'bulb', 'crown'),
    'dogma_effects': ''.join(
        (
            '1. You may splay your green or blue cards left. ',
            '2. Draw a 4 for every color you have splayed left. ',
        )
    ),
    'dogma_icon': 'bulb',
}
alchemy = {
    'name': 'Alchemy',
    'age': 3,
    'color': 'blue',
    'icons': ('', 'leaf', 'castle', 'castle'),
    'dogma_effects': ''.join(
        (
            '1. Draw and reveala 4 for every three castle icons on your board. ',
            'If any of the drawn cards are red, return the drawn cards and ',
            'all cards in your hand. Otherweise, keep them. ',
            '2. Meld a card from your hand, then score a card from your hand.',
        )
    ),
    'dogma_icon': 'castle',
}
translation = {
    'name': 'Translation',
    'age': 3,
    'color': 'blue',
    'icons': ('', 'crown', 'crown', 'crown'),
    'dogma_effects': ''.join(
        (
            '1. You may meld all the cards in your hand. ',
            'If you meld one you must meld them all. ',
            '2. If each top card on your board has a crown icon ',
            'claim the World achievement.',
        )
    ),
    'dogma_icon': 'crown',
}
education = {
    'name': 'Education',
    'age': 3,
    'color': 'purple',
    'icons': ('bulb', 'bulb', 'bulb', ''),
    'dogma_effects': ''.join(
        (
            'You may return the highest card from your score pile. ',
            'If you do, draw a card of value two higher than the ',
            'highest card remaining in your score pile.',
        )
    ),
    'dogma_icon': 'bulb',
}
feudalism = {
    'name': 'Feudalism',
    'age': 3,
    'color': 'purple',
    'icons': ('', 'castle', 'leaf', 'castle'),
    'dogma_effects': ''.join(
        (
            '1. I *demand* you transfer card with a castle icon from your hand to my score pile!',
            '2. You may splay your yellow or purple cards left',
        )
    ),
    'dogma_icon': 'castle',
}
colonialism = {
    'name': 'Colonialism',
    'age': 4,
    'color': 'red',
    'icons': ('', 'factory', 'bulb', 'factory'),
    'dogma_effects': 'Draw and tuck a 3. If it has a crown icon repeat this dogma effect',
    'dogma_icon': 'factory',
}
gunpowder = {
    'name': 'Gunpowder',
    'age': 4,
    'color': 'red',
    'icons': ('', 'factory', 'crown', 'factory'),
    'dogma_effects': ''.join(
        (
            '1. I *demand* you transfer a top card with a castle icon from your board to ',
            'my score pile!',
            '2. If any card was transferred due to the demand, draw and score a 2.',
        )
    ),
    'dogma_icon': 'factory',
}
anatomy = {
    'name': 'Anatomy',
    'age': 4,
    'color': 'yellow',
    'icons': ('leaf', 'leaf', 'leaf', ''),
    'dogma_effects': ''.join(
        (
            'I *demand* you return a card from your score pile!',
            ' If you do return a top card from your board of equal value!',
        )
    ),
    'dogma_icon': 'leaf',
}
invention = {
    'name': 'Invention',
    'age': 4,
    'color': 'green',
    'icons': ('', 'bulb', 'bulb', 'factory'),
    'dogma_effects': ''.join(
        (
            'You may spay right any color of your cards currently splayed left ',
            'if you do, draw and score a 4. '
            'If you have five top cards splayed in any direction, claim the Wonder achievement',
        )
    ),
    'dogma_icon': 'bulb',
}
experimentation = {
    'name': 'Experimentation',
    'age': 4,
    'color': 'blue',
    'icons': ('', 'bulb', 'bulb', 'bulb'),
    'dogma_effects': 'Draw and meld a 5.',
    'dogma_icon': 'bulb',
}
printing_press = {
    'name': 'Printing Press',
    'age': 4,
    'color': 'blue',
    'icons': ('', 'bulb', 'bulb', 'crown'),
    'dogma_effects': ''.join(
        (
            'You may return a card from yur score pile. If you do, draw a card of value two higher than ',
            'the highest card remaining in your score pile. ',
            'You may splay your blue cards right.',
        )
    ),
    'dogma_icon': 'bulb',
}
enterprise = {
    'name': 'Enterprise',
    'age': 4,
    'color': 'purple',
    'icons': ('', 'crown', 'crown', 'crown'),
    'dogma_effects': ''.join(
        (
            '1. I *demand* you transfer a top non-puprle card with a crown icon from your board to my board!',
            ' If you do, draw and meld a 4!',
            ' 2. You may splay your green cards right.',
        )
    ),
    'dogma_icon': 'crown',
}
perspective = {
    'name': 'Perspective',
    'age': 4,
    'color': 'yellow',
    'icons': ('', 'bulb', 'bulb', 'leaf'),
    'dogma_effects': ''.join(
        (
            'You may return a card from your hand. ',
            'If you do, score a card from your hand for every two bulb icons on your board',
        )
    ),
    'dogma_icon': 'bulb',
}
navigation = {
    'name': 'Navigation',
    'age': 4,
    'color': 'green',
    'icons': ('', 'crown', 'crown', 'crown'),
    'dogma_effects': 'I demad you transfer a 2 or 3 from your score pile, if it has any, to my score pile!',
    'dogma_icon': 'crown',
}
reformation = {
    'name': 'Reformation',
    'age': 4,
    'color': 'purple',
    'icons': ('leaf', 'leaf', '', 'leaf'),
    'dogma_effects': ''.join(
        (
            '1. You may tuck a card from your hand for every two leaf icons on your board ',
            '2. You may splay your yellow or purple cards right',
        )
    ),
    'dogma_icon': 'crown',
}
coal = {
    'name': 'Coal',
    'age': 5,
    'color': 'red',
    'icons': ('factory', 'factory', 'factory', ''),
    'dogma_effects': ''.join(
        (
            '1. Draw and tuck a 1. ',
            '2. You may splay your red cards right. ',
            '3. You may score any one of your top cards. If you do score the card beneath it also.',
        )
    ),
    'dogma_icon': 'factory',
}
pirate_code = {
    'name': 'The Pirate Code',
    'age': 5,
    'color': 'red',
    'icons': ('crown', 'factory', 'crown', ''),
    'dogma_effects': ''.join(
        (
            '1. I *demand* you transfer two cards of value 4 or less from your score pile to my score pile! ',
            '2. If any card was transferred due to the demand, score the lowest top card with a crown icon '
            'from your board.',
        )
    ),
    'dogma_icon': 'crown',
}
statistics = {
    'name': 'Statistics',
    'age': 5,
    'color': 'green',
    'icons': ('leaf', 'bulb', 'leaf', ''),
    'dogma_effects': ''.join(
        (
            '1. I *demand* you transfer the highest card in your score pile to your hand!',
            ' if you do, and have only one card in your hand afterwards, repeat this demand.',
            ' 2. You may splay your yellow cards right.',
        )
    ),
    'dogma_icon': 'bulb',
}
steam_engine = {
    'name': 'Steam Engine',
    'age': 5,
    'color': 'yellow',
    'icons': ('', 'factory', 'crown', 'factory'),
    'dogma_effects': 'Draw and tuck two 4s, then score your bottom yellow card',
    'dogma_icon': 'factory',
}
banking = {
    'name': 'Banking',
    'age': 5,
    'color': 'green',
    'icons': ('factory', 'crown', '', 'crown'),
    'dogma_effects': ''.join(
        (
            '1. I *demand* you transfer a top card with a factory icon from your board to my board! ',
            'If you do, draw and score a 5!',
            '2. You may splay your green cards right',
        )
    ),
    'dogma_icon': 'crown',
}
measurement = {
    'name': 'Measurement',
    'age': 5,
    'color': 'green',
    'icons': ('bulb', 'leaf', 'bulb', ''),
    'dogma_effects': ''.join(
        (
            'You may return a card from your hand. ',
            'If you do splay that color of your cards right, ',
            'and draw a card of value equal to the number of cards ',
            'of that color on your board.',
        )
    ),
    'dogma_icon': 'bulb',
}
chemistry = {
    'name': 'Chemistry',
    'age': 5,
    'color': 'blue',
    'icons': ('factory', 'bulb', 'factory', ''),
    'dogma_effects': ''.join(
        (
            '1. You may splay your blue cards right. ',
            '2. Score a card from your hand of value one higher than the highest '
            'card in your score pile, then return a card from your score pile.',
        )
    ),
    'dogma_icon': 'factory',
}
physics = {
    'name': 'Physics',
    'age': 5,
    'color': 'blue',
    'icons': ('factory', 'bulb', 'bulb', ''),
    'dogma_effects': ''.join(
        (
            'Draw three 6s and reveal them. ',
            'If two or more of the drawn cards are the same color',
            ' return them and all cards in your hand.',
            ' Otherwise, keep them.',
        )
    ),
    'dogma_icon': 'bulb',
}
astronomy = {
    'name': 'Astronomy',
    'age': 5,
    'color': 'purple',
    'icons': ('crown', 'bulb', 'bulb', ''),
    'dogma_effects': ''.join(
        (
            '1. Draw a 6. If the card is green or blue, meld it and repeat this dogma effect. ',
            '2. If all non-puprle cards on your board are value 6 or higher, ',
            'claim the Universe achievement',
        )
    ),
    'dogma_icon': 'bulb',
}
societies = {
    'name': 'Societies',
    'age': 5,
    'color': 'purple',
    'icons': (
        'crown',
        'bulb',
        '',
        'crown',
    ),
    'dogma_effects': ''.join(
        (
            'I *demand* you transfer a top non-puprle card with a bulb icon ',
            'from your board to my board! If you do, draw a 5!',
        )
    ),
    'dogma_icon': 'crown',
}
industrialization = {
    'name': 'Industrialization',
    'age': 6,
    'color': 'red',
    'icons': ('crown', 'factory', 'factory', ''),
    'dogma_effects': ''.join(
        (
            '1. Draw and tuck a 6 for every two factory icons on your board',
            '2. You may splay your red or purple cards right',
        )
    ),
    'dogma_icon': 'factory',
}
machine_tools = {
    'name': 'Machine Tools',
    'age': 6,
    'color': 'red',
    'icons': ('factory', 'factory', '', 'factory'),
    'dogma_effects': 'Draw and score a card of value equal to the highest card in your score pile.',
    'dogma_icon': 'factory',
}
canning = {
    'name': 'Canning',
    'age': 6,
    'color': 'yellow',
    'icons': ('', 'factory', 'leaf', 'factory'),
    'dogma_effects': ''.join(
        (
            '1. You may draw and tuck a 6. If you do, score all your top cards without a factory',
            '2. You may play your yellow cards right',
        )
    ),
    'dogma_icon': 'factory',
}
vaccination = {
    'name': 'Vaccination',
    'age': 6,
    'color': 'yellow',
    'icons': ('leaf', 'factory', 'leaf', ''),
    'dogma_effects': ''.join(
        (
            '1. I *demand* you return all the lowest cards in your score pile! ',
            'If you returned any, draw and meld a 5! ',
            '2. If any card was returned as a result of the demand, draw and meld a 7.',
        )
    ),
    'dogma_icon': 'leaf',
}
classification = {
    'name': 'Classification',
    'age': 6,
    'color': 'green',
    'icons': ('bulb', 'bulb', 'bulb', ''),
    'dogma_effects': ''.join(
        (
            'Reveal the color of a card from your hand. Take into your hand ',
            'all cards of that color from all other '
            "player's hands. Then, meld all cards of that color from your hand.",
        )
    ),
    'dogma_icon': 'bulb',
}
metric_system = {
    'name': 'Metric System',
    'age': 6,
    'color': 'green',
    'icons': ('', 'factory', 'crown', 'crown'),
    'dogma_effects': ''.join(
        (
            '1. If your green cards are splayed right, you may splay any color of your cards right',
            '2. You may splay your green cards right',
        )
    ),
    'dogma_icon': 'bulb',
}
atomic_theory = {
    'name': 'Atomic Theory',
    'age': 6,
    'color': 'blue',
    'icons': ('bulb', 'bulb', 'bulb', ''),
    'dogma_effects': 'Draw and meld a 7.',
    'dogma_icon': 'bulb',
}
encyclopedia = {
    'name': 'Encyclopedia',
    'age': 6,
    'color': 'blue',
    'icons': ('', 'crown', 'crown', 'crown'),
    'dogma_effects': ''.join(
        (
            'You may meld all the highest cards in your score pile. ',
            'If you meld one of the highest, you must meld all of the highest.',
        )
    ),
    'dogma_icon': 'crown',
}
democracy = {
    'name': 'Democracy',
    'age': 6,
    'color': 'purple',
    'icons': ('crown', 'bulb', 'bulb'),
    'dogma_effects': ''.join(
        (
            'You may return any number of cards from your hand. ',
            'If you have returned more cards than any other player '
            'due to Democracy this phase, draw and score an 8.',
        )
    ),
    'dogma_icon': 'bulb',
}
emancipation = {
    'name': 'Emancipation',
    'age': 6,
    'color': 'purple',
    'icons': ('factory', 'bulb', 'factory', ''),
    'dogma_effects': ''.join(
        (
            '1. I *demand* you transfer a card from your hand to my score pile!',
            ' if you do, draw a 6.',
            '2.You may splay your red or purple cards right',
        )
    ),
    'dogma_icon': 'factory',
}
combustion = {
    'name': 'Combustion',
    'age': 7,
    'color': 'red',
    'icons': ('crown', 'crown', 'factory', ''),
    'dogma_effects': 'I *demand* you transfer two cards from your score pile to my score pile!',
    'dogma_icon': 'crown',
}
explosives = {
    'name': 'Explosives',
    'age': 7,
    'color': 'red',
    'icons': ('', 'factory', 'factory', 'factory'),
    'dogma_effects': ''.join(
        (
            'I *demand* you transfer the three highest cards from your hand to my hand! ',
            'If you transferred any, and then have no scard in hand, draw a 1!',
        )
    ),
    'dogma_icon': 'factory',
}
refrigeration = {
    'name': 'Refrigeration',
    'age': 7,
    'color': 'yellow',
    'icons': ('', 'leaf', 'leaf', 'crown'),
    'dogma_effects': ''.join(
        (
            '1. I *demand* you return half (rounded down) of all the cards in your hand! ',
            '2. You may score a card from your hand.',
        )
    ),
    'dogma_icon': 'factory',
}
sanitation = {
    'name': 'Sanitation',
    'age': 7,
    'color': 'yellow',
    'icons': ('leaf', 'leaf', '', 'leaf'),
    'dogma_effects': ''.join(
        (
            'I *demand* you exchange the two highest cards in your hand ',
            'with the lowest card in my hand!',
        )
    ),
    'dogma_icon': 'leaf',
}
bicycle = {
    'name': 'Bicycle',
    'age': 7,
    'color': 'green',
    'icons': ('crown', 'crown', 'clock', ''),
    'dogma_effects': ''.join(
        (
            'You may exchange all teh cards in your hand with all the cards in your core pile.',
            ' If you exchange one, you must exchange them all.',
        )
    ),
    'dogma_icon': 'crown',
}
electricity = {
    'name': 'Electricity',
    'age': 7,
    'color': 'green',
    'icons': ('bulb', 'factory', '', 'factory'),
    'dogma_effects': 'Return all your top cards without a factory icon, then draw an 8 for each card your returned',
    'dogma_icon': 'factory',
}
evolution = {
    'name': 'Evolution',
    'age': 7,
    'color': 'blue',
    'icons': ('bulb', 'bulb', 'bulb', ''),
    'dogma_effects': ''.join(
        (
            'You may choose to either draw and score an 8 and then ',
            'return a card from your score pile, or sraw a card of '
            'value one higher than the highest card in your score pile. ',
        )
    ),
    'dogma_icon': 'bulb',
}
publications = {
    'name': 'Publications',
    'age': 7,
    'color': 'blue',
    'icons': ('', 'bulb', 'clock', 'bulb'),
    'dogma_effects': ''.join(
        (
            '1. You may rearrange the order of one color of cards on your board. ',
            '2. You may splay your yellow or blue cards up.',
        )
    ),
    'dogma_icon': 'bulb',
}
lighting = {
    'name': 'Lighting',
    'age': 7,
    'color': 'purple',
    'icons': ('', 'leaf', 'clock', 'leaf'),
    'dogma_effects': ''.join(
        (
            'You may tuck up to three cards from your hand. '
            'If you do, draw and score a 7 for every different value of card you tucked.',
        )
    ),
    'dogma_icon': 'leaf',
}
railroad = {
    'name': 'Railroad',
    'age': 7,
    'color': 'purple',
    'icons': ('clock', 'factory', 'clock', ''),
    'dogma_effects': ''.join(
        (
            '1. Return all cards from your hand, then draw three 6s. ',
            '2, You may splay up any one color of your cards currently splayed right.',
        )
    ),
    'dogma_icon': 'clock',
}
flight = {
    'name': 'Flight',
    'age': 8,
    'color': 'red',
    'icons': ('crown', '', 'clock', 'crown'),
    'dogma_effects': ''.join(
        (
            '1) If your red cards are splayed up you may splay any other color of cards up.',
            '2) You may splay your red cards up',
        )
    ),
    'dogma_icon': 'crown',
}
antibiotics = {
    'name': 'Antibiotics',
    'age': 8,
    'color': 'green',
    'icons': ('leaf', 'leaf', 'leaf', ''),
    'dogma_effects': ''.join(
        (
            'You may return up to three cards from your hand. '
            'For every different value of card that you returned, draw two 8s.',
        )
    ),
    'dogma_icon': 'leaf',
}
corporations = {
    'name': 'Corporations',
    'age': 8,
    'color': 'green',
    'icons': ('', 'factory', 'factory', 'crown'),
    'dogma_effects': ''.join(
        (
            '1. I *demand* you transfer a top non-green card with a factor icon ',
            'from your board to my score pile! ',
            'If you do, draw and meld an 8!' '2. Draw and meld an 8.',
        )
    ),
    'dogma_icon': 'factory',
}
quantum_theory = {
    'name': 'Quantum Theory',
    'age': 8,
    'color': 'blue',
    'icons': ('clock', 'clock', 'clock', ''),
    'dogma_effects': ''.join(
        (
            'You may return 1 or 2 cards from your hand. ',
            'If you returned two, draw a 10, then draw and score a 10',
        )
    ),
    'dogma_icon': 'clock',
}
empiricism = {
    'name': 'Empiricism',
    'age': 8,
    'color': 'purple',
    'icons': ('bulb', 'bulb', 'bulb', ''),
    'dogma_effects': ''.join(
        (
            '1. Choose two colors then draw a 9.',
            ' If it is either of the colors you chose, meld it',
            ' and you may splay that color of your cards up.',
            '2. If you have twenty or more light bulb icons on your board, you win',
        )
    ),
    'dogma_icon': 'bulb',
}
mobility = {
    'name': 'Mobility',
    'age': 8,
    'color': 'red',
    'icons': ('', 'factory', 'clock', 'factory'),
    'dogma_effects': ''.join(
        (
            'I *demand* you transfer the two highest non-red top cards without a ',
            'factory icon from your board to my score pile! '
            'If you transferred any cards, draw an 8!',
        )
    ),
    'dogma_icon': 'factory',
}
skyscrapers = {
    'name': 'Skyscrapers',
    'age': 8,
    'color': 'yellow',
    'icons': ('', 'factory', 'crown', 'crown'),
    'dogma_effects': ''.join(
        (
            'I *demand* you transfer a top non-yellow card with a clock icon from your board to my board! ',
            'If you do, score the card beneath it, then return all cards of that color!',
        )
    ),
    'dogma_icon': 'crown',
}
mass_media = {
    'name': 'Mass Media',
    'age': 8,
    'color': 'green',
    'icons': ('bulb', '', 'clock', 'bulb'),
    'dogma_effects': ''.join(
        (
            '1. You may return a card from your hand. If you do, choose a value and '
            'return all cards of that value from all score piles. ',
            '2. You may splay your purple cards up',
        )
    ),
    'dogma_icon': 'bulb',
}
rocketry = {
    'name': 'Rocketry',
    'age': 8,
    'color': 'blue',
    'icons': ('clock', 'clock', 'clock', ''),
    'dogma_effects': "Return a card in any other player's score pile for every two clock icons on your board",
    'dogma_icon': 'clock',
}
socialism = {
    'name': 'Socialism',
    'age': 8,
    'color': 'purple',
    'icons': ('leaf', '', 'leaf', 'leaf'),
    'dogma_effects': ''.join(
        (
            'You may tuck all the cards from your hand. If you tuck one, you must ',
            'tuck them all. If you tucked at least one purple card, take all the '
            "lowest cards in each other player's hand into your hand.",
        )
    ),
    'dogma_icon': 'leaf',
}
composites = {
    'name': 'Composites',
    'age': 9,
    'color': 'red',
    'icons': ('factory', 'factory', '', 'factory'),
    'dogma_effects': ''.join(
        (
            'I *demand* you transfer all but one card from your hand to my hand! ',
            'Also transfer the highest card from your score pile to my score pile!',
        )
    ),
    'dogma_icon': 'factory',
}
fission = {
    'name': 'Fission',
    'age': 9,
    'color': 'red',
    'icons': ('', 'clock', 'clock', 'clock'),
    'dogma_effects': ''.join(
        (
            '1. I *demand* you draw a 10! ',
            'If it is red, remove all hands, boards, and score piles from the game! ',
            'If this occurs the dogma action is complete. ',
            "2. Return a top card other than Fission from any other player's board",
        )
    ),
    'dogma_icon': 'clock',
}
ecology = {
    'name': 'Ecology',
    'age': 9,
    'color': 'green',
    'icons': ('leaf', 'bulb', 'bulb', ''),
    'dogma_effects': ''.join(
        (
            'You may return a card from your hand. If you do score a card ',
            'from your hand and draw two 10s.',
        )
    ),
    'dogma_icon': 'bulb',
}
suburbia = {
    'name': 'Suburbia',
    'age': 9,
    'color': 'yellow',
    'icons': ('', 'crown', 'leaf', 'leaf'),
    'dogma_effects': 'You may tuck any number of cards from your hand. Draw and score a 1 for each card you tucked',
    'dogma_icon': 'leaf',
}
collaboration = {
    'name': 'Collaboration',
    'age': 9,
    'color': 'green',
    'icons': ('', 'crown', 'clock', 'crown'),
    'dogma_effects': ''.join(
        (
            '1. I *demand* you draw two 9 and reveal them!',
            ' Transfer the card of my choice to my board and meld the other!',
            '2. If you have ten or more green cards on your board, you win',
        )
    ),
    'dogma_icon': 'bulb',
}
satellites = {
    'name': 'Satellites',
    'age': 9,
    'color': 'green',
    'icons': ('', 'clock', 'clock', 'clock'),
    'dogma_effects': ''.join(
        (
            '1. Return all cards from your hand, draw three 8s. ',
            '2. You may splay your purple cards up. ',
            '3. Meld a card from your hand, then execute each of its '
            'non-demand effects for yourself only.',
        )
    ),
    'dogma_icon': 'clock',
}
computers = {
    'name': 'Computers',
    'age': 9,
    'color': 'blue',
    'icons': ('clock', '', 'clock', 'factory'),
    'dogma_effects': ''.join(
        (
            '1. You may splay your red cards or your green cards up. ',
            '2. Draw and meld a 10 then execute its non-demand effects for yourself only.',
        )
    ),
    'dogma_icon': 'clock',
}
genetics = {
    'name': 'Genetics',
    'age': 9,
    'color': 'blue',
    'icons': ('bulb', 'bulb', 'bulb', ''),
    'dogma_effects': 'Draw and meld a 10. Score all cards beneath it',
    'dogma_icon': 'bulb',
}
services = {
    'name': 'Services',
    'age': 9,
    'color': 'yellow',
    'icons': ('', 'leaf', 'leaf', 'leaf'),
    'dogma_effects': ''.join(
        (
            'I *demand* you transfer all the highest cards from your score pile to my hand! ',
            'If you transferred any cards, then transfer a top card from your board '
            'without a leaf icon to your hand!',
        )
    ),
    'dogma_icon': 'crown',
}
specialization = {
    'name': 'Specialization',
    'age': 9,
    'color': 'purple',
    'icons': ('', 'factory', 'leaf', 'factory'),
    'dogma_effects': ''.join(
        (
            '1. Reveal a card from your hand, take into your hand the top card of that color',
            " from all other player's boards ",
            '2. You may splay your rellow or blue cards up',
        )
    ),
    'dogma_icon': 'factory',
}
miniaturization = {
    'name': 'Miniaturization',
    'age': 10,
    'color': 'yellow',
    'icons': ('', 'bulb', 'clock', 'bulb'),
    'dogma_effects': ''.join(
        (
            'You may return a card from your hand. ',
            'If you returned a 10, draw a 10 for every different value of card in your score pile.',
        )
    ),
    'dogma_icon': 'bulb',
}
robotics = {
    'name': 'Robotics',
    'age': 10,
    'color': 'red',
    'icons': ('', 'factory', 'clock', 'factory'),
    'dogma_effects': ''.join(
        (
            'Score your top green card. ',
            'draw and meld a 10, then execute its non-demand dogma effects, do not share them',
        )
    ),
    'dogma_icon': 'factory',
}
globalsization = {
    'name': 'globalsization',
    'age': 10,
    'color': 'yellow',
    'icons': ('', 'factory', 'factory', 'factory'),
    'dogma_effects': ''.join(
        (
            '1. I *demand* you return a top card with a leaf icon on your board! ',
            '2. Draw and score a 6. ',
            'If no player has more leaf icons on their board than factory icons, ',
            'the single player with the most points wins.',
        )
    ),
    'dogma_icon': 'factory',
}
stem_cells = {
    'name': 'Stem Cells',
    'age': 10,
    'color': 'yellow',
    'icons': ('', 'leaf', 'leaf', 'leaf'),
    'dogma_effects': 'You may score all the cards from your hand. If you score one you must score them all',
    'dogma_icon': 'leaf',
}
databases = {
    'name': 'Databases',
    'age': 10,
    'color': 'red',
    'icons': ('', 'clock', 'clock', 'clock'),
    'dogma_effects': 'I *demand* you return half (rounded up) of the cards in your score pile!',
    'dogma_icon': 'clock',
}
self_service = {
    'name': 'Self Service',
    'age': 10,
    'color': 'green',
    'icons': ('', 'crown', 'crown', 'crown'),
    'dogma_effects': ''.join(
        (
            '1. Execute the non-demand dogma effects of any other top card on your board',
            ' for yourself only.',
            '2. If you have more achievements than any other player, you win.',
        )
    ),
    'dogma_icon': 'crown',
}
bioengineering = {
    'name': 'Bioengineering',
    'age': 10,
    'color': 'blue',
    'icons': ('bulb', 'clock', 'clock', ''),
    'dogma_effects': ''.join(
        (
            "1. Transfer a top card with a leaf icon from any other player's board",
            ' to your score pile.',
            '2. If any other player has fewer than three leaf icons on their board,',
            'the player with the most leaf icons on their board wins.',
        )
    ),
    'dogma_icon': 'clock',
}
software = {
    'name': 'Software',
    'age': 10,
    'color': 'blue',
    'icons': ('clock', 'clock', 'clock', ''),
    'dogma_effects': ''.join(
        (
            '1. Draw and score a 10. ',
            "2. Draw and meld two 10s, then execute each of the second card's non-demand dogma ",
            'effects. Do not share them.',
        )
    ),
    'dogma_icon': 'clock',
}
ai = {
    'name': 'AI',
    'age': 10,
    'color': 'purple',
    'icons': ('bulb', 'bulb', 'clock', ''),
    'dogma_effects': ''.join(
        (
            '1. Draw and score a 10. ',
            '2. If Robotics and Software are top cards of any board, ',
            'the single player with the lowest score wins.',
        )
    ),
    'dogma_icon': 'bulb',
}
the_internet = {
    'name': 'The Internet',
    'age': 10,
    'color': 'purple',
    'icons': ('', 'clock', 'clock', 'bulb'),
    'dogma_effects': ''.join(
        (
            '1. You may splay your green cards up',
            '2. Draw and score a 10',
            '3. Draw and meld a 10 for every two clock icons on your board',
        )
    ),
    'dogma_icon': 'clock',
}
global decks
global achievements
decks, achievements = make_decks()
specials = ('World', 'Wonder', 'Universe', 'Monument', 'Empire')


def _test_setup():
    players, deck, achs = set_up()
    p1, p2 = players
    assert all((p1, p2, deck, achs))


def _test_meld():
    (
        players,
        _,
        _,
    ) = set_up()
    p1 = players[0]
    cardname = random.choice(list(p1['hand'].keys()))
    assert meld(p1, cardname)


if __name__ == '__main__':
    p1, p2 = init_two_player()
    # test_setup()
    # test_meld()
