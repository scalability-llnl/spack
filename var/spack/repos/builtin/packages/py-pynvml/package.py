# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyPynvml(PythonPackage):
    """Provides a Python interface to GPU management and monitoring
    functions. This is a wrapper around the NVML library. For
    information about the NVML library, see the NVML developer page
    https://developer.nvidia.com/nvidia-management-library-nvml"""

    homepage = "https://www.nvidia.com/"
    pypi = "pynvml/pynvml-8.0.4.tar.gz"

    license("Unlicense")

    version("8.0.4", sha256="c8d4eadc648c7e12a3c9182a9750afd8481b76412f83747bcc01e2aa829cde5d")

    depends_on("py-setuptools", type="build")
    depends_on("python@3.6:", type=("build", "run"))
