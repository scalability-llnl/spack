# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyResolvelib(PythonPackage):
    """Resolve abstract dependencies into concrete ones."""

    homepage = "https://github.com/sarugaku/resolvelib"
    pypi = "resolvelib/resolvelib-1.0.1.tar.gz"

    license("ISC")

    version("1.0.1", sha256="04ce76cbd63fded2078ce224785da6ecd42b9564b1390793f64ddecbe997b309")

    depends_on("py-setuptools@36.2.2:", type="build")
    depends_on("py-wheel@0.28:", type="build")
