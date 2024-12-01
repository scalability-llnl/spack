# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Tauola(AutotoolsPackage):
    """Tauola is a event generator for tau decays."""

    homepage = "https://tauolapp.web.cern.ch/tauolapp/"
    url = "https://tauolapp.web.cern.ch/tauolapp/resources/TAUOLA.1.1.8/TAUOLA.1.1.8-LHC.tar.gz"

    tags = ["hep"]

    license("GPL-3.0-or-later")

    version("1.1.8", sha256="3f734e8a967682869cca2c1ffebd3e055562613c40853cc81820d8b666805ed5")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant("hepmc", default=True, description="Enable hepmc 2.x support")
    variant("hepmc3", default=False, description="Enable hepmc3 support")
    variant("lhapdf", default=True, description="Enable lhapdf support. Required for TauSpinner.")
    variant(
        "cxxstd",
        default="11",
        values=("11", "14", "17", "20"),
        multi=False,
        description="Use the specified C++ standard when building.",
    )

    maintainers("vvolkl")

    depends_on("hepmc", when="+hepmc")
    depends_on("hepmc3", when="+hepmc3")
    depends_on("lhapdf", when="+lhapdf")

    def flag_handler(self, name, flags):
        if name == "cflags":
            flags.append("-O2")
        elif name == "cxxflags":
            flags.append("-O2")
            flags.append("-std=c++{0}".format(self.spec.variants["cxxstd"].value))
        elif name == "fflags":
            flags.append("-O2")
        return (None, None, flags)

    def configure_args(self):
        args = ["--with-pic"]

        args.extend(self.with_or_without("hepmc", "prefix"))
        args.extend(self.with_or_without("hepmc3", "prefix"))
        # tauola is not able to handle --with-lhapdf=no
        # argument has to be empty - so cannot use with_or_without
        if self.spec.satisfies("+lhapdf"):
            args.append("--with-lhapdf=%s" % self.spec["lhapdf"].prefix)
        else:
            args.append("--with-lhapdf=")
        return args
