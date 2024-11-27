# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlParamsValidate(PerlPackage):
    """Params::Validate - Validate method/function parameters"""

    homepage = "https://metacpan.org/pod/Params::Validate"
    url = "https://cpan.metacpan.org/authors/id/D/DR/DROLSKY/Params-Validate-1.29.tar.gz"

    license("Artistic-2.0")

    version("1.31", sha256="1bf2518ef2c4869f91590e219f545c8ef12ed53cf313e0eb5704adf7f1b2961e")
    version("1.29", sha256="49a68dfb430bea028042479111d19068e08095e5a467e320b7ab7bde3d729733")

    depends_on("perl-module-build", type="build")
    depends_on("perl-module-implementation", type=("build", "run"))
