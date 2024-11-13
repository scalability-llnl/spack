# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Numactl(AutotoolsPackage):
    """NUMA support for Linux"""

    homepage = "https://github.com/numactl/numactl"
    url = "https://github.com/numactl/numactl/archive/v2.0.11.tar.gz"

    force_autoreconf = True

    license("LGPL-2.1-only")

    version("2.0.18", sha256="8cd6c13f3096e9c2293c1d732f56e2aa37a7ada1a98deed3fac7bd6da1aaaaf6")
    version("2.0.17", sha256="af22829cda8b5bdee3d280e61291697bbd3f9bd372afdf119c9348b88369d40b")
    version("2.0.16", sha256="a35c3bdb3efab5c65927e0de5703227760b1101f5e27ab741d8f32b3d5f0a44c")
    version("2.0.14", sha256="1ee27abd07ff6ba140aaf9bc6379b37825e54496e01d6f7343330cf1a4487035")
    version("2.0.12", sha256="7c3e819c2bdeb883de68bafe88776a01356f7ef565e75ba866c4b49a087c6bdf")
    version("2.0.11", sha256="3e099a59b2c527bcdbddd34e1952ca87462d2cef4c93da9b0bc03f02903f7089")

    depends_on("c", type="build")  # generated

    patch("numactl-2.0.11-sysmacros.patch", when="@2.0.11")
    # https://github.com/numactl/numactl/issues/94
    patch("numactl-2.0.14-symver.patch", when="@2.0.14")
    patch("fix-empty-block.patch", when="@2.0.10:2.0.16")
    patch("link-with-latomic-if-needed.patch", when="@2.0.14")
    patch("link-with-latomic-if-needed-v2.0.16.patch", when="@2.0.16")
    patch("numactl-2.0.18-syscall-NR-ppc64.patch", when="@2.0.18 target=ppc64le:")

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")

    # Numactl has hardcoded minimum versions for libtool,
    # libtool@develop returns UNKOWN as a version tag and fails
    conflicts("^libtool@develop")

    # Numerous errors when trying to build on darwin
    conflicts("platform=darwin")

    def autoreconf(self, spec, prefix):
        Executable("./autogen.sh")()

    @when("%nvhpc")
    def patch(self):
        self._nvhpc_patch()

    @when("%pgi@20:")
    def patch(self):
        self._nvhpc_patch()

    def _nvhpc_patch(self):
        # Remove flags not recognized by the NVIDIA compiler
        filter_file("-ffast-math -funroll-loops", "", "Makefile.am")
        filter_file("-std=gnu99", "-c99", "Makefile.am")

        # Avoid undefined reference errors
        if self.spec.satisfies("@2.0.14"):
            filter_file("numa_sched_setaffinity_v1_int", "numa_sched_setaffinity_v1", "libnuma.c")
            filter_file("numa_sched_setaffinity_v2_int", "numa_sched_setaffinity_v2", "libnuma.c")
            filter_file("numa_sched_getaffinity_v2_int", "numa_sched_getaffinity_v2", "libnuma.c")
