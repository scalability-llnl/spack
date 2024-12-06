# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import pytest

import spack.util.naming


@pytest.fixture()
def trie():
    return spack.util.naming.NamespaceTrie()


def test_add_single(trie):
    trie["foo"] = "bar"

    assert trie.is_prefix("foo")
    assert trie.has_value("foo")
    assert trie["foo"] == "bar"


def test_add_multiple(trie):
    trie["foo.bar"] = "baz"

    assert not trie.has_value("foo")
    assert trie.is_prefix("foo")

    assert trie.is_prefix("foo.bar")
    assert trie.has_value("foo.bar")
    assert trie["foo.bar"] == "baz"

    assert not trie.is_prefix("foo.bar.baz")
    assert not trie.has_value("foo.bar.baz")


def test_add_three(trie):
    # add a three-level namespace
    trie["foo.bar.baz"] = "quux"

    assert trie.is_prefix("foo")
    assert not trie.has_value("foo")

    assert trie.is_prefix("foo.bar")
    assert not trie.has_value("foo.bar")

    assert trie.is_prefix("foo.bar.baz")
    assert trie.has_value("foo.bar.baz")
    assert trie["foo.bar.baz"] == "quux"

    assert not trie.is_prefix("foo.bar.baz.quux")
    assert not trie.has_value("foo.bar.baz.quux")

    # Try to add a second element in a prefix namespace
    trie["foo.bar"] = "blah"

    assert trie.is_prefix("foo")
    assert not trie.has_value("foo")

    assert trie.is_prefix("foo.bar")
    assert trie.has_value("foo.bar")
    assert trie["foo.bar"] == "blah"

    assert trie.is_prefix("foo.bar.baz")
    assert trie.has_value("foo.bar.baz")
    assert trie["foo.bar.baz"] == "quux"

    assert not trie.is_prefix("foo.bar.baz.quux")
    assert not trie.has_value("foo.bar.baz.quux")


def test_add_none_single(trie):
    trie["foo"] = None
    assert trie.is_prefix("foo")
    assert trie.has_value("foo")
    assert trie["foo"] is None

    assert not trie.is_prefix("foo.bar")
    assert not trie.has_value("foo.bar")


def test_add_none_multiple(trie):
    trie["foo.bar"] = None

    assert trie.is_prefix("foo")
    assert not trie.has_value("foo")

    assert trie.is_prefix("foo.bar")
    assert trie.has_value("foo.bar")
    assert trie["foo.bar"] is None

    assert not trie.is_prefix("foo.bar.baz")
    assert not trie.has_value("foo.bar.baz")
