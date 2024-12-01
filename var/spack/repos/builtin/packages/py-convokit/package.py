# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyConvokit(PythonPackage):
    """This toolkit contains tools to extract conversational features and
    analyze social phenomena in conversations, using a single unified interface
    inspired by (and compatible with) scikit-learn."""

    homepage = "https://convokit.cornell.edu/"
    pypi = "convokit/convokit-2.5.tar.gz"

    version("2.5", sha256="90de76c2a2df69eedeb20e0b89ff293a51180fb0152189f108c3331b7b7bb698")

    depends_on("python@3.6:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-matplotlib@3.0.0:", type=("build", "run"))
    depends_on("py-pandas@0.23.4:", type=("build", "run"))
    depends_on("py-msgpack-numpy@0.4.3.2:", type=("build", "run"))
    depends_on("py-spacy@2.3.5:", type=("build", "run"))
    depends_on("py-scipy@1.1.0:", type=("build", "run"))
    depends_on("py-scikit-learn@0.20.0:", type=("build", "run"))
    depends_on("py-nltk@3.4:", type=("build", "run"))
    depends_on("py-dill@0.2.9:", type=("build", "run"))
    depends_on("py-joblib@0.13.2:", type=("build", "run"))
    depends_on("py-clean-text@0.1.1:", type=("build", "run"))
    depends_on("py-unidecode@1.1.1:", type=("build", "run"))
