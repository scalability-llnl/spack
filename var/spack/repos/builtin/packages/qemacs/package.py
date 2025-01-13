# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Qemacs(MakefilePackage):
    """Light emacs clone."""

    homepage = "https://github.com/qemacs/qemacs/"
    git = "https://github.com/qemacs/qemacs.git"

    license("MIT", checked_by="Buldram")
    maintainers("Buldram")

    version("master", branch="master")
    version("6.3.3", commit="e3c5bfd457614773508feefdc12dbc60073030ed")
    version("6.3.2", commit="0e90c181078f3d85d0d44d985d541184223668e1")
    version("6.3.1", commit="288eeb450e534a39adb337396aa9ffcdc629f94e")
    version("6.2.1", commit="e566f230642f63fe7870990374e1bdc4d69fee9c")

    conflicts("%apple-clang", msg="Incompatible with Apple Clang's default linker.")

    depends_on("which", type="build")

    variant("docs", default=False, description="Build documentation")
    variant("plugins", default=False, description="Enable plugin support")
    variant("X", default=False, description="Build with X11 support")
    variant("png", default=True, when="+X", description="Build with PNG support")
    variant("xshm", default=True, when="+X", description="Build with XShm support")
    variant("xv", default=True, when="+X", description="Build with X Video support")

    conflicts("+docs", when="platform=freebsd")
    conflicts("+plugins", when="platform=freebsd")
    conflicts("+plugins", when="platform=darwin")

    depends_on("texi2html", type="build", when="+docs")
    depends_on("libx11", type="link", when="+X")
    depends_on("libxcb", type="link", when="+X")
    depends_on("libxau", type="link", when="+X")
    depends_on("libxdmcp", type="link", when="+X")
    depends_on("libpng", type="link", when="+png")
    depends_on("libxext", type="link", when="+xshm")
    depends_on("libxv", type="link", when="+xv")

    def edit(self, spec, prefix):
        Executable("./configure")(
            "--prefix=" + prefix,
            "--" + ("enable" if spec.satisfies("+plugins") else "disable") + "-plugins",
            "--" + ("enable" if spec.satisfies("+X") else "disable") + "-x11",
            "--" + ("enable" if spec.satisfies("+png") else "disable") + "-png",
            "--" + ("enable" if spec.satisfies("+xshm") else "disable") + "-xshm",
            "--" + ("enable" if spec.satisfies("+xv") else "disable") + "-xv",
            "--disable-tiny",  # Currently broken
            "--disable-html",  # Currently broken
            "--disable-ffmpeg",  # Currently broken
            "--disable-xrender",  # Currently broken
        )
