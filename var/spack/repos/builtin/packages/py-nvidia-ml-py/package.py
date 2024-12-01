# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyNvidiaMlPy(PythonPackage):
    """Python Bindings for the NVIDIA Management Library."""

    homepage = "https://www.nvidia.com/"
    pypi = "nvidia-ml-py/nvidia-ml-py-11.450.51.tar.gz"

    license("Unlicense")

    version("11.450.51", sha256="5aa6dd23a140b1ef2314eee5ca154a45397b03e68fd9ebc4f72005979f511c73")

    # pip silently replaces distutils with setuptools
    depends_on("py-setuptools", type="build")
