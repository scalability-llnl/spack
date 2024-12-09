# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Pinentry(AutotoolsPackage):
    """pinentry is a small collection of dialog programs that allow GnuPG to
    read passphrases and PIN numbers in a secure manner.

    There are versions for the common GTK and Qt toolkits as well as for
    the text terminal (Curses).
    """

    homepage = "https://gnupg.org/related_software/pinentry/index.html"
    url = "https://gnupg.org/ftp/gcrypt/pinentry/pinentry-1.1.0.tar.bz2"

    maintainers("alalazo")

    license("GPL-2.0-or-later")

    version("1.3.1", sha256="bc72ee27c7239007ab1896c3c2fae53b076e2c9bd2483dc2769a16902bce8c04")
    version("1.3.0", sha256="9b3cd5226e7597f2fded399a3bc659923351536559e9db0826981bca316494de")
    version("1.2.1", sha256="457a185e5a85238fb945a955dc6352ab962dc8b48720b62fc9fa48c7540a4067")
    version("1.2.0", sha256="10072045a3e043d0581f91cd5676fcac7ffee957a16636adedaa4f583a616470")
    version("1.1.1", sha256="cd12a064013ed18e2ee8475e669b9f58db1b225a0144debdb85a68cecddba57f")
    version("1.1.0", sha256="68076686fa724a290ea49cdf0d1c0c1500907d1b759a3bcbfbec0293e8f56570")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    supported_guis = [
        "curses",
        "tty",
        "emacs",
        "efl",
        "gtk2",
        "gnome3",
        "qt",
        "qt5",
        "tqt",
        "fltk",
    ]

    # Default to 'tty' as it has no additional dependencies
    variant(
        "gui",
        default="tty",
        description="GUI to use for passphrase entry",
        values=supported_guis,
        multi=True,
    )

    depends_on("libgpg-error@1.16:")
    depends_on("libassuan@2.1.0:")
    depends_on("libassuan@:2", when="@:1.2")

    # Optional GUI dependencies
    depends_on("ncurses", when="gui=curses")
    depends_on("emacs", when="gui=emacs")
    # depends_on('efl@1.18:', when='gui=efl')  # Enlightenment
    depends_on("gtkplus@2:", when="gui=gtk2")
    # depends_on('gnome@3:', when='gui=gnome3')  # GNOME
    depends_on("qt@4.4.0:", when="gui=qt")
    depends_on("qt@5.0:5", when="gui=qt5")
    # depends_on('tqt', when='gui=tqt')  # Trinity QT
    depends_on("fltk@1.3:", when="gui=fltk")

    # TODO: add packages for these optional GUIs
    conflicts("gui=efl")
    conflicts("gui=gnome3")
    conflicts("gui=tqt")

    def configure_args(self):
        args = [
            # Disable extra features
            "--disable-fallback-curses",
            "--disable-inside-emacs",
            "--disable-libsecret",
            # Required dependencies
            "--with-gpg-error-prefix=" + self.spec["libgpg-error"].prefix,
            "--with-libassuan-prefix=" + self.spec["libassuan"].prefix,
        ]

        if "gui=curses" in self.spec:
            args.append(
                "--with-ncurses-include-dir=" + self.spec["ncurses"].headers.directories[0]
            )

        for gui in self.supported_guis:
            if "gui=" + gui in self.spec:
                args.append("--enable-pinentry-" + gui)
            else:
                args.append("--disable-pinentry-" + gui)
        return args

    def check_version(self, exe_name):
        """Version check"""
        exe = which(join_path(self.prefix.bin, exe_name))
        out = exe("--version", output=str.split, error=str.split)
        assert str(self.version) in out

    def test_pinentry(self):
        """Confirm pinentry version"""
        self.check_version("pinentry")

    def test_guis(self):
        """Check gui versions"""
        for gui in self.supported_guis:
            if f"gui={gui}" not in self.spec:
                continue

            exe_name = f"pinentry-{gui}"
            with test_part(self, f"test_guis_{gui}", purpose=f"Check {exe_name} version"):
                self.check_version(exe_name)
