# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import re

from spack.package import *

# - vanilla CentOS 7, and possibly other systems, fail a test:
#   TestCloneNEWUSERAndRemapRootDisableSetgroups
#
#   The Fix, discussed here: https://github.com/golang/go/issues/16283
#   is to enable "user_namespace".
#
#   On a Digital Ocean image, this can be achieved by updating
#   `/etc/default/grub` so that the `GRUB_CMDLINE_LINUX` variable
#   includes `user_namespace.enable=1`, re-cooking the grub
#   configuration with `sudo grub2-mkconfig -o /boot/grub2/grub.cfg`,
#   and then rebooting.
#
# - on CentOS 7 systems (and possibly others) you need to have the
#   glibc package installed or various static cgo tests fail.
#


class Go(Package):
    """The golang compiler and build environment"""

    homepage = "https://go.dev"
    url = "https://go.dev/dl/go1.20.2.src.tar.gz"
    git = "https://go.googlesource.com/go.git"

    extendable = True
    executables = ["^go$"]

    maintainers("alecbcs")

    license("BSD-3-Clause")

    version("1.24.0", sha256="d14120614acb29d12bcab72bd689f257eb4be9e0b6f88a8fb7e41ac65f8556e5")
    version("1.23.6", sha256="039c5b04e65279daceee8a6f71e70bd05cf5b801782b6f77c6e19e2ed0511222")
    version("1.23.5", sha256="a6f3f4bbd3e6bdd626f79b668f212fbb5649daf75084fb79b678a0ae4d97423b")
    version("1.23.4", sha256="ad345ac421e90814293a9699cca19dd5238251c3f687980bbcae28495b263531")
    version("1.23.3", sha256="8d6a77332487557c6afa2421131b50f83db4ae3c579c3bc72e670ee1f6968599")
    version("1.23.2", sha256="36930162a93df417d90bd22c6e14daff4705baac2b02418edda671cdfa9cd07f")
    version("1.23.1", sha256="6ee44e298379d146a5e5aa6b1c5b5d5f5d0a3365eabdd70741e6e21340ec3b0d")
    version("1.22.8", sha256="df12c23ebf19dea0f4bf46a22cbeda4a3eca6f474f318390ce774974278440b8")
    version("1.22.7", sha256="66432d87d85e0cfac3edffe637d5930fc4ddf5793313fe11e4a0f333023c879f")
    version("1.22.6", sha256="9e48d99d519882579917d8189c17e98c373ce25abaebb98772e2927088992a51")
    version("1.22.4", sha256="fed720678e728a7ca30ba8d1ded1caafe27d16028fab0232b8ba8e22008fb784")

    # Deprecated versions due to CVEs
    with default_args(deprecated=True):
        # https://nvd.nist.gov/vuln/detail/CVE-2024-24790
        # https://nvd.nist.gov/vuln/detail/CVE-2024-24789
        version(
            "1.22.2", sha256="374ea82b289ec738e968267cac59c7d5ff180f9492250254784b2044e90df5a9"
        )
        version(
            "1.22.1", sha256="79c9b91d7f109515a25fc3ecdaad125d67e6bdb54f6d4d98580f46799caea321"
        )
        version(
            "1.22.0", sha256="4d196c3d41a0d6c1dfc64d04e3cc1f608b0c436bd87b7060ce3e23234e1f4d5c"
        )
        version(
            "1.21.6", sha256="124926a62e45f78daabbaedb9c011d97633186a33c238ffc1e25320c02046248"
        )
        version(
            "1.21.5", sha256="285cbbdf4b6e6e62ed58f370f3f6d8c30825d6e56c5853c66d3c23bcdb09db19"
        )

    provides("golang")

    depends_on("bash", type="build")
    depends_on("grep", type="build")
    depends_on("sed", type="build")

    depends_on("go-or-gccgo-bootstrap@1.22.6:", type="build", when="@1.24:")
    depends_on("go-or-gccgo-bootstrap@1.20.6:", type="build", when="@1.22:")
    depends_on("go-or-gccgo-bootstrap@1.17.13:", type="build", when="@1.20:")
    depends_on("go-or-gccgo-bootstrap", type="build")

    phases = ["build", "install"]

    def url_for_version(self, version):
        return f"https://go.dev/dl/go{version}.src.tar.gz"

    @classmethod
    def determine_version(cls, exe):
        output = Executable(exe)("version", output=str, error=str)
        match = re.search(r"go version go(\S+)", output)
        return match.group(1) if match else None

    def setup_build_environment(self, env):
        # We need to set CC/CXX_FOR_TARGET, otherwise cgo will use the
        # internal Spack wrappers and fail.
        env.set("CC_FOR_TARGET", self.compiler.cc)
        env.set("CXX_FOR_TARGET", self.compiler.cxx)
        env.set("GOMAXPROCS", make_jobs)

    def build(self, spec, prefix):
        # Build script depend on bash
        bash = which("bash")

        with working_dir("src"):
            bash(f"{'all' if self.run_tests else 'make'}.bash")

    def install(self, spec, prefix):
        install_tree(".", prefix.go)
        os.symlink(prefix.go.bin, prefix.bin)

    def setup_dependent_package(self, module, dependent_spec):
        """Called before go modules' build(), install() methods.

        go('get', '<package>', env=env)
        install_tree('bin', prefix.bin)
        """
        #  Add a go command/compiler for extensions
        module.go = self.spec["go"].command
