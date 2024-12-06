# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPastel(PythonPackage):
    """Bring colors to your terminal."""

    homepage = "https://github.com/sdispater/pastel"
    pypi = "pastel/pastel-0.2.1.tar.gz"

    license("MIT")

    version("0.2.1", sha256="e6581ac04e973cac858828c6202c1e1e81fee1dc7de7683f3e1ffe0bfd8a573d")

    depends_on("python@2.7,3.4:3", type=("build", "run"))
    depends_on("py-poetry-core@1:", type="build")
