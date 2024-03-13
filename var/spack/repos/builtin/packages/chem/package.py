from spack.package import AutotoolsPackage, depends_on, variant, version, which

class Chem(AutotoolsPackage):
    """MSU Chem"""

    homepage = "https://web.cse.msstate.edu/~luke/loci"
    url = "file:///aerolab/admin/software/dist/chem/chem-4.0-p6a.tgz"

    version("4.0-p5", sha256="47b67e7069fd7dc970025612533c4183ac5f8addfe653a96ff7ac4c8a45840f2")
    version("4.0-p6a", sha256="f5137523c06a591f7b0381f293b2bcb052c8803b04fcfcb1349db1592ff524c8")

    patch('chem_jsc_d.patch')

    variant("mpi",   default=False, description="Enable MPI support")

    depends_on("loci")
    depends_on("mpi", when="+mpi")

    #def configure_args(self):
    #    spec = self.spec
    #    return args

    def patch(self):
        """Remove the extra directory in the install path"""
        filter_file("^CHEM_INSTALL_DIR.*", "CHEM_INSTALL_DIR = .", 'revision.conf')
