# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *
from spack.pkg.builtin.boost import Boost


class Herwigpp(AutotoolsPackage):
    """Herwig is a multi-purpose particle physics event generator.
    This package provides old Herwig++ 2 generator"""

    homepage = "https://herwig.hepforge.org/"
    url = "http://lcgpackages.web.cern.ch/lcgpackages/tarFiles/sources/MCGeneratorsTarFiles/Herwig++-2.7.1.tar.bz2"

    tags = ["hep"]

    license("GPL-2.0-only")

    version("2.7.1", sha256="80a189376bb65f5ec4e64f42e76c00ea9102d8224010563a424fc11e619a6ad6")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated
    patch("herwig++-2.7.1.patch", when="@2.7.1", level=0)

    depends_on("gsl")

    # TODO: replace this with an explicit list of components of Boost,
    # for instance depends_on('boost +filesystem')
    # See https://github.com/spack/spack/pull/22303 for reference
    depends_on(Boost.with_default_variants)
    depends_on("fastjet")
    depends_on("thepeg@1.9.2", when="@2.7.1")

    def setup_build_environment(self, env):
        env.prepend_path("LD_LIBRARY_PATH", self.spec["thepeg"].prefix.lib.ThePEG)

    def configure_args(self):
        args = [
            "--with-gsl=" + self.spec["gsl"].prefix,
            "--with-thepeg=" + self.spec["thepeg"].prefix,
            "--with-fastjet=" + self.spec["fastjet"].prefix,
            "--with-boost=" + self.spec["boost"].prefix,
        ]
        return args

    def build(self, spec, prefix):
        make()
        with working_dir("Contrib"):
            make()

        with working_dir("Contrib/AlpGen"):
            make(
                "BasicLesHouchesFileReader.so",
                "HERWIGINCLUDE=-I{0}/include".format(self.stage.source_path),
            )
            make("AlpGenHandler.so", "HERWIGINCLUDE=-I{0}/include".format(self.stage.source_path))

    def install(self, spec, prefix):
        make("install")
        install(
            join_path(self.stage.source_path, "Contrib", "AlpGen", "AlpGenHandler.so"),
            join_path(prefix.lib, "Herwig++", "AlpGenHandler.so"),
        )

        install(
            join_path(self.stage.source_path, "Contrib", "AlpGen", "BasicLesHouchesFileReader.so"),
            join_path(prefix.lib, "Herwig++", "BasicLesHouchesFileReader.so"),
        )
