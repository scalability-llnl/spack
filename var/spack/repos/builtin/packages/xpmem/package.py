# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Xpmem(AutotoolsPackage):
    """XPMEM is a Linux kernel module that enables a process to map the memory
    of another process into its virtual address space."""

    # The README file of the repository says that the development was
    # transferred to a new repository on GitLab: https://gitlab.com/hjelmn/xpmem
    # However, it looks like that the repository on GitHub has a more recent
    # version of the codebase.
    homepage = "https://github.com/hjelmn/xpmem"
    url = "https://github.com/hjelmn/xpmem/archive/v2.6.3.tar.gz"
    git = "https://github.com/hjelmn/xpmem.git"

    maintainers("skosukhin")

    license("LGPL-2.1-or-later")

    version("master", branch="master")

    # Versions starting 2.6.4 are neither tagged nor released in the repo
    # (the choice of commits is based on the commit history of
    # 'kernel/xpmem_private.h'):
    version("2.6.5-36", commit="0d0bad4e1d07b38d53ecc8f20786bb1328c446da")
    version("2.6.5", commit="4efeed9cbaabe971f3766d67cb108e2c3316d4b8")
    version("2.6.4", commit="522054850e4d1479d69f50f7190d1548bf9749fd")

    # Released versions:
    version("2.6.3", sha256="ee239a32269f33234cdbdb94db29c12287862934c0784328d34aff82a9fa8b54")
    version("2.6.2", sha256="2c1a93b4cb20ed73c2093435a7afec513e0e797aa1e49d4d964cc6bdae89d65b")

    depends_on("c", type="build")  # generated

    variant("kernel-module", default=True, description="Enable building the kernel module")

    # Added RHEL 8.3 kernel support
    # Here 2.6.5-36 referes to 2.6.5 version and 36th commit id
    patch("xpmem_v2.6.5-36.patch", when="@2.6.5-36", level=1)
    patch(
        "https://github.com/hjelmn/xpmem/commit/cbd6e5bd3d2a1d3823c335ddcd3c57b94474f578.patch?full_index=1",
        sha256="75299398b6c15546479bfbb8aa972431f58637fe2f0328196a26738bd7148140",
        when="@2.6.5-36",
        level=1,
    )
    patch(
        "https://github.com/hjelmn/xpmem/commit/7d346aaf1fdfc24d38cebb4ad107b7f5c43769e9.patch?full_index=1",
        sha256="6be8c5f33d55c611924d8412253740f6f4b738e6d98e32981fa300d2ccbe99cc",
        when="@2.6.5-36",
        level=1,
    )

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")

    # It will become possible to disable the kernel module only starting 2.6.6:
    # https://github.com/hjelmn/xpmem/pull/24
    conflicts("~kernel-module", when="@:2.6.5")

    # Ideally, we should list all non-Linux-based platforms here:
    conflicts("+kernel-module", when="platform=darwin")

    # All compilers except for gcc are in conflict with +kernel-module:
    requires("%gcc", when="+kernel-module", msg="Linux kernel module must be compiled with gcc")

    def autoreconf(self, spec, prefix):
        Executable("./autogen.sh")()

    @run_before("build")
    def override_kernel_compiler(self):
        # Override the compiler for kernel module source files. We need
        # this additional argument for all installation phases.
        if "+kernel-module" in self.spec:
            make.add_default_arg("CC={0}".format(spack_cc))

    def configure_args(self):
        args = []

        if "~kernel-module" in self.spec:
            # The kernel module is enabled by default. An attempt of explicit
            # enabling with '--enable-kernel-module' disables the module.
            args.append("--disable-kernel-module")

        if self.spec.satisfies("@:2.6.5"):
            fmt = self.spec.format
            # The following arguments will not be needed starting 2.6.6:
            # https://github.com/hjelmn/xpmem/pull/18
            args.extend(
                [
                    fmt("--with-default-prefix={prefix}"),
                    fmt("--with-module={prefix.share}/Modules/{name}/{version}"),
                ]
            )

        return args

    @when("@:2.6.5")
    def install(self, spec, prefix):
        with working_dir(self.build_directory):
            # Override the hardcoded prefix for 'cray-xpmem.conf'
            make(
                "ldsoconfdir={0}".format(self.spec.prefix.etc.join("ld.so.conf.d")),
                *self.install_targets,
            )
