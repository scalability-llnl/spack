from spack.package import *


class Samurai(CMakePackage):
    """Intervals coupled with algebra of set to handle adaptive
    mesh refinement and operators on it"""

    homepage = "https://github.com/hpc-maths/samurai"
    url = "https://github.com/hpc-maths/samurai.git"

    version("master", git=url)

    depends_on("xtl@0.7.4")
    # depends_on("xsimd@11.0.0")
    depends_on("xtensor@0.24.1 ~tbb")
    depends_on("highfive~mpi", when="~mpi")
    depends_on("highfive+mpi", when="+mpi")
    depends_on("pugixml")
    depends_on("fmt")
    depends_on("nlohmann-json")
    depends_on("cli11")

    # option in future release
    depends_on("cxxopts")
    depends_on("cgal")
    depends_on("petsc~mpi", when="~mpi")
    depends_on("petsc+mpi", when="+mpi")
    depends_on("boost+serialization+mpi", when="+mpi")

    variant("mpi", default=False, description="Enable MPI support")
    variant("openmp", default=False, description="Enable OpenMP support")
    # variant("demos", default=False, description="Build Demos")
    # variant("benchmarks", default=False,description="Build benchmarks")
    variant("tests", default=False, description="Build tests")
    variant("check_nan", default=False, description="Check for Nan in computations")

    def setup_dependent_build_environment(self, env, dependent_spec):
        include_path = self.spec.prefix.include
        env.append_path("CXXFLAGS", f"-I{include_path}")

    def setup_run_environment(self, env):
        env.prepend_path("CPATH", self.spec.prefix.include)

    def cmake_args(self):
        spec = self.spec
        options = []

        options.append(self.define_from_variant("SAMURAI_CHECK_NAN", "check_nan"))

        # MPI support
        if "+mpi" in spec:
            options.append(self.define_from_variant("WITH_MPI", "mpi"))
            options.append(self.define("HDF5_IS_PARALLEL", True))

        # OpenMP support
        if "+openmp" in spec:
            options.append(self.define_from_variant("WITH_OPENMP", "openmp"))

        return options
