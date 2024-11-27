# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlModuleRuntimeConflicts(PerlPackage):
    """Provide information on conflicts for Module::Runtime"""

    homepage = "https://metacpan.org/pod/Module::Runtime::Conflicts"
    url = "http://search.cpan.org/CPAN/authors/id/E/ET/ETHER/Module-Runtime-Conflicts-0.003.tar.gz"

    license("GPL-1.0-or-later OR Artistic-1.0-Perl")

    version("0.003", sha256="707cdc75038c70fe91779b888ac050f128565d3967ba96680e1b1c7cc9733875")
