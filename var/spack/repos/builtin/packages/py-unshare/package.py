# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyUnshare(PythonPackage):
    """Python extension for Linux kernel's unshare syscall."""

    homepage = "https://github.com/shubham1172/unshare"
    pypi = "unshare/unshare-0.22.tar.gz"

    version("0.22", sha256="d521d72cca6e876f22cbd5ff5eb51f1beef75e8f9c53b599b55fa05fba1dd3a6")

    depends_on("c", type="build")  # generated

    depends_on("py-setuptools", type="build")

    conflicts("platform=darwin", msg="unshare is linux-only")
