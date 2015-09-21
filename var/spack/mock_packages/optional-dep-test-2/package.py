from spack import *

class OptionalDepTest2(Package):
    """Depends on the optional-dep-test package"""

    homepage = "http://www.example.com"
    url      = "http://www.example.com/optional-dep-test-2-1.0.tar.gz"

    version('1.0', '0123456789abcdef0123456789abcdef')

    variant('odt', default=False)
    variant('mpi', default=False)

    depends_on('optional-dep-test', when='+odt')
    depends_on('optional-dep-test+mpi', when='+mpi')

    def install(self, spec, prefix):
        pass
