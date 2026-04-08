# ProjectCS455
Ontology Project - Monopoly Game

Current packages required:

Python: owlready2


Monopoly CLI split into modules

Files:
- config.py: filename configuration
- utils.py: generic helpers
- ontology_io.py: load/save ontology
- ontology_lookup.py: class and individual lookup helpers
- state_helpers.py: ownership/bank helper functions
- queries.py: competency-question query functions
- modify.py: functions that edit ontology state
- menus.py: all CLI menu display and routing
- main.py: main application loop
- run_monopoly_cli.py: launcher script

How to run:
1. Keep monopoly_board_game_ontology_modified.owl next to these files
2. Run:
   python run_monopoly_cli.py
