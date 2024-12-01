# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPubchempy(PythonPackage):
    """PubChemPy provides a way to interact with PubChem in Python. It allows
    chemical searches by name, substructure and similarity, chemical standardization,
    conversion between chemical file formats, depiction and retrieval of chemical
    properties."""

    homepage = "https://github.com/mcs07/PubChemPy"
    pypi = "PubChemPy/PubChemPy-1.0.4.tar.gz"

    maintainers("meyersbs")

    license("MIT")

    version("1.0.4", sha256="24e9dc2fc90ab153b2764bf805e510b1410700884faf0510a9e7cf0d61d8ed0e")

    depends_on("py-setuptools", type="build")

    variant("pandas", default=False, description="Enable pandas support")
    depends_on("py-pandas", when="+pandas", type=("build", "run"))
