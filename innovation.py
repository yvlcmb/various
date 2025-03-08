"""Innovation without dogma implemented"""

import random
from collections import defaultdict, deque

# Define card structure as a dictionary
def create_card(name, age, color, icons, dogma_effects):
    return {
        "name": name,
        "age": age,
        "color": color,
        "icons": icons,  # List of 4 potential icon positions, one of which may be empty
        "dogma_effects": dogma_effects,  # List of effects
    }

def meld_card(player, card):
    """
    Melds a card from the player's hand to their board.
    """
    # 1. Remove the card from the player's hand.
    if card in player["hand"]:
        player["hand"].remove(card)
    else:
        print("Card not in hand.") # Added error handling
        return

    # 2. Determine the color of the card.
    color = card["color"]

    # 3. Place the card on the board in the appropriate color stack.
    board = player["board"]
    board[color]["cards"].append(card)

    print(f"Card '{card['name']}' melded to {color} stack.") #Added feedback

# Initialize game state
def initialize_game(num_players):
    supply_piles = {age: deque() for age in range(1, 11)}
    achievements = {age: None for age in range(1, 10)}  # Normal achievements
    players = [
        {"hand": [], "board": defaultdict(lambda: {"cards": [], "splay": "none"}), "score_pile": [], "achievements": []}
        for _ in range(num_players)
    ]
    return supply_piles, achievements, players

# Splay cards in a given direction
def splay_cards(player, color, direction):
    board = player.get("board", defaultdict(lambda: {"cards": [], "splay": "none"}))
    if len(board[color].get("cards", [])) < 2:
        return  # Cannot splay with fewer than two cards

    board[color]["splay"] = direction  # Update splay direction

    # Determine revealed icons based on splay direction
    if direction == "left":
        revealed_positions = [2]  # Lower center
    elif direction == "right":
        revealed_positions = [0, 1]  # Upper left, Lower left
    elif direction == "up":
        revealed_positions = [1, 2, 3]  # Lower left, Lower center, Lower right
    else:
        return  # Invalid direction

    # Extract the relevant icons based on splay direction
    revealed_icons = []
    for card in board[color].get("cards", [])[:-1]:  # Exclude the top card
        for pos in revealed_positions:
            if card.get("icons", [])[pos]:  # Only add non-empty icons
                revealed_icons.append(card["icons"][pos])

    return revealed_icons  # This could be used elsewhere if needed

# Count icons for a player
def count_icons(player):
    icon_count = defaultdict(int)
    board = player.get("board", {})

    for color, data in board.items():
        cards = data.get("cards", [])
        splay = data.get("splay", "none")

        if not cards:
            continue

        # Always count icons from the top card
        top_card = cards[-1]
        for icon in top_card.get("icons", []):
            if icon:
                icon_count[icon] += 1

        # Add revealed icons based on splay direction
        if splay == "left":
            positions = [3]  # Lower right  # Lower center
        elif splay == "right":
            positions = [0, 1]  # Upper left, Lower left
        elif splay == "up":
            positions = [1, 2, 3]  # Lower left, Lower center, Lower right
        else:
            continue

        for card in cards[:-1]:  # Exclude the top card
            for pos in positions:
                icon = card.get("icons", [])[pos]
                if icon:
                    icon_count[icon] += 1

    return dict(icon_count)

def draw_card(player, supply_piles, age):
    """Draws a card for a player from the supply piles,
    handling empty piles by drawing from the next higher age.
    """
    while age <= 10:
        if supply_piles[age]:
            return supply_piles[age].popleft()  # Draw card
        else:
            age += 1  # Try next higher age

    #If age exceeds 10, return None to indicate game end
    return None

def begin_game(supply_piles, achievements, players):
    """
    Begins the game for two players: deals initial cards,
    has players meld one, and determines the first player.
    """
    # 1. Deal two age 1 cards to each player.
    for player in players:
        for _ in range(2):
            card = supply_piles[1].popleft()
            player["hand"].append(card)

    # 2. Players simultaneously choose one card to meld.
    #    For simplicity, let's assume they always meld the first card in their hand.
    for player in players:
        card_to_meld = player["hand"].pop(0)
        color = card_to_meld["color"]
        player["board"][color]["cards"].append(card_to_meld)
        print(f"Player melded '{card_to_meld['name']}' to the {color} stack.") #Added feedback

    # 3. Determine the first player based on alphabetical order of melded cards.
    card1_name = players["board"][list(players["board"].keys())]["cards"]["name"]
    card2_name = players[1]["board"][list(players[1]["board"].keys())]["cards"]["name"]

    if card1_name < card2_name:
        first_player = players
        print("Player 1 goes first.") #Added feedback
    else:
        first_player = players[1]
        print("Player 2 goes first.") #Added feedback

    return first_player

# Example player setup
player = {
    "hand": deque([
        {"name": "Writing", "age": 1, "color": "Blue", "icons": ["", "Light Bulb", "Light Bulb", "Crown"], "dogma_effects": []},
        {"name": "Metalworking", "age": 1, "color": "Red", "icons": ["", "Tower", "Tower", "Tower"], "dogma_effects": []}
    ]),
    "board": {
        "Yellow": {
            "cards": [
                {"name": "Agriculture", "age": 1, "color": "Yellow", "icons": ["", "Leaf", "Leaf", "Leaf"], "dogma_effects": []}
            ],
            "splay": "none"
        },
        "Purple": {
            "cards": [
                {"name": "Mysticism", "age": 1, "color": "Purple", "icons": ["", "Tower", "Tower", "Tower"], "dogma_effects": []},
                {"name": "City States", "age": 1, "color": "Purple", "icons": ["", "Crown", "Crown", "Tower"], "dogma_effects": []}
            ],
            "splay": "left"  # Splaying Purple left
        }
    },
    "score_pile": deque(),
    "achievements": []
}

# Count icons after splaying
icon_totals = count_icons(player)

# cards
archery = {"name": "Archery", "age": 1, "color": "Red", "icons": ["", "", "", "Castle"], "dogma_effects": [], "dogma_icon": "Castle"}
metalworking = {"name": "Metalworking", "age": 1, "color": "Red", "icons": ["", "Castle", "Castle", "Castle"], "dogma_effects": [], "dogma_icon": "Castle"}
oars =  {"name": "Oars", "age": 1, "color": "Yellow", "icons": ["", "Castle", "", ""], "dogma_effects": [], "dogma_icon": "Castle"}
agriculture = {"name": "Agriculture", "age": 1, "color": "Yellow", "icons": ["", "Leaf", "Leaf", "Leaf"], "dogma_effects": [], "dogma_icon": "Leaf"}
domestication = {"name": "Domestication", "age": 1, "color": "Green", "icons": ["", "Leaf", "Leaf", "Castle"], "dogma_effects": [], "dogma_icon": "Leaf"}
masonry = {"name": "Masonry", "age": 1, "color": "Green", "icons": ["", "Castle", "Castle", "Leaf"], "dogma_effects": [], "dogma_icon": "Castle"}
clothing = {"name": "Clothing", "age": 1, "color": "Purple", "icons": ["", "Leaf", "Leaf", "Factory"], "dogma_effects": [], "dogma_icon": "Leaf"}
sailing = {"name": "Sailing", "age": 1, "color": "Purple", "icons": ["", "Castle", "Leaf", "Leaf"], "dogma_effects": [], "dogma_icon": "Castle"}
the_wheel = {"name": "The Wheel", "age": 1, "color": "Blue", "icons": ["", "Castle", "Castle", "Leaf"], "dogma_effects": [], "dogma_icon": "Castle"}
pottery = {"name": "Pottery", "age": 1, "color": "Blue", "icons": ["", "Leaf", "Leaf", "Leaf"], "dogma_effects": [], "dogma_icon": "Leaf"}
tools = {"name": "Tools", "age": 1, "color": "Yellow", "icons": ["", "Castle", "Leaf", "Leaf"], "dogma_effects": [], "dogma_icon": "Castle"}
writing = {"name": "Writing", "age": 1, "color": "Blue", "icons": ["", "Light Bulb", "Light Bulb", "Crown"], "dogma_effects": [], "dogma_icon": "Light Bulb"}
code_of_laws = {"name": "Code of Laws", "age": 1, "color": "Red", "icons": ["", "Crown", "Crown", "Crown"], "dogma_effects": [], "dogma_icon": "Crown"}
city_states = {"name": "City States", "age": 1, "color": "Purple", "icons": ["", "Crown", "Crown", "Castle"], "dogma_effects": [], "dogma_icon": "Crown"}
mysticism = {"name": "Mysticism", "age": 1, "color": "Purple", "icons": ["", "Castle", "Castle", "Castle"], "dogma_effects": [], "dogma_icon": "Castle"}
construction = {"name": "Construction", "age": 2, "color": "Green", "icons": ["", "Factory", "Factory", "Crown"], "dogma_effects": [], "dogma_icon": "Factory"}
road_building = {"name": "Road Building", "age": 2, "color": "Red", "icons": ["", "Castle", "Factory", "Crown"], "dogma_effects": [], "dogma_icon": "Castle"}
canal_building = {"name": "Canal Building", "age": 2, "color": "Blue", "icons": ["", "Castle", "Factory", "Leaf"], "dogma_effects": [], "dogma_icon": "Castle"}
fermenting = {"name": "Fermenting", "age": 2, "color": "Yellow", "icons": ["", "Leaf", "Leaf", "Factory"], "dogma_effects": [], "dogma_icon": "Leaf"}
currency = {"name": "Currency", "age": 2, "color": "Green", "icons": ["", "Factory", "Crown", "Leaf"], "dogma_effects": [], "dogma_icon": "Factory"}
mapmaking = {"name": "Mapmaking", "age": 2, "color": "Purple", "icons": ["", "Leaf", "Factory", "Castle"], "dogma_effects": [], "dogma_icon": "Leaf"}
calendar = {"name": "Calendar", "age": 2, "color": "Blue", "icons": ["", "Light Bulb", "Crown", "Leaf"], "dogma_effects": [], "dogma_icon": "Light Bulb"}
mathematics = {"name": "Mathematics", "age": 2, "color": "Yellow", "icons": ["", "Light Bulb", "Light Bulb", "Crown"], "dogma_effects": [], "dogma_icon": "Light Bulb"}
monotheism = {"name": "Monotheism", "age": 2, "color": "Red", "icons": ["", "Crown", "Crown", "Leaf"], "dogma_effects": [], "dogma_icon": "Crown"}
philosophy = {"name": "Philosophy", "age": 2, "color": "Green", "icons": ["", "Light Bulb", "Light Bulb", "Light Bulb"], "dogma_effects": [], "dogma_icon": "Light Bulb"}
engineering = {"name": "Engineering", "age": 3, "color": "Red", "icons": ["", "Light Bulb", "Factory", "Castle"], "dogma_effects": [], "dogma_icon": "Light Bulb"}
optics = {"name": "Optics", "age": 3, "color": "Blue", "icons": ["", "Light Bulb", "Light Bulb", "Factory"], "dogma_effects": [], "dogma_icon": "Light Bulb"}
machinery = {"name": "Machinery", "age": 3, "color": "Yellow", "icons":  ["", "Factory", "Factory", "Light Bulb"], "dogma_effects": [], "dogma_icon": "Factory"}
medicine = {"name": "Medicine", "age": 3, "color": "Purple", "icons": ["", "Leaf", "Light Bulb", "Factory"], "dogma_effects": [], "dogma_icon": "Leaf"}
compass = {"name": "Compass", "age": 3, "color": "Green", "icons": ["", "Factory", "Leaf", "Crown"], "dogma_effects": [], "dogma_icon": "Factory"}
paper = {"name": "Paper", "age": 3, "color": "Yellow", "icons": ["", "Light Bulb", "Light Bulb", "Leaf"], "dogma_effects": [], "dogma_icon": "Light Bulb"}
alchemy = {"name": "Alchemy", "age": 3, "color": "Red", "icons": ["", "Leaf", "Light Bulb", "Factory"], "dogma_effects": [], "dogma_icon": "Leaf"}
translation = {"name": "Translation", "age": 3, "color": "Blue", "icons": ["", "Light Bulb", "Crown", "Light Bulb"], "dogma_effects": [], "dogma_icon": "Light Bulb"}
education = {"name": "Education", "age": 3, "color": "Purple", "icons": ["", "Light Bulb", "Crown", "Leaf"], "dogma_effects": [], "dogma_icon": "Light Bulb"}
feudalism = {"name": "Feudalism", "age": 3, "color": "Green", "icons": ["", "Castle", "Crown", "Crown"], "dogma_effects": [], "dogma_icon": "Castle"}
colonialism = {"name": "Colonialism", "age": 4, "color": "Red", "icons": ["", "Factory", "Leaf", "Factory"], "dogma_effects": [], "dogma_icon": "Factory"}
gunpowder = {"name": "Gunpowder", "age": 4, "color": "Yellow", "icons": ["", "Castle", "Factory", "Factory"], "dogma_effects": [], "dogma_icon": "Castle"}
anatomy = {"name": "Anatomy", "age": 4, "color": "Purple", "icons": ["", "Leaf", "Light Bulb", "Light Bulb"], "dogma_effects": [], "dogma_icon": "Leaf"}
invention = {"name": "Invention", "age": 4, "color": "Blue", "icons": ["", "Light Bulb", "Light Bulb", "Factory"], "dogma_effects": [], "dogma_icon": "Light Bulb"}
experimentation = {"name": "Experimentation", "age": 4, "color": "Green", "icons": ["", "Light Bulb", "Factory", "Light Bulb"], "dogma_effects": [], "dogma_icon": "Light Bulb"}
printing_press = {"name": "Printing Press", "age": 4, "color": "Yellow", "icons": ["", "Light Bulb", "Light Bulb", "Crown"], "dogma_effects": [], "dogma_icon": "Light Bulb"}
enterprise = {"name": "Enterprise", "age": 4, "color": "Red", "icons": ["", "Factory", "Factory", "Crown"], "dogma_effects": [], "dogma_icon": "Factory"}
perspective = {"name": "Perspective", "age": 4, "color": "Blue", "icons": ["", "Light Bulb", "Light Bulb", "Light Bulb"], "dogma_effects": [], "dogma_icon": "Light Bulb"}
navigation = {"name": "Navigation", "age": 4, "color": "Green", "icons": ["", "Castle", "Factory", "Factory"], "dogma_effects": [], "dogma_icon": "Castle"}
reformation = {"name": "Reformation", "age": 4, "color": "Purple", "icons": ["", "Crown", "Crown", "Light Bulb"], "dogma_effects": [], "dogma_icon": "Crown"}
coal = {"name": "Coal", "age": 5, "color": "Red", "icons": ["", "Factory", "Factory", "Factory"], "dogma_effects": [], "dogma_icon": "Factory"}
the_pirate_code = {"name": "The Pirate Code", "age": 5, "color": "Blue", "icons": ["", "Castle", "Crown", "Factory"], "dogma_effects": [], "dogma_icon": "Castle"}
statistics = {"name": "Statistics", "age": 5, "color": "Purple", "icons": ["", "Light Bulb", "Factory", "Crown"], "dogma_effects": [], "dogma_icon": "Light Bulb"}
steam_engine = {"name": "Steam Engine", "age": 5, "color": "Yellow", "icons": ["", "Factory", "Factory", "Clock"], "dogma_effects": [], "dogma_icon": "Factory"}
banking = {"name": "Banking", "age": 5, "color": "Green", "icons": ["", "Factory", "Factory", "Crown"], "dogma_effects": [], "dogma_icon": "Factory"}
measurement = {"name": "Measurement", "age": 5, "color": "Yellow", "icons": ["", "Light Bulb", "Light Bulb", "Factory"], "dogma_effects": [], "dogma_icon": "Light Bulb"}
chemistry = {"name": "Chemistry", "age": 5, "color": "Blue", "icons": ["", "Light Bulb", "Factory", "Light Bulb"], "dogma_effects": [], "dogma_icon": "Light Bulb"}
physics = {"name": "Physics", "age": 5, "color": "Red", "icons": ["", "Light Bulb", "Light Bulb", "Factory"], "dogma_effects": [], "dogma_icon": "Light Bulb"}
astronomy = {"name": "Astronomy", "age": 5, "color": "Green", "icons": ["", "Light Bulb", "Light Bulb", "Crown"], "dogma_effects": [], "dogma_icon": "Light Bulb"}
societies = {"name": "Societies", "age": 5, "color": "Purple", "icons": ["", "Crown", "Crown", "Factory"], "dogma_effects": [], "dogma_icon": "Crown"}
industrialization = {"name": "Industrialization", "age": 6, "color": "Red", "icons": ["", "Factory", "Factory", "Clock"], "dogma_effects": [], "dogma_icon": "Factory"}
machine_tools = {"name": "Machine Tools", "age": 6, "color": "Yellow", "icons": ["", "Factory", "Clock", "Light Bulb"], "dogma_effects": [], "dogma_icon": "Factory"}
canning = {"name": "Canning", "age": 6, "color": "Green", "icons": ["", "Factory", "Factory", "Leaf"], "dogma_effects": [], "dogma_icon": "Factory"}
vaccination = {"name": "Vaccination", "age": 6, "color": "Purple", "icons": ["", "Leaf", "Light Bulb", "Light Bulb"], "dogma_effects": [], "dogma_icon": "Leaf"}
classification = {"name": "Classification", "age": 6, "color": "Blue", "icons": ["", "Light Bulb", "Light Bulb", "Leaf"], "dogma_effects": [], "dogma_icon": "Light Bulb"}
metric_system = {"name": "Metric System", "age": 6, "color": "Green", "icons": ["", "Light Bulb", "Light Bulb", "Factory"], "dogma_effects": [], "dogma_icon": "Light Bulb"}
atomic_theory = {"name": "Atomic Theory", "age": 6, "color": "Blue", "icons": ["", "Light Bulb", "Light Bulb", "Light Bulb"], "dogma_effects": [], "dogma_icon": "Light Bulb"}
encyclopedia = {"name": "Encyclopedia", "age": 6, "color": "Yellow", "icons": ["", "Light Bulb", "Light Bulb", "Leaf"], "dogma_effects": [], "dogma_icon": "Light Bulb"}
democracy = {"name": "Democracy", "age": 6, "color": "Red", "icons": ["", "Crown", "Crown", "Crown"], "dogma_effects": [], "dogma_icon": "Crown"}
emancipation = {"name": "Emancipation", "age": 6, "color": "Purple", "icons": ["", "Crown", "Crown", "Leaf"], "dogma_effects": [], "dogma_icon": "Crown"}
combustion = {"name": "Combustion", "age": 7, "color": "Red", "icons": ["", "Factory", "Clock", "Clock"], "dogma_effects": [], "dogma_icon": "Factory"}
explosives = {"name": "Explosives", "age": 7, "color": "Yellow", "icons": ["", "Factory", "Factory", "Clock"], "dogma_effects": [], "dogma_icon": "Factory"}
refrigeration = {"name": "Refrigeration", "age": 7, "color": "Green", "icons": ["", "Factory", "Clock", "Leaf"], "dogma_effects": [], "dogma_icon": "Factory"}
sanitation = {"name": "Sanitation", "age": 7, "color": "Purple", "icons": ["", "Leaf", "Light Bulb", "Clock"], "dogma_effects": [], "dogma_icon": "Leaf"}
bicycle = {"name": "Bicycle", "age": 7, "color": "Blue", "icons": ["", "Factory", "Clock", "Factory"], "dogma_effects": [], "dogma_icon": "Factory"}
electricity = {"name": "Electricity", "age": 7, "color": "Yellow", "icons": ["", "Light Bulb", "Clock", "Light Bulb"], "dogma_effects": [], "dogma_icon": "Light Bulb"}
evolution = {"name": "Evolution", "age": 7, "color": "Green", "icons": ["", "Leaf", "Leaf", "Clock"], "dogma_effects": [], "dogma_icon": "Leaf"}
publications = {"name": "Publications", "age": 7, "color": "Blue", "icons": ["", "Light Bulb", "Light Bulb", "Leaf"], "dogma_effects": [], "dogma_icon": "Light Bulb"}
lighting = {"name": "Lighting", "age": 7, "color": "Red", "icons": ["", "Light Bulb", "Clock", "Clock"], "dogma_effects": [], "dogma_icon": "Light Bulb"}
railroad = {"name": "Railroad", "age": 7, "color": "Purple", "icons": ["", "Factory", "Clock", "Clock"], "dogma_effects": [], "dogma_icon": "Factory"}
flight = {"name": "Flight", "age": 8, "color": "Red", "icons": ["", "Factory", "Clock", "Clock"], "dogma_effects": [], "dogma_icon": "Factory"}
antibiotics = {"name": "Antibiotics", "age": 8, "color": "Green", "icons": ["", "Leaf", "Light Bulb", "Clock"], "dogma_effects": [], "dogma_icon": "Leaf"}
corporations = {"name": "Corporations", "age": 8, "color": "Yellow", "icons": ["", "Factory", "Clock", "Crown"], "dogma_effects": [], "dogma_icon": "Factory"}
quantum_theory = {"name": "Quantum Theory", "age": 8, "color": "Blue", "icons": ["", "Light Bulb", "Light Bulb", "Clock"], "dogma_effects": [], "dogma_icon": "Light Bulb"}
empiricism = {"name": "Empiricism", "age": 8, "color": "Green", "icons": ["", "Light Bulb", "Light Bulb", "Leaf"], "dogma_effects": [], "dogma_icon": "Light Bulb"}
mobility = {"name": "Mobility", "age": 8, "color": "Purple", "icons": ["", "Factory", "Clock", "Clock"], "dogma_effects": [], "dogma_icon": "Factory"}
skyscrapers = {"name": "Skyscrapers", "age": 8, "color": "Red", "icons": ["", "Factory", "Clock", "Clock"], "dogma_effects": [], "dogma_icon": "Factory"}
mass_media = {"name": "Mass Media", "age": 8, "color": "Yellow", "icons": ["", "Light Bulb", "Clock", "Leaf"], "dogma_effects": [], "dogma_icon": "Light Bulb"}
rocketry = {"name": "Rocketry", "age": 8, "color": "Blue", "icons": ["", "Light Bulb", "Clock", "Factory"], "dogma_effects": [], "dogma_icon": "Light Bulb"}
socialism = {"name": "Socialism", "age": 8, "color": "Purple", "icons": ["", "Crown", "Crown", "Clock"], "dogma_effects": [], "dogma_icon": "Crown"}
composites = {"name": "Composites", "age": 9, "color": "Red", "icons": ["", "Factory", "Clock", "Clock"], "dogma_effects": [], "dogma_icon": "Factory"}
fission = {"name": "Fission", "age": 9, "color": "Yellow", "icons": ["", "Light Bulb", "Light Bulb", "Clock"], "dogma_effects": [], "dogma_icon": "Light Bulb"}
ecology = {"name": "Ecology", "age": 9, "color": "Green", "icons": ["", "Leaf", "Leaf", "Clock"], "dogma_effects": [], "dogma_icon": "Leaf"}
suburbia = {"name": "Suburbia", "age": 9, "color": "Purple", "icons": ["", "Factory", "Clock", "Leaf"], "dogma_effects": [], "dogma_icon": "Factory"}
collaboration = {"name": "Collaboration", "age": 9, "color": "Red", "icons": ["", "Light Bulb", "Crown", "Clock"], "dogma_effects": [], "dogma_icon": "Light Bulb"}
satellites = {"name": "Satellites", "age": 9, "color": "Purple", "icons": ["", "Light Bulb", "Clock", "Factory"], "dogma_effects": [], "dogma_icon": "Light Bulb"}
computers = {"name": "Computers", "age": 9, "color": "Green", "icons": ["", "Light Bulb", "Factory", "Clock"], "dogma_effects": [], "dogma_icon": "Clock"}
genetics = {"name": "Genetics", "age": 9, "color": "Blue", "icons": ["", "Leaf", "Light Bulb", "Clock"], "dogma_effects": [], "dogma_icon": "Leaf"}
services = {"name": "Services", "age": 9, "color": "Yellow", "icons": ["", "Crown", "Clock", "Light Bulb"], "dogma_effects": [], "dogma_icon": "Crown"}
specialization = {"name": "Specialization", "age": 9, "color": "Blue", "icons": ["", "Light Bulb", "Factory", "Clock"], "dogma_effects": [], "dogma_icon": "Light Bulb"}
miniaturization = {"name": "Miniaturization", "age": 10, "color": "Yellow", "icons": ["", "Factory", "Clock", "Light Bulb"], "dogma_effects": [], "dogma_icon": "Factory"}
robotics = {"name": "Robotics", "age": 10, "color": "Green", "icons": ["", "Factory", "Clock", "Clock"], "dogma_effects": [], "dogma_icon": "Clock"}
globalization = {"name": "Globalization", "age": 10, "color": "Red", "icons": ["", "Crown", "Clock", "Factory"], "dogma_effects": [], "dogma_icon": "Crown"}
stem_cells = {"name": "Stem Cells", "age": 10, "color": "Purple", "icons": ["", "Leaf", "Light Bulb", "Clock"], "dogma_effects": [], "dogma_icon": "Leaf"}
databases = {"name": "Databases", "age": 10, "color": "Red", "icons": ["", "Light Bulb", "Clock", "Leaf"], "dogma_effects": [], "dogma_icon": "Light Bulb"}
self_service = {"name": "Self Service", "age": 10, "color": "Yellow", "icons": ["", "Crown", "Clock", "Factory"], "dogma_effects": [], "dogma_icon": "Crown"}
bioengineering = {"name": "Bioengineering", "age": 10, "color": "Green", "icons": ["", "Leaf", "Light Bulb", "Clock"], "dogma_effects": [], "dogma_icon": "Leaf"}
software = {"name": "Software", "age": 10, "color": "Blue", "icons": ["", "Light Bulb", "Clock", "Clock"], "dogma_effects": [], "dogma_icon": "Clock"}
ai = {"name": "A.I.", "age": 10, "color": "Blue", "icons": ["", "Light Bulb", "Clock", "Clock"], "dogma_effects": [], "dogma_icon": "Clock"}
the_internet = {"name": "The Internet", "age": 10, "color": "Purple", "icons": ["", "Light Bulb", "Clock", "Clock"], "dogma_effects": [], "dogma_icon": "Light Bulb"}

