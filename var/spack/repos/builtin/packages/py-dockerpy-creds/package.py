# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyDockerpyCreds(PythonPackage):
    """Python bindings for the docker credentials store API"""

    homepage = "https://github.com/shin-/dockerpy-creds"
    url = "https://github.com/shin-/dockerpy-creds/archive/0.4.0.tar.gz"

    license("Apache-2.0")

    version("0.4.0", sha256="c76c2863c6e9a31b8f70ee5b8b0e5ac6860bfd422d930c04a387599e4272b4b9")
    version("0.3.0", sha256="3660a5e9fc7c2816ab967e4bdb4802f211e35011357ae612a601d6944721e153")
    version("0.2.3", sha256="7278a7e3c904ccea4bcc777b991a39cac9d4702bfd7d76b95ff6179500d886c4")
    version("0.2.2", sha256="bb26b8a8882b9d115a43169663cd9557d132a68147d9a1c77cb4a3ffc9897398")
    version("0.2.1", sha256="7882efd95f44b5df166b4e34c054b486dc7287932a49cd491edf406763695351")
    version("0.2.0", sha256="f2838348e1175079e3062bf0769b9fa5070c29f4d94435674b9f8a76144f4e5b")
    version("0.1.0", sha256="f7ab290cb536e7ef1c774d4eb5df86237e579a9c7a87805da39ff07bd14e0aff")

    depends_on("python@2.0:2.8,3.4:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-six", type=("build", "run"))
