# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyPlac(PythonPackage):
    """The smartest command line arguments parser in the world."""

    homepage = "https://github.com/micheles/plac"
    pypi = "plac/plac-1.1.3.tar.gz"

    # Skip 'plac_tk' imports
    import_modules = ["plac", "plac_ext", "plac_core"]

    license("BSD-2-Clause")

    version("1.3.5", sha256="38bdd864d0450fb748193aa817b9c458a8f5319fbf97b2261151cfc0a5812090")
    version("1.3.3", sha256="51e332dabc2aed2cd1f038be637d557d116175101535f53eaa7ae854a00f2a74")
    version("1.1.3", sha256="398cb947c60c4c25e275e1f1dadf027e7096858fb260b8ece3b33bcff90d985f")

    depends_on("py-setuptools", type="build")
