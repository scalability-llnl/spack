# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyBarectf(PythonPackage):
    """barectf (from bare metal and CTF) is a generator of
    tracer which produces CTF data streams."""

    pypi = "barectf/barectf-3.1.2.tar.gz"

    license("MIT")

    version("3.1.2", sha256="d4d626b22a33b7d9bc9ac033bba8893890aba0ee1011c9e78429a67296c09e1c")

    depends_on("py-poetry-core", type="build")
