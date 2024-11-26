# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import sys

from spack.package import *


class Mpibind(AutotoolsPackage):
    """A memory-driven algorithm to map parallel codes
    to heterogeneous architectures"""

    homepage = "https://github.com/LLNL/mpibind"
    git = "https://github.com/LLNL/mpibind.git"

    maintainers("eleon")

    license("MIT")

    # This package uses 'git describe --tags' to get the
    # package version in Autotools' AC_INIT, thus
    # 'get_full_repo' is needed.
    # Furthermore, the package can't be cached because
    # AC_INIT would be missing the version argument,
    # which is derived with git.
    version("master", branch="master", get_full_repo=True)
    version("0.8.0", commit="ff38b9dcd150ca1e8a8796835d8e1e1847b3ba68", no_cache=True)
    version("0.7.0", commit="3c437a97cd841b9c13abfbe1062a0285e1a29d3e", no_cache=True)
    version("0.5.0", commit="8698f07412232e4dd4de4802b508374dc0de48c9", no_cache=True)

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant("cuda", default=False, description="Build w/support for NVIDIA GPUs.")
    variant("rocm", default=False, description="Build w/support for AMD GPUs.")
    variant("flux", default=False, description="Build the Flux plugin.")
    variant("python", default=False, description="Build the Python bindings.")

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")
    depends_on("pkgconfig", type="build")

    depends_on("hwloc@2:+libxml2", type="link")
    depends_on("hwloc@2:+cuda+nvml", type="link", when="+cuda")
    depends_on("hwloc@2.4:+rocm+opencl", type="link", when="+rocm")
    depends_on("hwloc@2:+pci", type="link", when=(sys.platform != "darwin"))

    # flux-core >= 0.30.0 supports FLUX_SHELL_RC_PATH,
    # which is needed to load the plugin into Flux
    depends_on("flux-core@0.30:", when="+flux", type="link")

    depends_on("python@3:", when="+python", type=("build", "run"))
    depends_on("py-cffi", when="+python", type=("build", "run"))

    def autoreconf(self, spec, prefix):
        autoreconf("--install", "--verbose", "--force")

    @when("+flux")
    def setup_run_environment(self, env):
        """Load the mpibind plugin into Flux"""
        env.prepend_path("FLUX_SHELL_RC_PATH", join_path(self.prefix, "share", "mpibind"))

    # To build and run the C unit tests, make sure 'libtap'
    # is installed and recognized by pkgconfig.
    # To build and run the Python unit tests, make sure 'pycotap'
    # is installed in your Python environment.
    # Unfortunately, 'tap' and 'pycotap' are not in Spack.
