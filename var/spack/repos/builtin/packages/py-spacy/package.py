# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PySpacy(PythonPackage):
    """spaCy is a library for advanced Natural Language Processing in
    Python and Cython."""

    homepage = "https://spacy.io/"
    pypi = "spacy/spacy-2.3.2.tar.gz"

    license("MIT")

    version("2.3.7", sha256="c0f2315fea23497662e28212f89af3a03667f97c867c597b599c37ab84092e22")
    version("2.3.2", sha256="818de26e0e383f64ccbe3db185574920de05923d8deac8bbb12113b9e33cee1f")
    version("2.2.4", sha256="f0f3a67c5841e6e35d62c98f40ebb3d132587d3aba4f4dccac5056c4e90ff5b9")

    depends_on("cxx", type="build")  # generated

    depends_on("python@2.7:2.8,3.4:", type=("build", "run"), when="@2.2.4:2.2")
    depends_on("python@2.7:2.8,3.5:", type=("build", "run"), when="@2.3.0:")
    depends_on("py-cython@0.25:", type="build")
    depends_on("py-cymem@2.0.2:2.0", type=("build", "run"))
    depends_on("py-preshed@3.0.2:3.0", type=("build", "run"))
    depends_on("py-murmurhash@0.28:1.0", type=("build", "run"))
    depends_on("py-thinc@7.4.0", type=("build", "run"), when="@2.2.4:2.2")
    depends_on("py-thinc@7.4.1", type=("build", "run"), when="@2.3.0:")
    depends_on("py-thinc@7.4.1:7.4", type=("build", "run"), when="@2.3.7:")
    depends_on("py-blis@0.4.0:0.4", type=("build", "run"))
    depends_on("py-blis@0.4.0:0.7", type=("build", "run"), when="@2.3.7:")
    depends_on("py-wasabi@0.4.0:1.0", type=("build", "run"))
    depends_on("py-srsly@1.0.2:1.0", type=("build", "run"))
    depends_on("py-catalogue@0.0.7:1.0", type=("build", "run"))
    depends_on("py-tqdm@4.38:4", type=("build", "run"))
    depends_on("py-setuptools", type=("build", "run"))
    depends_on("py-numpy@1.15:", type=("build", "run"))
    depends_on("py-plac@0.9.6:1.1", type=("build", "run"))
    depends_on("py-requests@2.13:2", type=("build", "run"))
