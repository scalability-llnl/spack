# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyJupyterhub(PythonPackage):
    """Multi-user server for Jupyter notebooks."""

    pypi = "jupyterhub/jupyterhub-1.0.0.tar.gz"

    tags = ["e4s"]

    version("1.4.1", sha256="ee1b0718a4db8e0b339796e3e50b704ca6822ab22a7435289dbb5932f65b5199")
    version("1.0.0", sha256="33541a515a041b9a518ca057c1c4ab4215a7450fdddc206401713ee8137fa67f")
    version("0.9.4", sha256="7848bbb299536641a59eb1977ec3c7c95d931bace4a2803d7e9b28b9256714da")

    depends_on("py-alembic@1.4:", type=("build", "run"), when="@1.4.1:")
    depends_on("py-alembic", type=("build", "run"))
    depends_on("py-async-generator@1.9:", type=("build", "run"), when="@1.4.1:")
    depends_on("py-async-generator@1.8:", type=("build", "run"))
    depends_on("py-certipy@0.1.2:", when="@1.0.0:", type=("build", "run"))
    depends_on("py-entrypoints", when="@1.0.0:", type=("build", "run"))
    depends_on("py-jinja2@2.11.0:", type=("build", "run"), when="@1.4.1:")
    depends_on("py-jinja2", type=("build", "run"))
    depends_on("py-jupyter-telemetry@0.1.0:", type=("build", "run"), when="@1.4.1:")
    depends_on("py-mako", type=("build", "run"), when="@:1.4.1")
    depends_on("py-notebook", type=("build", "run"), when="@:1.4.1")
    depends_on("py-oauthlib@3.0:", when="@1.0.0:", type=("build", "run"))
    depends_on("py-pamela", type=("build", "run"))
    depends_on("py-prometheus-client@0.4.0:", type=("build", "run"), when="@1.4.1:")
    depends_on("py-prometheus-client@0.0.21:", type=("build", "run"))
    depends_on("py-python-dateutil", type=("build", "run"))
    depends_on("py-python-oauth2@1.0:", when="@:0.9.4", type=("build", "run"))
    depends_on("py-requests", type=("build", "run"))
    depends_on("py-setuptools", type=("build", "run"))
    depends_on("py-sqlalchemy@1.1:", type=("build", "run"))
    depends_on("py-tornado@5.1:", type=("build", "run"), when="@1.4.1:")
    depends_on("py-tornado@5.0:", type=("build", "run"))
    depends_on("py-traitlets@4.3.2:", type=("build", "run"))
    depends_on("python@3.6:", type=("build", "run"), when="@1.4.1:")
    depends_on("python@3.5:", type=("build", "run"))
