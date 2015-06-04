from spack import *

class Mitos(Package):
    """Mitos is a library and a tool for collecting sampled memory
    performance data to view with MemAxes"""

    homepage = "https://github.com/scalability-llnl/Mitos"
    url      = "https://github.com/scalability-llnl/Mitos"

    version('0.9', '8a8f05b35e04e9f37fa15436b98d5b25', git='https://github.com/scalability-llnl/Mitos.git', tag='v0.9')

    depends_on('dyninst')
    depends_on('hwloc')

    def install(self, spec, prefix):
        with working_dir('spack-build', create=True):
            cmake('..', *std_cmake_args)
            make()
            make("install")
