# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Constype(AutotoolsPackage, XorgPackage):
    """constype prints on the standard output the Sun code for the type of
    display that the specified device is.

    It was originally written for SunOS, but has been ported to other
    SPARC OS'es and to Solaris on both SPARC & x86."""

    homepage = "http://cgit.freedesktop.org/xorg/app/constype"
    xorg_mirror_path = "app/constype-1.0.4.tar.gz"

    version('1.0.4', sha256='ec09aff369cf1d527fd5b8075fb4dd0ecf89d905190cf1a0a0145d5e523f913d')

    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
