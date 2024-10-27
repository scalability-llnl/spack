# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libepoxy(AutotoolsPackage, MesonPackage):
    """Epoxy is a library for handling OpenGL function pointer management for
    you."""

    homepage = "https://github.com/anholt/libepoxy"
    url = "https://github.com/anholt/libepoxy/archive/refs/tags/1.5.9.tar.gz"

    license("MIT")

    build_system(
        conditional("autotools", when="@:1.5.4"),
        conditional("meson", when="@1.4.0:"),
        default="meson",
    )

    version("1.5.10", sha256="a7ced37f4102b745ac86d6a70a9da399cc139ff168ba6b8002b4d8d43c900c15")
    version("1.4.3", sha256="0b808a06c9685a62fca34b680abb8bc7fb2fda074478e329b063c1f872b826f6")

    depends_on("c", type="build")  # generated

    depends_on("pkgconfig", type="build")
    depends_on("gl")
    depends_on("libx11", when="+glx")

    variant("glx", default=True, description="enable GLX support")

    def url_for_version(self, version):
        if self.spec.satisfies("@1.5.10:"):
            # no more release artifacts are uploaded
            return f"https://github.com/anholt/libepoxy/archive/refs/tags/{version}.tar.gz"
        else:
            return f"https://github.com/anholt/libepoxy/releases/download/{version}/libepoxy-{version}.tar.xz"


class MesonBuilder(spack.build_systems.meson.MesonBuilder):

    def meson_args(self):
        # Disable egl, otherwise configure fails with:
        # error: Package requirements (egl) were not met
        # Package 'egl', required by 'virtual:world', not found
        args = ["-Degl=no"]

        # Option glx defaults to auto and was failing on PPC64LE systems
        # because libx11 was missing from the dependences. This explicitly
        # enables/disables glx support.
        if self.spec.satisfies("+glx"):
            args.append("-Dglx=yes")
        else:
            args.append("-Dglx=no")

        return args


class AutotoolsBuilder(spack.build_systems.autotools.AutotoolsBuilder):

    def configure_args(self):
        # Disable egl, otherwise configure fails with:
        # error: Package requirements (egl) were not met
        # Package 'egl', required by 'virtual:world', not found
        args = ["--enable-egl=no"]

        # --enable-glx defaults to auto and was failing on PPC64LE systems
        # because libx11 was missing from the dependences. This explicitly
        # enables/disables glx support.
        if self.spec.satisfies("+glx"):
            args.append("--enable-glx=yes")
        else:
            args.append("--enable-glx=no")

        return args
