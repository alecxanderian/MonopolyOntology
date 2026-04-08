from ontology_lookup import all_instances


def remove_from_all_players(space, onto):
    for player in all_instances(onto, "Player"):
        if hasattr(player, "owns") and space in list(player.owns):
            player.owns.remove(space)


def remove_from_bank(space, onto):
    for bank in all_instances(onto, "Bank"):
        if hasattr(bank, "bankHolds") and space in list(bank.bankHolds):
            bank.bankHolds.remove(space)


def add_to_bank(space, onto):
    banks = all_instances(onto, "Bank")
    if banks:
        bank = banks[0]
        if space not in list(bank.bankHolds):
            bank.bankHolds.append(space)
