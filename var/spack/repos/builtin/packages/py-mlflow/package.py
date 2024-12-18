# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyMlflow(PythonPackage):
    """MLflow: A Platform for ML Development and Productionization."""

    homepage = "https://pypi.org/project/mlflow/"
    pypi = "mlflow/mlflow-2.0.1.tar.gz"

    license("Apache-2.0")

    version("2.0.1", sha256="7ce6caf3c6acb022d6f5ce8a0995a92be1db524ae16aade1f83da661cdf993de")
    version("1.17.0", sha256="4898c58899e3101e09e2b37cf5bee7db04c5d73389a56942d3ef5a5e4396799e")

    depends_on("python@3.6:", type=("build", "run"), when="@1.17.0:")
    depends_on("python@3.7:", type=("build", "run"), when="@1.24.0:")
    depends_on("python@3.8:", type=("build", "run"), when="@2.0.1:")
    depends_on("py-setuptools", type="build")

    depends_on("py-click@7.0:8", type=("build", "run"))
    depends_on("py-cloudpickle@:2", type=("build", "run"))
    depends_on("py-databricks-cli@0.8.7:0", type=("build", "run"))
    depends_on("py-entrypoints@:0", type=("build", "run"))
    depends_on("py-gitpython@2.1.0:3", type=("build", "run"))
    depends_on("py-pyyaml@5.1:6", type=("build", "run"))
    depends_on("py-protobuf@3.12.0:4", type=("build", "run"))
    depends_on("py-pytz@:2022", type=("build", "run"))
    depends_on("py-requests@2.17.3:2", type=("build", "run"))
    depends_on("py-packaging@:21", type=("build", "run"))
    depends_on("py-importlib-metadata@3.7:4.6,4.7.1:5", type=("build", "run"))
    depends_on("py-sqlparse@0.4.0:0", type=("build", "run"))

    depends_on("py-alembic@:1", type=("build", "run"))
    depends_on("py-docker@4.0.0:6", type=("build", "run"))
    depends_on("py-flask@:2", type=("build", "run"))
    depends_on("py-numpy@:1", type=("build", "run"))
    depends_on("py-scipy@:1", type=("build", "run"))
    depends_on("py-pandas@:1", type=("build", "run"))
    depends_on("py-querystring-parser@:1", type=("build", "run"))
    depends_on("py-sqlalchemy@1.4.0:1", type=("build", "run"))
    for platform in ["linux", "darwin"]:
        depends_on("py-gunicorn@:20", type=("build", "run"), when=f"platform={platform}")
    depends_on("py-waitress@:2", type=("build", "run"), when="platform=windows")
    depends_on("py-scikit-learn@:1", type=("build", "run"))
    depends_on("py-pyarrow@4.0.0:10", type=("build", "run"))
    depends_on("py-shap@0.40:0", type=("build", "run"))
    depends_on("py-markdown@3.3:3", type=("build", "run"))
    for platform in ["linux", "darwin"]:
        depends_on("py-jinja2@2.11:3", type=("build", "run"), when=f"platform={platform}")
    depends_on("py-jinja2@3.0:3", type=("build", "run"), when="platform=windows")
    depends_on("py-matplotlib@:3", type=("build", "run"))
