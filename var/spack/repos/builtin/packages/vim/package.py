# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Vim(AutotoolsPackage):
    """Vim is a highly configurable text editor built to enable efficient text
    editing. It is an improved version of the vi editor distributed with most
    UNIX systems.  Vim is often called a "programmer's editor," and so useful
    for programming that many consider it an entire IDE. It's not just for
    programmers, though. Vim is perfect for all kinds of text editing, from
    composing email to editing configuration files.
    """

    homepage = "https://www.vim.org"
    url = "https://github.com/vim/vim/archive/v8.1.0338.tar.gz"

    maintainers("sethrj")

    license("Vim")

    version("9.1.0437", sha256="7024fbf8d0e8eec2eae21d279d487b60c58dc4ba3d42146388dc3743506d1fe6")
    version("9.0.0045", sha256="594a31e96e3eda07a358db305de939ca749693b4684de9e027bfa70311b1994d")
    version(
        "9.0.0000",
        sha256="1b3cd3732eb7039cf58a9321de26ab1a12d81c2f6760eb03c5d7b60d548f4587",
        deprecated=True,
    )
    version("8.2.2541", sha256="2699dfe87b524169e7390f0b383c406cb77a9fde7431665d3b9b80964d8d5daf")
    version("8.2.1201", sha256="39032fe866f44724b104468038dc9ac4ff2c00a4b18c9a1e2c27064ab1f1143d")
    version("8.2.0752", sha256="d616945810dac5a1fab2f23b003d22bdecd34861b31f208d5d0012a609821c0f")
    version("8.1.2141", sha256="7be3c3d88a6c871121230ffb9b7371b1d2ab462118dedb967c7265473af1144b")
    version("8.1.0338", sha256="3febcc4e49eaca458be1a1e8055a3a52887aa2054b03e24d5f38d192c3de51a0")
    version("8.1.0001", sha256="c342acaa26589f371fa34a5ca213b95811f26185c12443f8f48ad2868dee2935")
    version("8.0.1376", sha256="1ad8b5a0b9b63df5abc3f8050e31e1cb49379ffcfd2662a56daeff8bd3d780b9")
    version("8.0.0503", sha256="f2a316a7ae83eccfecf4a700e631094fce9df873358e3d5f112134faa74082ac")
    version("8.0.0454", sha256="e1f683c4a0e3fa56fa02769bbca576e4960850b0ca8640514a7b114b88c27b89")
    version("8.0.0134", sha256="1b3e3e7d187eed55cbdb0a1dae6b8f3b885005fbae84222420877d7afa3b2310")
    version("7.4.2367", sha256="a9ae4031ccd73cc60e771e8bf9b3c8b7f10f63a67efce7f61cd694cd8d7cda5c")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    _features = ("huge", "big", "normal", "small", "tiny")

    variant("cscope", default=False, description="build with cscope support")
    variant("features", default="normal", description="feature set", values=_features, multi=False)
    variant("gui", default=False, description="build with gui (gvim)")
    variant("lua", default=False, description="build with Lua")
    variant("perl", default=False, description="build with Perl")
    variant("python", default=False, description="build with Python")
    variant("ruby", default=False, description="build with Ruby")
    variant("x", default=False, description="use the X Window System")
    variant("gtk", default=False, when="+gui", description="use the GTKv3 gui.")

    for _f in _features[1:]:
        conflicts("+gui", when="features=" + _f, msg="+gui requires features=huge")

    depends_on("findutils", type="build")
    depends_on("ncurses", when="@7.4:")

    depends_on("cscope", when="+cscope", type="run")
    depends_on("lua", when="+lua")
    depends_on("perl", when="+perl")
    depends_on("python", when="+python")
    depends_on("ruby", when="+ruby")
    depends_on("fontconfig", when="+gui")
    depends_on("libx11", when="+x")
    depends_on("libsm", when="+x")
    depends_on("libxpm", when="+x")
    depends_on("libxt", when="+x")
    depends_on("libxtst", when="+x")
    depends_on("gtkplus@3:", when="+gtk")

    provides("xxd")

    def configure_args(self):
        spec = self.spec
        args = ["--enable-fail-if-missing"]

        def yes_or_no(variant):
            return "yes" if spec.variants[variant].value else "no"

        if "+termlib" in spec["ncurses"]:
            args.append("--with-tlib=tinfow")
        else:
            args.append("--with-tlib=ncursesw")

        args.append("--with-features=" + spec.variants["features"].value)

        if "+python" in spec:
            if spec["python"].version >= Version("3"):
                args.append("--enable-python3interp=dynamic")
                args.append("--enable-pythoninterp=no")
            else:
                args.append("--enable-python3interp=no")
                args.append("--enable-pythoninterp=dynamic")
        else:
            args.append("--enable-python3interp=no")

        if "+gui" in spec:
            args.append("--enable-gui={}".format("gtk3" if "+gtk" in spec else "auto"))
        else:
            args.append("--enable-gui=no")

        args.extend(
            [
                "--enable-luainterp=" + yes_or_no("lua"),
                "--enable-perlinterp=" + yes_or_no("perl"),
                "--enable-rubyinterp=" + yes_or_no("ruby"),
            ]
        )
        args.extend(self.enable_or_disable("cscope"))
        args.extend(self.with_or_without("x"))

        if "+lua" in spec:
            args.append("--with-lua-prefix=" + spec["lua"].prefix)

        return args

    # Tests must be run in serial
    def check(self):
        make("test", parallel=False)

    # Run the install phase with -j 1.  There seems to be a problem with
    # parallel builds that results in the creation of the links (e.g. view)
    # to the vim binary silently failing.
    def install(self, spec, prefix):
        make("install", parallel=False)
