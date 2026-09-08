"""Tests for the ontology-class description helpers in ontology_helper.py.

These build a tiny in-memory owlready2 ontology directly in the test instead
of loading a real Experimental Techniques Ontology file - no such file exists
in this repo, and owlready2 supports constructing classes/annotations purely
in Python, so no fixture file is needed.
"""

from owlready2 import Thing, World

from nomad_camels.utility import ontology_helper


def make_onto():
    # A fresh World() per call, not the shared default world/get_ontology() -
    # otherwise owlready2 caches the ontology by IRI and classes/comments
    # would accumulate across test functions.
    onto = World().get_ontology("http://test.example/onto.owl")
    with onto:

        class LAPExperiment(Thing):
            pass

        class FooExperiment(LAPExperiment):
            pass

    return onto, FooExperiment


def test_class_description_returns_the_comment():
    _, cls = make_onto()
    cls.comment.append("Does the foo.")
    assert ontology_helper.class_description(cls) == "Does the foo."


def test_class_description_joins_multiple_comments():
    _, cls = make_onto()
    cls.comment.append("Does the foo.")
    cls.comment.append("Also does the bar.")
    assert ontology_helper.class_description(cls) == "Does the foo. Also does the bar."


def test_class_description_empty_when_no_comment():
    _, cls = make_onto()
    assert ontology_helper.class_description(cls) == ""


def test_get_class_description_resolves_by_iri(monkeypatch):
    onto, cls = make_onto()
    cls.comment.append("Does the foo.")
    monkeypatch.setattr(ontology_helper, "load_local_ontology", lambda *a, **k: onto)
    assert ontology_helper.get_class_description(cls.iri) == "Does the foo."


def test_get_class_description_unknown_iri(monkeypatch):
    onto, _ = make_onto()
    monkeypatch.setattr(ontology_helper, "load_local_ontology", lambda *a, **k: onto)
    assert ontology_helper.get_class_description("http://test.example/onto.owl#gone") == ""
