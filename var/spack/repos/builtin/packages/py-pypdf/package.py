# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPypdf(PythonPackage):
    """A pure-python PDF library capable of splitting, merging, cropping, and
    transforming PDF files"""

    homepage = "https://github.com/py-pdf/pypdf"
    pypi = "pypdf/pypdf-4.3.1.tar.gz"

    license("BSD-3-Clause", checked_by="qwertos")

    version("4.3.1", sha256="b2f37fe9a3030aa97ca86067a56ba3f9d3565f9a791b305c7355d8392c30d91b")

    depends_on("py-flit-core@3.9:3", type="build")
    depends_on("py-typing-extensions@4:", when="^python@:3.10", type=("build", "run"))
