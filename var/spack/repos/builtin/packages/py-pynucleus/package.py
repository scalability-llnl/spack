# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.build_systems.python import PythonPipBuilder
from spack.package import *


class PyPynucleus(PythonPackage):
    """PyNucleus is a finite element code that specifically targets nonlocal operators."""

    homepage = "https://sandialabs.github.io/PyNucleus/index.html"
    git = "https://github.com/sandialabs/PyNucleus.git"

    maintainers("cgcgcg")

    refs = ["master", "develop"]

    license("MIT")

    for ref in refs:
        version(ref, branch=ref)

    variant("examples", default=True, description="Install examples")
    variant("tests", default=True, description="Install tests")

    depends_on("python@3.10:", type=("build", "run"))
    depends_on("py-mpi4py@2.0.0:", type=("build", "link", "run"))
    depends_on("py-cython@0.29.32:", type=("build", "run"))
    depends_on("py-numpy", type=("build", "link", "run"))
    depends_on("py-scipy", type=("build", "link", "run"))
    depends_on("metis", type=("build", "link", "run"))
    depends_on("parmetis", type=("build", "link", "run"))
    depends_on("suite-sparse", type=("build", "run"))
    depends_on("py-h5py", type=("build", "run"))
    depends_on("py-tabulate", type=("build", "run"))
    depends_on("py-pyyaml", type=("build", "run"))
    depends_on("py-matplotlib", type=("build", "run"))
    depends_on("py-scikit-sparse", type=("build", "run"))
    depends_on("py-modepy", type=("build", "run"))
    depends_on("py-meshpy", type=("build", "run"))
    depends_on("py-pytools", type=("build", "run"))
    depends_on("py-psutil", type="run")
    depends_on("py-pytest", when="+tests", type="run")
    depends_on("py-pytest-html", when="+tests", type="run")

    import_modules = [
        "PyNucleus",
        "PyNucleus-packageTools",
        "PyNucleus-base",
        "PyNucleus-metisCy",
        "PyNucleus-fem",
        "PyNucleus-multilevelSolver",
        "PyNucleus-nl",
    ]

    def setup_build_environment(self, env):
        env.set("PYNUCLEUS_BUILD_PARALLELISM", make_jobs)

    @run_before("install")
    def install_python(self):
        for subpackage in ["packageTools", "base", "metisCy", "fem", "multilevelSolver", "nl"]:
            with working_dir(subpackage):
                pip(*PythonPipBuilder.std_args(self), f"--prefix={self.prefix}", ".")

    @run_after("install")
    def install_additional_files(self):
        spec = self.spec
        prefix = self.prefix
        if "+examples" in spec or "+tests" in spec:
            install_tree("drivers", prefix.drivers)
        if "+examples" in spec:
            install_tree("examples", prefix.examples)
        if "+tests" in spec:
            install_tree("tests", prefix.tests)
