# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlSwissknife(PerlPackage):
    """An object-oriented Perl library to handle Swiss-Prot entries"""

    homepage = "http://swissknife.sourceforge.net"
    url      = "https://downloads.sourceforge.net/project/swissknife/swissknife/1.75/Swissknife_1.75.tar.gz"

    version('1.75', sha256='3d9af0d71366c90698488f6dae54118e6a4dba087b3c33d1bfa8245663cba53a')

    depends_on('perl-module-build', type='build')
