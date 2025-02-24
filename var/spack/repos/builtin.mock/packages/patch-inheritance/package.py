# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *  # noqa: F401
from spack.pkg.builtin.mock.patch import Patch


class PatchInheritance(Patch):
    def install(self, spec, prefix):
        Patch.install(self, spec, prefix)
