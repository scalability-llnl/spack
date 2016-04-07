from spack import *
import os, sys

class Hypre(Package):
    """Hypre is a library of high performance preconditioners that
       features parallel multigrid methods for both structured and
       unstructured grid problems."""

    homepage = "http://computation.llnl.gov/project/linear_solvers/software.php"
    url      = "http://computation.llnl.gov/project/linear_solvers/download/hypre-2.10.0b.tar.gz"

    version('2.10.1', 'dc048c4cabb3cd549af72591474ad674')
    version('2.10.0b', '768be38793a35bb5d055905b271f5b8e')

    # hypre does not know how to build shared libraries on Darwin
    variant('shared', default=sys.platform!='darwin', description="Build shared library version (disables static library)")
    # SuperluDist have conflicting headers with those in Hypre
    variant('internal-superlu', default=True, description="Use internal Superlu routines")

    depends_on("mpi")
    depends_on("blas")
    depends_on("lapack")

    def install(self, spec, prefix):
        blas_dir = spec['blas'].prefix
        lapack_dir = spec['lapack'].prefix
        mpi_dir = spec['mpi'].prefix

        os.environ['CC'] = os.path.join(mpi_dir, 'bin', 'mpicc')
        os.environ['CXX'] = os.path.join(mpi_dir, 'bin', 'mpicxx')
        os.environ['F77'] = os.path.join(mpi_dir, 'bin', 'mpif77')


        configure_args = [
                "--prefix=%s" % prefix,
                "--with-lapack-libs=lapack",
                "--with-lapack-lib-dirs=%s/lib" % lapack_dir,
                "--with-blas-libs=blas",
                "--with-blas-lib-dirs=%s/lib" % blas_dir]
        if '+shared' in self.spec:
            configure_args.append("--enable-shared")

        if '~internal-superlu' in self.spec:
            configure_args.append("--without-superlu")
            # MLI and FEI do not build without superlu on Linux
            configure_args.append("--without-mli")
            configure_args.append("--without-fei")

        # Hypre's source is staged under ./src so we'll have to manually
        # cd into it.
        with working_dir("src"):
            configure(*configure_args)

            make()
            make("install")
