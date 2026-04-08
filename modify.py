from utils import entity_name
from ontology_lookup import all_instances, find_by_name_or_label, get_class, get_group, get_player, get_space
from state_helpers import remove_from_all_players, remove_from_bank

def create_player(onto, player_name, cash_balance=1500):
    if get_player(onto, player_name):
        return f"Player '{player_name}' already exists."

    regular_player_class = get_class(onto, "RegularPlayer")
    if regular_player_class is None:
        regular_player_class = get_class(onto, "Player")

    if regular_player_class is None:
        return "Could not find Player or RegularPlayer class in the ontology."

    safe_name = "".join(ch for ch in player_name.title().replace(" ", "") if ch.isalnum())
    if not safe_name:
        safe_name = "NewPlayer"

    player = regular_player_class(safe_name)
    player.label = [player_name]
    player.cashBalance = [int(cash_balance)]
    player.isInJail = [False]
    player.isBankrupt = [False]

    go_space = get_space(onto, "Go")
    if go_space:
        player.currentSpace = [go_space]

    return f"Created player: {entity_name(player)}"


def move_player(onto, player_name, space_name):
    player = get_player(onto, player_name)
    if not player:
        return f"Player '{player_name}' not found."

    space = get_space(onto, space_name)
    if not space:
        return f"Space '{space_name}' not found."

    player.currentSpace = [space]
    return f"Moved {entity_name(player)} to {entity_name(space)}."


def set_jail_status(onto, player_name, in_jail):
    player = get_player(onto, player_name)
    if not player:
        return f"Player '{player_name}' not found."

    player.isInJail = [bool(in_jail)]

    if bool(in_jail):
        jail = get_space(onto, "Jail")
        if jail:
            player.currentSpace = [jail]

    return f"Updated jail status for {entity_name(player)} to {bool(in_jail)}."


def set_bankrupt_status(onto, player_name, bankrupt):
    player = get_player(onto, player_name)
    if not player:
        return f"Player '{player_name}' not found."

    player.isBankrupt = [bool(bankrupt)]
    return f"Updated bankruptcy status for {entity_name(player)} to {bool(bankrupt)}."


def buy_property(onto, player_name, property_name):
    player = get_player(onto, player_name)
    if not player:
        return f"Player '{player_name}' not found."

    space = find_by_name_or_label(all_instances(onto, "OwnableSpace"), property_name)
    if not space:
        return f"Property '{property_name}' not found."

    remove_from_all_players(space, onto)
    remove_from_bank(space, onto)

    if space not in list(player.owns):
        player.owns.append(space)

    try:
        if player not in list(space.belongsTo):
            space.belongsTo.append(player)
    except Exception:
        pass

    return f"{entity_name(player)} now owns {entity_name(space)}."


def mortgage_property(onto, property_name, mortgaged):
    space = find_by_name_or_label(all_instances(onto, "OwnableSpace"), property_name)
    if not space:
        return f"Property '{property_name}' not found."

    space.isMortgaged = [bool(mortgaged)]
    return f"Updated mortgage status for {entity_name(space)} to {bool(mortgaged)}."


def give_monopoly(onto, player_name, group_name):
    player = get_player(onto, player_name)
    if not player:
        return f"Player '{player_name}' not found."

    group = get_group(onto, group_name)
    if not group:
        return f"Property group '{group_name}' not found."

    if group not in list(player.hasMonopoly):
        player.hasMonopoly.append(group)

    return f"{entity_name(player)} now has monopoly on {entity_name(group)}."
