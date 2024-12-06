# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyFilelock(PythonPackage):
    """A platform-independent file lock for Python.

    This package contains a single module, which implements a platform
    independent file lock in Python, which provides a simple way of
    inter-process communication"""

    homepage = "https://github.com/tox-dev/py-filelock"
    pypi = "filelock/filelock-3.0.4.tar.gz"

    license("Unlicense")

    version("3.12.4", sha256="2e6f249f1f3654291606e046b09f1fd5eac39b360664c27f5aad072012f8bcbd")
    version("3.12.0", sha256="fc03ae43288c013d2ea83c8597001b1129db351aad9c57fe2409327916b8e718")
    version("3.8.0", sha256="55447caa666f2198c5b6b13a26d2084d26fa5b115c00d065664b2124680c4edc")
    version("3.5.0", sha256="137b661e657f7850eec9def2a001efadba3414be523b87cd3f9a037372d80a15")
    version("3.4.0", sha256="93d512b32a23baf4cac44ffd72ccf70732aeff7b8050fcaf6d3ec406d954baf4")
    version("3.0.12", sha256="18d82244ee114f543149c66a6e0c14e9c4f8a1044b5cdaadd0f82159d6a6ff59")
    version("3.0.4", sha256="011327d4ed939693a5b28c0fdf2fd9bda1f68614c1d6d0643a89382ce9843a71")
    version("3.0.3", sha256="7d8a86350736aa0efea0730e6a7f774195cbb1c2d61134c15f6be576399e87ff")
    version("3.0.0", sha256="b3ad481724adfb2280773edd95ce501e497e88fa4489c6e41e637ab3fd9a456c")
    version("2.0.13", sha256="d05079e7d7cae7576e192749d3461999ca6b0843d35b0f79f1fa956b0f6fc7d8")
    version("2.0.12", sha256="eb4314a9a032707a914b037433ce866d4ed363fce8605d45f0c9d2cd6ac52f98")
    version("2.0.11", sha256="e9e370efe86c30b19a2c8c36dd9fcce8e5ce294ef4ed6ac86664b666eaf852ca")
    version("2.0.10", sha256="c73bf706d8a0c5722de0b745495fed9cda0e46c0eabb44eb18ee3f00520fa85f")
    version("2.0.9", sha256="0f91dce339c9f25d6f2e0733a17e4f9a47b139dffda52619a0e61e013e5c6782")
    version("2.0.8", sha256="7e48e4906de3c9a5d64d8f235eb3ae1050dfefa63fd65eaf318cc915c935212b")

    depends_on("python@3.8:", when="@3.12.3:", type=("build", "run"))

    depends_on("py-hatch-vcs@0.3:", when="@3.8:", type="build")
    depends_on("py-hatchling@1.18:", when="@3.12.3:", type="build")
    depends_on("py-hatchling@1.14:", when="@3.8:", type="build")

    # Historical dependencies
    with when("@:3.8.0"):
        depends_on("py-setuptools@63.4:", when="@3.8:", type="build")
        depends_on("py-setuptools@41:", when="@3.1:", type="build")
        depends_on("py-setuptools", type="build")
        depends_on("py-setuptools-scm@7.0.5:", when="@3.8:", type="build")
        depends_on("py-setuptools-scm@2:", when="@3.1:", type="build")

    depends_on("py-wheel@0.30:", when="@3.1:3.7", type="build")
