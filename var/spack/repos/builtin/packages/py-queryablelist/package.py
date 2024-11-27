# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyQueryablelist(PythonPackage):
    """Python module to add support for ORM-style filtering to any list of
    items"""

    homepage = "https://github.com/kata198/QueryableList"
    pypi = "queryablelist/QueryableList-3.1.0.tar.gz"

    license("LGPL-2.1-or-later")

    version("3.1.0", sha256="8891dccbadc69a35f5944e1826d8f8db224522aa3af913e301a7a448f5b411e9")

    depends_on("py-setuptools", type="build")
