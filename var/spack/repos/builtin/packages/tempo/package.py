# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Tempo(AutotoolsPackage):
    """Tempo is a program for pulsar timing data analysis."""

    # Warning:  Tempo references reads files that it's shipped with.
    # It's written in Fortran and the fortran code declares strings of a certain length
    # for those files.  If you haven't modified some of the Spack configurations
    # in terms of where the install go, hash length, etc. then it is likely
    # that running tempo will fail with an error similar to
    #
    # more: cannot open /...../gcc-11.3.0/tempo-master-lnizs: No such file or directory
    #

    homepage = "http://tempo.sourceforge.net/"
    git = "https://git.code.sf.net/p/tempo/tempo.git"

    version("master", branch="master", preferred=True)
    version("develop")
    version("LWA-10-17-2020", commit="6bab1083350eca24745eafed79a55156bdd1e7d5")

    depends_on("c", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")

    @run_before("configure")
    def edit(self):
        # By default tempo.cfg.in uses abs_top_srcdir (i.e., the staging/build directory)
        # In spack this directory gets deleted by default so make the file use the
        # Install prefix directory instead but only for the master version
        # So we don't possibly break anything for the LWA version
        if "master" in str(self.version):
            tempocfg = FileFilter("tempo.cfg.in")
            tempocfg.filter(r"(.*)(abs_top_srcdir)(.*)", r"\1prefix\3")

    @run_after("install")
    def post_install_packages(self):

        # Copy some files over needed by TEMPO, again only for the master version
        if "master" in str(self.version):
            cd(self.stage.source_path)
            cp = which("cp")

            cp("obsys.dat", join_path(self.prefix, "obsys.dat"))
            cp("tempo.hlp", join_path(self.prefix, "tempo.hlp"))
            cp("tempo.cfg", join_path(self.prefix, "tempo.cfg"))

            cp("-r", "clock", join_path(self.prefix, "clock"))
            cp("-r", "ephem", join_path(self.prefix, "ephem"))
            cp("-r", "tzpar", join_path(self.prefix, "tzpar"))

    def setup_dependent_build_environment(self, env, dependent_spec):
        env.set("TEMPO", self.prefix)

    def setup_dependent_run_environment(self, env, dependent_spec):
        env.set("TEMPO", self.prefix)

        # For LWA-10-17-2020 version
        env.set("TEMPO_DIR", self.prefix)

    def setup_run_environment(self, env):
        env.set("TEMPO", self.prefix)
