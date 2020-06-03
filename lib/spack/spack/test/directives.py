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


def test_same_version_as(config, mock_packages):
    # check that every version of the wrapper depends on the corresponding
    # major version of the wrappee

    pkg = spack.repo.get("same_version_as_wrapper")

    for ver in pkg.versions:
        spec = pkg.spec.constrained("@{0}".format(ver))
        spec.concretize()
        deps = spec.dependencies()

        assert len(deps) == 1
        assert deps[0].version.up_to(1) == ver.up_to(1)
