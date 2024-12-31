# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class Turbovnc(CMakePackage):
    """A VNC server tuned to provide peak 3D performance"""

    homepage = "https://turbovnc.org/"
    url = "https://github.com/TurboVNC/turbovnc/archive/refs/tags/3.1.1.tar.gz"

    maintainers("teaguesterling")

    license("GPLv2", checked_by="teaguesterling")

    version("3.1.3", sha256="50ec787c716a1649e270cfd79bf57190fe78c874df541bad2876c1fa8e1de393")
    version("3.1.1", sha256="834392e985cf29a6d7d3b21b6b95b8249c1390f2c4bbf716e03945ca9384bbc8")
    version("3.1", sha256="218eaf769c29763d4e6062978b8f2fb5538dc2b232b77d3f094591fe63ddbf65")
    version("3.0.3", sha256="3a3e1bce1d6d41b33b52c51c8546c849db1226f42255f4cef306e7bd9e1cced4")

    generator("ninja")

    variant("viewer", default=True, description="Build VNC viewer")
    variant("server", default=True, description="Build VNC server")
    variant("web", default=True, description="Build with noVNC support", when="+server")
    variant("libs", default=True, description="Build with spack-provided core libs")
    variant("x11", default=True, description="Build with spack-provided X11")
    variant("glx", default=False, description="Build with GLX support", when="+x11")
    variant("tls", default=True, description="Build with TLS encryption")

    # This can be disable to statically link for compatibility
    variant("dynamicssl", default=True, description="Duynamically link openssl", when="+tls")
    variant("customjre", default=False, description="Build with a custom JRE", when="+viewer")

    with default_args(type="build"):
        depends_on("ninja")
        depends_on("cmake@2.8.12:")
        depends_on("cmake@3.12:", when="+web")
        depends_on("gettext")
        depends_on("perl-extutils-makemaker")
        depends_on("pkgconfig")

    depends_on("libjpeg-turbo@1.2:")
    depends_on("linux-pam")
    depends_on("libcap")
    depends_on("krb5")

    depends_on("libice")
    depends_on("libsm")
    depends_on("xz")
    depends_on("lua")

    depends_on("python")
    with when("+web"):
        depends_on("python@3:")
        depends_on("novnc")

    depends_on("openjdk@11:", when="+viewer")
    depends_on("openssl", when="+tls")

    with when("+libs"):
        depends_on("zlib-api")
        depends_on("bzip2")
        depends_on("freetype")

    with when("+x11"):
        # Core TurboVNC dependencies
        depends_on("libx11")
        depends_on("libxau")
        depends_on("libxdmcp")
        depends_on("libxkbfile")
        depends_on("libxfont2")
        depends_on("libfontenc")
        depends_on("pixman")

        depends_on("xorgproto")
        depends_on("libxfixes")
        depends_on("libxi")
        depends_on("libxrandr")

        # Dependencies separated out by spack's packaging
        depends_on("font-util")
        depends_on("xkbcomp")
        depends_on("xkeyboard-config")

    with when("+glx"):  # This may need more specific versions but I'm not able to test
        depends_on("libxext")
        depends_on("libglx")
        depends_on("egl")  # For dri_interface.h

    with default_args(type="run"):
        depends_on("xauth")

    conflicts("%gcc@14:", msg="GCC 14+ does not support implicit declarations", when="@:3.1.1")

    def cmake_args(self):
        spec = self.spec
        jpeg = spec["libjpeg-turbo"]
        fontutil = spec["font-util"]
        xkbcomp = spec["xkbcomp"]
        xkbbase = spec["xkeyboard-config"]

        args = [
            # Always need turbojpeg
            self.define("TJPEG_INCLUDE_DIR", jpeg.home.include),
            self.define("TJPEG_LIBRARY", f"-L{jpeg.home.lib} -lturbojpeg"),
            # Major components to build
            self.define_from_variant("TVNC_BUILDVIEWER", "viewer"),
            self.define_from_variant("TVNC_BUILDSERVER", "server"),
            self.define_from_variant("TVNC_BUILDWEBSERVER", "web"),
            self.define_from_variant("TVNC_GLX", "glx"),
            # Build with Spack libraries
            self.define_from_variant("TVNC_SYSTEMLIBS", "libs"),
            self.define_from_variant("TVNC_SYSTEMX11", "x11"),
            # Specialized build options
            self.define_from_variant("TVNC_DLOPENSSL", "dynamicssl"),
            self.define_from_variant("TVNC_INCLUDEJRE", "customjre"),
        ]

        if spec.satisfies("+x11"):
            args += [
                # Keyboard configuration (Xvnc wont start if this is wrong)
                # We need to tell TurboVNC where xkbcomp is
                self.define("XKB_BIN_DIRECTORY", xkbcomp.home.bin),
                # We also need to tell it where to find the xkb rules
                self.define("XKB_BASE_DIRECTORY", xkbbase.home.share.X11.xkb),
                # Where what the default rules are. This appears to be the only option from spack.
                self.define("XKB_DFLT_RULES", "base"),
                # Font configuration (Xvnc may not start if this is wrong)
                # Make sure the fonts directory is defined
                self.define("XORG_FONT_PATH", fontutil.home.share.fonts.X11),
                # And the font encodings directory
                self.define("FONT_ENCODINGS_DIRECTORY", fontutil.home.share.fonts.X11.encodings),
            ]

        # Other args for future reference
        # VNC_STATIC_XORG_PATHS=0 - If need to compile with fixed xorg lib paths
        # XORG_DRI_DRIVER_PATH    - Don't know how or if we actually need this, maybe for glx
        # XORG_REGISTRY_PATH      - Nothing provides protocols.txt but build still works
        return args
