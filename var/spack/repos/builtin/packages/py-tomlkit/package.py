# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyTomlkit(PythonPackage):
    """Style preserving TOML library"""

    homepage = "https://github.com/sdispater/tomlkit"
    pypi = "tomlkit/tomlkit-0.7.0.tar.gz"

    license("MIT")

    version("0.12.1", sha256="38e1ff8edb991273ec9f6181244a6a391ac30e9f5098e7535640ea6be97a7c86")
    version("0.11.4", sha256="3235a9010fae54323e727c3ac06fb720752fe6635b3426e379daec60fbd44a83")
    version("0.11.0", sha256="71ceb10c0eefd8b8f11fe34e8a51ad07812cb1dc3de23247425fbc9ddc47b9dd")
    version("0.7.2", sha256="d7a454f319a7e9bd2e249f239168729327e4dd2d27b17dc68be264ad1ce36754")
    version("0.7.0", sha256="ac57f29693fab3e309ea789252fcce3061e19110085aa31af5446ca749325618")

    depends_on("python@3.6:3", when="@0.11.0:0.11.5", type=("build", "run"))
    depends_on("py-poetry-core@1:", type="build")
