# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyYtopt(PythonPackage):
    """Ytopt package implements search using Random Forest (SuRF), an autotuning
    search method developed within Y-Tune ECP project."""

    maintainers("Kerilk")

    homepage = "https://github.com/ytopt-team/ytopt"
    url = "https://github.com/ytopt-team/ytopt/archive/refs/tags/v0.0.1.tar.gz"

    license("BSD-2-Clause")

    version("0.0.4", sha256="4e47315b658f1943f756816455ae491818c37b0f700dd895a97fb7792bb49e35")
    version("0.0.3", sha256="eac6ab87d4fd27517f136880016359c5b24836ec009e8cc9b4073a6c5edb17af")
    version("0.0.2", sha256="5a624aa678b976ff6ef867610bafcb0dfd5c8af0d880138ca5d56d3f776e6d71")
    version("0.0.1", sha256="3ca616922c8e76e73f695a5ddea5dd91b0103eada726185f008343cc5cbd7744")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant(
        "online",
        default=False,
        description="Install requirements for online tuning.",
        when="@0.0.3:",
    )

    depends_on("python@3.6:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-scikit-learn@0.23.1", type=("build", "run"), when="@:0.0.2")
    depends_on("py-scikit-learn@1.0.0:", type=("build", "run"), when="@0.0.3:")
    depends_on("py-dh-scikit-optimize", type=("build", "run"))
    depends_on("py-configspace", type=("build", "run"))
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-ytopt-autotune@1.0.0:1.0.999", type=("build", "run"))
    depends_on("py-joblib", type=("build", "run"))
    depends_on("py-deap", type=("build", "run"))
    depends_on("py-tqdm", type=("build", "run"))
    depends_on("py-ray", type=("build", "run"))
    depends_on("py-mpi4py@3.0.0:", type=("build", "run"))
    depends_on("py-sdv@0.13.1:0.13", type=("build", "run"), when="@0.0.3: +online")
