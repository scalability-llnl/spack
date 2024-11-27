# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyTypesDataclasses(PythonPackage):
    """Typing stubs for dataclasses"""

    homepage = "https://github.com/python/typeshed"
    pypi = "types-dataclasses/types-dataclasses-0.6.6.tar.gz"

    version("0.6.6", sha256="4b5a2fcf8e568d5a1974cd69010e320e1af8251177ec968de7b9bb49aa49f7b9")

    depends_on("py-setuptools", type="build")
