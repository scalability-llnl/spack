# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Simulationio(CMakePackage):
    """SimulationIO: Efficient and convenient I/O for large PDE simulations"""

    homepage = "https://github.com/eschnett/SimulationIO"
    url = "https://github.com/eschnett/SimulationIO/archive/version/9.0.1.tar.gz"
    git = "https://github.com/eschnett/SimulationIO.git"

    maintainers("eschnett")

    license("LGPL-3.0-only")

    version("master", branch="master")
    version("9.0.3", sha256="d07192fb69ae0d43364dc5807ce788c6cf1f8fbaa46f83028311b6935fd76aa8")
    version("9.0.2", sha256="3dd3422e64f6a75215783f6157effd07430e1d0af5884e565f73388a815511f8")
    version("9.0.1", sha256="c2f6c99417165f6eb8cbb9c44822d119586675abb34eabd553eb80f44b53e0c8")

    depends_on("cxx", type="build")  # generated

    variant("asdf", default=True, description="Enable ASDF bindings")
    variant("julia", default=False, description="Enable Julia bindings")
    variant("python", default=True, description="Enable Python bindings", when="@9:")
    variant("hdf5", default=True, description="Enable HDF5 bindings")
    variant("rnpl", default=False, description="Enable RNPL bindings")
    variant("silo", default=False, description="Enable Silo bindings")

    variant("pic", default=True, description="Produce position-independent code")

    depends_on("asdf-cxx ~python", when="+asdf")
    depends_on("asdf-cxx ~python", when="+asdf ~python")
    depends_on("asdf-cxx +python", when="+asdf +python")
    depends_on("hdf5 +cxx @1.10.1:", when="+hdf5")
    depends_on("julia", when="+julia", type=("build", "run"))
    depends_on("py-h5py", when="+python", type=("build", "run"))
    depends_on("py-numpy", when="+python", type=("build", "run"))
    depends_on("python@3:", when="+python", type=("build", "run"))
    depends_on("rnpletal", when="+rnpl")
    depends_on("silo", when="+silo")
    depends_on("swig @3", type="build")

    extends("python")

    def cmake_args(self):
        from_variant = self.define_from_variant
        options = [
            from_variant("ENABLE_ASDF_CXX", "asdf"),
            from_variant("ENABLE_HDF5", "hdf5"),
            from_variant("ENABLE_RNPL", "rnpl"),
            from_variant("ENABLE_SILO", "silo"),
            from_variant("CMAKE_POSITION_INDEPENDENT_CODE", "pic"),
        ]
        return options

    def check(self):
        with working_dir(self.build_directory):
            make("test", "CTEST_OUTPUT_ON_FAILURE=1")
