# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyEnumTools(PythonPackage):
    """Tools to expand Python's enum module."""

    homepage = "https://github.com/domdfcoding/enum_tools"
    pypi = "enum_tools/enum_tools-0.10.0.tar.gz"

    license("LGPL-3.0-or-later")

    version("0.10.0", sha256="777dc3cfb4314780bb9ca2460b518be58c3f29e13bd77b33badead4c2c136976")

    depends_on("py-whey", type="build")
    depends_on("py-pygments@2.6.1:", type=("build", "run"))
    depends_on("py-typing-extensions@3.7.4.3:", type=("build", "run"))
