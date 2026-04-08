from utils import bool_value, entity_name, format_list, first_or_none
from ontology_lookup import all_instances, find_by_name_or_label, get_player

def ask_owned_properties(onto, player_name):
    player = get_player(onto, player_name)
    if not player:
        return f"Player '{player_name}' not found."

    owned = list(getattr(player, "owns", []))
    return f"{entity_name(player)} owns: {format_list(owned)}"


def ask_players_in_jail(onto):
    players = []

    for p in all_instances(onto, "Player"):
        vals = list(getattr(p, "isInJail", []))
        if any(bool_value(v) for v in vals):
            players.append(p)

    return f"Players in jail: {format_list(players)}"


def ask_monopoly_holders(onto):
    lines = []

    for p in all_instances(onto, "Player"):
        groups = list(getattr(p, "hasMonopoly", []))
        if groups:
            lines.append(f"{entity_name(p)} -> {format_list(groups)}")

    return "\n".join(lines) if lines else "No players currently have a monopoly."


def ask_bankrupt_players(onto):
    players = []

    for p in all_instances(onto, "Player"):
        vals = list(getattr(p, "isBankrupt", []))
        if any(bool_value(v) for v in vals):
            players.append(p)

    return f"Bankrupt players: {format_list(players)}"


def ask_mortgaged_properties(onto):
    spaces = []

    for s in all_instances(onto, "OwnableSpace"):
        vals = list(getattr(s, "isMortgaged", []))
        if any(bool_value(v) for v in vals):
            spaces.append(s)

    return f"Mortgaged properties: {format_list(spaces)}"


def ask_purchasable_properties(onto):
    spaces = []

    for s in all_instances(onto, "Space"):
        vals = list(getattr(s, "isPurchasable", []))
        if any(bool_value(v) for v in vals):
            spaces.append(s)

    return f"Purchasable spaces: {format_list(spaces)}"


def ask_buildable_properties(onto):
    spaces = []

    for s in all_instances(onto, "Space"):
        vals = list(getattr(s, "isBuildable", []))
        if any(bool_value(v) for v in vals):
            spaces.append(s)

    return f"Buildable properties: {format_list(spaces)}"


def ask_rent_for_property(onto, property_name):
    prop = find_by_name_or_label(all_instances(onto, "OwnableSpace"), property_name)
    if not prop:
        return f"Property '{property_name}' not found."

    rent = first_or_none(list(getattr(prop, "baseRent", [])))
    if rent is None:
        return f"{entity_name(prop)} has no base rent stored."

    return f"Base rent for {entity_name(prop)} is {rent}."


def list_players(onto):
    return "Players: " + format_list(all_instances(onto, "Player"))
