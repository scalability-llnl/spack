# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyTextblob(PythonPackage):
    """TextBlob is a Python (2 and 3) library for processing textual
    data. It provides a simple API for diving into common natural
    language processing (NLP) tasks such as part-of-speech tagging,
    noun phrase extraction, sentiment analysis, classification,
    translation, and more."""

    homepage = "https://textblob.readthedocs.io/"
    url = "https://github.com/sloria/TextBlob/archive/0.16.0.tar.gz"

    license("MIT")

    version("0.16.0", sha256="bf29369f3260cc779b22b2b86337bcce0c8e929d994b1c8f0d39545ec2fb33aa")

    depends_on("python@3:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-nltk@3.1:+data", type=("build", "run"))
