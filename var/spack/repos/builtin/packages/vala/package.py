# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Vala(AutotoolsPackage):
    """Vala is a programming language that aims to bring modern programming
    language features to GNOME developers without imposing any additional
    runtime requirements and without using a different ABI compared to
    applications and libraries written in C."""

    homepage = "https://gitlab.gnome.org/GNOME/vala"
    url = "https://download.gnome.org/sources/vala/0.48/vala-0.48.25.tar.xz"

    maintainers("benkirk")

    license("LGPL-2.0-or-later")

    version("0.48.25", sha256="50cb3c5eccddc7fd4368bfa96414a556045e79d2b15a68918c727b8c83b18a24")
    version("0.48.24", sha256="3649ef84573b6865fc3470640ee603720099eb915b39faad19b7498de1a7df24")
    version("0.48.23", sha256="de3cc858d995e07474219e25a3e1f0ed998070d2e206d3a313d4379a5f77a06a")
    version("0.48.22", sha256="dbb3478c4be366f093164ac61cd3aedbdcf3e44404d9e36414ae15124e76e68b")
    version("0.48.21", sha256="305455aeb768d6ed9b018360b55182e48b16db1bc163a4e5b81420f98d21d998")
    version("0.48.20", sha256="46b1c817f74851fbcc395fc4f9ea119502cf87b9333cc9656e1cdccc0bd3376e")
    version("0.48.19", sha256="80b7658a37d9844fcd1b431dafc5804de616a58196e4f1f119e5b2aeb68b4a01")
    version("0.48.18", sha256="9e0f28f46f081d3bad4f3aab5a2078441752fa677a947433ba3cb99cbd257fdd")
    version("0.48.17", sha256="f26b8656aa2958884da26093c6fdec5f3ee6e0a2efda0434080f9a79da268bf2")
    version("0.48.16", sha256="4553663bfca3fa8a48c434e3fab18b6dabd429cfdec47ee25b957b6d2e20d390")
    version("0.48.15", sha256="5f64283f8e69a48c73256cb93578c7db4c35c0b7df079568a4d5b6065b602a50")
    version("0.48.14", sha256="dca57de29f4ce18ee8c6b1e4f1b37ca3843d19dae5c455fceebccc5ae3ffe347")

    depends_on("c", type="build")  # generated

    variant("doc", default=False, description="build valadoc")

    depends_on("pkgconfig", type="build")
    depends_on("glib@2.48:")
    depends_on("flex")
    depends_on("bison")
    depends_on("graphviz", when="+doc")

    def configure_args(self):
        args = []

        if "+doc" not in self.spec:
            args.append("--disable-valadoc")

        return args
