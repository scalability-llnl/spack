# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class W3m(AutotoolsPackage):
    """
    w3m is a text-based web browser as well as a pager like `more' or `less'.
    With w3m you can browse web pages through a terminal emulator window (xterm,
    rxvt or something like that). Moreover, w3m can be used as a text formatting
    tool which typesets HTML into plain text.
    """

    # The main w3m project is not active anymore, but distributions still keep
    # and maintain it:
    # https://sourceforge.net/p/w3m/support-requests/17/
    # What source should distro packagers use for their w3m packages?
    # Feel free to use Debian's branch as you need.
    # Currently, Arch and Ubuntu (and Debian derivatives) use Debian's branch.
    # Also, Gentoo, Fedora and openSUSE switched to Debian's branch.
    homepage = "https://w3m.sourceforge.net/index.en.html"
    url = "https://salsa.debian.org/debian/w3m/-/archive/upstream/0.5.3+git20230121/w3m-upstream-0.5.3+git20230121.tar.gz"
    git = "https://salsa.debian.org/debian/w3m.git"

    maintainers("ronin_gw")

    license("MIT")

    version(
        "0.5.3.git20230121",
        sha256="8f0592e1cf7cf1de053e22c114cd79b85ebdb8dab925be7d343a130343b97c25",
    )
    version("0.5.3", sha256="e994d263f2fd2c22febfbe45103526e00145a7674a0fda79c822b97c2770a9e3")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    # mandatory dependency
    depends_on("bdw-gc")

    # termlib
    variant(
        "termlib",
        default="ncurses",
        description="select termlib",
        values=("ncurses", "termcap", "none"),
        multi=False,
    )
    depends_on("termcap", when="termlib=termcap")
    depends_on("ncurses+termlib", when="termlib=ncurses")

    # https support
    variant("https", default=True, description="support https protocol")
    depends_on("openssl@:1.0.2u", when="+https")

    # X11 support
    variant("image", default=True, description="enable image")
    depends_on("libx11", when="+image")

    # inline image support
    variant(
        "imagelib",
        default="imlib2",
        description="select imagelib",
        values=("gdk-pixbuf", "imlib2"),
        multi=False,
    )
    depends_on("gdk-pixbuf@2:+x11", when="imagelib=gdk-pixbuf +image")
    depends_on("imlib2@1.0.5:", when="imagelib=imlib2 +image")

    # fix for modern libraries
    patch("fix_redef.patch", when="@=0.5.3")
    patch("fix_gc.patch", when="@=0.5.3")

    def url_for_version(self, version):
        if ".git" in version.string:
            v = version.string.replace(".git", "+git")
            return f"https://salsa.debian.org/debian/w3m/-/archive/upstream/{v}/w3m-upstream-{v}.tar.gz"
        else:
            return f"https://downloads.sourceforge.net/project/w3m/w3m/w3m-{version}/w3m-{version}.tar.gz"

    def patch(self):
        # w3m is not developed since 2012, everybody is doing this:
        # https://www.google.com/search?q=USE_EGD+w3m
        filter_file("#define USE_EGD", "#undef USE_EGD", "config.h.in")

    def _add_arg_for_variant(self, args, variant, choices):
        for avail_lib in choices:
            if self.spec.variants[variant].value == avail_lib:
                args.append("--with-{0}={1}".format(variant, avail_lib))
                return

    def configure_args(self):
        args = ["ac_cv_search_gettext=no", "--enable-unicode"]

        self._add_arg_for_variant(args, "termlib", ("termcap", "ncurses"))
        if "+image" in self.spec:
            args.append("--enable-image")
            self._add_arg_for_variant(args, "imagelib", ("gdk-pixbuf", "imlib2"))

        return args

    def setup_build_environment(self, env):
        if self.spec.variants["termlib"].value == "ncurses":
            env.append_flags("LDFLAGS", "-ltinfo")
            env.append_flags("LDFLAGS", "-lncurses")
        if "+image" in self.spec:
            env.append_flags("LDFLAGS", "-lX11")

    # parallel build causes build failure
    parallel = False

    def build(self, spec, prefix):
        make("NLSTARGET=scripts/w3mman")

    def install(self, spec, prefix):
        make("NLSTARGET=scripts/w3mman", "install")
