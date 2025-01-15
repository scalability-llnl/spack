# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyDeepdiff(PythonPackage):
    """Deep Difference and Search of any Python object/data.."""

    homepage = "https://github.com/seperman/deepdiff"
    pypi = "deepdiff/deepdiff-5.6.0.tar.gz"

    license("MIT")

    version("8.1.1", sha256="dd7bc7d5c8b51b5b90f01b0e2fe23c801fd8b4c6a7ee7e31c5a3c3663fcc7ceb")
    version("8.0.1", sha256="245599a4586ab59bb599ca3517a9c42f3318ff600ded5e80a3432693c8ec3c4b")
    version("7.0.1", sha256="260c16f052d4badbf60351b4f77e8390bee03a0b516246f6839bc813fb429ddf")
    version("6.7.1", sha256="b367e6fa6caac1c9f500adc79ada1b5b1242c50d5f716a1a4362030197847d30")
    version("6.6.1", sha256="75c75b1511f0e48edef2b70d785a9c32b2631666b465fa8c32270a77a7b950b5")
    version("6.5.0", sha256="080b1359d6128f3f5f1738c6be3064f0ad9b0cc41994aa90a028065f6ad11f25")
    version("6.4.1", sha256="744c4e54ff83eaa77a995b3311dccdce6ee67773335a34a5ef269fa048005457")
    version("6.3.1", sha256="e8c1bb409a2caf1d757799add53b3a490f707dd792ada0eca7cac1328055097a")
    version("6.3.0", sha256="6a3bf1e7228ac5c71ca2ec43505ca0a743ff54ec77aa08d7db22de6bc7b2b644")
    version("5.6.0", sha256="e3f1c3a375c7ea5ca69dba6f7920f9368658318ff1d8a496293c79481f48e649")

    depends_on("py-setuptools", type="build")
    depends_on("py-orderly-set@5.2.3:5", when="@8.1.0:", type=("build", "run"))
    depends_on("py-orderly-set@5.2.2", when="@8.0.1", type=("build", "run"))
    depends_on("py-orderly-set@5.2.1", when="@8.0.0", type=("build", "run"))

    depends_on("py-ordered-set@4.1", when="@7.0.1:7", type=("build", "run"))
    depends_on("py-ordered-set@4.0.2:4.1", when="@6:7.0.0", type=("build", "run"))
    depends_on("py-ordered-set@4.0.2", when="@:5", type=("build", "run"))
