# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyPdmPep517(PythonPackage):
    """A PEP 517 backend for PDM that supports PEP 621 metadata."""

    homepage = "https://pdm.fming.dev/latest/"
    pypi = "pdm-pep517/pdm-pep517-1.0.4.tar.gz"

    license("MIT")

    version("1.0.4", sha256="392f8c2b47c6ec20550cb8e19e24b9dbd27373413f067b56ecd75f9767f93015")

    depends_on("c", type="build")  # generated

    depends_on("python@3.7:", type=("build", "run"))
