# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import glob
import os
import sys

import llnl.util.filesystem as fs

from spack.package import *


class Papi(AutotoolsPackage, ROCmPackage):
    """PAPI provides the tool designer and application engineer with a
    consistent interface and methodology for use of the performance
    counter hardware found in most major microprocessors. PAPI
    enables software engineers to see, in near real time, the
    relation between software performance and processor events.  In
    addition Component PAPI provides access to a collection of
    components that expose performance measurement opportunities
    across the hardware and software stack."""

    homepage = "https://icl.utk.edu/papi/"
    maintainers("G-Ragghianti")

    tags = ["e4s"]

    url = "https://icl.utk.edu/projects/papi/downloads/papi-5.4.1.tar.gz"
    git = "https://github.com/icl-utk-edu/papi"

    license("BSD-3-Clause")

    version("master", branch="master")
    version("7.1.0", sha256="5818afb6dba3ece57f51e65897db5062f8e3464e6ed294b654ebf34c3991bc4f")
    version("7.0.1", sha256="c105da5d8fea7b113b0741a943d467a06c98db959ce71bdd9a50b9f03eecc43e")
    # Note: version 7.0.0 is omitted due to build issues, see PR 33940 for more information
    version("6.0.0.1", sha256="3cd7ed50c65b0d21d66e46d0ba34cd171178af4bbf9d94e693915c1aca1e287f")
    version("6.0.0", sha256="3442709dae3405c2845b304c06a8b15395ecf4f3899a89ceb4d715103cb4055f")
    version("5.7.0", sha256="d1a3bb848e292c805bc9f29e09c27870e2ff4cda6c2fba3b7da8b4bba6547589")
    version("5.6.0", sha256="49b7293f9ca2d74d6d80bd06b5c4be303663123267b4ac0884cbcae4c914dc47")
    version("5.5.1", sha256="49dc2c2323f6164c4a7e81b799ed690ee73158671205e71501f849391dd2c2d4")
    version("5.5.0", sha256="3ea15e6cc2354017335b659c1635409ddab1414e70573aa4df91fd892e99f98d")
    version("5.4.3", sha256="3aefd581e274f0a103f001f1ffd1009019b297c637e97f4b8c5fc13fa5a1e675")
    version("5.4.1", sha256="e131c1449786fe870322a949e44f974a5963824f683232e653fb570cc65d4e87")
    version("5.3.0", sha256="99f2f36398b370e75d100b4a189d5bc0ac4f5dd66df44d441f88fd32e1421524")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant("example", default=True, description="Install the example files")
    variant("infiniband", default=False, description="Enable Infiniband support")
    variant("powercap", default=False, description="Enable powercap interface support")
    variant("rapl", default=False, description="Enable RAPL support")
    variant("lmsensors", default=False, description="Enable lm_sensors support")
    variant("sde", default=False, description="Enable software defined events")
    variant("cuda", default=False, description="Enable CUDA support")
    variant("nvml", default=False, description="Enable NVML support")
    variant("rocm_smi", default=False, description="Enable ROCm SMI support")
    variant(
        "rdpmc",
        default=True,
        when="@6.0.0:",
        description="Enable use of rdpmc for reading counters, when possible",
    )

    variant("shared", default=True, description="Build shared libraries")
    # PAPI requires building static libraries, so there is no "static" variant
    variant("static_tools", default=False, description="Statically link the PAPI tools")
    variant("debug", default=False, description="Enable debug symbols in PAPI")
    # The PAPI configure option "--with-shlib-tools" is deprecated
    # and therefore not implemented here

    depends_on("lm-sensors", when="+lmsensors")
    depends_on("cuda", when="+cuda")
    depends_on("cuda", when="+nvml")
    depends_on("hsa-rocr-dev", when="+rocm")
    depends_on("rocprofiler-dev", when="+rocm")
    depends_on("llvm-amdgpu", when="+rocm")
    depends_on("rocm-openmp-extras", when="+rocm")
    depends_on("rocm-smi-lib", when="+rocm_smi")

    conflicts("%gcc@8:", when="@5.3.0", msg="Requires GCC version less than 8.0")
    conflicts("+sde", when="@:5", msg="Software defined events (SDE) added in 6.0.0")
    conflicts("^cuda", when="@:5", msg="CUDA support for versions < 6.0.0 not implemented")
    conflicts("%cce", when="@7.1:", msg="-ffree-form flag not recognized")

    conflicts("@=6.0.0", when="+static_tools", msg="Static tools cannot build on version 6.0.0")

    # Does not build with newer versions of gcc, see
    # https://bitbucket.org/icl/papi/issues/46/cannot-compile-on-arch-linux
    patch(
        "https://bitbucket.org/icl/papi/commits/53de184a162b8a7edff48fed01a15980664e15b1/raw",
        sha256="64c57b3ad4026255238cc495df6abfacc41de391a0af497c27d0ac819444a1f8",
        when="@5.4.0:5.6%gcc@8:",
    )
    # 7.1.0 erroneously adds -ffree-form for all fortran compilers
    patch("sysdetect-free-form-fix.patch", when="@7.1.0")
    patch("crayftn-fixes.patch", when="@6.0.0:%cce@9:")
    patch("intel-oneapi-compiler-fixes.patch", when="@6.0.0:%oneapi")
    patch("intel-cray-freeform.patch", when="@7.0.1")
    patch("spack-hip-path.patch", when="@7.0.1")

    configure_directory = "src"

    def setup_build_environment(self, env):
        spec = self.spec
        if "+lmsensors" in spec and self.version >= Version("6"):
            env.set("PAPI_LMSENSORS_ROOT", spec["lm-sensors"].prefix)
        if "+cuda" in spec:
            env.set("PAPI_CUDA_ROOT", spec["cuda"].prefix)
        if "+rocm" in spec:
            env.set("PAPI_ROCM_ROOT", spec["hsa-rocr-dev"].prefix)
            env.set("HSA_TOOLS_LIB", "%s/librocprofiler64.so" % spec["rocprofiler-dev"].prefix.lib)
            env.append_flags("CFLAGS", "-I%s/rocprofiler/include" % spec["rocprofiler-dev"].prefix)
            env.append_flags("LDFLAGS", "-L%s/lib" % spec["llvm-amdgpu"].prefix)
            env.set(
                "ROCP_METRICS", "%s/rocprofiler/lib/metrics.xml" % spec["rocprofiler-dev"].prefix
            )
            env.set("ROCPROFILER_LOG", "1")
            env.set("HSA_VEN_AMD_AQLPROFILE_LOG", "1")
            env.set("AQLPROFILE_READ_API", "1")
        if "+rocm_smi" in spec:
            env.append_flags("CFLAGS", "-I%s/rocm_smi" % spec["rocm-smi-lib"].prefix.include)
        #
        # Intel OneAPI LLVM cannot compile papi unless the DBG enviroment variable is cleared
        #
        if spec.satisfies("%oneapi"):
            env.set("DBG", "")

    setup_run_environment = setup_build_environment

    @when("@6.0.0:%oneapi")
    def autoreconf(self, spec, prefix):
        bash = which("bash")
        bash("-c", "cd src && autoreconf -ivf")

    def configure_args(self):
        spec = self.spec
        # PAPI uses MPI if MPI is present; since we don't require
        # an MPI package, we ensure that all attempts to use MPI
        # fail, so that PAPI does not get confused
        options = ["MPICC=:"]
        # Build a list of PAPI components
        components = filter(
            lambda x: spec.variants[x].value,
            [
                "example",
                "infiniband",
                "powercap",
                "rapl",
                "lmsensors",
                "sde",
                "cuda",
                "nvml",
                "rocm",
                "rocm_smi",
            ],
        )
        if components:
            options.append("--with-components=" + " ".join(components))

        build_shared = "yes" if "+shared" in spec else "no"
        options.append("--with-shared-lib=" + build_shared)

        build_rdpmc_support = "yes" if "+rdpmc" in spec else "no"
        options.append("--enable-perfevent-rdpmc=" + build_rdpmc_support)

        if "+static_tools" in spec:
            options.append("--with-static-tools")

        if "+debug" in spec:
            options.append("--with-debug=yes")

        return options

    @run_before("configure")
    def fortran_check(self):
        if not self.compiler.fc:
            msg = "PAPI requires a Fortran compiler to build"
            raise RuntimeError(msg)

    @run_before("configure")
    def component_configure(self):
        configure_script = Executable("./configure")
        if "+lmsensors" in self.spec and self.version < Version("6"):
            with working_dir("src/components/lmsensors"):
                configure_script(
                    "--with-sensors_incdir=%s/sensors"
                    % self.spec["lm-sensors"].headers.directories[0],
                    "--with-sensors_libdir=%s" % self.spec["lm-sensors"].libs.directories[0],
                )

    @run_before("build")
    def fix_build(self):
        # Don't use <malloc.h>
        for level in [".", "*", "*/*"]:
            files = glob.iglob(join_path(level, "*.[ch]"))
            filter_file(r"\<malloc\.h\>", "<stdlib.h>", *files)

    @run_after("install")
    def fix_darwin_install(self):
        # The shared library is not installed correctly on Darwin
        if sys.platform == "darwin":
            os.rename(
                join_path(self.prefix.lib, "libpapi.so"),
                join_path(self.prefix.lib, "libpapi.dylib"),
            )
            fs.fix_darwin_install_name(self.prefix.lib)

    test_src_dir = "src/smoke_tests"
    test_requires_compiler = True

    @run_after("install")
    def cache_test_sources(self):
        """Copy the example source files after the package is installed to an
        install test subdirectory for use during `spack test run`."""
        if os.path.exists(self.test_src_dir):
            cache_extra_test_sources(self, [self.test_src_dir])

    def test_smoke(self):
        """Compile and run simple code against the installed papi library."""
        test_dir = join_path(self.test_suite.current_test_cache_dir, self.test_src_dir)
        if not os.path.exists(test_dir):
            raise SkipTest("Skipping smoke tests, directory doesn't exist")
        with working_dir(test_dir, create=False):
            with spack.util.environment.set_env(PAPIROOT=self.prefix):
                make()
                exe_simple = which("simple")
                exe_simple()
                exe_threads = which("threads")
                exe_threads()
