# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyNvidiaMlPy3(PythonPackage):
    """Python Bindings for the NVIDIA Management Library."""

    homepage = "https://www.nvidia.com/"
    pypi = "nvidia-ml-py3/nvidia-ml-py3-7.352.0.tar.gz"

    license("Unlicense")

    version("7.352.0", sha256="390f02919ee9d73fe63a98c73101061a6b37fa694a793abf56673320f1f51277")

    # pip silently replaces distutils with setuptools
    depends_on("py-setuptools", type="build")
