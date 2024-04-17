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

    version(
        "3.0.12",
        sha256="476e3bd0d05f8c339ed60f40986c07387c0a71479245d6d0f4298dbd52cda55f",
        url="https://pypi.org/packages/c3/55/12e842c70ff8828e34e543a2c7176dac4da006ca6901c9e8b43efab8bc6b/spacy_legacy-3.0.12-py2.py3-none-any.whl",
    )
