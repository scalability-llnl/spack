# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Colordiff(Package):
    """Colorful diff utility."""

    homepage = "https://www.colordiff.org"
    url      = "https://www.colordiff.org/archive/colordiff-1.0.18.tar.gz"

    version('1.0.18', sha256='29cfecd8854d6e19c96182ee13706b84622d7b256077df19fbd6a5452c30d6e0')

    depends_on('perl')

    def install(self, spec, prefix):
        make("INSTALL_DIR=" + prefix.bin, "ETC_DIR=" + prefix.etc,
             "MAN_DIR=" + prefix.man, 'install', parallel=False)
