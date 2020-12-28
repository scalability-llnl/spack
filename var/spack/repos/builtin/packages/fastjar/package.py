# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Fastjar(AutotoolsPackage):
    """Fastjar is a version of Sun's 'jar' utility, written entirely in C."""

    homepage = "http://savannah.nongnu.org/projects/fastjar/"
    url      = "http://download.savannah.gnu.org/releases/fastjar/fastjar-0.98.tar.gz"

    version('0.98', sha256='f156abc5de8658f22ee8f08d7a72c88f9409ebd8c7933e9466b0842afeb2f145')

    depends_on('zlib')
