# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyHatchling(PythonPackage):
    """Modern, extensible Python build backend."""

    homepage = "https://hatch.pypa.io/latest/"
    pypi = "hatchling/hatchling-1.4.1.tar.gz"
    git = "https://github.com/pypa/hatch"

    license("MIT", checked_by="tgamblin")

    version("1.25.0", sha256="7064631a512610b52250a4d3ff1bd81551d6d1431c4eb7b72e734df6c74f4262")
    version("1.24.2", sha256="41ddc27cdb25db9ef7b68bef075f829c84cb349aa1bff8240797d012510547b0")
    version("1.21.0", sha256="5c086772357a50723b825fd5da5278ac7e3697cdf7797d07541a6c90b6ff754c")
    version("1.18.0", sha256="50e99c3110ce0afc3f7bdbadff1c71c17758e476731c27607940cfa6686489ca")
    version("1.17.0", sha256="b1244db3f45b4ef5a00106a46612da107cdfaf85f1580b8e1c059fefc98b0930")
    version("1.14.0", sha256="462ea91df03ff5d52813b5613fec1313a1a2059d2e37343e572b3f979867c5da")
    version("1.13.0", sha256="f8d275a2cc720735286b7c2e2bc35da05761e6d3695c2fa416550395f10c53c7")
    version("1.10.0", sha256="5d31f43dffaf6265c808e1b5353662ffa5146d844278b55caa6c7f74f427ec50")
    version("1.8.1", sha256="448b04b23faed669b2b565b998ac955af4feea66c5deed3a1212ac9399d2e1cd")
    version("1.4.1", sha256="13461b42876ade4f75ee5d2a2c656b288ca0aab7f048ef66657ef166996b2118")

    depends_on("py-editables@0.3:", type=("build", "run"))
    depends_on("py-packaging@21.3:", type=("build", "run"))
    depends_on("py-packaging@23.2:", when="@1.24.2:", type=("build", "run"))
    depends_on("py-pathspec@0.10.1:", when="@1.9:", type=("build", "run"))
    depends_on("py-pathspec@0.9:", type=("build", "run"))
    depends_on("py-pluggy@1:", type=("build", "run"))
    depends_on("py-tomli@1.2.2:", when="^python@:3.10", type=("build", "run"))
    depends_on("py-trove-classifiers", when="@1.14:", type=("build", "run"))
