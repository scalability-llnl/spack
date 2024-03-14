from spack.package import AutotoolsPackage, depends_on, variant, version, which

class Loci(AutotoolsPackage):
    """Logic Programming for Parallel Computational Field Simulations"""

    homepage = "https://web.cse.msstate.edu/~luke/loci"
    url = "file:///aerolab/admin/software/dist/loci/Loci-4.0-p5.tgz"

    version("4.0-p5",  sha256="47b67e7069fd7dc970025612533c4183ac5f8addfe653a96ff7ac4c8a45840f2")

    variant("mpi",   default=False, description="Enable MPI support")
    variant("tecio", default=True,  description="Enable TecIO support.")

    depends_on("libtirpc")
    depends_on("hdf5")

    depends_on("mpi", when="+mpi")
    depends_on("hdf5+mpi", when="+mpi")
    depends_on("tecio",     type=("build", "run"), when="+tecio")
    depends_on("tecio+mpi", type=("build", "run"), when="+tecio+mpi")

    # Loci has parmetis internally, so we'll let it use that
    #with when("+metis"):
    #    with when("+mpi"):
    #        depends_on("parmetis", type=("build", "run"))
    #    else:
    #        depends_on("metis",    type=("build", "run"))

    def configure_args(self):
        spec = self.spec
        args = [
            f"--with-hdf5={spec['hdf5'].prefix}/lib",
        ]

        print(f"spec = {spec}")

        if spec.satisfies("+mpi"):
            print("I found mpi in the spec")
            args.append(f"--with-mpi={spec['mpi'].prefix}")
        else:
            print("I did NOT find mpi in the spec")


        if spec.satisfies("+tecio"):
            f"--with-tec360={spec['tecio'].prefix}/lib",

        print(f"args = {args}")
        return args

    def setup_run_environment(self, env):
        # Redundant but chem needs this
        env.prepend_path("LOCI_BASE", f"{self.prefix}")

    def patch(self):
        """Remove the extra directory in the install path"""
        filter_file("^LOCI_INSTALL_DIR.*", "LOCI_INSTALL_DIR = .", 'src/conf/Loci.conf')
