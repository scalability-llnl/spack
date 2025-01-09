# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *
from spack.pkg.builtin.mock.variant_values import VariantValues


class VariantValuesOverride(VariantValues):
    """Test variant value validation with multiple definitions."""

    variant("v", default="baz", values=["bar", "baz"])
