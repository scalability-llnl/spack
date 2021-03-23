# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import spack.repo
from spack.util.mock_package import MockPackageMultiRepo


def test_mock_package_possible_dependencies():
    mock_repo = MockPackageMultiRepo()
    e = mock_repo.add_package('e')
    d = mock_repo.add_package('d', [e])
    c = mock_repo.add_package('c', [d])
    b = mock_repo.add_package('b', [d])
    a = mock_repo.add_package('a', [b, c])

    with spack.repo.use_repositories(mock_repo):
        assert set(a.possible_dependencies()) == set(['a', 'b', 'c', 'd', 'e'])
        assert set(b.possible_dependencies()) == set(['b', 'd', 'e'])
        assert set(c.possible_dependencies()) == set(['c', 'd', 'e'])
        assert set(d.possible_dependencies()) == set(['d', 'e'])
        assert set(e.possible_dependencies()) == set(['e'])

        assert set(
            a.possible_dependencies(transitive=False)) == set(['a', 'b', 'c'])
        assert set(
            b.possible_dependencies(transitive=False)) == set(['b', 'd'])
        assert set(
            c.possible_dependencies(transitive=False)) == set(['c', 'd'])
        assert set(
            d.possible_dependencies(transitive=False)) == set(['d', 'e'])
        assert set(
            e.possible_dependencies(transitive=False)) == set(['e'])


def test_mock_repo_is_virtual():
    mock_repo = MockPackageMultiRepo()

    # current implementation is always false
    assert mock_repo.is_virtual("foo") is False
    assert mock_repo.is_virtual("bar") is False
    assert mock_repo.is_virtual("baz") is False
