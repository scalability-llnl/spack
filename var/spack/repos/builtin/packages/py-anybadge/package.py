# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAnybadge(PythonPackage):
    """Python project for generating badges for your projects"""

    homepage = "https://github.com/jongracecox/anybadge"
    pypi = "anybadge/anybadge-1.14.0.tar.gz"

    version("1.14.0", sha256="47f06e0a6320d3e5eac55c712dc0bab71b9ed85353c591d448653c5a0740783f")

    depends_on("py-setuptools", type="build")
    depends_on("py-packaging", type="run")
