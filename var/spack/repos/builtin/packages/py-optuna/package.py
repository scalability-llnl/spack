# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyOptuna(PythonPackage):
    """Optuna is an automatic hyperparameter optimization software framework,
    particularly designed for machine learning. It features an imperative,
    define-by-run style user API. Thanks to our define-by-run API, the code
    written with Optuna enjoys high modularity, and the user of Optuna can
    dynamically construct the search spaces for the hyperparameters."""

    homepage = "https://optuna.org/"
    pypi = "optuna/optuna-3.2.0.tar.gz"

    maintainers("elliottslaughter", "eugeneswalker")

    license("MIT")

    version("3.2.0", sha256="683d8693643a761a41d251a6b8e13263b24acacf9fc46a9233d5f6aa3ce5c683")

    depends_on("py-setuptools@61.1:", type="build")

    depends_on("py-alembic@1.5:", type=("build", "run"))
    depends_on("py-cmaes@0.9.1:", type=("build", "run"))
    depends_on("py-colorlog", type=("build", "run"))
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-packaging@20:", type=("build", "run"))
    depends_on("py-pyyaml", type=("build", "run"))
    depends_on("py-sqlalchemy@1.3:", type=("build", "run"))
    depends_on("py-tqdm", type=("build", "run"))
