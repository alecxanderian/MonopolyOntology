from modify import (
    buy_property,
    create_player,
    give_monopoly,
    mortgage_property,
    move_player,
    set_bankrupt_status,
    set_jail_status,
)
from ontology_io import save_ontology
from queries import (
    ask_bankrupt_players,
    ask_buildable_properties,
    ask_monopoly_holders,
    ask_mortgaged_properties,
    ask_owned_properties,
    ask_players_in_jail,
    ask_purchasable_properties,
    ask_rent_for_property,
    list_players,
)


def print_main_menu():
    print("\n" + "=" * 42)
    print("           Monopoly Ontology CLI")
    print("=" * 42)
    print("1) Ask competency questions")
    print("2) Modify game state")
    print("3) View / save")
    print("4) Exit")


def print_questions_menu():
    print("\n--- Ask Competency Questions ---")
    print("1) What properties does a player own?")
    print("2) Which players are in jail?")
    print("3) Which players have a monopoly?")
    print("4) Which players are bankrupt?")
    print("5) Which properties are mortgaged?")
    print("6) Which properties can be purchased?")
    print("7) Which properties can have housing on them?")
    print("8) How much rent must be paid for a property?")
    print("9) Back")


def print_modify_menu():
    print("\n--- Modify Game State ---")
    print("1) Create a player")
    print("2) Move player to a space")
    print("3) Buy / assign a property to a player")
    print("4) Mortgage / unmortgage a property")
    print("5) Set player jail status")
    print("6) Set player bankruptcy status")
    print("7) Give a player a monopoly")
    print("8) Back")


def print_view_save_menu():
    print("\n--- View / Save ---")
    print("1) List players")
    print("2) Save ontology")
    print("3) Back")


def questions_menu(onto):
    while True:
        print_questions_menu()
        choice = input("\nChoose a question option: ").strip()

        if choice == "1":
            player_name = input("Player name: ").strip()
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
            property_name = input("Property name: ").strip()
            print(ask_rent_for_property(onto, property_name))
        elif choice == "9":
            break
        else:
            print("Invalid option.")


def modify_menu(onto):
    while True:
        print_modify_menu()
        choice = input("\nChoose a modify option: ").strip()

        if choice == "1":
            name = input("New player name: ").strip()
            cash = input("Starting cash (default 1500): ").strip()
            cash = int(cash) if cash else 1500
            print(create_player(onto, name, cash))
        elif choice == "2":
            player = input("Player name: ").strip()
            space = input("Space name: ").strip()
            print(move_player(onto, player, space))
        elif choice == "3":
            player = input("Player name: ").strip()
            prop = input("Property name: ").strip()
            print(buy_property(onto, player, prop))
        elif choice == "4":
            prop = input("Property name: ").strip()
            value = input("Mortgage? (true/false): ").strip().lower() == "true"
            print(mortgage_property(onto, prop, value))
        elif choice == "5":
            player = input("Player name: ").strip()
            value = input("In jail? (true/false): ").strip().lower() == "true"
            print(set_jail_status(onto, player, value))
        elif choice == "6":
            player = input("Player name: ").strip()
            value = input("Bankrupt? (true/false): ").strip().lower() == "true"
            print(set_bankrupt_status(onto, player, value))
        elif choice == "7":
            player = input("Player name: ").strip()
            group = input("Property group name: ").strip()
            print(give_monopoly(onto, player, group))
        elif choice == "8":
            break
        else:
            print("Invalid option.")


def view_save_menu(onto, owl_path):
    while True:
        print_view_save_menu()
        choice = input("\nChoose a view/save option: ").strip()

        if choice == "1":
            print(list_players(onto))
        elif choice == "2":
            save_ontology(onto, owl_path)
            print(f"Ontology saved to {owl_path}")
        elif choice == "3":
            break
        else:
            print("Invalid option.")
