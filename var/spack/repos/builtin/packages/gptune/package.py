# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Gptune(CMakePackage):
    """GPTune is an autotuning framework that relies on multitask and transfer
    learnings to help solve the underlying black-box optimization problem using
    Bayesian optimization methodologies."""

    homepage = "https://gptune.lbl.gov/"
    url = "https://github.com/gptune/GPTune/archive/refs/tags/3.0.0.tar.gz"
    git = "https://github.com/gptune/GPTune.git"
    maintainers("liuyangzhuan")

    license("BSD-3-Clause-LBNL")

    version("master", branch="master")
    version("4.0.0", sha256="4f954a810d83b73f5abe5b15b79e3ed5b7ebf7bc0ae7335d27b68111bd078102")
    version("3.0.0", sha256="e19bfc3033fff11ff8c20cae65b88b7ca005d2c4e4db047f9f23226126ec92fa")
    version("2.1.0", sha256="737e0a1d83f66531098beafa73dd479f12def576be83b1c7b8ea5f1615d60a53")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant("superlu", default=False, description="Build the SuperLU_DIST example")
    variant("hypre", default=False, description="Build the Hypre example")
    variant("mpispawn", default=True, description="MPI spawning-based interface")

    depends_on("mpi", type=("build", "link", "run"))
    depends_on("cmake@3.17:", type="build")
    depends_on("jq", type="run")
    depends_on("blas", type="link")
    depends_on("lapack", type="link")
    depends_on("scalapack", type="link")
    depends_on("py-setuptools", type="build")
    depends_on("py-ipyparallel", type=("build", "run"))
    depends_on("py-numpy@:1.24", type=("build", "run"), when="@:4.0.0")
    depends_on("py-numpy@:1.21.5", type=("build", "run"), when="@:2.1.0")
    depends_on("py-pandas", type=("build", "run"))
    depends_on("py-joblib", type=("build", "run"))
    depends_on("py-scikit-learn", type=("build", "run"))
    depends_on("py-matplotlib", type=("build", "run"))
    depends_on("py-pyyaml", type=("build", "run"))
    depends_on("py-scikit-optimize@0.9.0", patches=[patch("space.patch")], type=("build", "run"))
    depends_on("py-gpy", type=("build", "run"))
    depends_on("py-lhsmdu", type=("build", "run"))
    depends_on("py-hpbandster", type=("build", "run"))
    depends_on("py-opentuner", type=("build", "run"))
    depends_on("py-ytopt-autotune@1.1.0", type=("build", "run"))
    depends_on("py-filelock", type=("build", "run"))
    depends_on("py-requests", type=("build", "run"))
    depends_on("py-pyaml", type=("build", "run"))
    depends_on("py-statsmodels@0.13.0:", type=("build", "run"))
    depends_on("py-mpi4py@3.0.3:", type=("build", "run"))
    depends_on("python", type=("build", "run"))
    depends_on("pygmo", type=("build", "run"))
    depends_on("openturns", type=("build", "run"))
    depends_on("py-pymoo", type=("build", "run"), when="@3.0.0:")

    depends_on("superlu-dist@develop", when="+superlu", type=("build", "run"))
    depends_on("hypre+gptune@2.19.0", when="+hypre", type=("build", "run"))

    depends_on("openmpi@4:", when="+mpispawn", type=("build", "run"))
    conflicts("^mpich", when="+mpispawn")
    conflicts("^spectrum-mpi", when="+mpispawn")
    conflicts("^cray-mpich", when="+mpispawn")
    conflicts("%gcc@:7")

    def cmake_args(self):
        spec = self.spec
        fc_flags = []
        if "%gcc@10:" in spec or self.spec.satisfies("%apple-clang@11:"):
            fc_flags.append("-fallow-argument-mismatch")

        args = [
            "-DGPTUNE_INSTALL_PATH=%s" % python_platlib,
            "-DTPL_BLAS_LIBRARIES=%s" % spec["blas"].libs.joined(";"),
            "-DTPL_LAPACK_LIBRARIES=%s" % spec["lapack"].libs.joined(";"),
            "-DTPL_SCALAPACK_LIBRARIES=%s" % spec["scalapack"].libs.joined(";"),
            "-DCMAKE_Fortran_FLAGS=" + "".join(fc_flags),
            "-DBUILD_SHARED_LIBS=ON",
            "-DCMAKE_CXX_COMPILER=%s" % spec["mpi"].mpicxx,
            "-DCMAKE_C_COMPILER=%s" % spec["mpi"].mpicc,
            "-DCMAKE_Fortran_COMPILER=%s" % spec["mpi"].mpifc,
        ]

        return args

    examples_src_dir = "examples"
    src_dir = "GPTune"
    nodes = 1
    cores = 4

    @run_after("install")
    def cache_test_sources(self):
        """Copy the example source files after the package is installed to an
        install test subdirectory for use during `spack test run`."""
        self.cache_extra_test_sources([self.examples_src_dir])

    def setup_run_environment(self, env):
        env.set("GPTUNE_INSTALL_PATH", python_platlib)

    def test_all(self):
        """Run all gptune tests"""
        spec = self.spec
        comp_name = self.compiler.name
        comp_version = str(self.compiler.version).replace(".", ",")
        test_dir = join_path(self.test_suite.current_test_cache_dir, self.examples_src_dir)

        if spec.satisfies("+superlu"):
            superludriver = join_path(spec["superlu-dist"].prefix.lib, "EXAMPLE/pddrive_spawn")
            op = ["-r", superludriver, "."]
            # copy superlu-dist executables to the correct place
            wd = join_path(test_dir, "SuperLU_DIST")
            with working_dir(wd):

                with test_part(self, "test_part_rm", purpose="gptune rm test"):
                    exe = which("rm")
                    exe("-rf", "superlu_dist")

                with test_part(self, "test_part_git", purpose="gptune git test"):
                    exe = which("git")
                    exe("clone", "https://github.com/xiaoyeli/superlu_dist.git")

            with working_dir(wd + "/superlu_dist"):

                with test_part(self, "test_part_mkdir_build", purpose="gptune mkdir build test"):
                    exe = which("mkdir")
                    exe("-p", "build")

            with working_dir(wd + "/superlu_dist/build"):

                with test_part(
                    self, "test_part_mkdir_example", purpose="gptune cp mkdir example test"
                ):
                    exe = which("mkdir")
                    exe("-p", "EXAMPLE")

            with working_dir(wd + "/superlu_dist/build/EXAMPLE"):

                with test_part(self, f"test_part_cp_basic", purpose=f"gptune cp basic test"):
                    exe = which("cp")
                    exe(*op)

        if spec.satisfies("+hypre"):
            hypredriver = join_path(spec["hypre"].prefix.bin, "ij")
            op = ["-r", hypredriver, "."]
            # copy superlu-dist executables to the correct place
            wd = join_path(test_dir, "Hypre")
            with working_dir(wd):

                with test_part(self, "test_part_rm_hypre", purpose="gptune rm hypre test"):
                    exe = which("rm")
                    exe("-rf", "hypre")

                with test_part(self, "test_part_git_hypre", purpose="gptune git hypre test"):
                    exe = which("git")
                    exe("clone", "https://github.com/hypre-space/hypre.git")

            with working_dir(wd + "/hypre/src/test/"):

                with test_part(self, "test_part_cp_hypre", purpose="gptune cp hypre test"):
                    exe = which("cp")
                    exe(*op)

        wd = self.test_suite.current_test_cache_dir
        with open("{0}/run_env.sh".format(wd), "w") as envfile:
            envfile.write('if [[ $NERSC_HOST = "cori" ]]; then\n')
            envfile.write("    export machine=cori\n")
            envfile.write('elif [[ $(uname -s) = "Darwin" ]]; then\n')
            envfile.write("    export machine=mac\n")
            envfile.write("elif [[ $(dnsdomainname) = " + '"summit.olcf.ornl.gov" ]]; then\n')
            envfile.write("    export machine=summit\n")
            envfile.write(
                'elif [[ $(cat /etc/os-release | grep "PRETTY_NAME") =='
                + ' *"Ubuntu"* || $(cat /etc/os-release | grep'
                + ' "PRETTY_NAME") == *"Debian"* ]]; then\n'
            )
            envfile.write("    export machine=unknownlinux\n")
            envfile.write("fi\n")
            envfile.write("export GPTUNEROOT=$PWD\n")
            envfile.write("export MPIRUN={0}\n".format(which(spec["mpi"].prefix.bin + "/mpirun")))
            envfile.write("export PYTHONPATH={0}:$PYTHONPATH\n".format(python_platlib + "/gptune"))
            envfile.write("export proc=$(spack arch)\n")
            envfile.write("export mpi={0}\n".format(spec["mpi"].name))
            envfile.write("export compiler={0}\n".format(comp_name))
            envfile.write("export nodes={0} \n".format(self.nodes))
            envfile.write("export cores={0} \n".format(self.cores))
            envfile.write("export ModuleEnv=$machine-$proc-$mpi-$compiler \n")
            envfile.write(
                'software_json=$(echo ",\\"software_configuration\\":'
                + '{\\"'
                + spec["blas"].name
                + '\\":{\\"version_split\\":'
                + " ["
                + str(spec["blas"].versions).replace(".", ",")
                + ']},\\"'
                + spec["mpi"].name
                + '\\":{\\"version_split\\": ['
                + str(spec["mpi"].versions).replace(".", ",")
                + ']},\\"'
                + spec["scalapack"].name
                + '\\":{\\"version_split\\": ['
                + str(spec["scalapack"].versions).replace(".", ",")
                + ']},\\"'
                + str(comp_name)
                + '\\":{\\"version_split\\": ['
                + str(comp_version)
                + ']}}") \n'
            )
            envfile.write(
                'loadable_software_json=$(echo ",\\"loadable_software_'
                + 'configurations\\":{\\"'
                + spec["blas"].name
                + '\\":{\\"version_split\\": ['
                + str(spec["blas"].versions).replace(".", ",")
                + ']},\\"'
                + spec["mpi"].name
                + '\\":{\\"version_split\\": ['
                + str(spec["mpi"].versions).replace(".", ",")
                + ']},\\"'
                + spec["scalapack"].name
                + '\\":{\\"version_split\\": ['
                + str(spec["scalapack"].versions).replace(".", ",")
                + ']},\\"'
                + str(comp_name)
                + '\\":{\\"version_split\\": ['
                + str(comp_version)
                + ']}}") \n'
            )
            envfile.write(
                'machine_json=$(echo ",\\"machine_configuration\\":'
                + '{\\"machine_name\\":\\"$machine\\",\\"$proc\\":'
                + '{\\"nodes\\":$nodes,\\"cores\\":$cores}}") \n'
            )
            envfile.write(
                'loadable_machine_json=$(echo ",\\"loadable_machine_'
                + 'configurations\\":{\\"$machine\\":{\\"$proc\\":'
                + '{\\"nodes\\":$nodes,\\"cores\\":$cores}}}") \n'
            )

        # copy the environment configuration files to non-cache directories
        ops = [
            ["run_env.sh", python_platlib + "/gptune/."],
            ["run_env.sh", self.install_test_root + "/."],
        ]
        for op in ops:
            with test_part(self, f"test_part_cp_{op[1]}", purpose=f"gptune cp {op[1]} test"):
                with working_dir(wd):
                    exe = which("cp")
                    exe(*op)

        apps = ["Scalapack-PDGEQRF_RCI"]
        if spec.satisfies("+mpispawn"):
            apps = apps + ["GPTune-Demo", "Scalapack-PDGEQRF"]
        if spec.satisfies("+superlu"):
            apps = apps + ["SuperLU_DIST_RCI"]
            if spec.satisfies("+mpispawn"):
                apps = apps + ["SuperLU_DIST"]
        if spec.satisfies("+hypre"):
            if spec.satisfies("+mpispawn"):
                apps = apps + ["Hypre"]

        for app in apps:
            exe = which("bash")
            with test_part(self, f"test_part_{app}", purpose=f"gptune smoke test for {app}"):
                with working_dir(join_path(test_dir, app)):
                    exe("run_examples.sh")
