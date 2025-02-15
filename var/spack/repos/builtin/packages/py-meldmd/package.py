# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.build_systems.python import PythonPipBuilder
from spack.package import *


class PyMeldmd(CMakePackage, PythonExtension, CudaPackage):
    """MELD is a tool for inferring the structure of
    biomolecules from sparse, ambiguous, or noisy data."""

    homepage = "http://meldmd.org/"
    url = "https://github.com/maccallumlab/meld/archive/refs/tags/0.4.20.tar.gz"

    license("LGPL-3.0-or-later")

    version("0.6.1", sha256="aae8e5bfbdacc1e6de61768a3298314c51575cda477a511e98dc11f5730fd918")
    version("0.4.20", sha256="8c8d2b713f8dc0ecc137d19945b3957e12063c8dda569696e47c8820eeac6c92")

    depends_on("cxx", type="build")  # generated

    extends("python")

    depends_on("python@3.6:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("amber")
    depends_on("openmm+cuda")
    depends_on("py-netcdf4", type=("build", "run"))
    # Meld uses np.bool, deprecated in py-numpy@1.24.0
    # https://numpy.org/devdocs/release/1.24.0-notes.html
    depends_on("py-numpy@:1.23", type=("build", "run"))
    depends_on("py-scipy", type=("build", "run"))
    depends_on("py-scikit-learn", type=("build", "run"))
    depends_on("py-parmed", type=("build", "run"))
    depends_on("py-tqdm", type=("build", "run"))
    depends_on("py-mpi4py", type=("build", "run"))
    depends_on("py-pip", type="build")

    # C++ / CUDA
    depends_on("eigen", type="link")
    depends_on("swig@4.0", type="build")

    def cmake_args(self):
        args = []
        args.append("-DOPENMM_DIR={0}".format(self.spec["openmm"].prefix))
        return args

    root_cmakelists_dir = "plugin"

    @run_after("install")
    def install_python(self):
        pip(*PythonPipBuilder.std_args(self), f"--prefix={self.prefix}", ".")
        with working_dir(join_path(self.build_directory, "python")):
            make("MeldPluginPatch")
            pip(*PythonPipBuilder.std_args(self), f"--prefix={self.prefix}", ".")
        for _, _, files in os.walk(self.spec["openmm"].prefix.lib.plugins):
            for f in files:
                os.symlink(
                    join_path(self.spec["openmm"].prefix.lib.plugins, f),
                    join_path(self.prefix.lib.plugins, f),
                )

    def patch(self):
        filter_file(
            "# Compile the Python module.",
            "# Compile the Python module.\n"
            'add_custom_target(MeldPluginPatch DEPENDS "${WRAP_FILE}")',
            "plugin/python/CMakeLists.txt",
            string=True,
        )
        # Fixed, but not versioned yet:
        # https://github.com/maccallumlab/meld/commit/afe4b0c199e3562d112af7825f8839e76067039c
        filter_file(
            "MAXFLOAT", "FLT_MAX", "plugin/platforms/cuda/src/kernels/computeMeld.cu", string=True
        )
        # API Change: https://github.com/openmm/openmm/releases/tag/7.6.0
        if self.spec.satisfies("^openmm@7.6.0:"):
            filter_file("simtk.openmm", "openmm", "plugin/python/meldplugin.i", string=True)

    def setup_run_environment(self, env):
        env.set("OPENMM_PLUGIN_DIR", self.prefix.lib.plugins)

    @run_after("install")
    @on_package_attributes(run_tests=True)
    def install_test(self):
        python("-m", "meld.test_install")
