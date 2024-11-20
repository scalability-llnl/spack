# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPyfftw(PythonPackage):
    """A pythonic wrapper around FFTW, the FFT library,
    presenting a unified interface for all the supported transforms."""

    homepage = "https://pyfftw.readthedocs.io/en/latest/"
    pypi = "pyFFTW/pyfftw-0.14.0.tar.gz"

    maintainers("paugier")

    license("BSD-3-Clause")

    version("0.14.0", sha256="a55f94d3da9b5c04de1bc96932a93f922910f3984557931356173a515277b65b")
    version("0.13.1", sha256="09155e90a0c6d0c1f2d1f3668180a7de95fb9f83fef5137a112fb05978e87320")
    version("0.13.0", sha256="da85102405c0bd95d57eb19e99b01a0729d8406cb204c3900894b873784253da")
    version("0.12.0", sha256="60988e823ca75808a26fd79d88dbae1de3699e72a293f812aa4534f8a0a58cb0")
    version("0.11.1", sha256="05ea28dede4c3aaaf5c66f56eb0f71849d0d50f5bc0f53ca0ffa69534af14926")
    version("0.10.4", sha256="739b436b7c0aeddf99a48749380260364d2dc027cf1d5f63dafb5f50068ede1a")

    depends_on("python@3.9:", type=("build", "run"), when="@0.14.0:")
    depends_on("python@3.8:3.11", type=("build", "run"), when="@:0.13.1")

    depends_on("py-setuptools@:59.4.0", type="build")

    depends_on("py-cython@3.0:3", type="build", when="@0.14.0:")
    depends_on("py-cython@0.29.18:0", type="build", when="@0.13.0:0.13")
    depends_on("py-cython@0.29:0", type="build", when="@:0.13")

    depends_on("py-numpy@2.0:2", type=("build", "run"), when="@0.14.0:")
    depends_on("py-numpy@1.20:1", type=("build", "run"), when="@0.13.1")
    depends_on("py-numpy@1.16:1", type=("build", "run"), when="@0.13.0")
    depends_on("py-numpy@1.10:1", type=("build", "run"), when="@0.11:0.12")
    depends_on("py-numpy@1.6:1", type=("build", "run"), when="@:0.10.4")

    depends_on("fftw@3.3:")

    def url_for_version(self, version):
        url = "https://files.pythonhosted.org/packages/source/p/pyfftw/{0}-{1}.tar.gz"
        if version >= Version("0.14.0"):
            name = "pyfftw"
        else:
            name = "pyFFTW"
        return url.format(name, version)

    def setup_build_environment(self, env):
        env.append_flags("LDFLAGS", self.spec["fftw"].libs.search_flags)
