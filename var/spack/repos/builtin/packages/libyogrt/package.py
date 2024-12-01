# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Libyogrt(AutotoolsPackage):
    """Your One Get Remaining Time Library."""

    homepage = "https://github.com/LLNL/libyogrt"
    url = "https://github.com/LLNL/libyogrt/releases/download/1.21/libyogrt-1.21.tar.gz"

    license("LGPL-2.1-or-later")

    version("1.35", sha256="a03b3d24da49af626351aaca9ab3eaff102ed41d5171f1bcb2ff26a561bd0cd6")
    version("1.33", sha256="797d20c49cdc4f6beae8660b4f41ba7ac13f7e93a0344b47f0bdc64f780d1398")
    version("1.27", sha256="c57ce60770b61aa20bc83fe34ff52b5e444964338df3786f282d0d9bcdd26138")
    version("1.24", sha256="36695030e72b24b1f22bfcfe42bfd1d3c87f9c0eea5e94ce0120782581ea522f")
    version("1.23", sha256="c95e7a6be29c0d1ac1b673b0ba1d4e5781981722f93d0da99ae62ff3b5f35b5f")
    version("1.22", sha256="38e7d1ea3fa030f0169197aa96cde9f01caa595a590764ef1cb2ae07379cb711")
    version("1.21", sha256="5f8f0942d35ee4e418273e478e632210b3fa648dcb6a2e6a92c6ba4213cdc362")
    version("1.20-7", sha256="735e9d6fa572e239ccc73e11c84b4583338b24df0fa91c48e8bc038d882003f7")
    version("1.20-6", sha256="ba5a2e202f995cf7ae3bf87b451943733e760ede02ca172f712cbf2eea693222")
    version("1.20-5", sha256="1e41bc656abffb121145264bc898421c3f355d3be35f1711b7b5e3ffe7effdd9")
    version("1.20-4", sha256="0858a729068b272d4047d79f6a5187cdbd427bdfec64db4e143524b4789a06c5")
    version("1.20-3", sha256="61a8f28f452aef0e09d700dbaaffd91ae3855f7ac221c7ebe478a028df635e31")
    version("1.20-2", sha256="bf22a82ab3bfede780be3fb6c132cc354234f8d57d3cccd58fe594f074ed7f95")

    depends_on("c", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    # libyogrt supports the following schedulers:
    #     flux, lcrm, lsf, moab, slurm, AIX+slurm

    # however, only slurm exists in spack
    # libyogrt's build system is smart enough to detect the system scheduler
    # the slurm option here connects to a spack-installed slurm
    # if/when other schedulers have spack packages, they can be added

    variant(
        "scheduler",
        default="system",
        description="Select scheduler integration",
        values=["system", "flux", "lsf", "slurm"],
        multi=False,
    )
    depends_on("flux-core@0.21.0:", when="scheduler=flux")
    depends_on("lsf", when="scheduler=lsf")
    depends_on("slurm", when="scheduler=slurm")

    # support for flux added in libyogrt 1.27
    conflicts("scheduler=flux", when="@:1.26")

    conflicts("scheduler=lsf", when="@:1.22")

    variant("static", default=False, description="build static library")

    def url_for_version(self, version):
        if version < Version("1.21"):
            return f"https://github.com/LLNL/libyogrt/archive/{version}.tar.gz"
        else:
            return "https://github.com/LLNL/libyogrt/releases/download/{0}/libyogrt-{0}.tar.gz".format(
                version
            )

    def flag_handler(self, name, flags):
        if name == "cflags":
            if self.spec.satisfies("%oneapi"):
                flags.append("-Wno-error=implicit-function-declaration")
        return (flags, None, None)

    def configure_args(self):
        args = []

        sched = self.spec.variants["scheduler"].value
        if sched == "lsf":
            # The LSF library depends on a couple of other libraries,
            # and running the build inside of spack does not find
            # them, and the user has to add them when they want
            # to use -lyogrt. If we explicitly tell it what libraries
            # to use, the user does not need to specify them
            args.append("--with-lsf")
            args.append("LIBS=-llsf -lrt -lnsl")
        elif sched == "flux":
            args.append(f"--with-flux={self.spec['flux-core'].prefix}")
        elif sched != "system":
            args.append(f"--with-{sched}={self.spec[sched].prefix}")

        if self.spec.satisfies("+static"):
            args.append("--enable-static=yes")

        return args

    @run_after("install")
    def create_yogrt_conf(self):
        etcpath = os.path.join(prefix, "etc")

        # create subdirectory to hold yogrt.conf file
        if not os.path.isdir(etcpath):
            mode = 0o755
            os.mkdir(etcpath, mode)

        # if no scheduler is specified, create yogrt conf file
        # with backend=none
        sched = self.spec.variants["scheduler"].value
        if sched == "system":
            sched = "none"

        # create conf file to inform libyogrt about job scheduler
        with open(os.path.join(etcpath, "yogrt.conf"), "w+") as f:
            f.write(f"backend={sched}\n")
