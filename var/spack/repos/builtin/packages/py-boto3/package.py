# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyBoto3(PythonPackage):
    """The AWS SDK for Python."""

    homepage = "https://github.com/boto/boto3"
    pypi = "boto3/boto3-1.10.44.tar.gz"

    version("1.34.162", sha256="873f8f5d2f6f85f1018cbb0535b03cceddc7b655b61f66a0a56995238804f41f")
    version("1.34.44", sha256="86bcf79a56631609a9f8023fe8f53e2869702bdd4c9047c6d9f091eb39c9b0fa")
    version("1.26.26", sha256="a2349d436db6f6aa1e0def5501e4884572eb6f008f35063a359a6fa8ba3539b7")
    version("1.25.5", sha256="aec7db139429fe0f3fbe723170461192b0483b0070114a4b56351e374e0f294d")
    version("1.24.96", sha256="6b8899542cff82becceb3498a2240bf77c96def0515b0a31f7f6a9d5b92e7a3d")
    version("1.23.10", sha256="2a4395e3241c20eef441d7443a5e6eaa0ee3f7114653fb9d9cef41587526f7bd")
    version("1.22.13", sha256="02b6ad889f98c54274f83a4f862d78ce97a6366f805d8d8faaf14b789fd26172")
    version("1.21.46", sha256="9ac902076eac82112f4536cc2606a1f597a387dbc56b250575ac2d2c64c75e20")
    version("1.20.54", sha256="8129ad42cc0120d1c63daa18512d6f0b1439e385b2b6e0fe987f116bdf795546")
    version("1.19.12", sha256="182a2b756a2c2180b473bc8452227062394a24e3701548be23ebc30d85976c64")
    version("1.18.65", sha256="baedf0637dd0e47cff60eb5591133f9c10aeb49581e2ad5a99794996a2dfbe09")
    version("1.18.12", sha256="596fb9df00a816780db8620d9f62982eb783b3eb63a75947e172101d0785e6aa")
    version("1.17.112", sha256="08b6dacbe7ebe57ae8acfb7106b2728d946ae1e0c3da270caee1deb79ccbd8af")
    version("1.17.27", sha256="fa41987f9f71368013767306d9522b627946a01b4843938a26fb19cc8adb06c0")
    version("1.10.50", sha256="5c00d51101d6a7ddf2207ae8a738e5c815c5fcffbee76121f38bd41d83c936a5")
    version("1.10.44", sha256="adc0c0269bd65967fd528d7cd826304f381d40d94f2bf2b09f58167e5ac05d86")
    version("1.10.38", sha256="6cdb063b2ae5ac7b93ded6b6b17e3da1325b32232d5ff56e6800018d4786bba6")
    version("1.9.253", sha256="d93f1774c4bc66e02acdda2067291acb9e228a035435753cb75f83ad2904cbe3")
    version("1.9.169", sha256="9d8bd0ca309b01265793b7e8d7b88c1df439737d77c8725988f0277bbf58d169")

    depends_on("python@3.7:", when="@1.26:", type=("build", "run"))
    depends_on("python@3.6:", when="@1.18:", type=("build", "run"))
    depends_on("python@2.7:2.8,3.6:", when="@1.17:", type=("build", "run"))
    depends_on("python@2.6:", when="@1.9:", type=("build", "run"))
    depends_on("py-setuptools", type="build")

    depends_on("py-botocore@1.34.162:1.34", when="@1.34.162", type=("build", "run"))
    depends_on("py-botocore@1.34.44:1.34", when="@1.34.44", type=("build", "run"))
    depends_on("py-botocore@1.29.26:1.29", when="@1.26", type=("build", "run"))
    depends_on("py-botocore@1.28.5:1.28", when="@1.25", type=("build", "run"))
    depends_on("py-botocore@1.27.96:1.27", when="@1.24", type=("build", "run"))
    depends_on("py-botocore@1.26.10:1.26", when="@1.23", type=("build", "run"))
    depends_on("py-botocore@1.25.13:1.25", when="@1.22", type=("build", "run"))
    depends_on("py-botocore@1.24.46:1.24", when="@1.21", type=("build", "run"))
    depends_on("py-botocore@1.23.54:1.23", when="@1.20", type=("build", "run"))
    depends_on("py-botocore@1.22.12:1.22", when="@1.19", type=("build", "run"))
    depends_on("py-botocore@1.21.65:1.21", when="@1.18", type=("build", "run"))
    depends_on("py-botocore@1.20.27:1.20", when="@1.17", type=("build", "run"))
    depends_on("py-botocore@1.13.50:1.13", when="@1.10", type=("build", "run"))
    depends_on("py-botocore@1.12.253:1.12", when="@1.9", type=("build", "run"))

    depends_on("py-jmespath@0.7.1:0", when="@:1.20", type=("build", "run"))
    depends_on("py-jmespath@0.7.1:1", type=("build", "run"))

    depends_on("py-s3transfer@0.10", when="@1.34.6:", type=("build", "run"))
    depends_on("py-s3transfer@0.9", when="@1.34:1.34.5", type=("build", "run"))
    depends_on("py-s3transfer@0.8.2:0.8", when="@1.33.4:1.33", type=("build", "run"))
    depends_on("py-s3transfer@0.8", when="@1.29.7:1.33.3", type=("build", "run"))
    depends_on("py-s3transfer@0.7", when="@1.28.55:1.29.6", type=("build", "run"))
    depends_on("py-s3transfer@0.6", when="@1.24:1.28.54", type=("build", "run"))
    depends_on("py-s3transfer@0.5", when="@1.18:1.23", type=("build", "run"))
    depends_on("py-s3transfer@0.3", when="@1.17", type=("build", "run"))
    depends_on("py-s3transfer@0.2", when="@:1.10", type=("build", "run"))
