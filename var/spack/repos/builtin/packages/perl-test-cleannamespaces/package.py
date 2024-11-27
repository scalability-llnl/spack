# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlTestCleannamespaces(PerlPackage):
    """This module lets you check your module's namespaces for imported
    functions you might have forgotten to remove"""

    homepage = "https://metacpan.org/pod/Test::CleanNamespaces"
    url = "http://search.cpan.org/CPAN/authors/id/E/ET/ETHER/Test-CleanNamespaces-0.22.tar.gz"

    license("Artistic-1.0")

    version("0.22", sha256="862a221994dd413b2f350450f22c96f57cac78784b1aca1a8fc763fc5449aaca")

    depends_on("perl-sub-exporter", type=("build", "run"))
    depends_on("perl-module-runtime", type=("build", "run"))
    depends_on("perl-test-needs", type=("build", "run"))
    depends_on("perl-test-deep", type=("build", "run"))
    depends_on("perl-test-warnings", type=("build", "run"))
    depends_on("perl-file-pushd", type=("build", "run"))
    depends_on("perl-package-stash", type=("build", "run"))
    depends_on("perl-sub-identify", type=("build", "run"))
    depends_on("perl-namespace-clean", type=("build", "run"))
