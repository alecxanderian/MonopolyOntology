# monopoly_cli.py
from pathlib import Path
from owlready2 import get_ontology, sync_reasoner_pellet


OWL_FILENAME = "monopoly_board_game_ontology.owl"


def load_ontology():
    """
    Load the OWL ontology from the same folder as this script.
    Uses a plain Windows path string instead of as_uri() to avoid
    Windows path/URI issues.
    """
    script_dir = Path(__file__).resolve().parent
    owl_path = script_dir / OWL_FILENAME

    if not owl_path.exists():
        raise FileNotFoundError(
            f"Could not find OWL file at: {owl_path}\n"
            f"Make sure '{OWL_FILENAME}' is in the same folder as this script."
        )

    onto = get_ontology(str(owl_path)).load()

    # Pellet is often easier with Owlready2 on Windows than Java/HermiT setups.
    # infer_property_values=True helps bring in inferred object properties.
    try:
        with onto:
            sync_reasoner_pellet(
                infer_property_values=True,
                infer_data_property_values=True
            )
    except Exception as e:
        print("\n[Warning] Reasoner could not run.")
        print("The ontology still loaded, but answers will use asserted facts only.")
        print(f"Reasoner error: {e}\n")

    return onto


def entity_name(entity):
    """
    Return the nicest display name available.
    Prefer rdfs:label, then .name.
    """
    try:
        if hasattr(entity, "label") and entity.label:
            return str(entity.label[0])
    except Exception:
        pass

    return getattr(entity, "name", str(entity))


def format_list(items):
    names = sorted(entity_name(x) for x in items)
    if not names:
        return "None"
    return ", ".join(names)


def get_class(onto, class_name):
    return getattr(onto, class_name, None)


def get_player_by_name(onto, player_name):
    """
    Try multiple ways to find a player by entered text.
    Matches against OWL individual name and label.
    """
    player_class = get_class(onto, "Player")
    if player_class is None:
        return None

    target = player_name.strip().lower()

    for player in player_class.instances():
        if player.name.lower() == target:
            return player
        if hasattr(player, "label"):
            for lbl in player.label:
                if str(lbl).strip().lower() == target:
                    return player

    return None


def ask_owned_properties(onto, player_name):
    player = get_player_by_name(onto, player_name)
    if player is None:
        return f"Player '{player_name}' not found in the ontology."

    owned = list(getattr(player, "owns", []))
    if not owned:
        return f"{entity_name(player)} owns no properties in the ontology."

    return f"{entity_name(player)} owns: {format_list(owned)}"


def ask_players_in_jail(onto):
    player_class = get_class(onto, "Player")
    if player_class is None:
        return "Player class not found."

    players_in_jail = []

    for player in player_class.instances():
        # Prefer direct boolean if present in ontology
        is_in_jail_vals = list(getattr(player, "isInJail", []))
        if any(bool(v) for v in is_in_jail_vals):
            players_in_jail.append(player)
            continue

        # Fallback: check currentSpace against Jail individual/class
        current_spaces = list(getattr(player, "currentSpace", []))
        for space in current_spaces:
            if space.name == "Jail":
                players_in_jail.append(player)
                break
            if hasattr(space, "is_a"):
                for cls in space.is_a:
                    if getattr(cls, "name", "") == "JailSpace":
                        players_in_jail.append(player)
                        break

    if not players_in_jail:
        return "No players in jail were found."

    return f"Players in jail: {format_list(players_in_jail)}"


def ask_monopoly_holders(onto):
    player_class = get_class(onto, "Player")
    if player_class is None:
        return "Player class not found."

    holders = []
    for player in player_class.instances():
        monopolies = list(getattr(player, "hasMonopoly", []))
        if monopolies:
            holders.append((player, monopolies))

    if not holders:
        return "No players with a monopoly were found."

    lines = []
    for player, groups in holders:
        lines.append(f"{entity_name(player)} has monopoly on: {format_list(groups)}")
    return "\n".join(lines)


def ask_bankrupt_players(onto):
    player_class = get_class(onto, "Player")
    if player_class is None:
        return "Player class not found."

    bankrupt = []
    for player in player_class.instances():
        vals = list(getattr(player, "isBankrupt", []))
        if any(bool(v) for v in vals):
            bankrupt.append(player)

    if not bankrupt:
        return "No bankrupt players were found."

    return f"Bankrupt players: {format_list(bankrupt)}"


def ask_mortgaged_properties(onto):
    ownable_class = get_class(onto, "OwnableSpace")
    if ownable_class is None:
        return "OwnableSpace class not found."

    mortgaged = []
    for space in ownable_class.instances():
        vals = list(getattr(space, "isMortgaged", []))
        if any(bool(v) for v in vals):
            mortgaged.append(space)

    if not mortgaged:
        return "No mortgaged properties were found."

    return f"Mortgaged properties: {format_list(mortgaged)}"


def ask_purchasable_properties(onto):
    space_class = get_class(onto, "Space")
    if space_class is None:
        return "Space class not found."

    purchasable = []
    for space in space_class.instances():
        vals = list(getattr(space, "isPurchasable", []))
        if any(bool(v) for v in vals):
            purchasable.append(space)

    if not purchasable:
        return "No purchasable properties were found."

    return f"Purchasable spaces: {format_list(purchasable)}"


def ask_buildable_properties(onto):
    space_class = get_class(onto, "Space")
    if space_class is None:
        return "Space class not found."

    buildable = []
    for space in space_class.instances():
        vals = list(getattr(space, "isBuildable", []))
        if any(bool(v) for v in vals):
            buildable.append(space)

    if not buildable:
        return "No buildable properties were found."

    return f"Buildable properties: {format_list(buildable)}"


def ask_rent_for_property(onto, property_name):
    """
    Uses baseRent because that is what currently exists in your ontology.
    """
    target = property_name.strip().lower()

    ownable_class = get_class(onto, "OwnableSpace")
    if ownable_class is None:
        return "OwnableSpace class not found."

    for space in ownable_class.instances():
        names_to_check = [space.name.lower()]
        if hasattr(space, "label"):
            names_to_check.extend(str(lbl).strip().lower() for lbl in space.label)

        if target in names_to_check:
            rents = list(getattr(space, "baseRent", []))
            if rents:
                return f"Base rent for {entity_name(space)} is {rents[0]}."
            return f"{entity_name(space)} was found, but no base rent is stored."

    return f"Property '{property_name}' not found."


def print_menu():
    print("\nMonopoly Ontology CLI")
    print("-" * 30)
    print("1) What properties does a player own?")
    print("2) Which players are in jail?")
    print("3) Which players have a monopoly?")
    print("4) Which players are bankrupt?")
    print("5) Which properties are mortgaged?")
    print("6) Which properties can be purchased?")
    print("7) Which properties can have housing on them?")
    print("8) How much rent must be paid for a property?")
    print("9) Exit")


def main():
    try:
        onto = load_ontology()
    except Exception as e:
        print(f"Failed to load ontology: {e}")
        return

    while True:
        print_menu()
        choice = input("\nChoose an option: ").strip()

        if choice == "1":
            player_name = input("Enter player name: ").strip()
            print(ask_owned_properties(onto, player_name))

        elif choice == "2":
            print(ask_players_in_jail(onto))

        elif choice == "3":
            print(ask_monopoly_holders(onto))

        elif choice == "4":
            print(ask_bankrupt_players(onto))

        elif choice == "5":
            print(ask_mortgaged_properties(onto))

        elif choice == "6":
            print(ask_purchasable_properties(onto))

        elif choice == "7":
            print(ask_buildable_properties(onto))

        elif choice == "8":
            property_name = input("Enter property name: ").strip()
            print(ask_rent_for_property(onto, property_name))

        elif choice == "9":
            print("Exiting Monopoly Ontology CLI.")
            break

        else:
            print("Invalid option. Please choose 1-9.")


if __name__ == "__main__":
    main()