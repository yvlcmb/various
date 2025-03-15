"""Innovation the card game

code smells: 
stateful modifications in place, functions that don't return anything  

not yet implemented:
    achieve action
    dogma action 
    end game score calculation 
"""

import random
from collections import defaultdict, deque

def create_card(name, age, color, icons, dogma_icon) -> dict:
    return {
        "name": name,
        "age": age,
        "color": color,
        "icons": icons,  # tuple of 4 potential icon positions, one of which may be empty
        "dogma_icon": dogma_icon,  
    }


def create_player() -> dict: 
    return { 
        "hand": {},
        "board": {
            "red": {"cards": deque(), "splay": "none"},
            "yellow": {"cards": deque(), "splay": "none"},
            "green": {"cards": deque(), "splay": "none"},
            "blue": {"cards": deque(), "splay": "none"},
            "purple": {"cards": deque(), "splay": "none"},
        },
        "score_pile": [],
        "achievements": [],
    }


def meld(player, card):
    yes = card in player['hand']
    if not yes: 
        print('card not in hand')
        return None
    card = player['hand'].pop(card)
    color = card.get('color') 
    board = player.get('board')
    board.get('color').get('cards').append(card)
    print(f"{card.get('name')} melded to {color} stack")
    return None 


def splay(player, color, direction): 
    board = player.get("board")
    if len(board[color].get('cards', [])) < 2:
        print('cannot splay a single card')
        return None
    board[color]['splay'] = direction
    print(f'cards splayed {direction}.')
    return None


def tuck(player, cardname): 
    if not cardname in player.get('hand'):
        print(f"{cardname} not found in player's hand")
        return None
    card = player['hand'].pop(cardname)
    color = card.get('color')
    print(color)
    player['board'][color]['cards'].appendleft(card) 
    print(f"{card.get('name')} tucked in player's {card.get('color')} stack")
    return None


def draw(player, decks, age): 
    while age <= 10: 
        if decks.get(age): 
            card = decks[age].popleft()
            player['hand'].update({card.get('name'): card})
            print(f"Player drew {card.get('name')}") 
            return None
        else: 
            age += 1
    return None


def count_icons(player): 
    icon_count = defaultdict(int)
    board = player.get('board')
    for color, data in board.items(): 
        cards = data.get('cards', [])
        splay = data.get('splay', 'none')

        if not cards: 
            continue

        top_card = cards[-1]
        for icon in top_card.get('icons', []): 
            if icon: 
                icon_count[icon] += 1

        directions = {'left': [2], 'right': [0, 1], 'up': [1, 2, 3]}
        positions = directions.get(splay)
        for card in cards[:-1]: 
            for pos in positions: 
                icon = card.get(icons, [])[pos]
                if icon:
                    icon_count += 1
        return dict(icon_count) 


def init_game(num_players):
    age1 = deque() 
    age1.extend([archery, metalworking, oars, domestication, agriculture, tools, 
                 writing, pottery, clothing, sailing, wheel, city_states, 
                 codeoflaws, mysticism])
    random.shuffle(age1)
    
    age2 = deque() 
    age2.extend([construction, road_building, canal_building, fermenting, 
                 currency, mapmaking, calendar, mathematics, monotheism, philosophy])
    random.shuffle(age2) 

    age3 = deque() 
    age3.extend([engineering, optics, machinery, medicine, compass, paper, 
                  alchemy, translation, education, feuadlism])
    random.shuffle(age3) 

    age4 = deque() 
    age4.extend([colonialism, gunpowder, anatomy, invention, experimentation, 
                 printing_press, enterprise, perspective, navigation, reformation])
    random.shuffle(age4)

    age5 = deque() 
    age5.extend([coal, pirate_code, statistics, steam_engine, banking, measurement,
                 chemistry, physics, astrononmy, societies])
    random.shuffle(age5)

    decks = {1: age1, 2: age2, 3: age3, 4: age4, 5: age5}
    achievements = [create_player() for _ in range(num_players)]
    return decks, achievements, players 


def set_up(): 
    deck, achievements, players = init_game(2)
    p1 = players[0]
    p2 = players[1]
    draw(p1, deck, 1)
    draw(p2, deck, 1)
    draw(p1, deck, 1)
    draw(p2, deck, 1)
    return players, deck, achievements 
    

# Initialize game state
def initialize_game(num_players):
    supply_piles = {age: deque() for age in range(1, 11)}
    achievements = {age: None for age in range(1, 10)}  # Normal achievements
    players = [
        {"hand": [], "board": defaultdict(lambda: {"cards": [], "splay": "none"}), "score_pile": [], "achievements": []}
        for _ in range(num_players)
    ]
    return supply_piles, achievements, players


# cards
archery = {"name": "Archery", "age": 1, "color": "red", "icons": ["", "", "", "Castle"], "dogma_effects": 'place holder' "dogma_icon": "Castle"}
metalworking = {"name": "Metalworking", "age": 1, "color": "red", "icons": ["", "Castle", "Castle", "Castle"], "dogma_effects": 'place holder' "dogma_icon": "Castle"}
oars =  {"name": "Oars", "age": 1, "color": "yellow", "icons": ["", "Castle", "", ""], "dogma_effects": 'place holder' "dogma_icon": "Castle"}
agriculture = {"name": "Agriculture", "age": 1, "color": "yellow", "icons": ["", "leaf", "leaf", "leaf"], "dogma_effects": 'place holder' "dogma_icon": "leaf"}
domestication = {"name": "Domestication", "age": 1, "color": "green", "icons": ["", "leaf", "leaf", "Castle"], "dogma_effects": 'place holder' "dogma_icon": "leaf"}
masonry = {"name": "Masonry", "age": 1, "color": "green", "icons": ["", "Castle", "Castle", "leaf"], "dogma_effects": 'place holder' "dogma_icon": "Castle"}
clothing = {"name": "Clothing", "age": 1, "color": "purple", "icons": ["", "leaf", "leaf", "factory"], "dogma_effects": 'place holder' "dogma_icon": "leaf"}
sailing = {"name": "Sailing", "age": 1, "color": "purple", "icons": ["", "Castle", "leaf", "leaf"], "dogma_effects": 'place holder' "dogma_icon": "Castle"}
wheel = {"name": "The Wheel", "age": 1, "color": "blue", "icons": ["", "Castle", "Castle", "leaf"], "dogma_effects": 'place holder' "dogma_icon": "Castle"}
pottery = {"name": "Pottery", "age": 1, "color": "blue", "icons": ["", "leaf", "leaf", "leaf"], "dogma_effects": 'place holder' "dogma_icon": "leaf"}
tools = {"name": "Tools", "age": 1, "color": "yellow", "icons": ["", "Castle", "leaf", "leaf"], "dogma_effects": 'place holder' "dogma_icon": "Castle"}
writing = {"name": "Writing", "age": 1, "color": "blue", "icons": ["", "bulb", "bulb", "crown"], "dogma_effects": 'place holder' "dogma_icon": "bulb"}
codeoflaws = {"name": "Code of Laws", "age": 1, "color": "red", "icons": ["", "crown", "crown", "crown"], "dogma_effects": 'place holder' "dogma_icon": "crown"}
city_states = {"name": "City States", "age": 1, "color": "purple", "icons": ["", "crown", "crown", "Castle"], "dogma_effects": 'place holder' "dogma_icon": "crown"}
mysticism = {"name": "Mysticism", "age": 1, "color": "purple", "icons": ["", "Castle", "Castle", "Castle"], "dogma_effects": 'place holder' "dogma_icon": "Castle"}
construction = {"name": "Construction", "age": 2, "color": "green", "icons": ["", "factory", "factory", "crown"], "dogma_effects": 'place holder' "dogma_icon": "factory"}
road_building = {"name": "Road Building", "age": 2, "color": "red", "icons": ["", "Castle", "factory", "crown"], "dogma_effects": 'place holder' "dogma_icon": "Castle"}
canal_building = {"name": "Canal Building", "age": 2, "color": "blue", "icons": ["", "Castle", "factory", "leaf"], "dogma_effects": 'place holder' "dogma_icon": "Castle"}
fermenting = {"name": "Fermenting", "age": 2, "color": "yellow", "icons": ["", "leaf", "leaf", "factory"], "dogma_effects": 'place holder' "dogma_icon": "leaf"}
currency = {"name": "Currency", "age": 2, "color": "green", "icons": ["", "factory", "crown", "leaf"], "dogma_effects": 'place holder' "dogma_icon": "factory"}
mapmaking = {"name": "Mapmaking", "age": 2, "color": "purple", "icons": ["", "leaf", "factory", "Castle"], "dogma_effects": 'place holder' "dogma_icon": "leaf"}
calendar = {"name": "Calendar", "age": 2, "color": "blue", "icons": ["", "bulb", "crown", "leaf"], "dogma_effects": 'place holder' "dogma_icon": "bulb"}
mathematics = {"name": "Mathematics", "age": 2, "color": "yellow", "icons": ["", "bulb", "bulb", "crown"], "dogma_effects": 'place holder' "dogma_icon": "bulb"}
monotheism = {"name": "Monotheism", "age": 2, "color": "red", "icons": ["", "crown", "crown", "leaf"], "dogma_effects": 'place holder' "dogma_icon": "crown"}
philosophy = {"name": "Philosophy", "age": 2, "color": "green", "icons": ["", "bulb", "bulb", "bulb"], "dogma_effects": 'place holder' "dogma_icon": "bulb"}
engineering = {"name": "Engineering", "age": 3, "color": "red", "icons": ["", "bulb", "factory", "Castle"], "dogma_effects": 'place holder' "dogma_icon": "bulb"}
optics = {"name": "Optics", "age": 3, "color": "blue", "icons": ["", "bulb", "bulb", "factory"], "dogma_effects": 'place holder' "dogma_icon": "bulb"}
machinery = {"name": "Machinery", "age": 3, "color": "yellow", "icons":  ["", "factory", "factory", "bulb"], "dogma_effects": 'place holder' "dogma_icon": "factory"}
medicine = {"name": "Medicine", "age": 3, "color": "purple", "icons": ["", "leaf", "bulb", "factory"], "dogma_effects": 'place holder' "dogma_icon": "leaf"}
compass = {"name": "Compass", "age": 3, "color": "green", "icons": ["", "factory", "leaf", "crown"], "dogma_effects": 'place holder' "dogma_icon": "factory"}
paper = {"name": "Paper", "age": 3, "color": "yellow", "icons": ["", "bulb", "bulb", "leaf"], "dogma_effects": 'place holder' "dogma_icon": "bulb"}
alchemy = {"name": "Alchemy", "age": 3, "color": "red", "icons": ["", "leaf", "bulb", "factory"], "dogma_effects": 'place holder' "dogma_icon": "leaf"}
translation = {"name": "Translation", "age": 3, "color": "blue", "icons": ["", "bulb", "crown", "bulb"], "dogma_effects": 'place holder' "dogma_icon": "bulb"}
education = {"name": "Education", "age": 3, "color": "purple", "icons": ["", "bulb", "crown", "leaf"], "dogma_effects": 'place holder' "dogma_icon": "bulb"}
feudalism = {"name": "Feudalism", "age": 3, "color": "green", "icons": ["", "Castle", "crown", "crown"], "dogma_effects": 'place holder' "dogma_icon": "Castle"}
colonialism = {"name": "Colonialism", "age": 4, "color": "red", "icons": ["", "factory", "leaf", "factory"], "dogma_effects": 'place holder' "dogma_icon": "factory"}
gunpowder = {"name": "Gunpowder", "age": 4, "color": "yellow", "icons": ["", "Castle", "factory", "factory"], "dogma_effects": 'place holder' "dogma_icon": "Castle"}
anatomy = {"name": "Anatomy", "age": 4, "color": "purple", "icons": ["", "leaf", "bulb", "bulb"], "dogma_effects": 'place holder' "dogma_icon": "leaf"}
invention = {"name": "Invention", "age": 4, "color": "blue", "icons": ["", "bulb", "bulb", "factory"], "dogma_effects": 'place holder' "dogma_icon": "bulb"}
experimentation = {"name": "Experimentation", "age": 4, "color": "green", "icons": ["", "bulb", "factory", "bulb"], "dogma_effects": 'place holder' "dogma_icon": "bulb"}
printing_press = {"name": "Printing Press", "age": 4, "color": "yellow", "icons": ["", "bulb", "bulb", "crown"], "dogma_effects": 'place holder' "dogma_icon": "bulb"}
enterprise = {"name": "Enterprise", "age": 4, "color": "red", "icons": ["", "factory", "factory", "crown"], "dogma_effects": 'place holder' "dogma_icon": "factory"}
perspective = {"name": "Perspective", "age": 4, "color": "blue", "icons": ["", "bulb", "bulb", "bulb"], "dogma_effects": 'place holder' "dogma_icon": "bulb"}
navigation = {"name": "Navigation", "age": 4, "color": "green", "icons": ["", "Castle", "factory", "factory"], "dogma_effects": 'place holder' "dogma_icon": "Castle"}
reformation = {"name": "Reformation", "age": 4, "color": "purple", "icons": ["", "crown", "crown", "bulb"], "dogma_effects": 'place holder' "dogma_icon": "crown"}
coal = {"name": "Coal", "age": 5, "color": "red", "icons": ["", "factory", "factory", "factory"], "dogma_effects": 'place holder' "dogma_icon": "factory"}
pirate_code = {"name": "The Pirate Code", "age": 5, "color": "blue", "icons": ["", "Castle", "crown", "factory"], "dogma_effects": 'place holder' "dogma_icon": "Castle"}
statistics = {"name": "Statistics", "age": 5, "color": "purple", "icons": ["", "bulb", "factory", "crown"], "dogma_effects": 'place holder' "dogma_icon": "bulb"}
steam_engine = {"name": "Steam Engine", "age": 5, "color": "yellow", "icons": ["", "factory", "factory", "clock"], "dogma_effects": 'place holder' "dogma_icon": "factory"}
banking = {"name": "Banking", "age": 5, "color": "green", "icons": ["", "factory", "factory", "crown"], "dogma_effects": 'place holder' "dogma_icon": "factory"}
measurement = {"name": "Measurement", "age": 5, "color": "yellow", "icons": ["", "bulb", "bulb", "factory"], "dogma_effects": 'place holder' "dogma_icon": "bulb"}
chemistry = {"name": "Chemistry", "age": 5, "color": "blue", "icons": ["", "bulb", "factory", "bulb"], "dogma_effects": 'place holder' "dogma_icon": "bulb"}
physics = {"name": "Physics", "age": 5, "color": "red", "icons": ["", "bulb", "bulb", "factory"], "dogma_effects": 'place holder' "dogma_icon": "bulb"}
astronomy = {"name": "Astronomy", "age": 5, "color": "green", "icons": ["", "bulb", "bulb", "crown"], "dogma_effects": 'place holder' "dogma_icon": "bulb"}
societies = {"name": "Societies", "age": 5, "color": "purple", "icons": ["", "crown", "crown", "factory"], "dogma_effects": 'place holder' "dogma_icon": "crown"}
industrialization = {"name": "Industrialization", "age": 6, "color": "red", "icons": ["", "factory", "factory", "clock"], "dogma_effects": 'place holder' "dogma_icon": "factory"}
machine_tools = {"name": "Machine Tools", "age": 6, "color": "yellow", "icons": ["", "factory", "clock", "bulb"], "dogma_effects": 'place holder' "dogma_icon": "factory"}
canning = {"name": "Canning", "age": 6, "color": "green", "icons": ["", "factory", "factory", "leaf"], "dogma_effects": 'place holder' "dogma_icon": "factory"}
vaccination = {"name": "Vaccination", "age": 6, "color": "purple", "icons": ["", "leaf", "bulb", "bulb"], "dogma_effects": 'place holder' "dogma_icon": "leaf"}
classification = {"name": "Classification", "age": 6, "color": "blue", "icons": ["", "bulb", "bulb", "leaf"], "dogma_effects": 'place holder' "dogma_icon": "bulb"}
metric_system = {"name": "Metric System", "age": 6, "color": "green", "icons": ["", "bulb", "bulb", "factory"], "dogma_effects": 'place holder' "dogma_icon": "bulb"}
atomic_theory = {"name": "Atomic Theory", "age": 6, "color": "blue", "icons": ["", "bulb", "bulb", "bulb"], "dogma_effects": 'place holder' "dogma_icon": "bulb"}
encyclopedia = {"name": "Encyclopedia", "age": 6, "color": "yellow", "icons": ["", "bulb", "bulb", "leaf"], "dogma_effects": 'place holder' "dogma_icon": "bulb"}
democracy = {"name": "Democracy", "age": 6, "color": "red", "icons": ["", "crown", "crown", "crown"], "dogma_effects": 'place holder' "dogma_icon": "crown"}
emancipation = {"name": "Emancipation", "age": 6, "color": "purple", "icons": ["", "crown", "crown", "leaf"], "dogma_effects": 'place holder' "dogma_icon": "crown"}
combustion = {"name": "Combustion", "age": 7, "color": "red", "icons": ["", "factory", "clock", "clock"], "dogma_effects": 'place holder' "dogma_icon": "factory"}
explosives = {"name": "Explosives", "age": 7, "color": "yellow", "icons": ["", "factory", "factory", "clock"], "dogma_effects": 'place holder' "dogma_icon": "factory"}
refrigeration = {"name": "Refrigeration", "age": 7, "color": "green", "icons": ["", "factory", "clock", "leaf"], "dogma_effects": 'place holder' "dogma_icon": "factory"}
sanitation = {"name": "Sanitation", "age": 7, "color": "purple", "icons": ["", "leaf", "bulb", "clock"], "dogma_effects": 'place holder' "dogma_icon": "leaf"}
bicycle = {"name": "Bicycle", "age": 7, "color": "blue", "icons": ["", "factory", "clock", "factory"], "dogma_effects": 'place holder' "dogma_icon": "factory"}
electricity = {"name": "Electricity", "age": 7, "color": "yellow", "icons": ["", "bulb", "clock", "bulb"], "dogma_effects": 'place holder' "dogma_icon": "bulb"}
evolution = {"name": "Evolution", "age": 7, "color": "green", "icons": ["", "leaf", "leaf", "clock"], "dogma_effects": 'place holder' "dogma_icon": "leaf"}
publications = {"name": "Publications", "age": 7, "color": "blue", "icons": ["", "bulb", "bulb", "leaf"], "dogma_effects": 'place holder' "dogma_icon": "bulb"}
lighting = {"name": "Lighting", "age": 7, "color": "red", "icons": ["", "bulb", "clock", "clock"], "dogma_effects": 'place holder' "dogma_icon": "bulb"}
railroad = {"name": "Railroad", "age": 7, "color": "purple", "icons": ["", "factory", "clock", "clock"], "dogma_effects": 'place holder' "dogma_icon": "factory"}
flight = {"name": "Flight", "age": 8, "color": "red", "icons": ["", "factory", "clock", "clock"], "dogma_effects": 'place holder' "dogma_icon": "factory"}
antibiotics = {"name": "Antibiotics", "age": 8, "color": "green", "icons": ["", "leaf", "bulb", "clock"], "dogma_effects": 'place holder' "dogma_icon": "leaf"}
corporations = {"name": "Corporations", "age": 8, "color": "yellow", "icons": ["", "factory", "clock", "crown"], "dogma_effects": 'place holder' "dogma_icon": "factory"}
quantum_theory = {"name": "Quantum Theory", "age": 8, "color": "blue", "icons": ["", "bulb", "bulb", "clock"], "dogma_effects": 'place holder' "dogma_icon": "bulb"}
empiricism = {"name": "Empiricism", "age": 8, "color": "green", "icons": ["", "bulb", "bulb", "leaf"], "dogma_effects": 'place holder' "dogma_icon": "bulb"}
mobility = {"name": "Mobility", "age": 8, "color": "purple", "icons": ["", "factory", "clock", "clock"], "dogma_effects": 'place holder' "dogma_icon": "factory"}
skyscrapers = {"name": "Skyscrapers", "age": 8, "color": "red", "icons": ["", "factory", "clock", "clock"], "dogma_effects": 'place holder' "dogma_icon": "factory"}
mass_media = {"name": "Mass Media", "age": 8, "color": "yellow", "icons": ["", "bulb", "clock", "leaf"], "dogma_effects": 'place holder' "dogma_icon": "bulb"}
rocketry = {"name": "Rocketry", "age": 8, "color": "blue", "icons": ["", "bulb", "clock", "factory"], "dogma_effects": 'place holder' "dogma_icon": "bulb"}
socialism = {"name": "Socialism", "age": 8, "color": "purple", "icons": ["", "crown", "crown", "clock"], "dogma_effects": 'place holder' "dogma_icon": "crown"}
composites = {"name": "Composites", "age": 9, "color": "red", "icons": ["", "factory", "clock", "clock"], "dogma_effects": 'place holder' "dogma_icon": "factory"}
fission = {"name": "Fission", "age": 9, "color": "yellow", "icons": ["", "bulb", "bulb", "clock"], "dogma_effects": 'place holder' "dogma_icon": "bulb"}
ecology = {"name": "Ecology", "age": 9, "color": "green", "icons": ["", "leaf", "leaf", "clock"], "dogma_effects": 'place holder' "dogma_icon": "leaf"}
suburbia = {"name": "Suburbia", "age": 9, "color": "purple", "icons": ["", "factory", "clock", "leaf"], "dogma_effects": 'place holder' "dogma_icon": "factory"}
collaboration = {"name": "Collaboration", "age": 9, "color": "red", "icons": ["", "bulb", "crown", "clock"], "dogma_effects": 'place holder' "dogma_icon": "bulb"}
satellites = {"name": "Satellites", "age": 9, "color": "purple", "icons": ["", "bulb", "clock", "factory"], "dogma_effects": 'place holder' "dogma_icon": "bulb"}
computers = {"name": "Computers", "age": 9, "color": "green", "icons": ["", "bulb", "factory", "clock"], "dogma_effects": 'place holder' "dogma_icon": "clock"}
genetics = {"name": "Genetics", "age": 9, "color": "blue", "icons": ["", "leaf", "bulb", "clock"], "dogma_effects": 'place holder' "dogma_icon": "leaf"}
services = {"name": "Services", "age": 9, "color": "yellow", "icons": ["", "crown", "clock", "bulb"], "dogma_effects": 'place holder' "dogma_icon": "crown"}
specialization = {"name": "Specialization", "age": 9, "color": "blue", "icons": ["", "bulb", "factory", "clock"], "dogma_effects": 'place holder' "dogma_icon": "bulb"}
miniaturization = {"name": "Miniaturization", "age": 10, "color": "yellow", "icons": ["", "factory", "clock", "bulb"], "dogma_effects": 'place holder' "dogma_icon": "factory"}
robotics = {"name": "Robotics", "age": 10, "color": "green", "icons": ["", "factory", "clock", "clock"], "dogma_effects": 'place holder' "dogma_icon": "clock"}
globalization = {"name": "Globalization", "age": 10, "color": "red", "icons": ["", "crown", "clock", "factory"], "dogma_effects": 'place holder' "dogma_icon": "crown"}
stem_cells = {"name": "Stem Cells", "age": 10, "color": "purple", "icons": ["", "leaf", "bulb", "clock"], "dogma_effects": 'place holder' "dogma_icon": "leaf"}
databases = {"name": "Databases", "age": 10, "color": "red", "icons": ["", "bulb", "clock", "leaf"], "dogma_effects": 'place holder' "dogma_icon": "bulb"}
self_service = {"name": "Self Service", "age": 10, "color": "yellow", "icons": ["", "crown", "clock", "factory"], "dogma_effects": 'place holder' "dogma_icon": "crown"}
bioengineering = {"name": "Bioengineering", "age": 10, "color": "green", "icons": ["", "leaf", "bulb", "clock"], "dogma_effects": 'place holder' "dogma_icon": "leaf"}
software = {"name": "Software", "age": 10, "color": "blue", "icons": ["", "bulb", "clock", "clock"], "dogma_effects": 'place holder' "dogma_icon": "clock"}
ai = {"name": "A.I.", "age": 10, "color": "blue", "icons": ["", "bulb", "clock", "clock"], "dogma_effects": 'place holder' "dogma_icon": "clock"}
the_internet = {"name": "The Internet", "age": 10, "color": "purple", "icons": ["", "bulb", "clock", "clock"], "dogma_effects": 'place holder' "dogma_icon": "bulb"}
