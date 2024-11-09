# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPyrocko(PythonPackage):
    """Pyrocko is an open source seismology toolbox and library, written in the
    Python programming language"""

    homepage = "https://pyrocko.org/"
    pypi = "pyrocko/pyrocko-2023.6.29.tar.gz"

    maintainers("snehring")

    license("GPL-3.0", checked_by="snehring")

    version("2024.1.10", sha256="4fb2c72d0b036ce3c70bfd066e1ce4946eb93d9190d202e9fc689c1f29e4845f")
    version("2023.6.29", sha256="779a234592bfcfa1c96939fee53d0dfc5cadf111432a2679f08166cfd8bcae41")

    depends_on("c", type="build")  # generated

    depends_on("python@3.7:", type=("build", "run"))

    depends_on("py-setuptools", type="build")

    depends_on("py-numpy@1.16:", type=("build", "run"))
    depends_on("py-scipy@1:", type=("build", "run"))
    depends_on("py-pyyaml", type=("build", "run"))
    depends_on("py-matplotlib", type=("build", "run"))
    depends_on("py-requests", type=("build", "run"))
