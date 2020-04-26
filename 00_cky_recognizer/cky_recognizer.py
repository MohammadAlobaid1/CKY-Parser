#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def cky_recognize(string, grammar):
    """CKY recognizer to determine well-formedness of string.

    The string is assumed to be tokenized and lowercased already, e.g.
    ["the", "man", "water", "s", "the", "flower", "s"]
    """
    pass


def convert_grammar(grammar):
    # if you want to modify the grammar,
    # change this function
    return grammar


def convert_lexicon(lexicon):
    # if you want to modify the lexicon,
    # change this function
    return lexicon


def test_cky(sentence=None):
    """Test cky_recognize.

    You can either specify your own sentence as a string,
    or use the default test sentences.
    """
    lexicon = {
        "A": ["old", "former", "alleged", "handsome", "big", "ugly"],
        "Adv": ["very", "quickly", "allegedly", "today"],
        "Agr": ["s"],
        "Det": ["a", "the", "this", "these", "those", "some", "every"],
        "P": ["at", "on", "in", "near", "above", "below", "under"],
        "N": ["balcony", "boat", "man", "old", "woman", "singer", "opera", "water", "slide", "flower"],
        "Poss": ["'s"],
        "Vi": ["sleep", "slide", "rust", "flower"],
        "Vt": ["water", "see", "man", "like"],
        }
    grammar = (
        ("AdvP", ("Adv", "Adv")),
        ("AdvP", ("Adv", "AdvP")),
        ("AP", ("Adv", "A")),
        ("AP", ("AdvP", "A")),
        ("AP", ("Adv", "AP")),
        ("AP", ("AdvP", "AP")),
        ("D'", ("Poss", "NP")),
        ("DP", ("Det", "N")),
        ("DP", ("Det", "NP")),
        ("DP", ("DP", "D'")),
        ("N", ("N", "N")),
        ("N", ("N", "Agr")),
        ("NP", ("A", "N")),
        ("NP", ("A", "NP")),
        ("NP", ("AP", "N")),
        ("NP", ("AP", "NP")),
        ("NP", ("N", "PP")),
        ("PP", ("P", "DP")),
        ("S", ("DP", "VP")),
        ("S", ("DP", "Vi")),
        ("VP", ("Adv", "Vi")),
        ("VP", ("Adv", "VP")),
        ("VP", ("AdvP", "Vi")),
        ("VP", ("AdvP", "VP")),
        ("VP", ("Vi", "Adv")),
        ("VP", ("Vi", "AdvP")),
        ("VP", ("VP", "Adv")),
        ("VP", ("VP", "AdvP")),
        ("VP", ("Vt", "DP")),
        ("Vi", ("Vi", "Agr")),
        ("Vt", ("Vt", "Agr")),
        )
    # make any required changes to the grammar format
    lexicon = convert_lexicon(lexicon)
    grammar = convert_grammar(grammar)

    # default test sentences
    sentences = {
        "the ugly water slide s rust": True,
        "the old man the boat": True,
        "slide": False,
        "every opera singer 's water on some very very old woman 's balcony very quickly man s the boat today": True,
        "": False,
        "John sleep s": False,
        ]
    if sentence:
        return cky_recognize(sentence)
    else:
        for s, val in sentences.items():
            if cky_recognize(s.split()) != val:
                print("Wrong output!")
                print(f"The following sentence should be {val}")
                print(s)
