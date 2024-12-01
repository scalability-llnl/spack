# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class MirrorGnuBroken(AutotoolsPackage, GNUMirrorPackage):
    """Simple GNU package"""

    homepage = "https://www.gnu.org/software/make/"
    url = "https://ftpmirror.gnu.org/make/make-4.2.1.tar.gz"

    version("4.2.1", sha256="e40b8f018c1da64edd1cc9a6fce5fa63b2e707e404e20cad91fbae337c98a5b7")
