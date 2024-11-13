# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Sensei(CMakePackage):
    """SENSEI is a platform for scalable in-situ analysis and visualization.
    Its design motto is "Write once, run everywhere", this means that once
    the application is instrumented with SENSEI it can use existing and
    future analysis backends. Existing backends include: Paraview/Catalyst,
    Visit/Libsim, ADIOS, Python scripts, and so on."""

    homepage = "https://sensei-insitu.org"
    url = "https://github.com/SENSEI-insitu/SENSEI/releases/download/v3.2.1/SENSEI-3.2.1.tar.gz"
    git = "https://github.com/SENSEI-insitu/SENSEI.git"
    maintainers("sshudler", "kwryankrattiger")

    license("BSD-3-Clause-LBNL")

    version("develop", branch="develop")
    version("5.0.0", sha256="3ef948d753d37dfddbbc2c993c823487d4ce40543d35abc008e90c75dfbfa16e")
    version("4.1.0", sha256="e1154240c022069fee454c747d7c60e065d36b4d1dc71852b3cd527c22b531c1")
    version("4.0.0", sha256="fc1538aa1051789dbdefbe18b7f251bc46e7a6ae1db3a940c123552e0318db8b")
    version("3.2.2", sha256="d554b654880e899d97d572f02de87b0202faadaf899420ef871093b5bce320c0")
    version("3.2.1", sha256="7438fb4b148e4d1eb888c619366d0d8639122ecbbf1767e19549d6ca0c8698ca")
    version("3.2.0", sha256="fd1a69134d9f8151d85a7f84a67d6a648aef5580585b39f74a56367cff433c82")
    version("3.1.0", sha256="813075e033904835afa74231a841ab46424d4567157ee7366f3b785357ffc0ea")
    version("3.0.0", sha256="e9b4d7531bbe8848a7fb182f1d2706b397d18e1a580a51f79b4bf6793be195e5")
    version("2.1.1", sha256="7e211b3d9ce8576d33dbb39ea367c971bb8863e1cf53b9c0e13f00b53bd16526")
    version("2.1.0", sha256="3de667523d5a8e5576e29ff9528f7f341fcc799b55c9cd824dc61c7ca1a2a910")
    version("2.0.0", sha256="e985778ebbf0b9a103d11e069e58f8975f98a63dc2861b7cde34ea12a23fee20")
    version("1.1.0", sha256="769e0b5db50be25666c0d13176a7e4f89cbffe19cdc12349437d0efff615b200")
    version("1.0.0", sha256="5b8609352048e048e065a7b99f615a602f84b3329085e40274341488ef1b9522")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant("shared", default=True, description="Enables shared libraries")
    variant("ascent", default=False, description="Build with ParaView-Catalyst support")
    variant("catalyst", default=False, description="Build with ParaView-Catalyst support")
    variant("libsim", default=False, description="Build with VisIt-Libsim support")
    variant("vtkio", default=False, description="Enable adaptors to write to VTK XML format")
    variant("adios2", default=False, description="Enable ADIOS2 adaptors and endpoints")
    variant("hdf5", default=False, description="Enables HDF5 adaptors and endpoints", when="@3:")
    variant(
        "vtkm",
        default=False,
        description="Enable VTKm adaptors and endpoints",
        when="@4: +catalyst",
    )
    variant("python", default=False, description="Enable Python bindings", when="@3:")
    variant(
        "miniapps", default=False, description="Enable the parallel 3D and oscillators miniapps"
    )

    # All SENSEI versions up to 2.1.1 support only Python 2, so in this case
    # Paraview 6 cannot be used since it requires Python 3. Starting from
    # version 3, SENSEI supports Python 3.
    depends_on("paraview+mpi", when="+catalyst")
    depends_on("paraview+hdf5", when="+catalyst+hdf5")
    depends_on("paraview+python", when="+catalyst+python")

    depends_on("paraview@5.5.0:5.5.2", when="@:2.1.1 +catalyst")
    depends_on("paraview@5.6:5.7", when="@3:3.2.1 +catalyst")
    depends_on("paraview@5.7:5.9", when="@3.2.2 +catalyst")
    depends_on("paraview@5.7:5.10", when="@4:4 +catalyst")

    # Visit Dep
    depends_on("visit", when="+libsim")

    # VTK Dep
    depends_on("vtk@8:8", when="@:3 ~catalyst")
    depends_on("vtk+python", when="@:3 ~catalyst+python")
    depends_on("vtk@9:", when="@4: +vtkio ~catalyst")

    # VTK-m
    depends_on("paraview use_vtkm=on", when="+vtkm")

    # ADIOS2
    depends_on("adios2", when="+adios2")

    # Ascent
    depends_on("ascent", when="+ascent")

    # HDF5
    depends_on("hdf5", when="+hdf5")

    depends_on("python@3:", when="+python", type=("build", "run"))
    extends("python", when="+python")
    depends_on("py-numpy", when="+python", type=("build", "run"))
    depends_on("py-mpi4py@:3", when="+python", type=("build", "run"))
    depends_on("swig", when="+python", type="build")
    depends_on("cmake@3.6:", when="@3:", type="build")
    depends_on("pugixml")
    depends_on("mpi")

    depends_on("paraview use_vtkm=off", when="+catalyst+ascent ^ascent+vtkh")
    depends_on("paraview use_vtkm=off", when="+catalyst+ascent ^ascent+fides")

    # Can have either LibSim or Catalyst or Ascent, but not a combination
    conflicts("+libsim", when="+catalyst")
    conflicts("+ascent", when="+libsim")

    # Patches
    # https://github.com/SENSEI-insitu/SENSEI/pull/114
    patch("adios2-remove-deprecated-functions.patch", when="@4:4.1 ^adios2@2.9:")
    patch("libsim-add-missing-symbol-visibility-pr67.patch", when="@4.0.0")
    patch("sensei-find-mpi-component-cxx-pr68.patch", when="@4.0.0")
    patch("sensei-install-external-pugixml-pr69.patch", when="@4.0.0")
    patch("sensei-version-detection-pr75.patch", when="@4.0.0")
    patch(
        "https://patch-diff.githubusercontent.com/raw/SENSEI-insitu/SENSEI/pull/88.patch?full_index=1",
        sha256="6e5a190d4d3275c248b11b9258b79ddf2e5f0dc1b028b23dcdbdc13f9ea46813",
        when="@4.0.0 +python ^swig@4.1:",
    )

    def cmake_args(self):
        spec = self.spec
        prefix = ""
        if spec.satisfies("@5:"):
            prefix = "SENSEI_"

        # -Ox flags are set by default in CMake based on the build type
        args = [
            self.define_from_variant("BUILD_SHARED_LIBS", "shared"),
            self.define("SENSEI_USE_EXTERNAL_pugixml", True),
            self.define(f"{prefix}ENABLE_SENSEI", True),
            self.define("MPI_C_COMPILER", spec["mpi"].mpicc),
            self.define("MPI_CXX_COMPILER", spec["mpi"].mpicxx),
            # Don"t rely on MPI found in cray environment for cray systems.
            # On non-cray systems this should be a no-op
            self.define(f"{prefix}ENABLE_CRAY_MPICH", False),
            self.define_from_variant(f"{prefix}ENABLE_ASCENT", "ascent"),
            self.define_from_variant(f"{prefix}ENABLE_VTKM", "vtkm"),
            self.define_from_variant(f"{prefix}ENABLE_CATALYST", "catalyst"),
            self.define_from_variant(f"{prefix}ENABLE_LIBSIM", "libsim"),
            self.define_from_variant(f"{prefix}ENABLE_VTK_IO", "vtkio"),
            self.define_from_variant(f"{prefix}ENABLE_PYTHON", "python"),
            self.define_from_variant(f"{prefix}ENABLE_ADIOS2", "adios2"),
            self.define_from_variant(f"{prefix}ENABLE_HDF5", "hdf5"),
            self.define_from_variant(f"{prefix}ENABLE_PARALLEL3D", "miniapps"),
            self.define_from_variant(f"{prefix}ENABLE_OSCILLATORS", "miniapps"),
        ]

        if "+adios2" in spec:
            args.append(self.define("ADIOS2_DIR", spec["adios2"].prefix))

        if "+ascent" in spec:
            args.append(self.define("ASCENT_DIR", spec["ascent"].prefix))

        if "+libsim" in spec:
            # This is only for linux
            # Visit install location may be different on other platforms
            args.append("-DVISIT_DIR:PATH={0}/current/linux-x86_64".format(spec["visit"].prefix))

        if "+python" in spec:
            if spec.satisfies("@3:"):
                args.append(self.define("SENSEI_PYTHON_VERSION", 3))
            args.append(self.define_from_variant(f"{prefix}ENABLE_CATALYST_PYTHON", "catalyst"))

        return args
