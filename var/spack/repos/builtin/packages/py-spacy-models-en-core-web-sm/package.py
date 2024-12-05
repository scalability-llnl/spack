# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PySpacyModelsEnCoreWebSm(PythonPackage):
    """English multi-task CNN trained on OntoNotes. Assigns context-specific
    token vectors, POS tags, dependency parse and named entities."""

    homepage = "https://spacy.io/models/en#en_core_web_sm"
    url = "https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-2.3.1/en_core_web_sm-2.3.1.tar.gz"

    version("2.3.1", sha256="06c80936324012d1223291d2af41a5229e746dc2dee8fe31a532666ee3d18aaa")
    version("2.2.5", sha256="60b69065c97fd2e4972c33300205e1dead3501d2e0bfd6a182c3a033e337caee")

    depends_on("py-setuptools", type="build")
    depends_on("py-spacy@2.2.2:", type=("build", "run"), when="@:2.2.5")
    depends_on("py-spacy@2.3.0:2.3", type=("build", "run"), when="@2.3.1:")
