# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyFortranLanguageServer(PythonPackage):
    """A Fortran implementation of the Language Server Protocol using Python
    (2.7+ or 3.0+)."""

    homepage = "https://github.com/hansec/fortran-language-server"
    url = "https://github.com/hansec/fortran-language-server/archive/v1.11.1.tar.gz"

    maintainers("AndrewGaspar")

    license("MIT")

    version("1.12.0", sha256="5cda6341b1d2365cce3d80ba40043346c5dcbd0b35f636bfa57cb34df789ff17")
    version("1.11.1", sha256="8f03782dd992d6652a3f2d349115fdad3aa3464fee3fafbbc4f8ecf780166e3c")

    depends_on("fortran", type="build")  # generated

    depends_on("python@2.7:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
