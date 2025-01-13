# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Celeritas(CMakePackage, CudaPackage, ROCmPackage):
    """Celeritas is a new Monte Carlo transport code designed for
    high-performance (GPU-targeted) simulation of high-energy physics
    detectors.
    """

    homepage = "https://github.com/celeritas-project/celeritas"
    url = "https://github.com/celeritas-project/celeritas/releases/download/v0.1.0/celeritas-0.1.0.tar.gz"

    maintainers("sethrj")

    license("Apache-2.0")

    version("0.5.0", sha256="4a8834224d96fd01897e5872ac109f60d91ef0bd7b63fac05a73dcdb61a5530e")
    version(
        "0.4.4",
        sha256="8b5ae63aa2d50c2ecf48d752424e4a33c50c07d9f0f5ca5448246de3286fd836",
        deprecated=True,
    )
    version(
        "0.4.3",
        sha256="b4f603dce1dc9c4894ea4c86f6574026ea8536714982e7dc6dff7472c925c892",
        deprecated=True,
    )
    version(
        "0.4.2",
        sha256="eeca9705413f5e16e0fb81154e042600c8df125af7049912757feb01d43730e2",
        deprecated=True,
    )
    version(
        "0.4.1",
        sha256="24e5c15eb9eec45f52d94a6719ae3505388b49d409cb7e26c875c70ac409bd2c",
        deprecated=True,
    )
    version(
        "0.4.0",
        sha256="8b8eaef84641eeca0fc40321d358205fc9d51e3c6dc7bd1bf03218c1919c774e",
        deprecated=True,
    )

    depends_on("cxx", type="build")

    _cxxstd_values = ("17", "20")

    # Note: cuda and rocm variants are defined by mixin classes
    variant(
        "cxxstd",
        default="17",
        values=_cxxstd_values,
        multi=False,
        description="C++ standard version",
    )
    variant("debug", default=False, description="Enable runtime debug assertions")
    variant("doc", default=False, description="Build and install documentation")
    variant("geant4", default=True, description="Enable Geant4 integration")
    variant("hepmc3", default=True, description="Use HepMC3 I/O interfaces")
    variant("openmp", default=False, description="Use OpenMP multithreading")
    variant("root", default=False, description="Use ROOT I/O")
    variant("shared", default=True, description="Build shared libraries")
    variant("swig", default=False, when="@:0.4", description="Generate SWIG Python bindings")
    variant("vecgeom", default=True, description="Use VecGeom geometry")

    depends_on("cmake@3.13:", type="build")
    depends_on("cmake@3.18:", type="build", when="+cuda+vecgeom")
    depends_on("cmake@3.22:", type="build", when="+rocm")

    depends_on("nlohmann-json")
    depends_on("geant4@10.5:", when="@0.4.2: +geant4")
    depends_on("geant4@10.5:11.1", when="@0.3.1:0.4.1 +geant4")
    depends_on("hepmc3", when="+hepmc3")
    depends_on("root", when="+root")
    depends_on("swig@4.1:", when="+swig")
    depends_on("vecgeom@1.2.5:", when="+vecgeom")

    depends_on("python", type="build")
    depends_on("doxygen", type="build", when="+doc")
    depends_on("py-breathe", type="build", when="+doc")
    depends_on("py-sphinx", type="build", when="+doc")

    for _std in _cxxstd_values:
        depends_on("geant4 cxxstd=" + _std, when="+geant4 cxxstd=" + _std)
        depends_on("root cxxstd=" + _std, when="+root cxxstd=" + _std)
        depends_on("vecgeom cxxstd=" + _std, when="+vecgeom cxxstd=" + _std)

    for _arch in CudaPackage.cuda_arch_values:
        depends_on("vecgeom+cuda cuda_arch=" + _arch, when="+vecgeom +cuda cuda_arch=" + _arch)

    conflicts("+rocm", when="+cuda", msg="AMD and NVIDIA accelerators are incompatible")
    conflicts("+rocm", when="+vecgeom", msg="HIP support is only available with ORANGE")

    # geant4@11.3.0 now returns const G4Element::GetElementTable()
    patch(
        "https://github.com/celeritas-project/celeritas/commit/3c8ed9614fc695fba35e8a058bedb7bc1556f71c.patch?full_index=1",
        sha256="1161c4f1166860d35d2a3f103236a63acd6a35aee2d2c27561cb929941d1c170",
        when="@0.5.0 +geant4 ^geant4@11.3.0:",
    )
    conflicts(
        "^geant4@11.3.0:", when="@:0.4 +geant4", msg="geant4@11.3.0: requires at least 0.5.0"
    )

    def cmake_args(self):
        define = self.define
        from_variant = self.define_from_variant
        args = [
            from_variant("BUILD_SHARED_LIBS", "shared"),
            from_variant("CELERITAS_DEBUG", "debug"),
            from_variant("CELERITAS_BUILD_DOCS", "doc"),
            define("CELERITAS_BUILD_DEMOS", False),
            define("CELERITAS_BUILD_TESTS", False),
            from_variant("Celeritas_USE_HIP", "rocm"),
            define("CELERITAS_USE_MPI", False),
            define("CELERITAS_USE_JSON", True),
            define("CELERITAS_USE_Python", True),
        ]

        for pkg in ["CUDA", "Geant4", "HepMC3", "OpenMP", "ROOT", "SWIG", "VecGeom"]:
            args.append(from_variant("CELERITAS_USE_" + pkg, pkg.lower()))

        return args
