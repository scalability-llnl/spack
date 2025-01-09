# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyAsgiref(PythonPackage):
    """ASGI specification and utilities."""

    homepage = "https://asgi.readthedocs.io/en/latest/"
    pypi = "asgiref/asgiref-3.7.2.tar.gz"

    license("BSD-3-Clause")

    version("3.8.1", sha256="c343bd80a0bec947a9860adb4c432ffa7db769836c64238fc34bdc3fec84d590")
    version("3.7.2", sha256="9e0ce3aa93a819ba5b45120216b23878cf6e8525eb3848653452b4192b92afed")
    version("3.5.2", sha256="4a29362a6acebe09bf1d6640db38c1dc3d9217c68e6f9f6204d72667fc19a424")
    version("3.5.0", sha256="2f8abc20f7248433085eda803936d98992f1343ddb022065779f37c5da0181d0")
    version("3.2.7", sha256="8036f90603c54e93521e5777b2b9a39ba1bad05773fcf2d208f0299d1df58ce5")
    version("3.2.6", sha256="63007b556233381c5f22ae4c7e4292c9f1b953dc8909ae8fd268f611dc23cbd0")
    version("3.2.5", sha256="c8f49dd3b42edcc51d09dd2eea8a92b3cfc987ff7e6486be734b4d0cbfd5d315")
    version("3.2.4", sha256="f07043512078c76bb28a62fd1e327876599062b5f0aea60ed1d9cabc42e95fe2")
    version("3.2.3", sha256="7e06d934a7718bf3975acbf87780ba678957b87c7adc056f13b6215d610695a0")
    version("3.2.2", sha256="f62b1c88ebf5fe95db202a372982970edcf375c1513d7e70717df0750f5c2b98")
    version("3.2.1", sha256="57ed0d07634a23bebfa1b02a1aa05eba09c37aab3fc93893e4039e7bc2d96d9e")
    version("3.2.0", sha256="cefcbd64acbfc9f38913566824ef070dd9a50e63f1b4cc5a7f1c44be809d7ff3")
    version("3.1.4", sha256="865b7ccce5a6e815607b08d9059fe9c058cd75c77f896f5e0b74ff6c1ba81818")
    version("3.1.3", sha256="566126b4cbf190c315121965253ecb2159499197ff4afd686e0921f4dd987999")

    depends_on("py-setuptools", type="build")
    depends_on("py-typing-extensions@4:", type=("build", "run"), when="@3.7: ^python@:3.10")
    depends_on("py-typing-extensions", type=("build", "run"), when="@3.5 ^python@:3.7")
