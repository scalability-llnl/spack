# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *
from spack.pkg.builtin.mock.variant_values import VariantValues


class VariantValuesOverride(VariantValues):
    """Test variant value validation with multiple definitions."""

    variant("v", default="baz", values=["bar", "baz"])
