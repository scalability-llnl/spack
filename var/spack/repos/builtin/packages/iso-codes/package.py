# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class IsoCodes(AutotoolsPackage):
    """ISO-codes provides lists of various ISO standards"""

    homepage = "https://salsa.debian.org/iso-codes-team/iso-codes"
    url      = "https://deb.debian.org/debian/pool/main/i/iso-codes/iso-codes_4.3.orig.tar.xz"

    version('4.3', sha256='643eb83b2d714e8650ed7112706968d057bf5b101ba71c8ef219e20f1737b141')

    depends_on('m4', type='build')
    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool', type='build')
    depends_on('gettext', type='build')
    depends_on('python@3:', type='build')
