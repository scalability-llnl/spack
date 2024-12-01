# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPsycopg2(PythonPackage):
    """Python interface to PostgreSQL databases"""

    homepage = "https://psycopg.org/"
    pypi = "psycopg2/psycopg2-2.8.6.tar.gz"

    version("2.9.6", sha256="f15158418fd826831b28585e2ab48ed8df2d0d98f502a2b4fe619e7d5ca29011")
    version("2.9.1", sha256="de5303a6f1d0a7a34b9d40e4d3bef684ccc44a49bbe3eb85e3c0bffb4a131b7c")
    version("2.8.6", sha256="fb23f6c71107c37fd667cb4ea363ddeb936b348bbd6449278eb92c189699f543")

    depends_on("c", type="build")  # generated

    # https://www.psycopg.org/docs/install.html#prerequisites
    # https://github.com/psycopg/psycopg2/blob/master/doc/src/install.rst
    # https://www.psycopg.org/docs/news.html#news
    # https://pypi.org/project/psycopg2/#history
    depends_on("python@:3.11", when="@2.9.5:", type=("build", "link", "run"))
    depends_on("python@:3.10", when="@2.9.1:2.9.4", type=("build", "link", "run"))
    depends_on("python@:3.9", when="@2.8.6:2.9.0", type=("build", "link", "run"))

    depends_on("py-setuptools", type="build")

    depends_on("postgresql@9.1:15", when="@2.9.4:", type=("build", "link", "run"))
    depends_on("postgresql@9.1:14", when="@2.9.2:2.9.3", type=("build", "link", "run"))
    depends_on("postgresql@9.1:13", when="@2.9:2.9.1", type=("build", "link", "run"))
    depends_on("postgresql@9.1:12", when="@2.8.4:2.8", type=("build", "link", "run"))
    depends_on("postgresql@9.1:11", when="@2.8:2.8.3", type=("build", "link", "run"))
