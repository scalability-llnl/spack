# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyNibetaseries(PythonPackage):
    """BetaSeries Correlations implemented in Nipype."""

    homepage = "https://github.com/HBClab/NiBetaSeries"
    pypi = "nibetaseries/nibetaseries-0.6.0.tar.gz"
    git = "https://github.com/HBClab/NiBetaSeries.git"

    license("MIT")

    version("master", branch="master")

    depends_on("python@3.5:", type=("build", "run"))
    depends_on("py-setuptools@40.8:", type="build")
    depends_on("py-cython", type="build")

    with when("@master"):
        depends_on("py-nipype@1.5.1:", type=("build", "run"))
        depends_on("py-pybids@0.11.1:", type=("build", "run"))
        depends_on("py-nibabel@3:", type=("build", "run"))
        depends_on("py-nistats@0.0.1b2", type=("build", "run"))
        depends_on("py-niworkflows@1.3.1:1.3", type=("build", "run"))
        depends_on("py-nilearn", type=("build", "run"))
        depends_on("py-pandas", type=("build", "run"))
        depends_on("py-numpy", type=("build", "run"))
        depends_on("py-duecredit", type=("build", "run"))
        depends_on("py-scikit-learn@0.22.0:0.22", type=("build", "run"))
        depends_on("py-matplotlib", type=("build", "run"))
        depends_on("py-mne", type=("build", "run"))
        # pypiwin32; platform_system=="Windows"

    @run_after("install")
    def patch_bin(self):
        # pkg_resources fails to find the dependencies, resulting in errors
        # like: pkg_resources.DistributionNotFound: The 'sklearn' distribution
        # was not found and is required by nilearn
        filter_file(
            "__requires__ = 'nibetaseries==0.post1+gaa7d2ea'",
            "",
            join_path(self.prefix.bin, "nibs"),
            string=True,
        )
