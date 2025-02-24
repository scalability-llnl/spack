# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class MirrorGnu(AutotoolsPackage, GNUMirrorPackage):
    """Simple GNU package"""

    homepage = "https://www.gnu.org/software/make/"
    gnu_mirror_path = "make/make-4.2.1.tar.gz"

    version("4.2.1", sha256="e40b8f018c1da64edd1cc9a6fce5fa63b2e707e404e20cad91fbae337c98a5b7")
