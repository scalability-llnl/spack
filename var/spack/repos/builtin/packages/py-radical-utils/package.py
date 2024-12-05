# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyRadicalUtils(PythonPackage):
    """RADICAL-Utils contains shared code and tools for various
    RADICAL-Cybertools packages."""

    homepage = "https://radical-cybertools.github.io"
    git = "https://github.com/radical-cybertools/radical.utils.git"
    pypi = "radical.utils/radical.utils-1.47.0.tar.gz"

    maintainers("andre-merzky")

    license("MIT")

    version("develop", branch="devel")
    version("1.47.0", sha256="f85a4a452561dd018217f1ed38d97c9be96fa448437cfeb1b879121174fd5311")
    version("1.39.0", sha256="fade87ee4c6ccf335d5e26d5158ce22ee891e4d4c576464274999ddf36dc4977")

    version(
        "1.20.0",
        sha256="9b39dd616d70c387fb3f97d3510a506bac92c159b6482c3aebd3d11eeaeebcc9",
        deprecated=True,
    )
    version(
        "1.18.1",
        sha256="5b3ab15417a1ef82f63f8a77763a177d6bc59b61a80823be0df8c0f7502d9b3e",
        deprecated=True,
    )
    version(
        "1.17.0",
        sha256="ee3fec190e89522f648e191d2e380689842746f1eacda27772a9471215908cfe",
        deprecated=True,
    )
    version(
        "1.16.0",
        sha256="6eddfba5c73e71c7c5ddeba6c8ebe5260616d66b26d1f7123613c3cd543d61e9",
        deprecated=True,
    )
    version(
        "1.15.0",
        sha256="22e5028de75c0a471bfed587d437dded214625b150deaca0289474a3619d395b",
        deprecated=True,
    )
    version(
        "1.14.0",
        sha256="f61f0e335bbdc51e4023458e7e6959551686ebf170adc5353220dcc83fd677c9",
        deprecated=True,
    )
    version(
        "1.13.0",
        sha256="84c1cad8be988dad7fb2b8455d19a4fb0c979fab02c5b7a7b531a4ae8fe52580",
        deprecated=True,
    )
    version(
        "1.12.0",
        sha256="1474dbe4d94cdf3e992e1711e10d73dffa352c1c29ff51d81c1686e5081e9398",
        deprecated=True,
    )
    version(
        "1.11.1",
        sha256="4fec3f6d45d7309c891ab4f8aeda0257f06f9a8404ca87c7eb643cd8d7415804",
        deprecated=True,
    )
    version(
        "1.11.0",
        sha256="81537c2a2f8a1a409b4a1aac67323c6b49cc994e2b70052425e2bc8d4622e2de",
        deprecated=True,
    )
    version(
        "1.9.1",
        sha256="0837d75e7f9dcce5ba5ac63151ab1683d6ba9ab3954b076d1f170cc4a3cdb1b4",
        deprecated=True,
    )
    version(
        "1.8.4",
        sha256="4777ba20e9f881bf3e73ad917638fdeca5a4b253d57ed7b321a07f670e3f737b",
        deprecated=True,
    )
    version(
        "1.8.0",
        sha256="8582c65593f51d394fc263c6354ec5ad9cc7173369dcedfb2eef4f5e8146cf03",
        deprecated=True,
    )
    version(
        "1.6.7",
        sha256="552f6c282f960ccd9d2401d686b0b3bfab35dfa94a26baeb2d3b4e45211f05a9",
        deprecated=True,
    )

    depends_on("py-radical-gtod", type=("build", "run"), when="@:1.13")

    depends_on("py-pymongo@:3", type=("build", "run"), when="@:1.39")

    depends_on("python@3.6:", type=("build", "run"))
    depends_on("py-colorama", type=("build", "run"))
    depends_on("py-msgpack", type=("build", "run"))
    depends_on("py-netifaces", type=("build", "run"))
    depends_on("py-ntplib", type=("build", "run"))
    depends_on("py-pyzmq", type=("build", "run"))
    depends_on("py-regex", type=("build", "run"))
    depends_on("py-setproctitle", type=("build", "run"))
    depends_on("py-setuptools", type="build")
