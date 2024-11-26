# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class FeqParse(CMakePackage):
    """An equation parser Fortran class that
    is used to interpret and evaluate functions
    provided as strings."""

    homepage = "https://feqparse.fluidnumerics.com"
    url = "https://github.com/FluidNumerics/feq-parse/archive/v2.0.1.tar.gz"

    maintainers("fluidnumerics-joe")

    license("3-Clause BSD")

    version("2.2.2", sha256="cfbf6142186c2e61b373237dd94d68013c1e8202a2b14dfd7aa6b8befbe330eb")
    version("2.2.1", sha256="d25f81c0e514cf9fad77190d9edf994b94eaebd414cf639cfaa690a9a1cc9cbf")
    version("2.2.0", sha256="962fca2de745bc3b436cb2299c917184ce2d9ac5edf95aad3c103efb63ed311a")
    version("2.1.0", sha256="f3fd51c24c563fe1d0dcb880bc16a62c9e08fe0cdd6f58df08f0db0ed34c289a")
    version("2.0.3", sha256="a1c42507801adc55a63a9a904807058079d54e002e10f2b29a916b06fc815f80")
    version("2.0.1", sha256="08dd08bd100a0a2eb672a5b2792ad56a337df575c634aac0d7a300d7e484b21c")
    version("1.1.0", sha256="d33a4fd6904939bb70780e8f25f37c1291c4f24fd207feb4ffc0f8d89637d1e3")
    version("1.0.2", sha256="1cd1db7562908ea16fc65dc5268b654405d0b3d9dcfe11f409949c431b48a3e8")

    depends_on("fortran", type="build")  # generated

    depends_on("cmake@3.0.2:", type="build")

    parallel = False
