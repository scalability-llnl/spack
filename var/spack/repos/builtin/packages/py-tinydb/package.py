# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyTinydb(PythonPackage):
    """TinyDB is a tiny, document oriented database optimized for your happiness."""

    homepage = "https://tinydb.readthedocs.io"
    pypi = "tinydb/tinydb-4.7.0.tar.gz"

    license("MIT")

    version("4.7.1", sha256="8955c239a79b8a6c8f637900152e2de38690848199d71d870c33c16405433ca5")
    version("4.7.0", sha256="357eb7383dee6915f17b00596ec6dd2a890f3117bf52be28a4c516aeee581100")
    version("4.6.1", sha256="0d5400f5e5ae368a84d57cb234456f1cf70430fd39bcd77ccd568fea91ff2a4e")
    version("4.6.0", sha256="f25b0debbec555226c43d67e2a80bdf273ccfde4aa6b1b8d2049b7c648312b40")
    version("4.5.2", sha256="7d18b2d0217827c188f177cd23df60e5cd5316a717e836a8e21c8c2488262cf5")

    depends_on("python@3.6:3", type=("build", "run"))
    depends_on("py-poetry-core", type="build")
    depends_on("py-typing-extensions@3.10.0:4", type=("build", "run"), when="^python@:3.7")
