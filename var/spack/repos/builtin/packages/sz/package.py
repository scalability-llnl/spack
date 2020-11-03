# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Sz(CMakePackage):
    """Error-bounded Lossy Compressor for HPC Data"""

    homepage = "https://szcompressor.org"
    url      = "https://github.com/szcompressor/SZ/archive/v2.1.10.tar.gz"
    git      = "https://github.com/szcompressor/sz"
    maintainers = ['disheng222', 'robertu94']

    def url_for_version(self, version):
        """provide url to ensure that download counting via github releases
        works accurately"""
        url = "https://github.com/szcompressor/SZ/releases/download/v{0}/SZ-{0}.tar.gz"
        return url.format(version)

    version('master', branch='master')
    version('2.1.11', sha256='85b8ef99344a3317ba9ee63ca4b9d99a51d1832d4d8880e01c7c56b3a69cacc9')
    version('2.1.10', sha256='3aba7619bdb5412218f162696f946c9d3a3df5acf128ddc685b21e45c11f6ae3',
            url="https://github.com/szcompressor/SZ/releases/download/v2.1.10/sz-2.1.10.tar.gz")
    version('2.1.9', sha256='491724ff1c0eaaab5e1a7a28e36aba6da9dcbeddb29d8d21a6d1388383d4891e')
    version('2.1.8.3', sha256='be94f3c8ab03d6849c59a98e0ebf80816a6b8d07a1d762a4b285498acb2f3871')
    version('2.1.8.1', sha256='a27c9c9da16c9c4232c54813ba79178945f47609043f11501d49a171e47d3f46')
    version('2.1.8.0', sha256='8d6bceb59a03d52e601e29d9b35c21b146c248abae352f9a4828e91d8d26aa24')
    version('2.0.2.0',  sha256='176c65b421bdec8e91010ffbc9c7bf7852c799972101d6b66d2a30d9702e59b0')
    version('1.4.13.5', sha256='b5e37bf3c377833eed0a7ca0471333c96cd2a82863abfc73893561aaba5f18b9')
    version('1.4.13.4', sha256='c99b95793c48469cac60e6cf82f921babf732ca8c50545a719e794886289432b')
    version('1.4.13.3', sha256='9d80390f09816bf01b7a817e07339030d596026b00179275616af55ed3c1af98')
    version('1.4.13.2', sha256='bc45329bf54876ed0f721998940855dbd5fda54379ef35dad8463325488ea4c6')
    version('1.4.13.0', sha256='baaa7fa740a47e152c319b8d7b9a69fe96b4fea5360621cdc96cb250635f946f')
    version('1.4.12.3', sha256='c1413e1c260fac7a48cb11c6dd705730525f134b9f9b244af59885d564ac7a6f')
    version('1.4.12.1', sha256='98289d75481a6e407e4027b5e23013ae83b4aed88b3f150327ea711322cd54b6')
    version('1.4.11.1', sha256='6cbc5b233a3663a166055f1874f17c96ba29aa5a496d352707ab508288baa65c')
    version('1.4.11.0', sha256='52ff03c688522ebe085caa7a5f73ace28d8eaf0eb9a161a34a9d90cc5672ff8c')
    version('1.4.10.0', sha256='cf23cf1ffd7c69c3d3128ae9c356b6acdc03a38f92c02db5d9bfc04f3fabc506')
    version('1.4.9.2',  sha256='9dc785274d068d04c2836955fc93518a9797bfd409b46fea5733294b7c7c18f8')

    variant('python', default=False, description="builds the python wrapper")
    variant('netcdf', default=False, description="build the netcdf reader")
    variant('hdf5', default=False, description="build the hdf5 filter")
    variant('pastri', default=False, description="build the pastri mode")
    variant('time_compression', default=False, description="build the time based compression mode")
    variant('random_access', default=False, description="build the random access compression mode")
    variant('fortran', default=False, description='Enable fortran compilation')
    variant('shared', default=True, description="build shared versions of the libraries")
    variant('stats', default=False, description="build profiling statistics for compression")

    # Part of latest sources don't support -O3 optimization
    # with Fujitsu compiler.
    patch('fix_optimization.patch', when='@2.0.2.0:%fj')

    depends_on('zlib')
    depends_on('zstd')

    extends('python', when="+python")
    depends_on('python@3:', when="+python", type=('build', 'link', 'run'))
    depends_on('swig@3.12:', when="+python", type='build')
    depends_on('py-numpy', when="+python", type=('build', 'link', 'run'))
    depends_on('hdf5', when="+hdf5")
    depends_on('netcdf-c', when="+netcdf")
    depends_on('cmake@3.13:', type='build')

    patch('ctags-only-if-requested.patch', when='@2.1.8.1:2.1.8.3')

    @property
    def build_directory(self):
        """autotools needs a different build directory to work"""
        if self.version >= Version("2.1.8.1"):
            return "spack-build"
        else:
            return "."

    @when("@:2.1.8.0")
    def cmake(self, spec, prefix):
        """use autotools before 2.1.8.1"""
        configure_args = ["--prefix=" + prefix]
        if "+fortran" in spec:
            configure_args.append("--enable-fortran")
        else:
            configure_args.append("--disable-fortran")
        configure(*configure_args)
        # at least the v2.0.2.0 tarball contains object files
        # which need to be cleaned out
        make("clean")

    def cmake_args(self):
        """configure the package with CMake for version 2.1.8.1 and later"""
        args = []

        if "+python" in self.spec:
            args.append("-DBUILD_PYTHON_WRAPPER=ON")
        else:
            args.append("-DBUILD_PYTHON_WRAPPER=OFF")

        if "+netcdf" in self.spec:
            args.append("-DBUILD_NETCDF_READER=ON")
        else:
            args.append("-DBUILD_NETCDF_READER=OFF")

        if "+hdf5" in self.spec:
            args.append("-DBUILD_HDF5_FILTER=ON")
        else:
            args.append("-DBUILD_HDF5_FILTER=OFF")

        if "+pastri" in self.spec:
            args.append("-DBUILD_PASTRI=ON")
        else:
            args.append("-DBUILD_PASTRI=OFF")

        if "+time_compression" in self.spec:
            args.append("-DBUILD_TIMECMPR=ON")
        else:
            args.append("-DBUILD_TIMECMPR=OFF")

        if "+random_access" in self.spec:
            args.append("-DBUILD_RANDOMACCESS=ON")
        else:
            args.append("-DBUILD_RANDOMACCESS=OFF")

        if "+fortran" in self.spec:
            args.append("-DBUILD_FORTRAN=ON")
        else:
            args.append("-DBUILD_FORTRAN=OFF")

        if "+shared" in self.spec:
            args.append("-DBUILD_SHARED_LIBS=ON")
        else:
            args.append("-DBUILD_SHARED_LIBS=OFF")

        if "+stats" in self.spec:
            args.append("-DBUILD_STATS=ON")
        else:
            args.append("-DBUILD_STATS=OFF")
        return args
