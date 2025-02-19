# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.build_systems import autotools, meson
from spack.package import *


class Cairo(AutotoolsPackage, MesonPackage):
    """Cairo is a 2D graphics library with support for multiple output
    devices."""

    homepage = "https://www.cairographics.org/"
    url = "https://www.cairographics.org/releases/cairo-1.16.0.tar.xz"

    license("LGPL-2.1-or-later OR MPL-1.1", checked_by="tgamblin")

    version("1.18.2", sha256="a62b9bb42425e844cc3d6ddde043ff39dbabedd1542eba57a2eb79f85889d45a")
    version("1.18.0", sha256="243a0736b978a33dee29f9cca7521733b78a65b5418206fef7bd1c3d4cf10b64")
    version(
        "1.17.4",
        sha256="74b24c1ed436bbe87499179a3b27c43f4143b8676d8ad237a6fa787401959705",
        url="https://cairographics.org/snapshots/cairo-1.17.4.tar.xz",
    )  # Snapshot
    version(
        "1.17.2",
        sha256="6b70d4655e2a47a22b101c666f4b29ba746eda4aa8a0f7255b32b2e9408801df",
        url="https://cairographics.org/snapshots/cairo-1.17.2.tar.xz",
    )  # Snapshot
    version("1.16.0", sha256="5e7b29b3f113ef870d1e3ecf8adf21f923396401604bda16d44be45e66052331")
    version("1.14.12", sha256="8c90f00c500b2299c0a323dd9beead2a00353752b2092ead558139bd67f7bf16")
    version("1.14.8", sha256="d1f2d98ae9a4111564f6de4e013d639cf77155baf2556582295a0f00a9bc5e20")
    version("1.14.0", sha256="2cf5f81432e77ea4359af9dcd0f4faf37d015934501391c311bfd2d19a0134b7")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    # 1.17.4 is the last autotools based version. From 1.18.0 onward it is meson only
    build_system(
        conditional("meson", when="@1.18.0:"),
        conditional("autotools", when="@:1.17.4"),
        default="meson",
    )

    variant("X", default=False, description="Build with X11 support")
    variant("gobject", default=False, description="Enable cairo's gobject functions feature")

    # variants and build system depends for the autotools builds
    with when("build_system=autotools"):
        variant("png", default=False, description="Enable cairo's PNG functions feature")
        variant("svg", default=False, description="Enable cairo's SVG functions feature")
        variant("pic", default=True, description="Enable position-independent code (PIC)")
        variant("pdf", default=False, description="Enable cairo's PDF surface backend feature")
        variant("ft", default=False, description="Enable cairo's FreeType font backend feature")
        variant("fc", default=False, description="Enable cairo's Fontconfig font backend feature")

        # seems to be an older cairo limitation as cairo@1.18.2 seems to build fine against libpng
        conflicts("+png", when="platform=darwin")
        conflicts("+svg", when="platform=darwin")

        # meson build already defines these and maps them to args
        # variant("shared", default=True, description="Build shared libraries")
        variant("shared", default=True, description="Build shared libraries")
        conflicts("+shared~pic")

        depends_on("automake", type="build")
        depends_on("autoconf", type="build")
        depends_on("libtool", type="build")
        depends_on("m4", type="build")
        depends_on("which", type="build")

    # variants and build system depends for the autotools builds
    # these names follow those listed here
    # https://gitlab.freedesktop.org/cairo/cairo/-/blob/1.18.2/meson_options.txt
    with when("build_system=meson"):
        variant("dwrite", default=False, description="Microsoft Windows DWrite font backend")

        # doesn't exist @1.17.8: but kept as compatibility
        variant(
            "pdf",
            default=False,
            description="""+pdf is combined into +zlib now, kept seperate for compatibility.
              +pdf implies +zlib now. Please use the updated variants""",
        )
        # svg is combined into png now, kept seperate for compatibility
        variant(
            "svg",
            default=False,
            description="""+svg is combined into +png now, kept seperate for compatibility.
              +svg implies +png now. Please use the updated variants""",
        )

        # meson seems to have assumptions about what is enabled/disabled
        # these four compile best if +variant in unison, otherwise various errors happen
        # if these aren't in sync. It is  easier to have a sane default. conflicts below
        # to try to protect known incompatibilities
        variant("png", default=True, description="Enable cairo's PNG and SVG functions feature")
        variant("ft", default=True, description="Enable cairo's FreeType font backend feature")
        variant("fc", default=True, description="Enable cairo's Fontconfig font backend feature")
        variant(
            "zlib",
            default=True,
            description="Enable cairo's script, ps, pdf, xml functions feature",
        )

        variant("quartz", default=False, description="Enable cairo's Quartz functions feature")
        variant("tee", default=False, description="Enable cairo's tee functions feature")

        # not in spack
        variant(
            "spectre",
            default=False,
            description="Not available. Enable cairo's spectre functions feature",
        )

        # (bfd might be too old) with binutils 2.43.1 on macos
        #  so not sure how this is supposed to work
        variant(
            "symbol-lookup",
            default=False,
            description="Not available. Enable cairo's symbol lookup functions feature",
        )

        # not currently supported variants
        conflicts("+spectre", msg="Not currently supported")
        conflicts("+symbol-lookup", msg="Not currently supported")

        # meson seems to have assumptions about what is enabled/disabled
        # so this protects against incompatible combinations
        conflicts("~zlib+png", msg="+png requires +zlib")
        conflicts("~ft+fc", msg="+fc requires +ft")
        conflicts("+ft~fc", msg="+ft requires +fc")
        conflicts("+ft+fc~zlib", msg="+fc+ft requires +zlib")
        conflicts("+fc+ft~png+zlib", msg="+ft+fc+zlib requires +png")

        # +pdf implies zlib now
        requires("+zlib", when="+pdf")
        requires("~zlib", when="~pdf", msg="+pdf implies +zlib now")
        # +svg implies png now
        requires("+svg", when="+png")
        requires("~png", when="~svg", msg="+svg implies +png now")

        # https://gitlab.freedesktop.org/cairo/cairo/-/blob/1.18.2/meson.build?ref_type=tags#L2
        depends_on("meson@1.3.0:", type="build")

    # both autotools and meson need this for auto discovery of depends
    depends_on("pkgconfig", type="build")

    # non build system specific depends
    # versions that use (the old) autotools build
    with when("@:1.17.4"):
        depends_on("pixman@0.36.0:", when="@1.17.2:")
        depends_on("freetype", when="+ft")
        depends_on("fontconfig@2.10.91:", when="+fc")
        depends_on("libpng", when="+png")
        depends_on("glib")

    # non build system specific depends
    # versions that use (the new) meson build
    with when("@1.18.0:"):
        depends_on("binutils", when="+symbol-lookup")
        depends_on("freetype@2.13.0:", when="+ft")
        depends_on("libpng@1.4.0:", when="+png")
        depends_on("glib@2.14:", when="+gobject")
        depends_on("pixman@0.40.0:")
        depends_on("fontconfig@2.13.0:", when="+fc")

        # lzo is not strictly required, but cannot be disabled and may be pulled in accidentally
        # https://github.com/mesonbuild/meson/issues/8224
        # https://github.com/microsoft/vcpkg/pull/38313
        depends_on("lzo")

    # needed for both meson and autotools builds when including X
    with when("+X"):
        depends_on("libx11")
        depends_on("libxext")

        depends_on("libxrender")
        depends_on("libxrender@0.6:", when="@1.17.8:")

        depends_on("libxcb")
        depends_on("libxcb@1.6:", when="@1.17.8:")

        depends_on("python", type="build")

    # patch from https://gitlab.freedesktop.org/cairo/cairo/issues/346
    patch("fontconfig.patch", when="@1.16.0:1.17.2")
    # Don't regenerate docs to avoid a dependency on gtk-doc
    patch("disable-gtk-docs.patch", when="build_system=autotools ^autoconf@2.70:")


class MesonBuilder(meson.MesonBuilder):
    def enable_or_disable(self, feature_name, variant=None):
        if variant is None:
            variant = feature_name
        return (
            f"-D{feature_name}=enabled"
            if self.spec.satisfies(f"+{variant}")
            else f"-D{feature_name}=disabled"
        )

    def meson_args(self):
        args = []

        args.append(self.enable_or_disable("dwrite"))
        args.append(self.enable_or_disable("fontconfig", variant="ft"))
        args.append(self.enable_or_disable("freetype", variant="fc"))

        args.append(self.enable_or_disable("png"))

        args.append(self.enable_or_disable("quartz"))
        args.append(self.enable_or_disable("tee"))
        args.append(self.enable_or_disable("xcb"))

        args.append(self.enable_or_disable("xlib", variant="X"))
        args.append(self.enable_or_disable("xlib-xcb", variant="X"))

        args.append(self.enable_or_disable("zlib"))

        args.append(self.enable_or_disable("glib", variant="gobject"))
        args.append(self.enable_or_disable("spectre"))
        args.append(self.enable_or_disable("symbol-lookup"))

        return args


class AutotoolsBuilder(autotools.AutotoolsBuilder):
    def autoreconf(self, pkg, spec, prefix):
        # Regenerate, directing the script *not* to call configure before Spack
        # does
        which("sh")("./autogen.sh", extra_env={"NOCONFIGURE": "1"})

    def configure_args(self):
        args = ["--disable-trace", "--enable-tee"]  # can cause problems with libiberty

        if self.spec.satisfies("+X"):
            args.extend(["--enable-xlib", "--enable-xcb"])
        else:
            args.extend(["--disable-xlib", "--disable-xcb"])

        args.extend(self.enable_or_disable("pdf"))
        args.extend(self.enable_or_disable("gobject"))
        args.extend(self.enable_or_disable("ft"))
        args.extend(self.enable_or_disable("fc"))
        args.extend(self.enable_or_disable("shared"))
        args.extend(self.with_or_without("pic"))

        if self.spec.satisfies("+ft ^freetype~shared"):
            pkgconf = which("pkg-config")
            ldflags = pkgconf("--libs-only-L", "--static", "freetype2", output=str)
            libs = pkgconf("--libs-only-l", "--static", "freetype2", output=str)
            args.append(f"LDFLAGS={ldflags}")
            args.append(f"LIBS={libs}")

        return args

    def check(self):
        """The checks are only for the cairo devs: They write others shouldn't bother"""
        pass
