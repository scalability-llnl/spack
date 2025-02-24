# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Xolotl(CMakePackage, CudaPackage):
    """Xolotl is a high-performance computing code using
    advection-reaction-diffusion (ADR) kinetic rate theory to model the
    time evolution of the divertor material in next generation tokamaks,
    like ITER, as well as nuclear fuel in fission reactors."""

    homepage = "https://github.com/ORNL-Fusion/xolotl"
    url = "https://github.com/ORNL-Fusion/xolotl/archive/refs/tags/v3.1.0.tar.gz"
    git = "https://github.com/ORNL-Fusion/xolotl.git"

    # notify when the package is updated.
    maintainers("sblondel", "PhilipFackler")

    license("BSD-3-Clause", checked_by="PhilipFackler")

    version("3.1.0", sha256="68a495ab0c3efb495189f73474d218eb591099b90d52d427ac868b63e8fc2ee8")

    depends_on("cxx", type="build")

    depends_on("mpi")
    depends_on("boost +log +program_options")
    depends_on("hdf5 +mpi")

    variant("int64", default=True, description="Use 64-bit indices")
    variant("openmp", default=False, description="Activates OpenMP backend")

    conflicts("+cuda", when="cuda_arch=none")
    conflicts("+openmp", when="+cuda", msg="Can't use both OpenMP and CUDA")

    depends_on("petsc ~fortran +kokkos")
    depends_on("petsc +int64", when="+int64")
    depends_on("petsc +openmp", when="+openmp")

    depends_on("plsm@2.0.4", when="@3.1.0")
    depends_on("plsm")
    depends_on("plsm +int64", when="+int64")
    depends_on("plsm +openmp", when="+openmp")

    for cuda_arch in CudaPackage.cuda_arch_values:
        depends_on(f"petsc+cuda cuda_arch={cuda_arch}", when=f"+cuda cuda_arch={cuda_arch}")
        depends_on(f"plsm+cuda cuda_arch={cuda_arch}", when=f"+cuda cuda_arch={cuda_arch}")

    variant("papi", default=False, description="Activates PAPI perfHandler")
    depends_on("papi", when="+papi")

    variant("vtkm", default=False, description="Activates VTK-m vizHandler")
    depends_on("vtk-m", when="+vtkm")

    depends_on("boost +test", type="test")

    def cmake_args(self):
        args = [self.define("BUILD_TESTING", self.run_tests)]

        spec = self.spec
        if "+vtk-m" in spec:
            args.append(self.define("VTKm_DIR", spec["vtk-m"].prefix))

        return args
