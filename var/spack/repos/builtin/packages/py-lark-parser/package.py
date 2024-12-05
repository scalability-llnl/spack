# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyLarkParser(PythonPackage):
    """Lark is a modern general-purpose parsing library for Python."""

    homepage = "https://github.com/lark-parser/lark/"
    pypi = "lark-parser/lark-parser-0.6.2.tar.gz"

    license("MIT")

    version("0.12.0", sha256="15967db1f1214013dca65b1180745047b9be457d73da224fcda3d9dd4e96a138")

    depends_on("py-setuptools", type="build")
