# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import spack.repo
from spack.spec import Spec


def test_false_directives_do_not_exist(mock_packages):
    """Ensure directives that evaluate to False at import time are added to
       dicts on packages.
    """
    cls = spack.repo.path.get_pkg_class('when-directives-false')
    assert not cls.dependencies
    assert not cls.resources
    assert not cls.patches


def test_true_directives_exist(mock_packages):
    """Ensure directives that evaluate to True at import time are added to
       dicts on packages.
    """
    cls = spack.repo.path.get_pkg_class('when-directives-true')

    assert cls.dependencies
    assert Spec() in cls.dependencies['extendee']
    assert Spec() in cls.dependencies['b']

    assert cls.resources
    assert Spec() in cls.resources

    assert cls.patches
    assert Spec() in cls.patches


def test_import_resources_zero(mock_packages):
    pkg = spack.repo.get("import-resources-zero")
    assert len(pkg.resources) == 0


def test_import_resources_one(mock_packages):
    pkg = spack.repo.get("import-resources-one")
    assert len(pkg.resources) == 1
    assert set(pkg.resources.keys()) == set([Spec()])
    assert len(pkg.resources[Spec()]) == 1


def test_import_resources_several(mock_packages):
    pkg = spack.repo.get("import-resources-several")
    assert len(pkg.resources) == 3
    assert set(pkg.resources.keys()) == set(
        [Spec(), Spec("@1"), Spec("@2.2:")])
    assert len(pkg.resources[Spec()]) == 1
    assert len(pkg.resources[Spec("@1")]) == 1
    assert len(pkg.resources[Spec("@2.2:")]) == 2


def test_import_resources_bad_json(mock_packages):
    caught_exception = None
    pkg = None
    try:
        pkg = spack.repo.get("import-resources-bad-json")
    except spack.directives.ResourcesFileError as e:
        message = str(e)
        caught_exception = True

    assert(caught_exception and "Expected exception not thrown.")
    assert("JSON" in message)
    assert(pkg is None)  # do something w/ pkg for flake8 joy


def test_import_resources_missing_file(mock_packages):
    caught_exception = None
    pkg = None
    try:
        pkg = spack.repo.get("import-resources-missing-file")
    except spack.directives.ResourcesFileError as e:
        message = str(e)
        caught_exception = True

    assert("No such file" in message)
    assert(caught_exception and "Expected exception not thrown.")
    assert(pkg is None)  # do something w/ pkg for flake8 joy
