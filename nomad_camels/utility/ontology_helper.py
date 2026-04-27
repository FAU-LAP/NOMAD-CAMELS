from pathlib import Path
from owlready2 import get_ontology



DEFAULT_ONTOLOGY_PATH = (
    Path(__file__).parent.parent.parent / "external/LAP-ET-ontology/LAP_ET.owl"
)



def load_local_ontology(ontology_path=None):
    """
    Load and return the ontology object.
    """

    path = Path(ontology_path) if ontology_path else DEFAULT_ONTOLOGY_PATH
    path = path.expanduser().resolve()

    if not path.exists():
        raise FileNotFoundError(f"Ontology file not found: {path}")

    return get_ontology(str(path)).load()


def subclass_tree_as_list(ontology_path=None):
    ontology = load_local_ontology(ontology_path)
    parent_class = ontology["LAPExperiment"]

    return _class_tree_as_list(parent_class, visited=set())


def _class_tree_as_list(parent_class, visited=None):
    if visited is None:
        visited = set()

    if parent_class in visited:
        return [
            {"name": parent_class.name, "children": []}
        ]

    visited.add(parent_class)

    return [
        {
            "name": parent_class.name,
            "children": [
                child
                for subcls in parent_class.subclasses()
                for child in _class_tree_as_list(subcls, visited)
            ]
        }
    ]
