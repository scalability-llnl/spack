# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyGradioClient(PythonPackage):
    """Python library for easily interacting with trained machine learning models"""

    homepage = "https://github.com/gradio-app/gradio"
    pypi = "gradio_client/gradio_client-0.2.9.tar.gz"

    version("0.2.9", sha256="d4071709ab45a3dbacdbd0797fde5d66d87a98424559e060d576fbe9b0171f4d")

    depends_on("python@3.8:", type=("build", "run"))
    depends_on("py-hatchling", type="build")
    depends_on("py-hatch-requirements-txt", type="build")
    depends_on("py-hatch-fancy-pypi-readme@22.5:", type="build")
    depends_on("py-requests", type=("build", "run"))
    depends_on("py-websockets", type=("build", "run"))
    depends_on("py-packaging", type=("build", "run"))
    depends_on("py-fsspec", type=("build", "run"))
    depends_on("py-huggingface-hub@0.13:", type=("build", "run"))
    depends_on("py-typing-extensions", type=("build", "run"))
    depends_on("py-httpx", type=("build", "run"))
