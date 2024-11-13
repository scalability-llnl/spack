# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyRequests(PythonPackage):
    """Python HTTP for Humans."""

    homepage = "https://requests.readthedocs.io"
    pypi = "requests/requests-2.24.0.tar.gz"
    git = "https://github.com/psf/requests"

    license("Apache-2.0")

    version("2.32.3", sha256="55365417734eb18255590a9ff9eb97e9e1da868d4ccd6402399eaf68af20a760")
    version("2.32.2", sha256="dd951ff5ecf3e3b3aa26b40703ba77495dab41da839ae72ef3c8e5d8e2433289")
    version("2.31.0", sha256="942c5a758f98d790eaed1a29cb6eefc7ffb0d1cf7af05c3d2791656dbd6ad1e1")
    version("2.28.2", sha256="98b1b2782e3c6c4904938b84c0eb932721069dfdb9134313beff7c83c2df24bf")
    version("2.28.1", sha256="7c5599b102feddaa661c826c56ab4fee28bfd17f5abca1ebbe3e7f19d7c97983")
    version("2.28.0", sha256="d568723a7ebd25875d8d1eaf5dfa068cd2fc8194b2e483d7b1f7c81918dbec6b")
    version("2.27.1", sha256="68d7c56fd5a8999887728ef304a6d12edc7be74f1cfa47714fc8b414525c9a61")
    version("2.26.0", sha256="b8aa58f8cf793ffd8782d3d8cb19e66ef36f7aba4353eec859e74678b01b07a7")
    version("2.25.1", sha256="27973dd4a904a4f13b263a19c866c13b92a39ed1c964655f025f3f8d3d75b804")
    version("2.24.0", sha256="b3559a131db72c33ee969480840fff4bb6dd111de7dd27c8ee1f820f4f00231b")
    version("2.23.0", sha256="b3f43d496c6daba4493e7c431722aeb7dbc6288f52a6e04e7b6023b0247817e6")
    version("2.22.0", sha256="11e007a8a2aa0323f5a921e9e6a2d7e4e67d9877e85773fba9ba6419025cbeb4")
    version("2.21.0", sha256="502a824f31acdacb3a35b6690b5fbf0bc41d63a24a45c4004352b0242707598e")
    version("2.18.4", sha256="9c443e7324ba5b85070c4a818ade28bfabedf16ea10206da1132edaa6dda237e")
    version("2.14.2", sha256="a274abba399a23e8713ffd2b5706535ae280ebe2b8069ee6a941cb089440d153")
    version("2.13.0", sha256="5722cd09762faa01276230270ff16af7acf7c5c45d623868d9ba116f15791ce8")
    version("2.11.1", sha256="5acf980358283faba0b897c73959cecf8b841205bb4b2ad3ef545f46eae1a133")
    version("2.3.0", sha256="1c1473875d846fe563d70868acf05b1953a4472f4695b7b3566d1d978957b8fc")

    variant("socks", default=False, description="SOCKS and HTTP proxy support")

    depends_on("python@3.7:", when="@2.28:", type=("build", "run"))
    depends_on("py-setuptools", type="build")

    depends_on("py-charset-normalizer@2:3", when="@2.28.2:", type=("build", "run"))
    depends_on("py-charset-normalizer@2", when="@2.26:2.28.1", type=("build", "run"))
    depends_on("py-idna@2.5:3", when="@2.26:", type=("build", "run"))
    depends_on("py-idna@2.5:2", when="@2.23:2.25", type=("build", "run"))
    depends_on("py-idna@2.5:2.8", when="@2.16:2.22", type=("build", "run"))
    depends_on("py-urllib3@1.21.1:2", when="@2.30:", type=("build", "run"))
    depends_on("py-urllib3@1.21.1:1.26", when="@2.25:2.29", type=("build", "run"))
    depends_on("py-urllib3@1.21.1:1.24,1.25.2:1.25", when="@2.16:2.24", type=("build", "run"))
    depends_on("py-certifi@2017.4.17:", when="@2.16:", type=("build", "run"))
    depends_on("py-pysocks@1.5.6,1.5.8:", when="+socks", type=("build", "run"))

    # Historical dependencies
    depends_on("py-chardet@3.0.2:4", type=("build", "run"), when="@2.25.1:2.25")
    depends_on("py-chardet@3.0.2:3", type=("build", "run"), when="@2.23:2.25.0")
    depends_on("py-chardet@3.0.2:3.0", type=("build", "run"), when="@2.16:2.22")
