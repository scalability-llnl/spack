# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyOptEinsum(PythonPackage):
    """Optimized Einsum: A tensor contraction order optimizer."""

    homepage = "https://github.com/dgasmith/opt_einsum"
    pypi = "opt_einsum/opt_einsum-3.1.0.tar.gz"

    license("MIT")

    version("3.4.0", sha256="96ca72f1b886d148241348783498194c577fa30a8faac108586b14f1ba4473ac")
    version("3.3.0", sha256="59f6475f77bbc37dcf7cd748519c0ec60722e91e63ca114e68821c0c54a46549")
    version("3.2.1", sha256="83b76a98d18ae6a5cc7a0d88955a7f74881f0e567a0f4c949d24c942753eb998")
    version("3.2.0", sha256="738b0a1db1d3084d360081bb64d826f9db06d2df7cc0bf8e2c9356028da1fa31")
    version("3.1.0", sha256="edfada4b1d0b3b782ace8bc14e80618ff629abf53143e1e6bbf9bd00b11ece77")

    with default_args(type=("build", "run")):
        depends_on("python@3.8:", when="@3.4:")
        # https://github.com/dgasmith/opt_einsum/commit/7c8f193f90b6771a6b3065bb5cf6ec2747af8209
        depends_on("python@:3.11", when="@:3.3")

        depends_on("py-numpy@1.7:", when="@:3.3")

    depends_on("py-setuptools", when="@:3.3", type="build")

    depends_on("py-hatchling", when="@3.4:", type="build")
    depends_on("py-hatch-fancy-pypi-readme@22.5:", when="@3.4:", type="build")
    depends_on("py-hatch-vcs", when="@3.4:", type="build")
