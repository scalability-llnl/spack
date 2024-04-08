from spack.package import *
import sys

class Dac(MakefilePackage):
    """NASA JSC's Direct Simulation Monte Carlo code"""

    homepage = "https://gitlab-fsl.jsc.nasa.gov/rgd-team/dac"
    git = "ssh://git@gitlab-fsl.jsc.nasa.gov/rgd-team/dac.git"

    version("devel", commit="aec9946b284eebe0080dc7051427196739854a7b")

    depends_on("mpi")

    build_directory = "src"

    def edit(self, spec, prefix):

        # Need logic to select the correct Makefile.

        comp=""
        print(f"self.compiler.name = {self.compiler.name}")
        if self.compiler.name == "intel":
            comp = "intel"
        elif self.compiler.name == "oneapi":
            comp = "intel"
        elif self.compiler.name == "gcc":
            comp = "gfortran"
        elif self.compiler.name == "pgi":
            comp = "pgi"
        else:
            sys.exit(
                f"ERROR: Unknown compiler ({self.compiler.name}), quitting."
            )


        print(f"spec['mpi'].name = {spec['mpi'].name}")
        mpiname=""
        if spec["mpi"].name == "openmpi":
            mpiname="openmpi"
        elif spec["mpi"].name == "mpich":
            mpiname="mpich"
        elif spec["mpi"].name == "mpt":
            mpiname="mpt"
        else:
            sys.exit(
                f"ERROR: Unknown mpi ({spec['mpi'].name}), quitting."
            )

        # Copy the Makefile into the src directory
        with working_dir("src"):
            copy(f"../Makefiles/Makefile.{comp}.{mpiname}", "Makefile")

            # Now filter it to change a few variables
            makefile = FileFilter("Makefile")
            makefile.filter(r"^INSTALL_DIR.*",f"INSTALL_DIR = {prefix.bin}")
            makefile.filter(r"^FCOMPILER.*",  f"FCOMPILER = {spack_fc}")
            makefile.filter(r"^PFCOMPILER.*", f"PFCOMPILER = {spec['mpi'].mpifc}")
            makefile.filter(r"^CCOMPILER.*",  f"CCOMPILER = {spack_cc}")

            # Finally, make the install dir so "make install" works
            mkdir(prefix.bin)
