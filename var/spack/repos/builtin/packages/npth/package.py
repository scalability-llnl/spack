# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Npth(AutotoolsPackage):
    """nPth is a library to provide the GNU Pth API and thus a
       non-preemptive threads implementation."""

    homepage = "https://gnupg.org/software/npth/index.html"
    url      = "https://gnupg.org/ftp/gcrypt/npth/npth-1.6.tar.bz2"

    version('1.6', sha256='1393abd9adcf0762d34798dc34fdcf4d0d22a8410721e76f1e3afcd1daa4e2d1')
    version('1.5', sha256='294a690c1f537b92ed829d867bee537e46be93fbd60b16c04630fbbfcd9db3c2')
    version('1.4', sha256='8915141836a3169a502d65c1ebd785fcc6d406cae5ee84474272ebf2fa96f1f2')
