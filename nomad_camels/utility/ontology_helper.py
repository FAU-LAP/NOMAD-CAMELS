from pathlib import Path
from owlready2 import get_ontology, sync_reasoner
from functools import lru_cache



DEFAULT_ONTOLOGY_PATH = (
    Path(__file__).parent.parent.parent / "external/LAP-ET-ontology/LAP_ET.owl"
)



def load_local_ontology(ontology_path=None, run_reasoner=False):
    """
    Load and return the ontology object.
    The ontology is cached because GUI widgets may request the same ontology
    repeatedly while rebuilding semantic dropdowns.
    """
    path = Path(ontology_path) if ontology_path else DEFAULT_ONTOLOGY_PATH
    path = path.expanduser().resolve()
    if not path.exists():
        raise FileNotFoundError(f"Ontology file not found: {path}")
    return _load_local_ontology_cached(str(path), bool(run_reasoner))


@lru_cache(maxsize=4)
def _load_local_ontology_cached(path, run_reasoner):
    ontology = get_ontology(path).load()
    if run_reasoner:
        try:
            sync_reasoner([ontology], infer_property_values=True)
        except Exception:
            # Java-based reasoners are not always available in every environment.
            # Fall back to the asserted ontology if reasoning cannot run.
            pass
    return ontology


def nice_name(obj):
    if hasattr(obj, "name"):
        return obj.name
    return str(obj)

def ontology_object_to_label_iri(obj):
    """Return a human-readable label and stable IRI for an ontology object."""
    return nice_name(obj), getattr(obj, "iri", "")


def subclass_tree_as_list(ontology_path=None):
    ontology = load_local_ontology(ontology_path, run_reasoner=True)
    parent_class = ontology["LAPExperiment"]

    return _class_tree_as_list(parent_class, visited=set())


def _class_tree_as_list(parent_class, visited=None):
    if visited is None:
        visited = set()

    if parent_class in visited:
        return [
            {"name": parent_class.name,
             "iri": getattr(parent_class, "iri", ""),
             "children": []}
        ]

    visited.add(parent_class)

    return [
        {
            "name": parent_class.name,
            "iri": getattr(parent_class, "iri", ""),
            "children": [
                child
                for subcls in parent_class.subclasses()
                for child in _class_tree_as_list(subcls, visited)
            ]
        }
    ]


def get_physical_quantities(ontology_path=None, class_name=None):
    """
    Get the physical quantities associated with a class.
    The ontology is reasoned first when possible so inferred restrictions are
    visible in the class expressions we inspect.
    """
    if not class_name:
        return []
    path = Path(ontology_path) if ontology_path else DEFAULT_ONTOLOGY_PATH
    path = path.expanduser().resolve()
    if not path.exists():
        raise FileNotFoundError(f"Ontology file not found: {path}")
    return list(_get_physical_quantities_cached(str(path), class_name))

@lru_cache(maxsize=128)
def _get_physical_quantities_cached(ontology_path, class_name):
    ontology = load_local_ontology(ontology_path, run_reasoner=True)
    experiment_class = ontology[class_name]
    if not experiment_class:
        return tuple()
    quantities = _get_class_physical_quantities(experiment_class)
    return tuple(
        sorted(
            {ontology_object_to_label_iri(quantity) for quantity in quantities},
            key=lambda option: option[0],
        )
    )

def _get_class_physical_quantities(cls):
    quantities = set()
    _collect_quantity_targets_from_expression(cls, "relatesToQuantity", quantities, set())
    return quantities


def _collect_quantity_targets_from_expression(expr, property_name, results, visited):
    if expr is None:
        return

    marker = id(expr)
    if marker in visited:
        return
    visited.add(marker)

    property_obj = getattr(expr, "property", None)
    if getattr(property_obj, "name", None) == property_name:
        value = getattr(expr, "value", None)
        if value is not None:
            results.add(value)

    for subexpr in getattr(expr, "Classes", []):
        _collect_quantity_targets_from_expression(subexpr, property_name, results, visited)

    nested_class = getattr(expr, "Class", None)
    if nested_class is not None:
        _collect_quantity_targets_from_expression(nested_class, property_name, results, visited)

    if hasattr(expr, "is_a") and hasattr(expr, "equivalent_to") and not hasattr(expr, "property"):
        for parent in expr.is_a:
            _collect_quantity_targets_from_expression(parent, property_name, results, visited)
        for parent in expr.equivalent_to:
            _collect_quantity_targets_from_expression(parent, property_name, results, visited)
