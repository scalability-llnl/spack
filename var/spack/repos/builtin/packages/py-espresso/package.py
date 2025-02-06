# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *
from spack.pkg.builtin.boost import Boost


class PyEspresso(CMakePackage):
    """ESPResSo is a highly versatile software package for performing and
    analyzing scientific Molecular Dynamics many-particle simulations of
    coarse-grained atomistic or bead-spring models as they are used in
    soft matter research in physics, chemistry and molecular biology. It
    can be used to simulate systems such as polymers, liquid crystals,
    colloids, polyelectrolytes, ferrofluids and biological systems, for
    example DNA and lipid membranes. It also has a DPD and lattice
    Boltzmann solver for hydrodynamic interactions, and allows several
    particle couplings to the LB fluid.
    """

    homepage = "https://espressomd.org/"
    git = "https://github.com/espressomd/espresso.git"
    url = "https://github.com/espressomd/espresso/releases/download/4.0.0/espresso-4.0.0.tar.gz"

    license("GPL-3.0-only")

    version("develop", branch="python")
    version("4.2.2", sha256="2bc02f91632b0030f1203759768bd718bd8a0005f72696980b12331b4bfa0d76")
    version("4.2.1", sha256="d74b46438b0d013cac35602e28f3530686446a3a307f6771baf15395066bdad5")
    version("4.2.0", sha256="080bbf6bec5456192ce4e1bc0ddebb9e8735db723d3062ec87154f1ac411aaab")

    version("4.1.4", sha256="c1b68de63755475c5eb3ae8117d8c6d96c8ac36cc0f46dd44417a8e7ebe9242c")
    version("4.1.3", sha256="13dd998f71547c6c979a33d918b7f83e1a0e1c5f2bf2ddeeb0d1e99a3dcd6008")
    version("4.1.2", sha256="00bc8e4cab8fc8f56d18978970b55f09168521ed5898a92769986f2157a81a2c")
    version("4.1.1", sha256="61f19f17469522d4aa480ff5254217668ba713589c6b74576e6305920d688f90")
    version("4.1.0", sha256="83cd5dd50c022d028697ff3e889005e4881100ed8cd56b558978f23d0b590c85")

    version("4.0.2", sha256="89878ab44a58e90b69d56368e961b8ca13d9307f8d4b282967a1f3071a62c740")
    version("4.0.1", sha256="17b7268eeba652a77f861bc534cdd05d206e7641d203a9dd5029b44bd422304b")
    version("4.0.0", sha256="8e128847447eebd843de24be9b4ad14aa19c028ae48879a5a4535a9683836e6b")

    # espressomd/espresso#2244 merge upstream
    patch("2244.patch", when="@4.0.0")

    # Support for modern gcc was fixed in 4.2 (https://github.com/espressomd/espresso/pull/3990)
    conflicts("%gcc@11:", when="@:4.1")

    variant("hdf5", default=True, description="Enable HDF5 backend")

    depends_on("cmake@3.0:", type="build")
    depends_on("mpi")
    depends_on("boost+serialization+filesystem+system+python+mpi")

    # TODO: replace this with an explicit list of components of Boost,
    # for instance depends_on('boost +filesystem')
    # See https://github.com/spack/spack/pull/22303 for reference
    depends_on(Boost.with_default_variants)
    extends("python")
    depends_on("py-cython@0.23:", type="build")
    depends_on("py-numpy", type=("build", "run"))
    depends_on("fftw")
    depends_on("hdf5+hl+mpi", when="+hdf5")

    def cmake_args(self):
        args = []

        if self.spec.satisfies("@4.0:4.1"):
            # 4.1 defaults CUDA options to ON, which this package does not currently support
            # Ideally a future version of the package would add proper CUDA support.
            args.append(self.define("WITH_CUDA", False))

        args.append(self.define_from_variant("WITH_HDF5", "hdf5"))

        return args
