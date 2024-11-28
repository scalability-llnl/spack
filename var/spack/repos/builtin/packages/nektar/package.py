# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

import llnl.util.filesystem as fs

from spack.package import *


class Nektar(CMakePackage):
    """Nektar++: Spectral/hp Element Framework"""

    homepage = "https://www.nektar.info/"
    git = "https://gitlab.nektar.info/nektar/nektar.git"

    version("5.5.0", commit="4365d5d7156139f238db962deae5eb25e0437d12", preferred=True)
    version("5.4.0", commit="002bf62648ec667e10524ceb8a98bb1c21804130")
    version("5.3.0", commit="f286f809cfeb26cb73828c90a689a048898971d2")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant("mpi", default=True, description="Builds with mpi support")
    variant("fftw", default=True, description="Builds with fftw support")
    variant("arpack", default=True, description="Builds with arpack support")
    variant("tinyxml", default=True, description="Builds with external tinyxml support")
    variant("hdf5", default=True, description="Builds with hdf5 support")
    variant("scotch", default=False, description="Builds with scotch partitioning support")
    variant("demos", default=False, description="Build demonstration codes")
    variant("python", default=True, description="Enable python support")
    # Solver variants
    variant(
        "acoustic_solver",
        default=False,
        description="Builds an executable associated with the Acoustic solver",
    )
    variant(
        "adr_solver",
        default=False,
        description="Builds an executable associated with the ADR solver",
    )
    variant(
        "cardiac_solver",
        default=False,
        description="Builds an executable associated with the Cardiac electrophysiology solver",
    )
    variant(
        "compflow_solver",
        default=False,
        description="Builds an executable associated with the CompressibleFlow solver",
    )
    variant(
        "diff_solver",
        default=False,
        description="Builds an executable associated with the Diffusion solver",
    )
    variant(
        "dummy_solver",
        default=False,
        description="Builds an executable associated with the Dummy solver",
    )
    variant(
        "elasticity_solver",
        default=False,
        description="Builds an executable associated with the Elasticity solver",
    )
    variant(
        "imgwarp_solver",
        default=False,
        description="Builds an executable associated with the Image Warping solver",
    )
    variant(
        "ins_solver",
        default=False,
        description="Builds an executable associated with the Incompressible Navier Stokes solver",
    )
    variant(
        "mmf_solver",
        default=False,
        description="Builds an executable associated with the MMF solver",
    )
    variant(
        "pulsewave_solver",
        default=False,
        description="Builds an executable associated with the Pulse Wave solver",
    )
    variant(
        "shwater_solver",
        default=False,
        description="Builds an executable associated with the Shallow Water solver",
    )
    variant(
        "vortexwave_solver",
        default=False,
        description="Builds an executable associated with the Vortex Wave solver",
    )

    depends_on("cmake@2.8.8:", type="build", when="~hdf5")
    depends_on("cmake@3.2:", type="build", when="+hdf5")

    depends_on("blas")
    depends_on("zlib")
    depends_on("tinyxml", when="+tinyxml")
    depends_on("lapack")
    depends_on(
        "boost@1.74.0: +thread +iostreams +filesystem +system +program_options +regex +pic"
        "+python +numpy",
        when="+python",
    )
    depends_on(
        "boost@1.74.0: +thread +iostreams +filesystem +system +program_options +regex +pic",
        when="~python",
    )
    depends_on("tinyxml", when="platform=darwin")

    depends_on("mpi", when="+mpi", type=("build", "link", "run"))
    depends_on("fftw@3.0: +mpi", when="+mpi+fftw")
    depends_on("fftw@3.0: ~mpi", when="~mpi+fftw")
    depends_on("arpack-ng +mpi", when="+arpack+mpi")
    depends_on("arpack-ng ~mpi", when="+arpack~mpi")
    depends_on("hdf5 +mpi +hl", when="+mpi+hdf5")
    depends_on("scotch ~mpi ~metis", when="~mpi+scotch")
    depends_on("scotch +mpi ~metis", when="+mpi+scotch")

    extends("python@3:", when="+python")

    conflicts("+hdf5", when="~mpi", msg="Nektar's hdf5 output is for parallel builds only")

    def cmake_args(self):
        def hasfeature(feature):
            return True if feature in self.spec else False

        args = [
            self.define_from_variant("NEKTAR_BUILD_DEMOS", "demos"),
            self.define_from_variant("NEKTAR_BUILD_PYTHON", "python"),
            self.define("NEKTAR_BUILD_SOLVERS", True),
            self.define("NEKTAR_BUILD_UTILITIES", True),
            self.define("NEKTAR_ERROR_ON_WARNINGS", False),
            self.define_from_variant("NEKTAR_SOLVER_ACOUSTIC", "acoustic_solver"),
            self.define_from_variant("NEKTAR_SOLVER_ADR", "adr_solver"),
            self.define_from_variant("NEKTAR_SOLVER_CARDIAC_EP", "cardiac_solver"),
            self.define_from_variant("NEKTAR_SOLVER_COMPRESSIBLE_FLOW", "compflow_solver"),
            self.define_from_variant("NEKTAR_SOLVER_DIFFUSION", "diff_solver"),
            self.define_from_variant("NEKTAR_SOLVER_DUMMY", "dummy_solver"),
            self.define_from_variant("NEKTAR_SOLVER_ELASTICITY", "elasticity_solver"),
            self.define_from_variant("NEKTAR_SOLVER_IMAGE_WARPING", "imgwarp_solver"),
            self.define_from_variant("NEKTAR_SOLVER_INCNAVIERSTOKES", "ins_solver"),
            self.define_from_variant("NEKTAR_SOLVER_MMF", "mmf_solver"),
            self.define_from_variant("NEKTAR_SOLVER_PULSEWAVE", "pulsewave_solver"),
            self.define_from_variant("NEKTAR_SOLVER_SHALLOW_WATER", "shwater_solver"),
            self.define_from_variant("NEKTAR_SOLVER_VORTEXWAVE", "vortexwave_solver"),
            self.define_from_variant("NEKTAR_USE_ARPACK", "arpack"),
            self.define_from_variant("NEKTAR_USE_FFTW", "fftw"),
            self.define_from_variant("NEKTAR_USE_HDF5", "hdf5"),
            self.define_from_variant("NEKTAR_USE_MPI", "mpi"),
            self.define("NEKTAR_USE_PETSC", False),
            self.define_from_variant("NEKTAR_USE_SCOTCH", "scotch"),
            self.define("NEKTAR_USE_THREAD_SAFETY", True),
            self.define("NEKTAR_USE_MKL", hasfeature("^intel-oneapi-mkl")),
            self.define("NEKTAR_USE_OPENBLAS", hasfeature("^openblas")),
        ]
        return args

    def install(self, spec, prefix):
        super(Nektar, self).install(spec, prefix)
        if "+python" in spec:
            python = which("python")
            with fs.working_dir(self.build_directory):
                python("setup.py", "install", "--prefix", prefix)

    def setup_run_environment(self, env):
        env.append_path(
            "CMAKE_PREFIX_PATH",
            os.path.join(
                self.spec.prefix, os.path.join("lib64", os.path.join("nektar++", "cmake"))
            ),
        )
        env.append_path(
            "PYTHONPATH", os.path.abspath(os.path.join(self.spec.prefix, "build_tree"))
        )

    def setup_dependent_run_environment(self, env, dependent_spec):
        self.setup_run_environment(env)

    def setup_dependent_build_environment(self, env, dependent_spec):
        self.setup_run_environment(env)

    def add_files_to_view(self, view, merge_map, skip_if_exists=True):
        super(Nektar, self).add_files_to_view(view, merge_map, skip_if_exists)
        path = self.view_destination(view)
        view.link(os.path.join(path, "lib64", "nektar++"), os.path.join(path, "lib", "nektar++"))
