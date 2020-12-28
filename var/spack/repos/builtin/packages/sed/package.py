# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Sed(AutotoolsPackage, GNUMirrorPackage):
    """GNU implementation of the famous stream editor."""
    homepage = "http://www.gnu.org/software/sed/"
    gnu_mirror_path = "sed/sed-4.2.2.tar.bz2"

    version('4.2.2', sha256='f048d1838da284c8bc9753e4506b85a1e0cc1ea8999d36f6995bcb9460cddbd7')
