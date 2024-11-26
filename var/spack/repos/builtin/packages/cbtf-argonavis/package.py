# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *
from spack.pkg.builtin.boost import Boost


class CbtfArgonavis(CMakePackage):
    """CBTF Argo Navis project contains the CUDA collector and supporting
    libraries that was done as a result of a DOE SBIR grant.
    """

    homepage = "https://sourceforge.net/p/cbtf/wiki/Home/"
    git = "https://github.com/OpenSpeedShop/cbtf-argonavis.git"

    maintainers("jgalarowicz")

    version("develop", branch="master")
    version("1.9.4.1", branch="1.9.4.1")
    version("1.9.4", branch="1.9.4")
    version("1.9.3", branch="1.9.3")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant(
        "crayfe",
        default=False,
        description="build only the FE tool using the runtime_dir \
                         to point to target build.",
    )
    variant(
        "runtime", default=False, description="build only the runtime libraries and collectors."
    )

    variant(
        "build_type",
        default="RelWithDebInfo",
        description="The build type to build",
        values=("Debug", "Release", "RelWithDebInfo"),
    )

    depends_on("cmake@3.0.2:", type="build")

    # To specify ^elfutils@0.170 on the command line spack
    # apparently needs/wants this dependency explicity here
    # even though it is referenced downstream
    depends_on("elfutils", type="link")

    # For boost
    depends_on("boost@1.70.0:")

    # TODO: replace this with an explicit list of components of Boost,
    # for instance depends_on('boost +filesystem')
    # See https://github.com/spack/spack/pull/22303 for reference
    depends_on(Boost.with_default_variants)

    # For MRNet
    depends_on("mrnet@5.0.1-3:+lwthreads", when="@develop", type=("build", "link", "run"))
    depends_on("mrnet@5.0.1-3+lwthreads", when="@1.9.3:9999", type=("build", "link", "run"))

    # For CBTF
    depends_on("cbtf@develop", when="@develop", type=("build", "link", "run"))
    depends_on("cbtf@1.9.3:9999", when="@1.9.3:9999", type=("build", "link", "run"))

    # For CBTF with runtime
    depends_on("cbtf@develop+runtime", when="@develop+runtime", type=("build", "link", "run"))
    depends_on(
        "cbtf@1.9.3:9999+runtime", when="@1.9.3:9999+runtime", type=("build", "link", "run")
    )

    # For libmonitor
    depends_on("libmonitor@2013.02.18+commrank", type=("build", "link", "run"))

    # For PAPI
    depends_on("papi@5.4.1:", type=("build", "link", "run"))

    # For CBTF-KRELL
    depends_on("cbtf-krell@develop", when="@develop", type=("build", "link", "run"))
    depends_on("cbtf-krell@1.9.3:9999", when="@1.9.3:9999", type=("build", "link", "run"))

    depends_on(
        "cbtf-krell@develop+runtime", when="@develop+runtime", type=("build", "link", "run")
    )
    depends_on(
        "cbtf-krell@1.9.3:9999+runtime", when="@1.9.3:9999+runtime", type=("build", "link", "run")
    )

    # For CUDA
    depends_on("cuda")

    parallel = False

    build_directory = "build_cbtf_argonavis"

    def cmake_args(self):
        spec = self.spec
        compile_flags = "-O2 -g -Wall"

        cmake_args = [
            "-DCMAKE_CXX_FLAGS=%s" % compile_flags,
            "-DCMAKE_C_FLAGS=%s" % compile_flags,
            "-DCUDA_DIR=%s" % spec["cuda"].prefix,
            "-DCUDA_INSTALL_PATH=%s" % spec["cuda"].prefix,
            "-DCUDA_TOOLKIT_ROOT_DIR=%s" % spec["cuda"].prefix,
            "-DCUPTI_DIR=%s" % spec["cuda"].prefix.extras.CUPTI,
            "-DCUPTI_ROOT=%s" % spec["cuda"].prefix.extras.CUPTI,
            "-DPAPI_ROOT=%s" % spec["papi"].prefix,
            "-DCBTF_DIR=%s" % spec["cbtf"].prefix,
            "-DCBTF_KRELL_DIR=%s" % spec["cbtf-krell"].prefix,
            "-DBoost_NO_SYSTEM_PATHS=TRUE",
            "-DBoost_NO_BOOST_CMAKE=TRUE",
            "-DBOOST_ROOT=%s" % spec["boost"].prefix,
            "-DBoost_DIR=%s" % spec["boost"].prefix,
            "-DBOOST_LIBRARYDIR=%s" % spec["boost"].prefix.lib,
            "-DMRNET_DIR=%s" % spec["mrnet"].prefix,
            "-DLIBMONITOR_DIR=%s" % spec["libmonitor"].prefix,
        ]

        return cmake_args

    def setup_run_environment(self, env):
        """Set up the compile and runtime environments for a package."""

        env.prepend_path("LD_LIBRARY_PATH", self.spec["cuda"].prefix + "/extras/CUPTI/lib64")

    def setup_build_environment(self, env):
        """Set up the compile and runtime environments for a package."""

        env.prepend_path("LD_LIBRARY_PATH", self.spec["cuda"].prefix + "/extras/CUPTI/lib64")
