# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Damaris(CMakePackage):
    """Damaris is a middleware for I/O and in situ analytics
    targeting large-scale, MPI-based HPC simulations."""

    homepage = "https://project.inria.fr/damaris/"
    git = "https://gitlab.inria.fr/Damaris/damaris.git"
    maintainers("jcbowden")

    license("LGPL-3.0-or-later")

    version("master", branch="master")
    version("1.11.0", tag="v1.11.0", commit="1aee2a8971584712d81323d77f9805448fe54947")
    version("1.10.0", tag="v1.10.0", commit="4e6b2641be1f7ded379312a8e7f4644ebe009ec9")
    version("1.9.2", tag="v1.9.2", commit="22c146b4b4ca047d4d36fd904d248e0280b3c0ea")
    version("1.9.1", tag="v1.9.1", commit="2fe83f587837b7ad0b5c187b8ff453f7d3ad2c18")
    version("1.9.0", tag="v1.9.0", commit="23cac3a8ade9f9c20499081a8ed10b3e51801428")
    version("1.8.2", tag="v1.8.2", commit="bd447e677cdf81389f93bea3139af0fa54554a01")
    version("1.8.1", tag="v1.8.1", commit="18513edb1e11974a4296263ff8499d2802e17891")
    version("1.8.0", tag="v1.8.0", commit="56701eee59d464cc73d248fbd5e7a8a70e7a3933")
    version("1.7.1", tag="v1.7.1", commit="09dfbe7828ee295b4433c9e01c6523fa6b4adab5")
    version("1.7.0", tag="v1.7.0", commit="9ab3ea4c568de16f5d43b8b5ad71feb4864a5584")
    version(
        "1.6.0", tag="v1.6.0", commit="1fe4c61cce03babd24315b8e6156f226baac97a2", deprecated=True
    )
    version(
        "1.5.0", tag="v1.5.0", commit="68206a696ad430aa8426ca370501aa71914fbc87", deprecated=True
    )
    version(
        "1.3.3", tag="v1.3.3", commit="f1c473507c080738f7092f6a7d72deb938ade786", deprecated=True
    )
    version(
        "1.3.2", tag="v1.3.2", commit="38b50664523e56900809a19f0cf52fc0ab5dca53", deprecated=True
    )
    version(
        "1.3.1", tag="v1.3.1", commit="6cee3690fa7d387acc8f5f650a7b019e13b90284", deprecated=True
    )

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant("fortran", default=True, description="Enables Fortran support")
    variant("hdf5", default=False, description="Enables the HDF5 storage plugin")
    variant("static", default=False, description="Builds a static version of the library")
    variant("catalyst", default=False, description="Enables the Catalyst visualization plugin")
    variant("visit", default=False, description="Enables the VisIt visualization plugin")
    variant(
        "examples",
        default=False,
        description="Enables compilation and installation of the examples code",
    )
    variant("docs", default=False, description="Enables the building of dOxygen documentation")
    variant(
        "python",
        default=False,
        description="Enables building of Python enabled Damaris library using Boost::python",
    )
    extends("python", when="+python")

    depends_on("xsd")
    depends_on("xerces-c")
    depends_on("mpi")
    depends_on("cmake@3.18.0:", type=("build"))
    depends_on("boost@1.67:+thread+log+filesystem+date_time+system")
    depends_on("boost+python", when="+python")
    depends_on("py-mpi4py", when="+python", type=("build", "run"))
    depends_on("hdf5@1.8.20:", when="+hdf5")
    depends_on("paraview+python+mpi+development_files", when="+catalyst")
    depends_on("visit+mpi", when="+visit")

    def cmake_args(self):
        args = []
        if not self.spec.variants["static"].value:
            args.extend(["-DBUILD_SHARED_LIBS=ON"])

        args.extend(["-DCMAKE_CXX_COMPILER=%s" % self.spec["mpi"].mpicxx])
        args.extend(["-DCMAKE_C_COMPILER=%s" % self.spec["mpi"].mpicc])
        args.extend(["-DBOOST_ROOT=%s" % self.spec["boost"].prefix])
        args.extend(["-DXercesC_ROOT=%s" % self.spec["xerces-c"].prefix])
        args.extend(["-DXSD_ROOT=%s" % self.spec["xsd"].prefix])

        if self.spec.variants["fortran"].value:
            args.extend(["-DCMAKE_Fortran_COMPILER=%s" % self.spec["mpi"].mpifc])
            args.extend(["-DENABLE_FORTRAN:BOOL=ON"])

        if self.spec.variants["hdf5"].value:
            args.extend(["-DENABLE_HDF5:BOOL=ON"])
            args.extend(["-DHDF5_ROOT:PATH=%s" % self.spec["hdf5"].prefix])

        if self.spec.variants["catalyst"].value:
            args.extend(["-DENABLE_CATALYST:BOOL=ON"])
            args.extend(["-DParaView_ROOT:PATH=%s" % self.spec["catalyst"].prefix])

        if self.spec.variants["examples"].value:
            args.extend(["-DENABLE_EXAMPLES:BOOL=ON"])

        if self.spec.variants["docs"].value:
            args.extend(["-DENABLE_DOCS:BOOL=ON"])

        if self.spec.variants["python"].value:
            args.extend(["-DENABLE_PYTHON:BOOL=ON"])
            args.extend(["-DENABLE_PYTHONMOD:BOOL=ON"])
            args.append(self.define("PYTHON_MODULE_INSTALL_PATH", python_platlib))

        if self.spec.variants["visit"].value:
            args.extend(["-DENABLE_VISIT:BOOL=ON"])
            args.extend(["-DVisIt_ROOT:PATH=%s" % self.spec["visit"].prefix])
        return args
