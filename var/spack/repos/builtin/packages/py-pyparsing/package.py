# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPyparsing(PythonPackage):
    """A Python Parsing Module."""

    homepage = "https://pyparsing-docs.readthedocs.io/en/latest/"
    pypi = "pyparsing/pyparsing-2.4.2.tar.gz"

    license("MIT")

    version("3.1.2", sha256="a1bac0ce561155ecc3ed78ca94d3c9378656ad4c94c1270de543f621420f94ad")
    version("3.1.1", sha256="ede28a1a32462f5a9705e07aea48001a08f7cf81a021585011deba701581a0db")
    version("3.1.0", sha256="edb662d6fe322d6e990b1594b5feaeadf806803359e3d4d42f11e295e588f0ea")
    version("3.0.9", sha256="2b020ecf7d21b687f219b71ecad3631f644a47f01403fa1d1036b0c6416d70fb")
    version("3.0.6", sha256="d9bdec0013ef1eb5a84ab39a3b3868911598afa494f5faa038647101504e2b81")
    version("2.4.7", sha256="c203ec8783bf771a155b207279b9bccb8dea02d8f0c9e5f8ead507bc3246ecc1")
    version("2.4.2", sha256="6f98a7b9397e206d78cc01df10131398f1c8b8510a2f4d97d9abd82e1aacdd80")
    version("2.4.0", sha256="1873c03321fc118f4e9746baf201ff990ceb915f433f23b395f5580d1840cb2a")
    version("2.3.1", sha256="66c9268862641abcac4a96ba74506e594c884e3f57690a696d21ad8210ed667a")
    version("2.2.0", sha256="0832bcf47acd283788593e7a0f542407bd9550a55a8a8435214a1960e04bcb04")
    version("2.1.10", sha256="811c3e7b0031021137fc83e051795025fcb98674d07eb8fe922ba4de53d39188")
    version("2.0.3", sha256="06e729e1cbf5274703b1f47b6135ed8335999d547f9d8cf048b210fb8ebf844f")

    depends_on("python@3.6.8:", when="@3.0.9:", type=("build", "run"))
    depends_on("python@3.6:", when="@3:", type=("build", "run"))
    depends_on("python@2.6:2.8,3.3:", type=("build", "run"))
    depends_on("py-setuptools", when="@:3.0.8", type="build")
    depends_on("py-flit-core@3.2:3", when="@3.0.9:", type="build")

    import_modules = ["pyparsing"]
