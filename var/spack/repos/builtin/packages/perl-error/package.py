# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlError(PerlPackage):
    """The Error package provides two interfaces. Firstly Error provides a
    procedural interface to exception handling. Secondly Error is a base class
    for errors/exceptions that can either be thrown, for subsequent catch, or
    can simply be recorded."""

    homepage = "https://metacpan.org/pod/Error"
    url = "https://cpan.metacpan.org/authors/id/S/SH/SHLOMIF/Error-0.17028.tar.gz"

    license("GPL-1.0-or-later OR Artistic-1.0-Perl")

    version("0.17029", sha256="1a23f7913032aed6d4b68321373a3899ca66590f4727391a091ec19c95bf7adc")
    version("0.17028", sha256="3ad85c5e58b31c8903006298424a51bba39f1840e324f5ae612eabc8b935e960")

    depends_on("perl-module-build", type="build")
