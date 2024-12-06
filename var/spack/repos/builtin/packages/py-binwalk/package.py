# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyBinwalk(PythonPackage):
    """Binwalk is a fast, easy to use tool for analyzing, reverse engineering,
    and extracting firmware images."""

    homepage = "https://github.com/devttys0/binwalk"
    pypi = "binwalk/binwalk-2.1.0.tar.gz"

    version("2.1.0", sha256="218c8045c6cb3ed6e21814fb89cdb913808b02dfe5a6cc30f85f4a59e8129f6b")

    depends_on("python")
    depends_on("py-setuptools", type="build")
