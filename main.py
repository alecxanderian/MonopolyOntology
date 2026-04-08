from menus import modify_menu, print_main_menu, questions_menu, view_save_menu
from ontology_io import load_ontology

def main():
    try:
        onto, owl_path = load_ontology()
    except Exception as e:
        print(f"Failed to load ontology: {e}")
        return

    print(f"Loaded ontology from: {owl_path}")

    while True:
        print_main_menu()
        choice = input("\nChoose an option: ").strip()

        if choice == "1":
            questions_menu(onto)
        elif choice == "2":
            modify_menu(onto)
        elif choice == "3":
            view_save_menu(onto, owl_path)
        elif choice == "4":
            print("Exiting Monopoly Ontology CLI.")
            break
        else:
            print("Invalid option.")


if __name__ == "__main__":
    main()
