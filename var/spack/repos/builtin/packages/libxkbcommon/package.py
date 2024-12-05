# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import spack.build_systems.autotools
import spack.build_systems.meson
from spack.package import *


class Libxkbcommon(MesonPackage, AutotoolsPackage):
    """xkbcommon is a library to handle keyboard descriptions, including
    loading them from disk, parsing them and handling their state. It's mainly
    meant for client toolkits, window systems, and other system
    applications."""

    homepage = "https://xkbcommon.org/"
    url = "https://xkbcommon.org/download/libxkbcommon-0.8.2.tar.xz"

    build_system(
        conditional("meson", when="@0.9:"), conditional("autotools", when="@:0.8"), default="meson"
    )

    license("MIT")

    version("1.7.0", sha256="65782f0a10a4b455af9c6baab7040e2f537520caa2ec2092805cdfd36863b247")
    version("1.6.0", sha256="0edc14eccdd391514458bc5f5a4b99863ed2d651e4dd761a90abf4f46ef99c2b")
    version("1.5.0", sha256="560f11c4bbbca10f495f3ef7d3a6aa4ca62b4f8fb0b52e7d459d18a26e46e017")
    version("1.4.1", sha256="943c07a1e2198026d8102b17270a1f406e4d3d6bbc4ae105b9e1b82d7d136b39")
    version("1.4.0", sha256="106cec5263f9100a7e79b5f7220f889bc78e7d7ffc55d2b6fdb1efefb8024031")
    version(
        "0.8.2",
        sha256="7ab8c4b3403d89d01898066b72cb6069bddeb5af94905a65368f671a026ed58c",
        deprecated=True,
    )
    version(
        "0.8.0",
        sha256="e829265db04e0aebfb0591b6dc3377b64599558167846c3f5ee5c5e53641fe6d",
        deprecated=True,
    )
    version(
        "0.7.1",
        sha256="ba59305d2e19e47c27ea065c2e0df96ebac6a3c6e97e28ae5620073b6084e68b",
        deprecated=True,
    )

    depends_on("c", type="build")  # generated

    variant("wayland", default=False, description="Enable Wayland support")

    depends_on("meson@0.41:", type="build", when="@0.9:")
    depends_on("meson@0.49:", type="build", when="@1.0:")
    depends_on("meson@0.51:", type="build", when="@1.5:")
    depends_on("meson@0.52:", type="build", when="@1.6:")
    depends_on("pkgconfig@0.9.0:", type="build")
    depends_on("bison", type="build")
    depends_on("util-macros")
    depends_on("xkbdata")
    depends_on("libxcb@1.10:")
    depends_on("libxml2", when="@1:")

    depends_on("wayland@1.2.0:", when="+wayland")
    depends_on("wayland-protocols@1.7:", when="+wayland")


class MesonBuilder(spack.build_systems.meson.MesonBuilder):
    def meson_args(self):
        args = [
            "-Dxkb-config-root={0}".format(self.spec["xkbdata"].prefix),
            "-Denable-docs=false",
            "-Denable-wayland=" + str(self.spec.satisfies("+wayland")),
        ]

        if self.spec.satisfies("@1.6:"):
            args.append("-Denable-bash-completion=false")

        return args


class AutotoolsBuilder(spack.build_systems.autotools.AutotoolsBuilder):
    def configure_args(self):
        """Configure arguments are passed using meson_args functions"""
        return [
            "--with-xkb-config-root={0}".format(self.spec["xkbdata"].prefix),
            "--disable-docs",
        ] + self.enable_or_disable("wayland")
