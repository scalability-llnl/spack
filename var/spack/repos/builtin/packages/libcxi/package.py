# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libcxi(AutotoolsPackage):
    """The CXI library provides interfaces which interact directly with CXI
    drivers."""

    homepage = "https://github.com/HewlettPackard/shs-libcxi"
    git = "https://github.com/HewlettPackard/shs-libcxi.git"

    license("LGPL-2.1-or-later or BSD-3-Clause")

    # no releases, tags: see https://github.com/HewlettPackard/shs-libcxi/issues/2
    version("main", branch="main")

    variant("level_zero", default=False, description="Enable level zero support")
    variant("cuda", default=False, description="Build with CUDA support")
    variant("rocm", default=False, description="Build with ROCm support")

    depends_on("c", type="build")

    depends_on("cassini-headers")
    depends_on("cxi-driver")

    depends_on("libconfig@1.5:")
    depends_on("libuv@1.18:")
    # configure fails with newer libfuse
    # see https://github.com/HewlettPackard/shs-libcxi/issues/3
    depends_on("libfuse@2.9.7:2")
    depends_on("libyaml@0.1.7:")
    depends_on("libnl@3:")
    depends_on("numactl@2:")
    depends_on("lm-sensors")

    depends_on("oneapi-level-zero", when="+level_zero")
    depends_on("cuda", when="+cuda")
    depends_on("hip", when="+rocm")

    # required due to https://github.com/HewlettPackard/shs-libcxi/issues/4
    def patch(self):
        filter_file(
            r"/usr/share/cassini-headers/csr_defs.json",
            f"{self.spec['cassini-headers'].prefix}/share/cassini-headers/csr_defs.json",
            "utils/cxi_dump_csrs.py",
            string=True,
        )

    @when("@main")
    def autoreconf(self, spec, prefix):
        sh = which("sh")
        sh("autogen.sh")

    def setup_build_environment(self, env):
        env.append_flags("CFLAGS", f"-I{self.spec['cassini-headers'].prefix.include}")

    def configure_args(self):
        args = [
            f"--with-udevrulesdir={self.prefix}/lib/udev/rules.d",
            f"--with-systemdsystemunitdir={self.prefix}/lib/systemd/system",
        ]

        if self.spec.satisfies("+level_zero"):
            args.append(f"--with-ze={self.spec['oneapi-level-zero'].prefix}")
        if self.spec.satisfies("+cuda"):
            args.append(f"--with-cuda={self.spec['cuda'].prefix}")
        if self.spec.satisfies("+rocm"):
            args.append(f"--with-rocm={self.spec['hip'].prefix}")

        return args
