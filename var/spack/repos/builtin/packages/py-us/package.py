# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyUs(PythonPackage):
    """US state meta information and other fun stuff."""

    pypi = "us/us-1.0.0.tar.gz"

    license("BSD-3-Clause")

    version("1.0.0", sha256="09dc9ba763e2e4399e6a042104f3e415a7de6bfa4df6f557b4f19e3ba9a22fda")

    depends_on("py-setuptools", type="build")
    depends_on("py-jellyfish@0.5.6", type=("build", "run"))
