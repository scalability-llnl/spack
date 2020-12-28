# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class PyNvidiaMlPy(PythonPackage):
    """Python Bindings for the NVIDIA Management Library."""

    homepage = "http://www.nvidia.com/"
    url      = "https://pypi.io/packages/source/n/nvidia-ml-py/nvidia-ml-py-11.450.51.tar.gz"

    version('11.450.51', sha256='5aa6dd23a140b1ef2314eee5ca154a45397b03e68fd9ebc4f72005979f511c73')
