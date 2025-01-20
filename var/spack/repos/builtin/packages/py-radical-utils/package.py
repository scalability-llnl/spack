# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyRadicalUtils(PythonPackage):
    """RADICAL-Utils contains shared code and tools for various
    RADICAL-Cybertools packages."""

    homepage = "https://radical-cybertools.github.io"
    git = "https://github.com/radical-cybertools/radical.utils.git"
    pypi = "radical_utils/radical_utils-1.90.0.tar.gz"

    maintainers("andre-merzky")

    license("MIT")

    version("develop", branch="devel")
    version("1.90.0", sha256="bcd89ffee5a73def1013470854cf2afaf25a575e0ce461e3619f058d2d0dee1f")

    version(
        "1.47.0",
        sha256="f85a4a452561dd018217f1ed38d97c9be96fa448437cfeb1b879121174fd5311",
        deprecated=True,
    )
    version(
        "1.39.0",
        sha256="fade87ee4c6ccf335d5e26d5158ce22ee891e4d4c576464274999ddf36dc4977",
        deprecated=True,
    )

    depends_on("python@3.7:", type=("build", "run"))
    depends_on("python@3.6:", type=("build", "run"), when="@:1.52")

    depends_on("py-colorama", type=("build", "run"))
    depends_on("py-msgpack", type=("build", "run"))
    depends_on("py-netifaces", type=("build", "run"))
    depends_on("py-ntplib", type=("build", "run"))
    depends_on("py-pyzmq", type=("build", "run"))
    depends_on("py-regex", type=("build", "run"))
    depends_on("py-setproctitle", type=("build", "run"))
    with default_args(type="build"):
        depends_on("py-setuptools")
        # https://github.com/radical-cybertools/radical.utils/issues/403
        depends_on("py-setuptools@:69.2", when="@:1.51")
