# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlAlienBuild(PerlPackage):
    """This module provides tools for building external (non-CPAN) dependencies
    for CPAN. It is mainly designed to be used at install time of a CPAN
    client, and work closely with Alien::Base which is used at runtime."""

    homepage = "https://metacpan.org/pod/Alien::Build"
    url      = "https://cpan.metacpan.org/authors/id/P/PL/PLICEASE/Alien-Build-1.86.tar.gz"

    version('1.86', sha256='f856a46aea72fe77daea5b1788b4ea0dc215f5704f5a35fa063171be8523e4e9')

    depends_on('perl-capture-tiny', type=('build', 'run'))
    depends_on('perl-ffi-checklib', type=('build', 'run'))
    depends_on('perl-file-which', type=('build', 'run'))
    depends_on('perl-file-chdir', type=('build', 'run'))
    depends_on('perl-path-tiny', type=('build', 'run'))
