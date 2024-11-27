# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyAlembic(PythonPackage):
    """Alembic is a database migrations tool."""

    pypi = "alembic/alembic-1.0.7.tar.gz"

    license("MIT")

    version("1.5.5", sha256="df0028c19275a2cff137e39617a39cdcdbd1173733b87b6bfa257b7c0860213b")
    version("1.0.7", sha256="16505782b229007ae905ef9e0ae6e880fddafa406f086ac7d442c1aaf712f8c2")

    depends_on("python@2.7:2.8,3.6:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-sqlalchemy@1.3.0:", type=("build", "run"), when="@1.5:")
    depends_on("py-sqlalchemy@1.1.0:", type=("build", "run"), when="@:1.4")
    depends_on("py-mako", type=("build", "run"))
    depends_on("py-python-dateutil", type=("build", "run"))
    depends_on("py-python-editor@0.3:", type=("build", "run"))
