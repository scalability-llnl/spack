# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyMoreItertools(PythonPackage):
    """Additions to the standard Python itertools package."""

    homepage = "https://github.com/erikrose/more-itertools"
    pypi = "more-itertools/more-itertools-7.2.0.tar.gz"

    license("MIT")

    version("9.1.0", sha256="cabaa341ad0389ea83c17a94566a53ae4c9d07349861ecb14dc6d0345cf9ac5d")
    version("8.14.0", sha256="c09443cd3d5438b8dafccd867a6bc1cb0894389e90cb53d227456b0b0bccb750")
    version("8.12.0", sha256="7dc6ad46f05f545f900dd59e8dfb4e84a4827b97b3cfecb175ea0c7d247f6064")
    version("8.11.0", sha256="0a2fd25d343c08d7e7212071820e7e7ea2f41d8fb45d6bc8a00cd6ce3b7aab88")
    version("8.9.0", sha256="8c746e0d09871661520da4f1241ba6b908dc903839733c8203b552cffaf173bd")
    version("7.2.0", sha256="409cd48d4db7052af495b09dec721011634af3753ae1ef92d2b32f73a745f832")
    version("7.0.0", sha256="c3e4748ba1aad8dba30a4886b0b1a2004f9a863837b8654e7059eebf727afa5a")
    version("5.0.0", sha256="38a936c0a6d98a38bcc2d03fdaaedaba9f412879461dd2ceff8d37564d6522e4")
    version("4.3.0", sha256="c476b5d3a34e12d40130bc2f935028b5f636df8f372dc2c1c01dc19681b2039e")
    version("4.1.0", sha256="c9ce7eccdcb901a2c75d326ea134e0886abfbea5f93e91cc95de9507c0816c44")
    version("2.2", sha256="93e62e05c7ad3da1a233def6731e8285156701e3419a5fe279017c429ec67ce0")

    depends_on("py-flit-core@3.2:3", when="@8.14.0:", type="build")

    # Historical dependencies
    depends_on("py-setuptools", when="@:8.12.0", type="build")
    depends_on("py-six@1.0.0:1", when="@:5", type=("build", "run"))
