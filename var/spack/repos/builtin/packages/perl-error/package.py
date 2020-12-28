# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
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
    url      = "https://cpan.metacpan.org/authors/id/S/SH/SHLOMIF/Error-0.17028.tar.gz"

    version('0.17028', sha256='3ad85c5e58b31c8903006298424a51bba39f1840e324f5ae612eabc8b935e960')

    depends_on('perl-module-build', type='build')
