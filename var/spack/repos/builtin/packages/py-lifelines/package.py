# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyLifelines(PythonPackage):
    """Survival analysis was originally developed and applied heavily
    by the actuarial and medical community. Its purpose was to answer
    *why do events occur now versus later* under uncertainty (where
    *events* might refer to deaths, disease remission,
    etc.). *lifelines* is a pure Python implementation of the best
    parts of survival analysis."""

    homepage = "https://github.com/CamDavidsonPilon/lifelines"
    pypi = "lifelines/lifelines-0.25.5.tar.gz"

    license("MIT")

    version("0.25.5", sha256="f24260aa371829354440dfc2c1be8d59d9e841cce7a933230213cecd67787b89")
    version("0.9.4", sha256="0f19a8b18ace80c231de60487b2b1a3de3eb418445c6a6d0d72c1110d860f676")

    depends_on("py-setuptools", type="build")
    depends_on("py-numpy", type=("build", "run"), when="@0.9.4")
    depends_on("py-scipy", type=("build", "run"), when="@0.9.4")
    depends_on("py-pandas@0.18.0:", type=("build", "run"), when="@0.9.4")
    depends_on("python@3.6:", type=("build", "run"), when="@0.25.5:")
    depends_on("py-pandas@0.23.0:", type=("build", "run"), when="@0.25.5:")
    depends_on("py-scipy@1.2.0:", type=("build", "run"), when="@0.25.5:")
    depends_on("py-numpy@1.14:", type=("build", "run"), when="@0.25.5:")
    depends_on("py-pandas@0.23.0:", type=("build", "run"), when="@0.25.5:")
    depends_on("py-matplotlib@3.0:", type=("build", "run"), when="@0.25.5:")
    depends_on("py-autograd@1.3:", type=("build", "run"), when="@0.25.5:")
    depends_on("py-autograd-gamma@0.3:", type=("build", "run"), when="@0.25.5:")
    depends_on("py-patsy@0.5.0:", type=("build", "run"), when="@0.25.5:")
