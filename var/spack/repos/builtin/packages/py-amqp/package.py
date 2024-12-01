# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyAmqp(PythonPackage):
    """Low-level AMQP client for Python (fork of amqplib)."""

    pypi = "amqp/amqp-2.4.1.tar.gz"

    license("BSD-3-Clause")

    version("5.2.0", sha256="a1ecff425ad063ad42a486c902807d1482311481c8ad95a72694b2975e75f7fd")
    version("5.1.1", sha256="2c1b13fecc0893e946c65cbd5f36427861cffa4ea2201d8f6fca22e2a373b5e2")
    version("5.0.9", sha256="1e5f707424e544078ca196e72ae6a14887ce74e02bd126be54b7c03c971bef18")
    version("5.0.6", sha256="03e16e94f2b34c31f8bf1206d8ddd3ccaa4c315f7f6a1879b7b1210d229568c2")
    version("5.0.1", sha256="9881f8e6fe23e3db9faa6cfd8c05390213e1d1b95c0162bc50552cad75bffa5f")
    version("5.0.0", sha256="1183b66e54a5c533b679d9f557b31c5b31d26701761f2bbd144054cce58f3588")
    version("2.6.1", sha256="70cdb10628468ff14e57ec2f751c7aa9e48e7e3651cfd62d431213c0c4e58f21")
    version("2.6.0", sha256="24dbaff8ce4f30566bb88976b398e8c4e77637171af3af6f1b9650f48890e60b")
    version("2.5.2", sha256="77f1aef9410698d20eaeac5b73a87817365f457a507d82edf292e12cbb83b08d")
    version("2.5.1", sha256="19a917e260178b8d410122712bac69cb3e6db010d68f6101e7307508aded5e68")
    version("2.5.0", sha256="cbb6f87d53cac612a594f982b717cc1c54c6a1e17943a0a0d32dc6cc9e2120c8")
    version("2.4.2", sha256="043beb485774ca69718a35602089e524f87168268f0d1ae115f28b88d27f92d7")
    version("2.4.1", sha256="6816eed27521293ee03aa9ace300a07215b11fee4e845588a9b863a7ba30addb")
    version("2.4.0", sha256="9f181e4aef6562e6f9f45660578fc1556150ca06e836ecb9e733e6ea10b48464")

    depends_on("python@2.7:2.8,3.5:", type=("build", "run"))
    depends_on("python@3.6:", type=("build", "run"), when="@5.0.9:")

    depends_on("py-setuptools", type="build")
    depends_on("py-cython", type="build")

    depends_on("py-vine@1.1.3:4", when="@2", type=("build", "run"))
    depends_on("py-vine@5.0.0", when="@5.0.0:5", type=("build", "run"))

    def setup_build_environment(self, env):
        env.set("CELERY_ENABLE_SPEEDUPS", True)
