# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyMultiKeyDict(PythonPackage):
    """Multi key dictionary implementation"""

    homepage = "https://github.com/formiaczek/multi_key_dict"
    pypi = "multi_key_dict/multi_key_dict-2.0.3.tar.gz"

    version("2.0.3", sha256="deebdec17aa30a1c432cb3f437e81f8621e1c0542a0c0617a74f71e232e9939e")

    # pip silently replaces distutils with setuptools
    depends_on("py-setuptools", type="build")
