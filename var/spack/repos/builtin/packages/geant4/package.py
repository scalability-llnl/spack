# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *
from spack.variant import _ConditionalVariantValues


class Geant4(CMakePackage):
    """Geant4 is a toolkit for the simulation of the passage of particles
    through matter. Its areas of application include high energy, nuclear
    and accelerator physics, as well as studies in medical and space
    science."""

    homepage = "http://geant4.cern.ch/"
    url = "https://gitlab.cern.ch/geant4/geant4/-/archive/v10.7.1/geant4-v10.7.1.tar.gz"

    tags = ["hep"]

    executables = ["^geant4-config$"]

    maintainers("drbenmorgan", "sethrj")
    version(
        "11.3.0.beta",
        sha256="572ba1570ca3b5b6f2a28ccbffa459901f6a986b79da1ebfdbf2f6f3dc5e14bf",
        deprecated=True,
    )
    version(
        "11.2.2",
        sha256="3a8d98c63fc52578f6ebf166d7dffaec36256a186d57f2520c39790367700c8d",
        preferred=True,
    )
    version("11.2.1", sha256="76c9093b01128ee2b45a6f4020a1bcb64d2a8141386dea4674b5ae28bcd23293")
    version("11.2.0", sha256="9ff544739b243a24dac8f29a4e7aab4274fc0124fd4e1c4972018213dc6991ee")
    version("11.1.3", sha256="5d9a05d4ccf8b975649eab1d615fc1b8dce5937e01ab9e795bffd04149240db6")
    version("11.1.2", sha256="e9df8ad18c445d9213f028fd9537e174d6badb59d94bab4eeae32f665beb89af")
    version("11.1.1", sha256="c5878634da9ba6765ce35a469b2893044f4a6598aa948733da8436cdbfeef7d2")
    version("11.1.0", sha256="c4a23f2f502efeab56de43a4412b21f65c7ca1b0877b9bc1d7e845ee12edf70a")
    version("11.0.4", sha256="673fb409fd1f54b65b52ddd21596f33ebb210f153730b7887a5dee7fea4d15a2")
    version("11.0.3", sha256="1e6560b802aa84e17255b83987dfc98a1457154fb603d0f340fae978238de3e7")
    version("11.0.2", sha256="661e1ab6f42e58910472d771e76ffd16a2b411398eed70f39808762db707799e")
    version("11.0.1", sha256="fa76d0774346b7347b1fb1424e1c1e0502264a83e185995f3c462372994f84fa")
    version("11.0.0", sha256="04d11d4d9041507e7f86f48eb45c36430f2b6544a74c0ccaff632ac51d9644f1")
    version("10.7.4", sha256="7e381f8945c75388b79af98b95be31a0933641c1af8d74ab9b6cf39d5aa98317")
    version("10.7.3", sha256="8615d93bd4178d34f31e19d67bc81720af67cdab1c8425af8523858dcddcf65b")
    version("10.7.2", sha256="593fc85883a361487b17548ba00553501f66a811b0a79039276bb75ad59528cf")
    version("10.7.1", sha256="2aa7cb4b231081e0a35d84c707be8f35e4edc4e97aad2b233943515476955293")
    version("10.7.0", sha256="c991a139210c7f194720c900b149405090058c00beb5a0d2fac5c40c42a262d4")
    version("10.6.3", sha256="bf96d6d38e6a0deabb6fb6232eb00e46153134da645715d636b9b7b4490193d3")
    version("10.6.2", sha256="e381e04c02aeade1ed8cdd9fdbe7dcf5d6f0f9b3837a417976b839318a005dbd")
    version("10.6.1", sha256="4fd64149ae26952672a81ce5579d3806fda4bd251d486897093ac57633a42b7e")
    version("10.6.0", sha256="eebe6a170546064ff81ab3b00f513ccd1d4122a026514982368d503ac55a4ee4")
    version("10.5.1", sha256="2397eb859dc4de095ff66059d8bda9f060fdc42e10469dd7890946293eeb0e39")
    version("10.4.3", sha256="67f3bb6405a2c77e573936c2b933f5a4a33915aa379626a2eb3012009b91e1da")
    version("10.4.0", sha256="e919b9b0a88476e00c0b18ab65d40e6a714b55ee4778f66bac32a5396c22aa74")
    version("10.3.3", sha256="bcd36a453da44de9368d1d61b0144031a58e4b43a6d2d875e19085f2700a89d8")
    version("10.0.4", sha256="97f3744366b00143d1eed52f8786823034bbe523f45998106f798af61d83f863")

    depends_on("cxx", type="build")

    _cxxstd_values = (
        conditional("11", "14", when="@:10"),
        conditional("17", when="@10.4.1:"),
        conditional("20", when="@10.7.0:"),
    )
    variant(
        "cxxstd",
        default="11",
        values=_cxxstd_values,
        multi=False,
        description="Use the specified C++ standard when building.",
    )

    variant("threads", default=True, description="Build with multithreading")
    variant("vecgeom", default=False, description="Enable vecgeom support", when="@10.4:")
    variant("opengl", default=False, description="Optional OpenGL support")
    variant("x11", default=False, description="Optional X11 support")
    variant("motif", default=False, description="Optional motif support")
    variant("qt", default=False, description="Enable Qt support")
    variant("hdf5", default=False, description="Enable HDF5 support", when="@10.4:")
    variant("python", default=False, description="Enable Python bindings", when="@10.6.2:11.0")
    variant("tbb", default=False, description="Use TBB as a tasking backend", when="@11:")
    variant("timemory", default=False, description="Use TiMemory for profiling", when="@9.5:")
    variant("vtk", default=False, description="Enable VTK support", when="@11:")

    depends_on("cmake@3.16:", type="build", when="@11.0.0:")
    depends_on("cmake@3.8:", type="build", when="@10.6.0:")
    depends_on("cmake@3.5:", type="build")

    for _vers in [
        "10.0.4",
        "10.3.3",
        "10.4.0",
        "10.4.3",
        "10.5.1",
        "10.6.0",
        "10.6.1",
        "10.6.2",
        "10.6.3",
        "10.7.0",
        "10.7.1",
        "10.7.2",
        "10.7.3",
        "10.7.4",
        "11.0",
        "11.1",
        "11.2.0:11.2.1",
        "11.2.2:11.2",
        "11.3:",
    ]:
        depends_on("geant4-data@" + _vers, type="run", when="@" + _vers)

    depends_on("expat")
    depends_on("zlib-api")

    depends_on("tbb", when="+tbb")
    depends_on("timemory@3.2:", when="+timemory")
    depends_on("vtk@8.2:", when="+vtk")

    # Python, with boost requirement dealt with in cxxstd section
    depends_on("python@3:", when="+python")
    extends("python", when="+python")

    # CLHEP version requirements to be reviewed
    depends_on("clhep@2.4.7.1:", when="@11.3:")
    depends_on("clhep@2.4.6.0:", when="@11.1:")
    depends_on("clhep@2.4.5.1:", when="@11.0.0:")
    depends_on("clhep@2.4.4.0:", when="@10.7.0:")
    depends_on("clhep@2.3.3.0:", when="@10.3:10.6")
    depends_on("clhep@2.1.2.3", when="@:10.2")

    # Vecgeom specific versions for each Geant4 version
    with when("+vecgeom"):
        depends_on("vecgeom@1.2.8:", when="@11.3:")
        depends_on("vecgeom@1.2.6:", when="@11.2:")
        depends_on("vecgeom@1.2.0:", when="@11.1")
        depends_on("vecgeom@1.1.18:1.1", when="@11.0.0:11.0")
        depends_on("vecgeom@1.1.8:1.1", when="@10.7.0:10.7")
        depends_on("vecgeom@1.1.5", when="@10.6.0:10.6")
        depends_on("vecgeom@1.1.0", when="@10.5.0:10.5")
        depends_on("vecgeom@0.5.2", when="@10.4.0:10.4")

    with when("+hdf5"):
        depends_on("hdf5 +threadsafe")

    def std_when(values):
        for v in values:
            if isinstance(v, _ConditionalVariantValues):
                for c in v:
                    yield (c.value, c.when)
            else:
                yield (v, "")

    for _std, _when in std_when(_cxxstd_values):
        depends_on(f"clhep cxxstd={_std}", when=f"{_when} cxxstd={_std}")
        depends_on(f"vecgeom cxxstd={_std}", when=f"{_when} +vecgeom cxxstd={_std}")

        # Spack only supports Xerces-c 3 and above, so no version req
        depends_on(f"xerces-c netaccessor=curl cxxstd={_std}", when=f"{_when} cxxstd={_std}")

        # Boost.python, conflict handled earlier
        depends_on(f"boost@1.70: +python cxxstd={_std}", when=f"{_when} +python cxxstd={_std}")

    # Visualization driver dependencies
    depends_on("gl", when="+opengl")
    depends_on("glu", when="+opengl")
    depends_on("glx", when="+opengl+x11")
    depends_on("libx11", when="+x11")
    depends_on("libxmu", when="+x11")
    depends_on("motif", when="+motif")
    with when("+qt"):
        depends_on("qmake")
        with when("^[virtuals=qmake] qt-base"):
            depends_on("qt-base +accessibility +gui +opengl")
        with when("^[virtuals=qmake] qt"):
            depends_on("qt@5: +opengl")
            depends_on("qt@5.9:", when="@11.2:")
    conflicts("@:11.1 ^[virtuals=qmake] qt-base", msg="Qt6 not supported before 11.2")

    # As released, 10.0.4 has inconsistently capitalised filenames
    # in the cmake files; this patch also enables cxxstd 14
    patch("geant4-10.0.4.patch", when="@10.0.4")
    # As released, 10.03.03 has issues with respect to using external
    # CLHEP.
    patch("CLHEP-10.03.03.patch", level=1, when="@10.3")
    # Build failure on clang 15, ubuntu 22: see Geant4 problem report #2444
    # fixed by ascii-V10-07-03
    patch("geant4-10.6.patch", level=1, when="@10.0:10.6")
    # These patches can be applied independent of the cxxstd value?
    patch("cxx17.patch", when="@10.3 cxxstd=17")
    patch("cxx17_geant4_10_0.patch", level=1, when="@10.4.0 cxxstd=17")
    patch("geant4-10.4.3-cxx17-removed-features.patch", level=1, when="@10.4.3 cxxstd=17")

    # See https://bugzilla-geant4.kek.jp/show_bug.cgi?id=2556
    patch("package-cache.patch", level=1, when="@10.7.0:11.1.2^cmake@3.17:")

    # Issue with Twisted tubes, see https://bugzilla-geant4.kek.jp/show_bug.cgi?id=2619
    patch("twisted-tubes.patch", level=1, when="@11.2.0:11.2.2")

    # NVHPC: "thread-local declaration follows non-thread-local declaration"
    conflicts("%nvhpc", when="+threads")

    @classmethod
    def determine_version(cls, exe):
        output = Executable(exe)("--version", output=str, error=str)
        # We already get the correct format
        return output.strip()

    @classmethod
    def determine_variants(cls, exes, version_str):
        variants = []
        cxxstd = Executable(exes[0])("--cxxstd", output=str, error=str)
        # output will be something like c++17, we only want the number
        variants.append("cxxstd={}".format(cxxstd[-3:]))

        def _has_feature(feature):
            res = Executable(exes[0])("--has-feature", feature, output=str, error=str)
            return res.strip() == "yes"

        def _add_variant(feature, variant):
            """Helper to determine whether a given feature is present and append the
            corresponding variant to the list"""
            if _has_feature(feature):
                variants.append("+{}".format(variant))
            else:
                variants.append("~{}".format(variant))

        _add_variant("qt", "qt")
        _add_variant("motif", "motif")
        _add_variant("multithreading", "threads")
        _add_variant("usolids", "vecgeom")

        if _has_feature("opengl-x11"):
            variants.append("+opengl")
            variants.append("+x11")
        else:
            variants.append("~opengl")
            # raytracer-x11 could still lead to the activation of the x11
            # variant without +opengl
            _add_variant("raytracer-x11", "x11")

        # TODO: The following variants cannot be determined from geant4-config.
        # - python
        # - tbb
        # - vtk
        # Should we have a (version dependent) warning message for these?

        return " ".join(variants)

    def flag_handler(self, name, flags):
        spec = self.spec
        if name == "cxxflags":
            if spec.satisfies("%nvhpc"):
                # error: excessive recursion at instantiation of class
                # "G4Number<191>" (G4CTCounter.hh)
                flags.append("-Wc,--pending_instantiations=256")
                return (None, flags, None)
        return (flags, None, None)

    def cmake_args(self):
        spec = self.spec

        # Core options
        options = [
            self.define("GEANT4_USE_SYSTEM_CLHEP", True),
            self.define("GEANT4_USE_SYSTEM_EXPAT", True),
            self.define("GEANT4_USE_SYSTEM_ZLIB", True),
            self.define("GEANT4_USE_G3TOG4", True),
            self.define("GEANT4_USE_GDML", True),
            self.define("XERCESC_ROOT_DIR", spec["xerces-c"].prefix),
        ]

        # Use the correct C++ standard option for the requested version
        if spec.version >= Version("11.0"):
            options.append(self.define_from_variant("CMAKE_CXX_STANDARD", "cxxstd"))
        elif spec.version >= Version("10.3"):
            options.append(self.define_from_variant("GEANT4_BUILD_CXXSTD", "cxxstd"))
        else:
            cxxstd = spec.variants["cxxstd"].value
            options.append(self.define("GEANT4_BUILD_CXXSTD", f"c++{cxxstd}"))

        if spec.version >= Version("10.6"):
            # When building a downstream library/app outside of Spack, make
            # sure that Geant4's dependencies are found
            options.append(self.define("GEANT4_INSTALL_PACKAGE_CACHE", True))

        # Multithreading
        options.append(self.define_from_variant("GEANT4_BUILD_MULTITHREADED", "threads"))
        options.append(self.define_from_variant("GEANT4_USE_TBB", "tbb"))

        if spec.satisfies("+threads"):
            # Locked at global-dynamic to allow use cases that load the
            # geant4 libs at application runtime
            options.append(self.define("GEANT4_BUILD_TLS_MODEL", "global-dynamic"))

        # Profiling
        options.append(self.define_from_variant("GEANT4_USE_TIMEMORY", "timemory"))

        # Never install the data with geant4, but point to the dependent
        # geant4-data's install directory to correctly set up the
        # Geant4Config.cmake values for Geant4_DATASETS .
        options.append(self.define("GEANT4_INSTALL_DATA", False))
        options.append(self.define("GEANT4_INSTALL_DATADIR", self.datadir))

        # Vecgeom
        if spec.satisfies("+vecgeom"):
            options.append(self.define("GEANT4_USE_USOLIDS", True))
            options.append(self.define("USolids_DIR", spec["vecgeom"].prefix.lib.CMake.USolids))

        # Visualization options
        if "platform=darwin" not in spec:
            if spec.satisfies("+x11 +opengl"):
                options.append(self.define("GEANT4_USE_OPENGL_X11", True))
            if spec.satisfies("+motif +opengl"):
                options.append(self.define("GEANT4_USE_XM", True))
            if spec.satisfies("+x11"):
                options.append(self.define("GEANT4_USE_RAYTRACER_X11", True))

        if spec.satisfies("+qt"):
            options.append(self.define("GEANT4_USE_QT", True))
            if spec.satisfies("^[virtuals=qmake] qt-base"):
                options.append(self.define("GEANT4_USE_QT_QT6", True))
            options.append(self.define("QT_QMAKE_EXECUTABLE", spec["qmake"].prefix.bin.qmake))

        options.append(self.define_from_variant("GEANT4_USE_HDF5", "hdf5"))

        options.append(self.define_from_variant("GEANT4_USE_VTK", "vtk"))

        # Python
        if spec.version > Version("10.6.1"):
            options.append(self.define_from_variant("GEANT4_USE_PYTHON", "python"))

        return options

    @property
    def datadir(self):
        dataspec = self.spec["geant4-data"]
        return join_path(
            dataspec.prefix.share, "{0}-{1}".format(dataspec.name, dataspec.version.dotted)
        )
