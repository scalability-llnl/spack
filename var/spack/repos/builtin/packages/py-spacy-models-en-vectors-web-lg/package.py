# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PySpacyModelsEnVectorsWebLg(PythonPackage):
    """1.2m 300d vectors trained on Common Crawl with GloVe"""

    homepage = "https://spacy.io/models/en-starters#en_vectors_web_lg"
    url = "https://github.com/explosion/spacy-models/releases/download/en_vectors_web_lg-2.3.0/en_vectors_web_lg-2.3.0.tar.gz"

    version("2.3.0", sha256="839c177a604cd916e10700b43f7c80ca67fff1f3b5961847ef6c01c8b308e08d")

    depends_on("py-setuptools", type="build")
    depends_on("py-spacy@2.3.0:2.3", type=("build", "run"))
