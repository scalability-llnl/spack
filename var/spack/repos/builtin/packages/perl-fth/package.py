# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import re

from spack.package import *


class PerlFth(Package):
    """Ftagshtml is a Fortran (and simple C) to HTML browsing,
    resolves static interface overload.
    It can handle some LaTeX comments inside the source files.
    It only needs to be put somewhere into your disk since it uses Perl.
    It also provides javatex2.pl initmak.pl getin.pl tex3ht.pl and view.pl:
    (1) javatex2 complements latex2html to make nice browsing,
    (2) initmak makes fortran 90 dependencies, either full deps or partial
       (when interface is not modified it is silly to recompile everything)
    (3) getin is an advanced search tool for Fortran variables and calls,
    (4) view.pl is used for CGI search when source is on http server.
    """

    homepage = "https://sourceforge.net/projects/ftagshtml/"
    url = "https://downloads.sourceforge.net/project/ftagshtml/ftagshtml-0.529.tgz"

    maintainers("cessenat")

    version("0.529", sha256="3cc2030372cf88dad257bd0cfbe662873a454d55035c54a76090e0da860074c4")
    version("0.527", sha256="df98e9e2f4dbef863b09a22ed92681dff028a6f345ba530bc3afd8221efe633c")
    version("0.526", sha256="ada1c7306111d59d64572fe8a9b038026fd0daebaff630924997ef2dc22d87a8")
    version("0.525", sha256="378116febeb20f4b0c1e298de90305e8494335949d853c7e390d1b6386c1326a")
    version("0.524", sha256="2f378e969d1dd267985342f7fb1b3a0b9fd73334627cbc7ab17d61717bcd3c29")
    version("0.523", sha256="d5d3fbd3caca30eee9de45baa46612841d55b2960db8e11411af6db76cf214ad")
    version("0.522", sha256="acb73eb2c05b1ed7b75f86fbd9656c00158519b3d11d89a082117004deb0fb9e")
    version("0.521", sha256="f980c9cc1ce644340a9e9630ef252f92bc89a411ea0a661fcb80cdae07f0731c")
    version("0.520", sha256="0ac509a7416d67f5ddc4ad9f629cb0443e1ce515cf9eb92f4272eb6b545a4c50")
    version("0.519", sha256="7a440ca08a18edbc57a4a5da7c90c98551ae1adaa303c9f984e5712e1cd54ffb")
    version("0.518", sha256="7aed7c831270bb1935d4ccd090ef1360ec9446dd773c10350645985047f8879b")
    version("0.517", sha256="e24488a7edbfa764060f007693329d5ee3154e1ce49a627ec109c41a9d7abcbe")

    depends_on("c", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant(
        "hevea", default=False, description="Use hevea when inputting LaTeX files (fth.pl -hevea)"
    )
    variant(
        "pdflatex",
        default=False,
        description="Use pdflatex to make a LaTeX index file (fth.pl -latexindex)",
    )

    depends_on("perl", type="run")
    depends_on("perl-cgi", type="run")
    # Actual dependency was on etags only, but no longer in recent releases:
    depends_on("emacs", type="run", when="@:0.520")
    # For fth.pl -hevea option
    depends_on("hevea", when="+hevea", type="run")
    # Actual dependency is on pdflatex only for fth.pl -latexindex option
    depends_on("texlive", when="+pdflatex", type="run")
    # initmak.pl uses md5sum provided by coreutils
    depends_on("coreutils", type="run")
    depends_on("dos2unix", type="build")

    # Patches to remove the ancient ksh shebang for fth.pl and initmak.pl.
    # git diff a/bin/fth.pl b/bin/fth.pl
    patch(
        "fth-shebang.patch",
        when="@0.517:0.522",
        sha256="3e82d34c8ae1709e5480fac87db387c1c2e219d7b7d596c8a9d62f0da2439ab3",
    )
    patch(
        "fth-shebang2.patch",
        when="@0.517:0.522",
        sha256="839be7c0efad752ae341379c81ee1df4a3a81f608f802998c6b4ebc4bae8e167",
    )

    executables = [r"^fth.pl$"]

    def _make_executable(self, name):
        return Executable(join_path(self.prefix.bin, name + ".pl"))

    def setup_dependent_package(self, module, dependent_spec):
        # https://spack-tutorial.readthedocs.io/en/latest/tutorial_advanced_packaging.html
        checks = ["fth", "getin", "view", "javatex2", "tex3ht", "initmak"]
        for name in checks:
            setattr(module, name, self._make_executable(name))

    def setup_dependent_build_environment(self, env, dependent_spec):
        env.set("JAVATEX_DIR", self.prefix)
        env.set("FTAGSHTML_DIR", self.prefix)
        env.set("FTAGSHTML_DOC", join_path(self.prefix, "doc"))

    def setup_run_environment(self, env):
        # https://github.com/spack/spack/discussions/13926
        # Let us set the adequate environment when loading perl-fth
        env.set("JAVATEX_DIR", self.prefix)
        env.set("FTAGSHTML_DIR", self.prefix)
        env.set("FTAGSHTML_DOC", join_path(self.prefix, "doc"))

    def install(self, spec, prefix):
        # Remove the perl shebang with the local perl
        # (since ftagshtml has no Makefile.PL to do it).
        checks = ["fth", "getin", "view", "javatex2", "tex3ht", "initmak"]
        # mstr = '#!' + join_path(spec['perl'].prefix.bin, 'perl')
        mstr = "#!" + spec["perl"].command.path
        with working_dir("bin"):
            for exe in checks:
                fic = exe + ".pl"
                if os.path.exists(fic):
                    dos2unix = which("dos2unix")
                    dos2unix(fic)
                    fthfile = FileFilter(fic)
                    fthfile.filter("#!/usr/bin/perl", mstr, backup=False)
                    fthfile.filter("#!/usr/bin/env perl", mstr, backup=False)

        # Adds a Makefile with an rsync rule
        makefile_inc = ["RSYNC_OPTS = -avuzL", "RSYNC = rsync"]
        makefile_inc.append("install:")
        makefile_inc.append("\t$(RSYNC) $(RSYNC_OPTS) . %s" % prefix)
        makefile_inc.append("")
        with working_dir("."):
            with open("Makefile", "a") as fh:
                fh.write("\n".join(makefile_inc))

        # Remove obsolete ftagshtml files, if they exist:
        with working_dir("bin"):
            if os.path.exists("ftagshtml"):
                os.remove("ftagshtml")
            if os.path.exists("tata.pl"):
                os.remove("tata.pl")
            if os.path.exists("truc.pl"):
                os.remove("truc.pl")

        # Install the full directory structure
        install_tree(".", prefix)

    @classmethod
    def determine_version(cls, exe):
        output = Executable(exe)("--version", output=str, error=str)
        match = re.search(r"([\d\.]+)", output)
        return match.group(1) if match else None
