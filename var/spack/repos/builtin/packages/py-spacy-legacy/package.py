# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySpacyLegacy(PythonPackage):
    """Legacy registered functions for spaCy backwards compatibility"""

    homepage = "https://spacy.io/"
    pypi = "spacy-legacy/spacy-legacy-3.0.12.tar.gz"

    license("MIT")

    version("3.0.12", sha256="b37d6e0c9b6e1d7ca1cf5bc7152ab64a4c4671f59c85adaf7a3fcb870357a774")

    depends_on("python@3.6:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
