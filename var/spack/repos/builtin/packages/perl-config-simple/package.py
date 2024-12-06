# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlConfigSimple(PerlPackage):
    """Config::Simple - simple configuration file class."""

    homepage = "https://metacpan.org/pod/Config::Simple"
    url = "https://cpan.metacpan.org/authors/id/S/SH/SHERZODR/Config-Simple-4.58.tar.gz"

    license("GPL-1.0-or-later OR Artistic-1.0-Perl")

    version("4.58", sha256="dd9995706f0f9384a15ccffe116c3b6e22f42ba2e58d8f24ed03c4a0e386edb4")
