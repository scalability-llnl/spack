# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from datetime import date

import spack.projections
import spack.spec


def test_projection_expansion(mock_packages, monkeypatch):
    """Test that env variables and spack config variables are expanded in projections"""

    monkeypatch.setenv("FOO_ENV_VAR", "test-string")
    projections = {"all": "{name}-{version}/$FOO_ENV_VAR/$date"}
    spec = spack.spec.Spec("fake@1.0")
    projection = spack.projections.get_projection(projections, spec)
    assert "{name}-{version}/test-string/%s" % date.today().strftime("%Y-%m-%d") == projection
