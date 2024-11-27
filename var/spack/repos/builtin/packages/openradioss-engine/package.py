# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class OpenradiossEngine(CMakePackage):
    """
    OpenRadioss is the publicly available open-source code base that a worldwide
    community of researchers, software developers, and industry leaders are
    enhancing every day. OpenRadioss is changing the game by empowering users to
    make rapid contributions that tackle the latest challenges brought on by rapidly
    evolving technologies like battery development, lightweight materials and composites,
    human body models and biomaterials, autonomous driving and flight,
    as well as the desire to give passengers the safest environment possible via virtual testing.
    OpenRadioss Engine is a component of the OpenRadioss that runs the simulation in parallel.
    """

    homepage = "https://www.openradioss.org/"
    git = "https://github.com/OpenRadioss/OpenRadioss.git"

    license("AGPL-3.0-or-later")

    maintainers("kjrstory")
    version("main", branch="main")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant("mpi", default=False, description="Enable MPI support")
    variant("sp", default=False, description="Using single precision option")
    variant("debug", default=False, description="Debug Option")
    variant("static_link", default=True, description="Static_link Option")

    depends_on("openmpi", when="+mpi")
    depends_on("cmake@2.8:", type="build")
    depends_on("perl", type="build")
    depends_on("python", type="build")

    requires(
        "%gcc",
        "%intel",
        "%oneapi",
        "%aocc",
        "%arm",
        policy="one_of",
        msg="Openradioss-starter can be built using GNU Fortran, Intel Fortran, AOCC, \
             or Armflang compilers only.",
    )

    build_directory = "engine"
    root_cmakelists_dir = "engine"

    @property
    def compiler_name(self):
        compiler_mapping = {
            "aocc": "linux64_AOCC",
            "intel": "linux64_intel",
            "oneapi": "linux64_intel",
            "gcc": "linux64_gf",
            "arm": "linuxa64",
        }
        compiler_name = compiler_mapping[self.spec.compiler.name]
        return compiler_name

    def cmake_args(self):
        args = [
            self.define("mpi_os", False),
            self.define("CMAKE_Fortran_COMPILER", spack_fc),
            self.define("CMAKE_C_COMPILER", spack_cc),
            self.define("CMAKE_CPP_COMPILER", spack_cxx),
            self.define("CMAKE_CXX_COMPILER", spack_cxx),
            self.define("sanitize", False),
            self.define("arch", self.compiler_name),
            self.define_from_variant("debug", "debug"),
            self.define_from_variant("static_link", "static_link"),
        ]

        if "+sp" in self.spec:
            args.append(self.define("precision", "sp"))
        else:
            args.append(self.define("precision", "dp"))

        if "+mpi" in self.spec:
            args.append(self.define("MPI", "ompi"))
            args.append(self.define("mpi_root", self.spec["mpi"].prefix))
            args.append(self.define("mpi_incdir", self.spec["mpi"].prefix.include))
            args.append(self.define("mpi_libdir", self.spec["mpi"].prefix.lib))
        else:
            args.append(self.define("MPI", "smp"))

        exec_file = f"engine_{self.compiler_name}"
        exec_file += "_ompi" if "+mpi" in self.spec else ""
        args.append(self.define("EXEC_NAME", exec_file))

        return args

    def install(self, spec, prefix):
        mkdirp(join_path(prefix, "exec"))

        exec_file = f"engine_{self.compiler_name}"
        exec_file += "_ompi" if "+mpi" in self.spec else ""

        install(
            join_path(self.stage.source_path, "engine", exec_file),
            join_path(prefix, "exec", exec_file),
        )
        install_tree(
            join_path(self.stage.source_path, "hm_cfg_files"), join_path(prefix, "hm_cfg_files")
        ),
        install_tree(
            join_path(self.stage.source_path, "extlib", "h3d"), join_path(prefix, "extlib", "h3d")
        ),
        install_tree(
            join_path(self.stage.source_path, "extlib", "hm_reader"),
            join_path(prefix, "extlib", "hm_reader"),
        )

    def setup_run_environment(self, env):
        env.set("OPENRADIOSS_PATH", self.prefix)
        env.set("RAD_CFG_PATH", join_path(self.prefix, "hm_cfg_files"))
        env.set("RAD_H3D_PATH", join_path(self.prefix, "extlib", "h3d", "lib", "linux64"))
        env.set("OMP_STACKSIZE", "400m")
        env.prepend_path("LD_LIBRARY_PATH", join_path(self.prefix, "extlib", "h3d", "linux64"))
        env.prepend_path(
            "LD_LIBRARY_PATH", join_path(self.prefix, "extlib", "hm_reader", "linux64")
        )
        env.prepend_path("PATH", join_path(self.prefix, "exec"))
        if "+mpi" in self.spec:
            env.prepend_path("PATH", self.spec["mpi"].prefix.bin)
            env.prepend_path("LD_LIBRARY_PATH", self.spec["mpi"].prefix.lib)
