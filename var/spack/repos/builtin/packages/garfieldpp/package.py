# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Garfieldpp(CMakePackage):
    """Garfield++ is a toolkit for the detailed simulation of particle
    detectors based on ionisation measurement in gases and semiconductors."""

    homepage = "https://garfieldpp.web.cern.ch/garfieldpp/"
    url = "https://gitlab.cern.ch/garfield/garfieldpp/-/archive/4.0/garfieldpp-4.0.tar.gz"
    git = "https://gitlab.cern.ch/garfield/garfieldpp.git"

    tags = ["hep"]

    maintainers("mirguest")
    patch(
        "https://gitlab.cern.ch/garfield/garfieldpp/-/commit/882c3023cfa89b45ca7a0c95ab1518454536e8e1.diff",
        sha256="ea3b91d67011abe41e72c7b55578d14b77bd2ef5e7f344077091934b24f38f0d",
        when="@4.0",
    )

    variant("examples", default=False, description="Build garfield examples")

    version("master", branch="master")
    version("5.0", sha256="453e83c2829f57046c471a691e7cd9630650a3c6a696f3be6e86bf2d5159e7b3")
    version("4.0", sha256="82bc1f0395213bd30a7cd854426e6757d0b4155e99ffd4405355c9648fa5ada3")
    version("3.0", sha256="c1282427a784658bc38b71c8e8cfc8c9f5202b185f0854d85f7c9c5a747c5406")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    depends_on("root")
    depends_on("gsl")
    depends_on("geant4", when="+examples")

    def cmake_args(self):
        args = [
            "-DCMAKE_INSTALL_LIBDIR=lib",
            self.define_from_variant("WITH_EXAMPLES", "examples"),
        ]
        return args

    def setup_run_environment(self, env):
        env.set("GARFIELD_INSTALL", self.prefix)
        env.set("HEED_DATABASE", self.prefix.share.Heed.database)

        # In order to get Garfield work in python, need to setup both ROOT and GSL
        pyver = self.spec["python"].version.up_to(2)
        site_packages = "python{}/site-packages".format(pyver)
        pypath = join_path(self.prefix.lib, site_packages)
        env.prepend_path("PYTHONPATH", pypath)
        env.prepend_path("LD_LIBRARY_PATH", self.spec["root"].prefix.lib.root)
        env.prepend_path("LD_LIBRARY_PATH", self.spec["gsl"].prefix.lib.root)

    def setup_dependent_build_environment(self, env, dependent_spec):
        env.set("GARFIELD_INSTALL", self.prefix)
        env.set("HEED_DATABASE", self.prefix.share.Heed.database)
