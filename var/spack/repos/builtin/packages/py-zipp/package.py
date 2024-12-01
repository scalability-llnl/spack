# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyZipp(PythonPackage):
    """Backport of pathlib-compatible object wrapper for zip files."""

    homepage = "https://github.com/jaraco/zipp"
    pypi = "zipp/zipp-0.6.0.tar.gz"

    license("MIT")

    version("3.17.0", sha256="84e64a1c28cf7e91ed2078bb8cc8c259cb19b76942096c8d7b84947690cabaf0")
    version("3.8.1", sha256="05b45f1ee8f807d0cc928485ca40a07cb491cf092ff587c0df9cb1fd154848d2")
    version("3.6.0", sha256="71c644c5369f4a6e07636f0aa966270449561fcea2e3d6747b8d23efaa9d7832")
    version("0.6.0", sha256="3718b1cbcd963c7d4c5511a8240812904164b7f381b647143a89d3b98f9bcd8e")
    version("0.5.1", sha256="ca943a7e809cc12257001ccfb99e3563da9af99d52f261725e96dfe0f9275bc3")

    depends_on("python@3.8:", when="@3.16:", type=("build", "run"))
    # needed for spack bootstrap as spack itself supports python 3.6
    depends_on("python@3.7:", when="@3.8.1:", type=("build", "run"))
    depends_on("py-setuptools@56:", when="@3.5.1:", type="build")
    depends_on("py-setuptools@34.4:", when="@0.3.3:", type="build")
    depends_on("py-setuptools-scm@3.4.1: +toml", when="@2.0.1:", type="build")
    depends_on("py-setuptools-scm@1.15.0:", type="build")

    # Historical dependencies
    depends_on("py-more-itertools", type=("build", "run"), when="@0.6.0:2.1.0")
