# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class PyHollandBackup(PythonPackage):
    """Holland is an Open Source backup framework originally developed
    by Rackspace and written in Python. Its goal is to help facilitate
    backing up databases with greater configurability, consistency, and ease.
    Holland currently focuses on MySQL, however future development will include
    other database platforms and even non-database related applications.
    Because of its plugin structure, Holland can be used to backup anything
    you want by whatever means you want."""

    homepage = "https://hollandbackup.org/"
    url = "https://github.com/holland-backup/holland/archive/1.2.2.tar.gz"

    license("BSD-3-Clause")

    version("1.2.2", sha256="836337c243b2dff5ff6a3ce0b647f123ab24697a5de8ac8ae8b7839aa23dff68")

    depends_on("py-setuptools", type=("build", "run"))
    depends_on("py-configobj@4.6.0:", type=("build", "run"))
