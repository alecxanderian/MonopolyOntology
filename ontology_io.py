from pathlib import Path
from owlready2 import get_ontology
from config import OWL_FILENAME


def load_ontology():
    script_dir = Path(__file__).resolve().parent
    owl_path = script_dir / OWL_FILENAME

    if not owl_path.exists():
        raise FileNotFoundError(
            f"Could not find {OWL_FILENAME} in the same folder as this script.\n"
            f"Expected path: {owl_path}"
        )

    onto = get_ontology(str(owl_path)).load()
    return onto, owl_path


def save_ontology(onto, path):
    onto.save(file=str(path), format="rdfxml")
