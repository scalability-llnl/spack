# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyMystParser(PythonPackage):
    """A Sphinx and Docutils extension to parse MyST, a rich and
    extensible flavour of Markdown for authoring technical and
    scientific documentation."""

    homepage = "https://github.com/executablebooks/MyST-Parser"
    pypi = "myst-parser/myst-parser-0.18.1.tar.gz"

    license("MIT")

    version("0.18.1", sha256="79317f4bb2c13053dd6e64f9da1ba1da6cd9c40c8a430c447a7b146a594c246d")

    depends_on("python@3.7:", type=("build", "run"))
    depends_on("py-flit-core@3.4:3", type="build")
    depends_on("py-docutils@0.15:0.19", type=("build", "run"))
    depends_on("py-jinja2", type=("build", "run"))  # let sphinx decide version
    depends_on("py-markdown-it-py@1.0.0:2", type=("build", "run"))
    depends_on("py-mdit-py-plugins@0.3.1:0.3", type=("build", "run"))
    depends_on("py-pyyaml", type=("build", "run"))
    depends_on("py-sphinx@4.0.0:5", type=("build", "run"))
    depends_on("py-typing-extensions", type=("build", "run"))
