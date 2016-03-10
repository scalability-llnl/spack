from spack import *

class Samrai(Package):
    """SAMRAI (Structured Adaptive Mesh Refinement Application Infrastructure)
       is an object-oriented C++ software library enables exploration of numerical,
       algorithmic, parallel computing, and software issues associated with applying
       structured adaptive mesh refinement (SAMR) technology in large-scale parallel
       application development.
    """
    homepage = "https://computation.llnl.gov/project/SAMRAI/"
    url      = "https://computation.llnl.gov/project/SAMRAI/download/SAMRAI-v3.9.1.tar.gz"
    list_url = homepage

    version('3.9.1',      '232d04d0c995f5abf20d94350befd0b2')
    version('3.8.0',      'c18fcffa706346bfa5828b36787ce5fe')
    version('3.7.3',      '12d574eacadf8c9a70f1bb4cd1a69df6')
    version('3.7.2',      'f6a716f171c9fdbf3cb12f71fa6e2737')
    version('3.6.3-beta', 'ef0510bf2893042daedaca434e5ec6ce')
    version('3.5.2-beta', 'd072d9d681eeb9ada15ce91bea784274')
    version('3.5.0-beta', '1ad18a319fc573e12e2b1fbb6f6b0a19')
    version('3.4.1-beta', '00814cbee2cb76bf8302aff56bbb385b')
    version('3.3.3-beta', '1db3241d3e1cab913dc310d736c34388')
    version('3.3.2-beta', 'e598a085dab979498fcb6c110c4dd26c')
    version('2.4.4',      '04fb048ed0efe7c531ac10c81cc5f6ac')

    depends_on("mpi")
    depends_on("zlib")
    depends_on("hdf5+mpi")
    depends_on("boost")

    # don't build tools with gcc
    patch('no-tool-build.patch', when='%gcc')

    # TODO: currently hard-coded to use openmpi - be careful!
    def install(self, spec, prefix):
        mpi_provider = spec['mpi'].package
        configure(
            "--prefix=%s" % prefix,
            "--with-CXX=%s" % mpi_provider.cxx_compiler_wrapper,
            "--with-CC=%s" % mpi_provider.cc_compiler_wrapper,
            "--with-hdf5=%s" % spec['hdf5'].prefix,
            "--with-boost=%s" % spec['boost'].prefix,
            "--with-zlib=%s" % spec['zlib'].prefix,
            "--without-blas",
            "--without-lapack",
            "--with-hypre=no",
            "--with-petsc=no",
            "--enable-opt",
            "--disable-debug")

        make()
        make("install")
