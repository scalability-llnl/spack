# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyTermgraph(PythonPackage):
    """Command-line tool that draws basic graphs in the terminal, written in
    Python."""

    homepage = "https://github.com/mkaz/termgraph"
    pypi = "termgraph/termgraph-0.5.3.tar.gz"

    maintainers("TomMelt")

    license("MIT", checked_by="tommelt")

    version("0.5.3", sha256="36ff2098e41eeab1e7cdda7366dc3e5b514ea799fa3e77537564492a7edefdd5")

    depends_on("py-setuptools", type="build")
    depends_on("py-colorama", type=("build", "run"))
