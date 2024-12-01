# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyTern(PythonPackage):
    """
    Tern is a software package inspection tool that can create a Software Bill
    of Materials (SBoM) for containers.
    """

    pypi = "tern/tern-2.8.0.tar.gz"
    git = "https://github.com/tern-tools/tern.git"

    license("BSD-2-Clause")

    version("main", branch="main")

    depends_on("py-setuptools", type="build")
    depends_on("py-wheel", type="build")
    depends_on("py-pip", type="build")
