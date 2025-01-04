# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Geomodel(CMakePackage):
    """GeoModel is a user-friendly C++ Toolkit and Suite for
    HEP Detector Description with minimal dependencies."""

    homepage = "https://gitlab.cern.ch/GeoModelDev/GeoModel"
    url = "https://gitlab.cern.ch/GeoModelDev/GeoModel/-/archive/4.6.0/GeoModel-4.6.0.tar.bz2"
    git = "https://gitlab.cern.ch/GeoModelDev/GeoModel"

    maintainers("wdconinc", "stephenswat")

    license("Apache-2.0", checked_by="wdconinc")

    version("6.7.0", sha256="bfa69062ba191d0844d7099b28c0d6c3c0f87e726dacfaa21dba7a6f593d34bf")
    version("6.6.0", sha256="3cefeaa409177d45d3fa63e069b6496ca062991b0d7d71275b1748487659e91b")
    version("6.5.0", sha256="8a2f71493e54ea4d393f4c0075f3ca13df132f172c891825f3ab949cda052c5f")
    version("6.4.0", sha256="369f91f021be83d294ba6a9bdbe00077625e9fe798a396aceece8970e7dd5838")
    version("6.3.0", sha256="d2b101e06d20a8a3b638e6021f517a939f49ea6d8347ce40c927c27efe66b28c")
    version("6.2.0", sha256="99bb3908bf710ce5ba0bcdd192942705a183a9f2886079df091dc69423b7bdf1")
    version("6.1.0", sha256="2974f0e35e07cd44170d29ef106ec1ee50cb3fa3ba88382bea7394eb341dcd32")
    version("6.0.0", sha256="7263d44ae2b99da9bc45cf0bbda64b2d8bdce1b350328fe41fce001d5266c3a1")
    version("5.6.0", sha256="51e6570e119c2d3037b594779bb78d78b524c41132fac38d83ae162b5b6ffe54")
    version("5.4.0", sha256="82cd08bea5791d862244211f8367cd6f5698b311e4862b2eb5584f835d551821")
    version("5.3.0", sha256="d30c31f387716415542f3424a7f64ab62ef640a4e6f832243944918f7daca080")
    version("5.1.0", sha256="bbe7d6ea46fe750d9421fb741b2340d16afcddbf5d6aeafab09d60577d55f93d")
    version("4.6.0", sha256="d827dc79a5555fd7b09d1b670fc6f01f91476d0edf98ccd644c624f18fb729ca")

    depends_on("cxx", type="build")  # generated

    variant(
        "visualization", default=False, description="Enable the build of GeoModelVisualization"
    )
    variant("geomodelg4", default=False, description="Enable the build of GeoModelG4")
    variant("fullsimlight", default=False, description="Enable the build of FullSimLight")
    variant("fsl", default=False, description="Enable the build of FSL and FullSimLight")
    variant("examples", default=False, description="Enable the build of GeoModelExamples")
    variant("tools", default=False, description="Enable the build of GeoModelTools")
    variant(
        "hepmc3",
        default=False,
        description="Build GeoModel tools with support for the HepMC3 exchange format",
        when="+fullsimlight",
    )
    variant(
        "pythia",
        default=False,
        description="Build GeoModel tools with support for the Pythia event generator",
        when="+fullsimlight",
    )

    variant(
        "cxxstd",
        default="17",
        values=("17", "20", "23"),
        multi=False,
        description="Use the specified C++ standard when building",
    )

    conflicts("+fullsimlight", when="+fsl", msg="FSL triggers the build of the FullSimLight")

    depends_on("cmake@3.16:", type="build")

    depends_on("eigen@3.2.9:")
    depends_on("nlohmann-json@3.6.1:")
    depends_on("sqlite@3.7.17:")
    depends_on("xerces-c@3.2.3:")

    depends_on("geant4", when="+geomodelg4")
    depends_on("geant4", when="+fullsimlight")
    depends_on("hdf5+cxx", when="+fullsimlight")
    depends_on("hepmc3", when="+hepmc3")
    depends_on("pythia8", when="+pythia")
    with when("+visualization"):
        depends_on("hdf5+cxx")
        depends_on("qt +gui +opengl +sql")
        depends_on("coin3d")
        depends_on("soqt")
        depends_on("opengl")

    def cmake_args(self):
        args = [
            self.define_from_variant("GEOMODEL_BUILD_VISUALIZATION", "visualization"),
            self.define_from_variant("GEOMODEL_BUILD_GEOMODELG4", "geomodelg4"),
            self.define_from_variant("GEOMODEL_BUILD_FULLSIMLIGHT", "fullsimlight"),
            self.define_from_variant("GEOMODEL_BUILD_FSL", "fsl"),
            self.define_from_variant("GEOMODEL_BUILD_EXAMPLES", "examples"),
            self.define_from_variant("GEOMODEL_BUILD_TOOLS", "tools"),
            self.define_from_variant("CMAKE_CXX_STANDARD", "cxxstd"),
        ]
        return args
