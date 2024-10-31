# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class PyPdmBackend(PythonPackage):
    """The build backend used by PDM that supports latest packaging standards"""

    homepage = "https://backend.pdm-project.org/"
    pypi = "pdm_backend/pdm_backend-2.3.0.tar.gz"

    license("MIT", checked_by="matz-e")

    version("2.3.0", sha256="e39ed2da206d90d4a6e9eb62f6dce54ed4fa65ddf172a7d5700960d0f8a09e09")

    depends_on("python@3.8:", type=("build", "run"))
    depends_on("py-importlib-metadata@3.6:", type=("build", "run"), when="^python@:3.9")
