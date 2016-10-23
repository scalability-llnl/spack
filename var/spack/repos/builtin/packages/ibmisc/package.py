from spack import *


class Ibmisc(CMakePackage):
    """Misc. reusable utilities used by IceBin."""

    homepage = "https://github.com/citibeth/ibmisc"
    url      = "https://github.com/citibeth/ibmisc/tarball/v0.1.3"

    version('0.1.3', 'bb1876a8d1f0710c1a031280c0fc3f2e')

    version('develop',
        git='https://github.com/citibeth/ibmisc.git',
        branch='develop')

    variant('everytrace', default=False,
            description='Report errors through Everytrace')
    variant('proj', default=True,
            description='Compile utilities for PROJ.4 library')
    variant('blitz', default=True,
            description='Compile utilities for Blitz library')
    variant('netcdf', default=True,
            description='Compile utilities for NetCDF library')
    variant('boost', default=True,
            description='Compile utilities for Boost library')
    variant('udunits2', default=True,
            description='Compile utilities for UDUNITS2 library')
    variant('googletest', default=True,
            description='Compile utilities for Google Test library')
    variant('python', default=True,
            description='Compile utilities for use with Python/Cython')
    variant('docs', default=False,
            description='Build the documentation')

    extends('python')
    depends_on('python@3:')    # Needed for the build...

    depends_on('eigen')
    depends_on('everytrace', when='+everytrace')
    depends_on('proj', when='+proj')
    depends_on('blitz', when='+blitz')
    depends_on('netcdf-cxx4', when='+netcdf')
    depends_on('udunits2', when='+udunits2')
    depends_on('googletest', when='+googletest', type='build')
    depends_on('py-cython', when='+python', type=nolink)
    depends_on('py-numpy', when='+python')
    depends_on('boost', when='+boost')

    # Build dependencies
    depends_on('cmake', type='build')
    depends_on('doxygen', when='+docs', type='build')

    def configure_args(self):
        spec = self.spec
        args = [
            '-DBUILD_PYTHON=%s' % ('YES' if '+python' in spec else 'NO'),
            '-DUSE_EVERYTRACE=%s' % ('YES' if '+everytrace' in spec else 'NO'),
            '-DUSE_PROJ4=%s' % ('YES' if '+proj' in spec else 'NO'),
            '-DUSE_BLITZ=%s' % ('YES' if '+blitz' in spec else 'NO'),
            '-DUSE_NETCDF=%s' % ('YES' if '+netcdf' in spec else 'NO'),
            '-DUSE_BOOST=%s' % ('YES' if '+boost' in spec else 'NO'),
            '-DUSE_UDUNITS2=%s' % ('YES' if '+udunits2' in spec else 'NO'),
            '-DUSE_GTEST=%s' % ('YES' if '+googletest' in spec else 'NO'),
            '-DBUILD_DOCS=%s' % ('YES' if '+docs' in spec else 'NO')]

        if '+python' in spec:
            args.append('-DCYTHON_EXECUTABLE=%s' %
                        join_path(spec['py-cython'].prefix.bin, 'cython'))

        return args
