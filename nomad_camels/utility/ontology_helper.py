from pathlib import Path
from owlready2 import get_ontology, sync_reasoner
from functools import lru_cache

from nomad_camels.utility import variables_handling


EXPERIMENTAL_TECHNIQUES_ONTOLOGY_PREF = "experimental_techniques_ontology_path"

SUPPORTED_ONTOLOGY_SUFFIXES = {
    ".owl",
    ".rdf",
    ".ttl",
    ".xml",
}


def get_configured_ontology_path():
    """Return the ontology path configured in the global CAMELS preferences."""
    preferences = getattr(variables_handling, "preferences", {}) or {}
    path = preferences.get(EXPERIMENTAL_TECHNIQUES_ONTOLOGY_PREF, "")
    return str(path).strip()


def get_effective_ontology_path(ontology_path=None):
    """
    Return a resolved ontology path or None.

    If ontology_path is None, use the ontology path configured in the global
    CAMELS settings. This intentionally does not silently fall back to a bundled
    ontology, because the semantic-mapping UI should only become available
    after explicit user configuration.
    """
    raw_path = ontology_path or get_configured_ontology_path()
    if not raw_path:
        return None
    path = Path(raw_path).expanduser().resolve()
    if not path.exists() or not path.is_file():
        return None
    return path


def ontology_path_is_valid(ontology_path=None, require_loadable=False):
    """
    Return True if the ontology path exists and, optionally, can be loaded.
    """
    path = get_effective_ontology_path(ontology_path)
    if path is None:
        return False
    if path.suffix.lower() not in SUPPORTED_ONTOLOGY_SUFFIXES:
        return False
    if require_loadable:
        try:
            load_local_ontology(str(path), run_reasoner=False)
        except Exception:
            return False
    return True


def semantic_mapping_available():
    """Return True if semantic mapping can be used in the GUI."""
    return ontology_path_is_valid(require_loadable=True)


def load_local_ontology(ontology_path=None, run_reasoner=False):
    """
    Load and return the configured Experimental Techniques ontology.
    If no explicit ontology_path is passed, the global CAMELS preference
    'experimental_techniques_ontology_path' is used.
    """
    path = get_effective_ontology_path(ontology_path)
    if path is None:
        raise FileNotFoundError(
            "No valid Experimental Techniques Ontology path configured. "
            "Set it in the CAMELS settings first."
        )
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
            {
                "name": parent_class.name,
                "iri": getattr(parent_class, "iri", ""),
                "children": [],
            }
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
            ],
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
    path = get_effective_ontology_path(ontology_path)
    if path is None:
        return []
    return list(_get_physical_quantities_cached(str(path), class_name))


def semantic_mapping_enabled_for_protocol(protocol):
    """Return True if semantic mapping should be shown for this protocol."""
    return bool(
        protocol is not None
        and getattr(protocol, "semantic_mapping_enabled", False)
        and semantic_mapping_available()
    )


def get_protocol_physical_quantity_options(protocol):
    """Return physical quantity options for the protocol's selected experiment."""
    if not semantic_mapping_enabled_for_protocol(protocol):
        return []
    experiment_class = getattr(protocol, "experiment_ontology_class", "")
    if not experiment_class:
        return []
    try:
        return get_physical_quantities(class_name=experiment_class)
    except Exception:
        return []


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
    _collect_quantity_targets_from_expression(
        cls, "relatesToQuantity", quantities, set()
    )
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
