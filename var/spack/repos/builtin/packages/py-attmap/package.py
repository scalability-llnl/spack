# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAttmap(PythonPackage):
    """Key-value mapping that supports nested attribute-style access."""

    homepage = "https://github.com/pepkit/attmap/"
    pypi = "attmap/attmap-0.13.2.tar.gz"

    license("BSD-2-Clause")

    version("0.13.2", sha256="fdffa45f8671c13428eb8c3a1702bfdd1123badb99f7af14d72ad53cc7e770de")

    depends_on("py-setuptools", type="build")

    depends_on("py-ubiquerg@0.2.1:", type=("build", "run"))
