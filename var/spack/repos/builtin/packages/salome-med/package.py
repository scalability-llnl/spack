# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
#
# Important feature: to interoperate goodly MED files, it is imperative to fix
# the HDF5 version for a salome-med version

from spack.package import *


class SalomeMed(CMakePackage):
    """salome-med is the MED file format that is the SALOME platform standard
    file for meshes and fields and salome-med is based on HDF5 library."""

    maintainers("franciskloss")

    homepage = "https://docs.salome-platform.org/latest/dev/MEDCoupling/developer/med-file.html"
    url = "ftp://ftp.cea.fr/pub/salome/prerequisites/med-4.1.0.tar.gz"

    license("LGPL-3.0-only")

    version(
        "5.0.0",
        sha256="267e76d0c67ec51c10e3199484ec1508baa8d5ed845c628adf660529dce7a3d4",
        url="ftp://ftp.cea.fr/pub/salome/prerequisites/med-5.0.0.tar.bz2",
    )
    version("4.1.1", sha256="a082b705d1aafe95d3a231d12c57f0b71df554c253e190acca8d26fc775fb1e6")
    version("4.1.0", sha256="847db5d6fbc9ce6924cb4aea86362812c9a5ef6b9684377e4dd6879627651fce")
    version("4.0.0", sha256="a474e90b5882ce69c5e9f66f6359c53b8b73eb448c5f631fa96e8cd2c14df004")
    version("3.3.1", sha256="856e9c4bb75eb0cceac3d5a5c65b1ce52fb3c46b9182920e1c9f34ae69bd2d5f")
    version("3.2.0", sha256="d52e9a1bdd10f31aa154c34a5799b48d4266dc6b4a5ee05a9ceda525f2c6c138")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant("mpi", default=False, description="Enable MPI")
    variant("static", default=False, description="Enable static library build")
    variant("fortran", default=False, description="Enable Fortran")
    variant("int64", default=False, description="Use 64-bit integers as indices.")

    depends_on("mpi", when="+mpi")

    for _mpi_variant in ("~mpi", "+mpi"):
        depends_on(f"hdf5@1.12{_mpi_variant}", when=f"@5:{_mpi_variant}")
        depends_on(f"hdf5@1.10{_mpi_variant}", when=f"@4{_mpi_variant}")
        depends_on(f"hdf5@1.8{_mpi_variant}", when=f"@3{_mpi_variant}")

    patch("MAJ_400_410_champs.patch", when="@4.1.0+static", working_dir="./tools/medimport/4.0.0")

    def check(self):
        with working_dir(self.build_directory):
            make("test", parallel=False)

    def patch(self):
        # resembles FindSalomeHDF5.patch as in salome-configuration
        # see https://cmake.org/cmake/help/latest/prop_tgt/IMPORTED_LINK_INTERFACE_LIBRARIES.html
        filter_file(
            "GET_PROPERTY(_lib_lst TARGET hdf5 PROPERTY IMPORTED_LINK_INTERFACE_LIBRARIES_NOCONFIG)",  # noqa: E501
            "#GET_PROPERTY(_lib_lst TARGET hdf5 PROPERTY IMPORTED_LINK_INTERFACE_LIBRARIES_NOCONFIG)",  # noqa: E501
            "config/cmake_files/FindMedfileHDF5.cmake",
            string=True,
        )

    def setup_dependent_build_environment(self, env, dependent_spec):
        env.set("HDF5_ROOT_DIR", self.spec["hdf5"].prefix)

    def cmake_args(self):
        spec = self.spec
        options = []

        if "+mpi" in spec:
            options.extend(["-DMEDFILE_USE_MPI=ON", "-DMPI_ROOT_DIR=%s" % spec["mpi"].prefix])
        else:
            options.extend(["-DMEDFILE_USE_MPI=OFF"])

        if "+static" in spec:
            options.extend(["-DMEDFILE_BUILD_SHARED_LIBS=OFF", "-DMEDFILE_BUILD_STATIC_LIBS=ON"])
        else:
            options.extend(["-DMEDFILE_BUILD_SHARED_LIBS=ON", "-DMEDFILE_BUILD_STATIC_LIBS=OFF"])

        if "+fortran" in spec:
            options.extend(["-DCMAKE_Fortran_COMPILER=%s" % self.compiler.fc])
        else:
            options.extend(["-DCMAKE_Fortran_COMPILER="])

        if "+int64" in spec:
            options.append("-DMED_MEDINT_TYPE=long")
        else:
            options.append("-DMED_MEDINT_TYPE=int")

        options.extend(
            [
                "-DMEDFILE_BUILD_PYTHON=OFF",
                "-DMEDFILE_INSTALL_DOC=OFF",
                "-DMEDFILE_BUILD_TESTS=%s" % self.run_tests,
                "-DHDF5_ROOT_DIR=%s" % spec["hdf5"].prefix,
            ]
        )

        return options
