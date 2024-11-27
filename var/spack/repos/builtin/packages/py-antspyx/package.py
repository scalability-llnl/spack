# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyAntspyx(PythonPackage):
    """Advanced Normalization Tools in Python."""

    homepage = "https://pypi.org/project/antspyx/"
    pypi = "antspyx/antspyx-0.3.7.tar.gz"

    license("Apache-2.0")

    version("0.3.7", sha256="cd831eb966d4ce82cc0afb65edddd8e2db6b439d418316e6356199f966104c1b")

    depends_on("python@3.6:", type=("build", "run"))
    depends_on("py-setuptools", type="build")

    depends_on("cmake@3.10:", type="build")
    depends_on("itk+review+antspy")

    depends_on("pil", type=("build", "run"))
    depends_on("py-pandas", type=("build", "run"))
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-scipy", type=("build", "run"))
    depends_on("py-scikit-image", type=("build", "run"))
    depends_on("py-scikit-learn", type=("build", "run"))
    depends_on("py-statsmodels", type=("build", "run"))
    depends_on("py-webcolors", type=("build", "run"))
    depends_on("py-matplotlib", type=("build", "run"))
    depends_on("py-pyyaml", type=("build", "run"))
    depends_on("py-chart-studio", type=("build", "run"))
    depends_on("py-nibabel", type=("build", "run"))

    # from ITK, somehow does not get passed through. Required for building, together with
    # the following patch
    depends_on("googletest")
    patch("fix-itk-gtest.diff")

    patch("submodule-imposter.diff")

    resource(
        name="submodule-imposter-pybind11",
        git="https://github.com/stnava/pybind11/",
        destination="ants/lib",
    )

    resource(
        name="submodule-imposter-antscore",
        git="https://github.com/ANTsX/ANTs.git",
        commit="871cad073908952b095e4b520335fc441e059264",
        destination="ants/lib",
        when="@0.3.7",  # ANTs dependency needs updating for every version
    )

    def setup_build_environment(self, env):
        env.set("ITK_DIR", self.spec["itk"].prefix)
