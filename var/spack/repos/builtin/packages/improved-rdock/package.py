# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class ImprovedRdock(MakefilePackage):
    """Improved version of rDock.
    rDock is a fast and versatile Open Source docking program
    that can be used to dock small molecules against proteins and
    nucleic acids.
    The original version is found at the following URL:
    https://sourceforge.net/projects/rdock/files/rDock_2013.1_src.tar.gz
    """

    homepage = "https://github.com/clinfo/improved_rDock"
    git = "https://github.com/clinfo/improved_rDock.git"

    license("LGPL-3.0-or-later")

    version("main", branch="main")

    depends_on("cxx", type="build")  # generated

    depends_on("popt")
    depends_on("cppunit")
    depends_on("openbabel @3.0.0: +python", type="run")
    depends_on("py-numpy", type="run")
    depends_on("mpi")

    patch("rdock_ld.patch")
    patch("rdock_python3.patch", when="^python@3:")
    patch("rdock_newcxx.patch")
    patch("rdock_useint.patch")
    patch("rdock_erase.patch")
    patch("rdock_loop.patch", when="target=aarch64:")
    patch("rdock_const.patch", when="%fj")
    patch("rdock_const2.patch", when="%fj")

    def edit(self, spec, prefix):
        # compiler path
        tm = FileFilter(join_path("build", "tmakelib", "linux-g++-64", "tmake.conf"))
        tm.filter("/usr/bin/gcc", spack_cc)
        tm.filter("mpicxx", self.spec["mpi"].mpicxx)
        # compiler option
        if self.spec.target.family == "aarch64":
            tm.filter("-m64", "")
        if not self.spec.satisfies("%gcc"):
            tm.filter("-pipe", "")

    def build(self, spec, prefix):
        with working_dir("build"):
            make("linux-g++-64")

    def install(self, spec, prefix):
        for shfile in find("bin", "*"):
            set_executable(shfile)
        install_tree(".", prefix)

    def setup_run_environment(self, env):
        env.set("RBT_ROOT", self.prefix)

    def test_rdock(self):
        """improved-rdock test suite"""
        copy(join_path(self.prefix.example, "1sj0", "*"), ".")

        with test_part(self, "test_rdock_rbcavity", purpose="Check rbcavity"):
            rbcavity = which("rbcavity")
            rbcavity("-r", "1sj0_rdock.prm", "-was")

        with test_part(self, "test_rdock_rbdock", purpose="Use mpirun to run rbdock in parallel"):
            mpiexe = which(str(self.spec["mpi"].prefix.bin.mpirun))
            opts = [
                self.prefix.bin.rbdock,
                "-r",
                "1sj0_rdock.prm",
                "-p",
                "dock.prm",
                "-n",
                "100",
                "-i",
                "1sj0_ligand.sd",
                "-o",
                "1sj0_docking_out",
                "-s",
                "1",
            ]
            mpiexe(*opts)

        with test_part(self, "test_rdock_test_sh", purpose="Sort the output"):
            bash = which("bash")
            opts = [join_path(self.test_suite.current_test_data_dir, "test.sh")]
            bash(*opts)

        with test_part(self, "test_rdock_sdrmsd", purpose="Check sdrmsd calculations"):
            pythonexe = which(str(self.spec["python"].command.path))
            opts = [self.spec.prefix.bin.sdrmsd, "1sj0_ligand.sd", "1sj0_docking_out_sorted.sd"]
            expected = ["1\t0.55", "100\t7.91"]
            out = pythonexe(*opts, out=str.split, error=str.split)
            check_outputs(expected, out)
