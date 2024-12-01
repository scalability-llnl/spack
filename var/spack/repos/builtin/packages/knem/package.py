# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Knem(AutotoolsPackage):
    """KNEM is a Linux kernel module enabling high-performance intra-node MPI
    communication for large messages."""

    homepage = "https://knem.gforge.inria.fr"
    url = "https://gitlab.inria.fr/knem/knem/uploads/4a43e3eb860cda2bbd5bf5c7c04a24b6/knem-1.1.4.tar.gz"
    list_url = "https://knem.gitlabpages.inria.fr/download"
    git = "https://gitlab.inria.fr/knem/knem.git"

    maintainers("skosukhin")

    version("master", branch="master")
    version(
        "1.1.4",
        sha256="9f0e360579ae7655e07d6644583fd325515e9ff2b42ef5decb5421a003510937",
        url="https://gitlab.inria.fr/knem/knem/uploads/4a43e3eb860cda2bbd5bf5c7c04a24b6/knem-1.1.4.tar.gz",
    )
    version(
        "1.1.3",
        sha256="50d3c4a20c140108b8ce47aaafd0ade0927d6f507e1b5cc690dd6bddeef30f60",
        url="https://gitlab.inria.fr/knem/knem/uploads/59375c38537e6ff2d94209f190c54aa6/knem-1.1.3.tar.gz",
    )

    depends_on("c", type="build")  # generated

    variant("hwloc", default=True, description="Enable hwloc in the user-space tools")

    patch(
        "https://gitlab.inria.fr/knem/knem/-/commit/5c8cb902d6040df58cdc4e4e4c10d1f1426c3525.diff",
        sha256="a422277f02247bde680d4a3c8ccb8c05498a79109ba1ade4a037bedd6efe3c79",
        when="@1.1.4",
    )

    depends_on("hwloc", when="+hwloc")
    depends_on("pkgconfig", type="build", when="+hwloc")
    depends_on("autoconf", type="build", when="@master")
    depends_on("automake", type="build", when="@master")
    depends_on("m4", type="build", when="@master")

    # The support for hwloc was added in 0.9.1:
    conflicts("+hwloc", when="@:0.9.0")

    # Ideally, we should list all non-Linux-based platforms here:
    conflicts("platform=darwin")

    requires("%gcc", msg="Linux kernel module must be compiled with gcc")

    @run_before("build")
    def override_kernel_compiler(self):
        # Override the compiler for kernel module source files. We need
        # this additional argument for all installation phases.
        make.add_default_arg("CC={0}".format(spack_cc))

    def configure_args(self):
        return self.enable_or_disable("hwloc")

    @when("@master")
    def autoreconf(self, spec, prefix):
        Executable("./autogen.sh")()
