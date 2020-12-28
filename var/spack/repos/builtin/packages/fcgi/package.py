# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Fcgi(AutotoolsPackage):
    """FastCGI is simple because it is actually CGI with only a few extensions.
    Like CGI, FastCGI is also language-independent. For instance, FastCGI
    provides a way to improve the performance of the thousands of Perl
    applications that have been written for the Web."""

    homepage = "https://fastcgi-archives.github.io/"
    url      = "https://github.com/FastCGI-Archives/FastCGI.com/raw/master/original_snapshot/fcgi-2.4.1-SNAP-0910052249.tar.gz"

    version('2.4.1-SNAP-0910052249', sha256='829dc89a0a372c7b0b172303ec9b42e9d20615d6d0e9fc81570fdac6c41a0f30')

    parallel = False
