# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyGpaw(PythonPackage):
    """GPAW is a density-functional theory (DFT) Python code based on the
    projector-augmented wave (PAW) method and the atomic simulation environment
    (ASE)."""

    homepage = "https://wiki.fysik.dtu.dk/gpaw/index.html"
    url      = "https://pypi.io/packages/source/g/gpaw/gpaw-1.3.0.tar.gz"

    version('19.8.1', sha256='79dee367d695d68409c4d69edcbad5c8679137d6715da403f6c2500cb2178c2a')
    version('1.3.0', sha256='cf601c69ac496421e36111682bcc1d23da2dba2aabc96be51accf73dea30655c')

    variant('mpi', default=True, description='Build with MPI support')
    variant('scalapack', default=True,
            description='Build with ScaLAPACK support')
    variant('fftw', default=True, description='Build with FFTW support')
    variant('libvdwxc', default=True, description='Build with libvdwxc support')

    depends_on('mpi', when='+mpi', type=('build', 'link', 'run'))
    depends_on('python@2.6:', type=('build', 'run'), when='@:1.3.0')
    depends_on('python@3.5:', type=('build', 'run'), when='@19.8.1:')
    depends_on('py-ase@3.13.0:', type=('build', 'run'), when='@1.3.0')
    depends_on('py-ase@3.18.0:', type=('build', 'run'), when='@19.8.1')
    depends_on('py-numpy +blas +lapack', type=('build', 'run'))
    depends_on('py-scipy', type=('build', 'run'))
    depends_on('libxc')
    depends_on('blas')
    depends_on('lapack')
    depends_on('fftw+mpi', when='+fftw +mpi')
    depends_on('fftw~mpi', when='+fftw ~mpi')
    depends_on('scalapack', when='+scalapack')
    depends_on('libvdwxc', when='+libvdwxc')

    patch('libxc.patch', when='@1.3.0')

    def patch(self):
        spec = self.spec
        # For build notes see https://wiki.fysik.dtu.dk/gpaw/install.html

        libxc = spec['libxc']
        blas = spec['blas']
        lapack = spec['lapack']

        python_include = spec['python'].headers.directories[0]
        numpy_include = join_path(
            spec['py-numpy'].prefix,
            spec['python'].package.site_packages_dir,
            'numpy', 'core', 'include')

        libs = blas.libs + lapack.libs + libxc.libs
        include_dirs = [
            python_include,
            numpy_include,
            blas.prefix.include,
            lapack.prefix.include,
            libxc.prefix.include
        ]
        if '+mpi' in spec:
            libs += spec['mpi'].libs
            mpi_include_dirs = repr([spec['mpi'].prefix.include])
            mpi_library_dirs = repr(list(spec['mpi'].libs.directories))
            include_dirs.append(spec['mpi'].prefix.include)
        if '+scalapack' in spec:
            libs += spec['scalapack'].libs
            include_dirs.append(spec['scalapack'].prefix.include)
            scalapack_macros = repr([
                ('GPAW_NO_UNDERSCORE_CBLACS', '1'),
                ('GPAW_NO_UNDERSCORE_CSCALAPACK', '1')
            ])
        if '+fftw' in spec:
            libs += spec['fftw'].libs
            include_dirs.append(spec['fftw'].prefix.include)
        if '+libvdwxc' in spec:
            libs += spec['libvdwxc'].libs
            include_dirs.append(spec['libvdwxc'].prefix.include)

        lib_dirs = list(libs.directories)
        libs = list(libs.names)
        rpath_str = ':'.join(self.rpath)

        with open('customize.py', 'w') as f:
            f.write("libraries = {0}\n".format(repr(libs)))
            f.write("include_dirs = {0}\n".format(repr(include_dirs)))
            f.write("library_dirs = {0}\n".format(repr(lib_dirs)))
            f.write(
                "extra_link_args += ['-Wl,-rpath={0}']\n".format(rpath_str)
            )
            if '+mpi' in spec:
                f.write("define_macros += [('PARALLEL', '1')]\n")
                f.write("compiler='{0}'\n".format(spec['mpi'].mpicc))
                f.write("mpicompiler = '{0}'\n".format(spec['mpi'].mpicc))
                f.write("mpi_include_dirs = {0}\n".format(mpi_include_dirs))
                f.write("mpi_library_dirs = {0}\n".format(mpi_library_dirs))
            else:
                f.write("compiler='{0}'\n".format(self.compiler.cc))
                f.write("mpicompiler = None\n")
            if '+scalapack' in spec:
                f.write("scalapack = True\n")
                f.write("define_macros += {0}\n".format(scalapack_macros))
            if '+fftw' in spec:
                f.write("fftw = True\n")
            if '+libvdwxc' in spec:
                f.write("libvdwxc = True\n")
