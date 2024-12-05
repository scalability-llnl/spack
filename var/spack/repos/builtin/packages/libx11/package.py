# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libx11(AutotoolsPackage, XorgPackage):
    """libX11 - Core X11 protocol client library."""

    homepage = "https://www.x.org/"
    xorg_mirror_path = "lib/libX11-1.6.7.tar.gz"
    git = "https://gitlab.freedesktop.org/xorg/lib/libx11.git"

    license("X11")

    maintainers("wdconinc")

    version("1.8.10", sha256="b7a1a90d881bb7b94df5cf31509e6b03f15c0972d3ac25ab0441f5fbc789650f")
    version("1.8.9", sha256="57ca5f07d263788ad661a86f4139412e8b699662e6b60c20f1f028c25a935e48")
    version("1.8.8", sha256="26997a2bc48c03df7d670f8a4ee961d1d6b039bf947475e5fec6b7635b4efe72")
    version("1.8.7", sha256="793ebebf569f12c864b77401798d38814b51790fce206e01a431e5feb982e20b")
    version("1.8.6", sha256="5ff0d26c94d82ebb94a944b9f1f55cd01b9713fd461fe93f62f3527ce14ad94e")
    version("1.8.5", sha256="d84a35c324d5a1724692eafc1ed76f1689c833021e0062933773ec437f91a56b")
    version("1.8.4", sha256="efd3a3a43c1f177edc2c205bedb0719b6648203595e54c0b83a32576aeaca7cd")
    version("1.8.3", sha256="5a55945b7da86ce94733faf229342f75867e9c1090685f47f4d82b7f88602a14")
    version("1.8.2", sha256="f1bc56187bee0f830e1179ac5068ac93b78c51ace94eb27702ffb2efd116587b")
    version("1.8.1", sha256="d52f0a7c02a45449f37b0831d99ff936d92eb4ce8b4c97dc17a63cea79ce5a76")
    version("1.8", sha256="68e0a30c4248b9f41492891a4b49672c3b0c59e84c4868144f03eef01ebc5eea")
    version("1.7.5", sha256="78992abcd2bfdebe657699203ad8914e7ae77025175460e04a1045387192a978")
    version("1.7.4", sha256="252fb028524caa878e6507729efc115d7434f867f6549fe087e7869a66adfa2c")
    version("1.7.3.1", sha256="d9d2c45f89687cfc915a766aa91f01843ae97607baa1d1027fd208f8e014f71e")
    version("1.7.3", sha256="029acf61e7e760a3150716b145a58ce5052ee953e8cccc8441d4f550c420debb")
    version("1.7.2", sha256="2c26ccd08f43a6214de89110554fbe97c71692eeb7e7d4829f3004ae6fafd2c0")
    version("1.7.1", sha256="7e6d4120696e90995e66ac24f1042d4f11c14fbefd7aab48de0ed1fe3c4b922b")
    version("1.7.0", sha256="c48ec61785ec68fc6a9a6aca0a9578393414fe2562e3cc9cca30234345c7b6ac")
    version("1.6.7", sha256="f62ab88c2a87b55e1dc338726a55bb6ed8048084fe6a3294a7ae324ca45159d1")
    version("1.6.5", sha256="3abce972ba62620611fab5b404dafb852da3da54e7c287831c30863011d28fb3")
    version("1.6.3", sha256="0b03b9d22f4c9e59b4ba498f294e297f013cae27050dfa0f3496640200db5376")

    depends_on("c", type="build")

    depends_on("libxcb@1.11.1:", when="@1.6.4:")
    depends_on("libxcb@1.1.92:")

    depends_on("xproto@7.0.25:", when="@1.7.0:", type=("build", "link"))
    depends_on("xproto@7.0.17:", type=("build", "link"))
    depends_on("xextproto", type="build")
    depends_on("xtrans")
    depends_on("kbproto", type=("build", "link"))
    depends_on("inputproto", type="build")
    depends_on("pkgconfig", type="build")
    depends_on("util-macros", type="build")
    depends_on("perl", type="build")

    def configure_args(self):
        config_args = []

        # -Werror flags are not properly interpreted by the NVIDIA compiler
        if self.spec.satisfies("%nvhpc@:20.11"):
            config_args.append("--disable-selective-werror")

        return config_args

    def setup_dependent_build_environment(self, env, dependent_spec):
        env.prepend_path("XLOCALEDIR", self.prefix.share.X11.locale)

    def setup_dependent_run_environment(self, env, dependent_spec):
        env.prepend_path("XLOCALEDIR", self.prefix.share.X11.locale)

    @property
    def libs(self):
        for dir in ["lib64", "lib"]:
            libs = find_libraries(
                "libX11", join_path(self.prefix, dir), shared=True, recursive=False
            )
            if libs:
                return libs
        return None
