# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyCoilmq(PythonPackage):
    """Lightweight Python STOMP message broker."""

    homepage = "https://github.com/hozn/coilmq"
    url = "https://github.com/hozn/coilmq/archive/1.0.0.tar.gz"

    version("1.0.0", sha256="95d12de9b007fc679d4ad2eba0253aee8f6ecf42b79a94be6a2e0349f91086b0")
    version("0.6.1", sha256="402a5f88631a848926c442385248d7ae7bd05607bba8f20605e31fd49c3677f9")
    version("0.6.0", sha256="50d22fde72f058720bb48ad96bdd7c87594372d7917dd5d2cca40a9d195fde27")
    version("0.5.0", sha256="ffe2648e0a336ff61f729ad76090f8a16e681b3d3d6b14ba7ce3ef840de32cd9")
    version("0.4.4", sha256="2a0d494c73412e76075d2a72698948fb1d84c9c5719b134c364c07bcc6a3eacf")
    version("0.4.3", sha256="7a051f4fd2b76c8accf0b3f435267566910085c18483726e9eb56416e40703b7")

    depends_on("py-setuptools", type="build")
    depends_on("py-python-daemon", type=("build", "run"))
    depends_on("py-pid", type=("build", "run"))
    depends_on("py-wheel", type=("build", "run"))
    depends_on("py-six", type=("build", "run"))
    depends_on("py-click", type=("build", "run"))
