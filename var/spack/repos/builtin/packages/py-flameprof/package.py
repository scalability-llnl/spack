# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyFlameprof(PythonPackage):
    """Flamegraph generator for python's cProfile stats."""

    homepage = "https://github.com/baverman/flameprof/"
    pypi = "flameprof/flameprof-0.4.tar.gz"

    maintainers("haampie")

    license("MIT")

    version("0.4", sha256="dbc86d4190cbbba624f1e0a40f44d9db96138e27534d83c8ef42d420857875a3")

    depends_on("py-setuptools", type="build")
