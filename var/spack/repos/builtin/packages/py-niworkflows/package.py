# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyNiworkflows(PythonPackage):
    """Common workflows for MRI (anatomical, functional, diffusion, etc)"""

    homepage = "https://github.com/nipreps/niworkflows"
    pypi = "niworkflows/niworkflows-1.4.0.tar.gz"

    license("Apache-2.0")

    version("1.4.0", sha256="d4e59070fde0290e0bfeece120ff1d2ff1f9573e3f2e6a719fe463c913af25ec")
    version("1.3.5", sha256="92e24f3462fb3ad4d8ee724506fba05da2b3ca0626850dd2e637a553e17d69b8")
    version("1.0.4", sha256="34bfa5561e6f872dbd85bb30a1b44c5e1be525167abe3932aee8ac06d15f6ed9")

    variant("fsl", default=False, description="Enable fsl support.")
    variant("ants", default=False, description="Enable ants support.")

    depends_on("python@3.7:", when="@1.3.3:", type=("build", "run"))
    depends_on("python@3.6:", when="@1.2:", type=("build", "run"))
    depends_on("python@3.5:", type=("build", "run"))
    depends_on("py-setuptools@38.4.1:", when="@1.2.3:", type="build")
    depends_on("py-setuptools@30.4.0:", type="build")
    depends_on("py-attrs", when="@1.1.4:", type=("build", "run"))
    depends_on("py-jinja2", type=("build", "run"))
    depends_on("py-matplotlib@2.2.0:", type=("build", "run"))
    depends_on("py-nibabel@3.0.1:", when="@1.1.6:", type=("build", "run"))
    depends_on("py-nibabel@2.4.1:", type=("build", "run"))
    depends_on("py-nilearn@0.2.6:0.4,0.5.2:", type=("build", "run"))
    depends_on("py-nipype@1.5.1:", when="@1.3:", type=("build", "run"))
    depends_on("py-nipype@1.3.1:", type=("build", "run"))
    depends_on("py-nitransforms@20:20.1", when="@1.2:", type=("build", "run"))
    depends_on("py-numpy", when="@1.3.3:", type=("build", "run"))
    depends_on("py-packaging", type=("build", "run"))
    depends_on("py-pandas", type=("build", "run"))
    depends_on("py-pybids@0.11.1:", when="@1.3:", type=("build", "run"))
    depends_on("py-pybids@0.9.4:", type=("build", "run"))
    depends_on("py-pyyaml", type=("build", "run"))
    depends_on("py-scikit-image", type=("build", "run"))
    depends_on("py-scikit-learn", when="@:1.3", type=("build", "run"))
    depends_on("py-scipy", type=("build", "run"))
    depends_on("py-seaborn", type=("build", "run"))
    depends_on("py-svgutils@0.3.4:", when="@1.4:", type=("build", "run"))
    depends_on("py-svgutils@0.3.1", when="@1.3.5", type=("build", "run"))
    depends_on("py-svgutils", type=("build", "run"))
    depends_on("py-transforms3d", type=("build", "run"))
    depends_on("py-templateflow@0.6:", when="@1.3:", type=("build", "run"))
    depends_on("py-templateflow@0.4.1:0.4", when="@:1.0", type=("build", "run"))

    with when("+fsl"):
        depends_on("fsl@5.0.9:", type=("build", "run"))
    with when("+ants"):
        depends_on("ants@2.2:", type=("build", "run"))

    # dependencies that are not yet in spack
    # depends_on('afni@Debian-16.2.07:', type=('build', 'run'))
    # depends_on('c3d@1:', type=('build', 'run'))
    # depends_on('freesurfer@6.0.1:', type=('build', 'run'))
