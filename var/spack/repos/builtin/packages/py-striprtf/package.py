# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyStriprtf(PythonPackage):
    """A simple library to convert rtf to text"""

    homepage = "https://github.com/joshy/striprtf"
    pypi = "striprtf/striprtf-0.0.26.tar.gz"

    license("BSD-3-Clause", checked_by="qwertos")

    version("0.0.26", sha256="fdb2bba7ac440072d1c41eab50d8d74ae88f60a8b6575c6e2c7805dc462093aa")

    depends_on("py-setuptools", type="build")
