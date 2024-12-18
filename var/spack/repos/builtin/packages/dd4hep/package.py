# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Dd4hep(CMakePackage):
    """DD4hep is a software framework for providing a complete solution for
    full detector description (geometry, materials, visualization, readout,
    alignment, calibration, etc.) for the full experiment life cycle
    (detector concept development, detector optimization, construction,
    operation). It offers a consistent description through a single source
    of detector information for simulation, reconstruction, analysis, etc.
    It distributed under the LGPLv3 License."""

    homepage = "https://dd4hep.web.cern.ch/dd4hep/"
    url = "https://github.com/AIDASoft/DD4hep/archive/v01-12-01.tar.gz"
    git = "https://github.com/AIDASoft/DD4hep.git"

    maintainers("vvolkl", "drbenmorgan", "jmcarcell")

    tags = ["hep"]

    license("LGPL-3.0-or-later")

    version("master", branch="master")
    version("1.30", sha256="02de46151e945eff58cffd84b4b86d35051f4436608199c3efb4d2e1183889fe")
    version("1.29", sha256="435d25a7ef093d8bf660f288b5a89b98556b4c1c293c55b93bf641fb4cba77e9")
    version("1.28", sha256="b28d671eda0154073873a044a384486e66f1f200065deca99537aa84f07328ad")
    version("1.27.2", sha256="09d8acd743d010274562b856d39e2a88aeaf89cf287a4148f52223b0cd960ab2")
    version("1.27.1", sha256="e66ae726c0a9a55e5603024a7f8a48ffbc5613ea36e5f892e9a90d87833f92e0")
    version("1.27", sha256="51fbd0f91f2511261d9b01e4b3528c658bea1ea1b5d67b25b6812615e782a902")
    version("1.26", sha256="de2cc8d8e99217e23fdf0a55b879d3fd3a864690d6660e7808f1ff99eb47f384")
    version("1.25.1", sha256="6267e76c74fbb346aa881bc44de84434ebe788573f2997a189996252fc5b271b")
    version("1.25", sha256="102a049166a95c2f24fc1c03395a819fc4501c175bf7915d69ccc660468d094d")
    version("1.24", sha256="361a932b9af2479458c0759281fef0161439d8bd119da426ce462a0467adc679")
    version("1.23", sha256="64e4f213e500147e4067301b03143b872381e2ae33710cb6eea8c578529dd596")
    version("1.22", sha256="0e729b8897b7a9c348bc3304c63d4efd1a88e032a2ff5a8c4daf6c927fd7f8ee")
    version("1.21", sha256="0f9fe9784bf28fa20ce5555ff074430da430e9becc2566fe11e27c4904a51c94")
    version("1.20.2", sha256="3dab7a300f749452791e160db9394180b65533e91b1b628e568da72ca79b211a")
    version("1.20.1", sha256="18c18a125583c39cb808c602e052cc2379aa3a8029aa78dbb40bcc31f1deb798")
    version("1.20", sha256="cf6af0c486d5c84e8c8a8e40ea16cec54d4ed78bffcef295a0eeeaedf51cab59")
    version("1.19", sha256="d2eccf5e8402ba7dab2e1d7236e12ee4db9b1c5e4253c40a140bf35580db1d9b")
    version("1.18", sha256="1e909a42b969dfd966224fa8ab1eca5aa05136baf3c00a140f2f6d812b497152")
    version("1.17", sha256="036a9908aaf1e13eaf5f2f43b6f5f4a8bdda8183ddc5befa77a4448dbb485826")
    version("1.16.1", sha256="c8b1312aa88283986f89cc008d317b3476027fd146fdb586f9f1fbbb47763f1a")

    depends_on("cxx", type="build")  # generated

    generator("ninja")

    # Workaround for failing build file generation in some cases
    # See https://github.com/spack/spack/issues/24232
    patch("cmake_language.patch", when="@:1.17")
    # Fix missing SimCaloHits when using the LCIO format
    patch(
        "https://patch-diff.githubusercontent.com/raw/AIDASoft/DD4hep/pull/1019.patch?full_index=1",
        when="@1.19:1.23",
        sha256="6466719c82de830ce728db57004fb7db03983587a63b804f6dc95c6b92b3fc76",
    )

    # variants for subpackages
    variant("ddcad", default=True, description="Enable CAD interface based on Assimp")
    variant("ddg4", default=True, description="Enable the simulation part based on Geant4")
    variant("ddrec", default=True, description="Build DDRec subpackage.")
    variant("dddetectors", default=True, description="Build DDDetectors subpackage.")
    variant("ddcond", default=True, description="Build DDCond subpackage.")
    variant("ddalign", default=True, description="Build DDAlign subpackage.")
    variant("dddigi", default=True, description="Build DDDigi subpackage.")
    variant("ddeve", default=True, description="Build DDEve subpackage.")
    variant("utilityapps", default=True, description="Build UtilityApps subpackage.")

    # variants for other build options
    variant("xercesc", default=False, description="Enable 'Detector Builders' based on XercesC")
    variant("hepmc3", default=False, description="Enable build with hepmc3")
    variant(
        "hepmc3-gz",
        default=False,
        description="Enable build with compressed hepmc3",
        when="@1.26: +hepmc3",
    )
    variant("lcio", default=False, description="Enable build with lcio")
    variant("edm4hep", default=True, description="Enable build with edm4hep")
    variant("geant4units", default=False, description="Use geant4 units throughout")
    variant("tbb", default=False, description="Enable build with tbb")
    variant(
        "debug",
        default=False,
        description="Enable debug build flag - adds extra info in"
        " some places in addtion to the debug build type",
    )

    depends_on("cmake @3.12:", type="build")
    depends_on("cmake @3.14:", type="build", when="@1.26:")
    depends_on("boost @1.49:")
    depends_on("boost +iostreams", when="+ddg4")
    depends_on("boost +system +filesystem", when="%gcc@:7")
    depends_on("root @6.08: +gdml +math +python")
    depends_on("root @6.12.2: +root7", when="@1.26:")  # DDCoreGraphics needs ROOT::ROOTHistDraw
    with when("+ddeve"):
        depends_on("root @6.08: +x +opengl")
        depends_on("root @:6.27", when="@:1.23")
        conflicts("^root ~webgui", when="^root@6.28:")
        # For DD4hep >= 1.24, DDEve_Interface needs ROOT::ROOTGeomViewer only if ROOT >= 6.27
        requires("^root +root7 +webgui", when="@1.24: ^root @6.27:")
    depends_on("root @6.08: +gdml +math +python +x +opengl", when="+utilityapps")

    extends("python")
    depends_on("xerces-c", when="+xercesc")
    depends_on("geant4@10.2.2:", when="+ddg4")
    depends_on("assimp@5.0.2:", when="+ddcad")
    depends_on("hepmc3", when="+hepmc3")
    depends_on("hepmc3@3.2.6:", when="+hepmc3-gz")
    depends_on("bzip2", when="+hepmc3-gz")
    depends_on("xz", when="+hepmc3-gz")
    depends_on("zlib-api", when="+hepmc3-gz")
    depends_on("tbb", when="+tbb")
    depends_on("intel-tbb@:2020.3", when="+tbb @:1.23")
    depends_on("lcio", when="+lcio")
    depends_on("edm4hep", when="+edm4hep")
    depends_on("podio", when="+edm4hep")
    depends_on("podio@:0.16.03", when="@:1.23 +edm4hep")
    depends_on("podio@0.16:", when="@1.24: +edm4hep")
    depends_on("podio@0.16.3:", when="@1.26: +edm4hep")
    depends_on("podio@:0", when="@:1.29 +edm4hep")
    depends_on("py-pytest", type=("build", "test"))

    # See https://github.com/AIDASoft/DD4hep/pull/771 and https://github.com/AIDASoft/DD4hep/pull/876
    conflicts(
        "^cmake@3.16:3.17.2",
        when="@:1.18",
        msg="cmake version with buggy FindPython breaks dd4hep cmake config",
    )
    conflicts("~ddrec+dddetectors", msg="Need to enable +ddrec to build +dddetectors.")

    # Geant4 needs to be (at least) the same version as DD4hep, but we don't
    # have a very good handle on that at this stage, because we make that
    # dependent on roots cxxstd. However, cxxstd=11 will never work
    # See https://github.com/AIDASoft/DD4hep/pull/1191
    conflicts("^geant4 cxxstd=11", when="+ddg4")

    # See https://github.com/AIDASoft/DD4hep/issues/1210
    conflicts("^root@6.31.1:", when="@:1.27")

    @property
    def libs(self):
        # We need to override libs here, because we don't build a libdd4hep so
        # the default discovery fails. All libraries that are built by DD4hep
        # start with libDD
        return find_libraries("libDD*", root=self.prefix, shared=True, recursive=True)

    def cmake_args(self):
        spec = self.spec
        cxxstd = spec["root"].variants["cxxstd"].value
        # root can be built with cxxstd=11, but dd4hep requires 14
        if cxxstd == "11":
            cxxstd = "14"
        args = [
            self.define_from_variant("DD4HEP_USE_EDM4HEP", "edm4hep"),
            self.define_from_variant("DD4HEP_USE_XERCESC", "xercesc"),
            self.define_from_variant("DD4HEP_USE_TBB", "tbb"),
            self.define_from_variant("DD4HEP_USE_GEANT4", "ddg4"),
            self.define_from_variant("DD4HEP_USE_LCIO", "lcio"),
            self.define_from_variant("DD4HEP_USE_HEPMC3", "hepmc3"),
            self.define_from_variant("DD4HEP_USE_GEANT4_UNITS", "geant4units"),
            self.define_from_variant("DD4HEP_BUILD_DEBUG", "debug"),
            # DD4hep@1.26: with hepmc3@3.2.6: allows compressed hepmc3 files
            self.define(
                "DD4HEP_HEPMC3_COMPRESSION_SUPPORT", self.spec.satisfies("@1.26: ^hepmc3@3.2.6:")
            ),
            # Downloads assimp from github and builds it on the fly.
            # However, with spack it is preferrable to have a proper external
            # dependency, so we disable it.
            self.define("DD4HEP_LOAD_ASSIMP", False),
            "-DCMAKE_CXX_STANDARD={0}".format(cxxstd),
            "-DBUILD_TESTING={0}".format(self.run_tests),
            "-DBOOST_ROOT={0}".format(spec["boost"].prefix),
            "-DBoost_NO_BOOST_CMAKE=ON",
        ]
        subpackages = []
        if spec.satisfies("+ddg4"):
            subpackages += ["DDG4"]
        if spec.satisfies("+ddcond"):
            subpackages += ["DDCond"]
        if spec.satisfies("+ddcad"):
            subpackages += ["DDCAD"]
        if spec.satisfies("+ddrec"):
            subpackages += ["DDRec"]
        if spec.satisfies("+dddetectors"):
            subpackages += ["DDDetectors"]
        if spec.satisfies("+ddalign"):
            subpackages += ["DDAlign"]
        if spec.satisfies("+dddigi"):
            subpackages += ["DDDigi"]
        if spec.satisfies("+ddeve"):
            subpackages += ["DDEve"]
        if spec.satisfies("+utilityapps"):
            subpackages += ["UtilityApps"]
        subpackages = " ".join(subpackages)
        args += [self.define("DD4HEP_BUILD_PACKAGES", subpackages)]
        return args

    def setup_run_environment(self, env):
        # used p.ex. in ddsim to find DDDetectors dir
        env.set("DD4hepINSTALL", self.prefix)
        env.set("DD4HEP", self.prefix.examples)
        env.set("DD4hep_DIR", self.prefix)
        env.set("DD4hep_ROOT", self.prefix)
        if len(self.libs.directories) > 0:
            env.prepend_path("LD_LIBRARY_PATH", self.libs.directories[0])

    def url_for_version(self, version):
        # dd4hep releases are dashes and padded with a leading zero
        # the patch version is omitted when 0
        # so for example v01-12-01, v01-12 ...
        base_url = self.url.rsplit("/", 1)[0]
        if len(version) == 1:
            major = version[0]
            minor, patch = 0, 0
        elif len(version) == 2:
            major, minor = version
            patch = 0
        else:
            major, minor, patch = version
        # By now the data is normalized enough to handle it easily depending
        # on the value of the patch version
        if patch == 0:
            version_str = "v%02d-%02d.tar.gz" % (major, minor)
        else:
            version_str = "v%02d-%02d-%02d.tar.gz" % (major, minor, patch)

        return base_url + "/" + version_str

    # dd4hep tests need to run after install step:
    # disable the usual check
    def check(self):
        pass

    # instead add custom check step that runs after installation
    @run_after("install")
    def build_test(self):
        with working_dir(self.build_directory):
            if self.run_tests:
                ninja("test")
