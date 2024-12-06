# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyMizani(PythonPackage):
    """Mizani is a scales package for graphics. It is based on Hadley Wickham's
    Scales package."""

    homepage = "https://mizani.readthedocs.io/en/latest"
    pypi = "mizani/mizani-0.7.4.tar.gz"

    license("BSD-3-Clause")

    version("0.8.1", sha256="8ad0a0efa52f1bcdf41f675b64a8c0f7cd24e763d53baced6613f20bd6ed4928")
    version("0.7.4", sha256="b84b923cd3b8b4c0421a750672e5a85ed2aa05e632bd37af8419d5bbf65c397c")
    version("0.7.3", sha256="f521300bd29ca918fcd629bc8ab50fa04e41bdbe00f6bcf74055d3c6273770a4")
    version("0.6.0", sha256="2cdba487ee54faf3e5bfe0903155a13ff13d27a2dae709f9432194915b4fb1cd")

    # common requirements
    depends_on("py-palettable", type=("build", "run"))

    # variable requirements
    depends_on("python@3.8:", type=("build", "run"), when="@0.7.4:")
    depends_on("python@3.6:", type=("build", "run"), when="@0.6.0:")

    depends_on("py-setuptools@45:", type="build", when="@0.8.1:")
    depends_on("py-setuptools@42:", type="build", when="@0.7.4:")
    depends_on("py-setuptools", type="build", when="@0.6.0:")

    depends_on("py-setuptools-scm@6.2:", type="build", when="@0.8.1:")

    depends_on("py-matplotlib@3.5.0:", type=("build", "run"), when="@0.7.4:")
    depends_on("py-matplotlib@3.1.1:", type=("build", "run"), when="@0.6.0:")

    depends_on("py-numpy@1.19.0:", type=("build", "run"), when="@0.7.4:")
    depends_on("py-numpy", type=("build", "run"), when="@0.6.0:")

    depends_on("py-scipy@1.5.0:", type=("build", "run"), when="@0.7.4:")

    depends_on("py-pandas@1.3.5:", type=("build", "run"), when="@0.7.4:")
    depends_on("py-pandas@1.1.0:", type=("build", "run"), when="@0.7.2:")
    depends_on("py-pandas@1.0.0:", type=("build", "run"), when="@0.7.0:")
    depends_on("py-pandas@0.25.0:", type=("build", "run"), when="@0.6.0:")

    depends_on("py-backports-zoneinfo", type=("build", "run"), when="@0.8.1:^python@:3.8")
