# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyFusepy(PythonPackage):
    """Fusepy is a Python module that provides a simple interface to FUSE and
    MacFUSE. It's just one file and is implemented using ctypes."""

    homepage = "https://github.com/fusepy/fusepy"
    pypi = "fusepy/fusepy-3.0.1.tar.gz"

    license("ISC")

    version("3.0.1", sha256="72ff783ec2f43de3ab394e3f7457605bf04c8cf288a2f4068b4cde141d4ee6bd")
    version("2.0.4", sha256="10f5c7f5414241bffecdc333c4d3a725f1d6605cae6b4eaf86a838ff49cdaf6c")

    depends_on("py-setuptools", type="build")
    depends_on("fuse@2.6:")
