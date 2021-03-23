# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

#
# Author: Matteo Giantomassi <matteo.giantomassiNOSPAM AT uclouvain.be>
# Date: October 11, 2016
from spack import *


class Abinit(AutotoolsPackage):
    """ABINIT is a package whose main program allows one to find the total
    energy, charge density and electronic structure of systems made of
    electrons and nuclei (molecules and periodic solids) within
    Density Functional Theory (DFT), using pseudopotentials and a planewave
    or wavelet basis.

    ABINIT also includes options to optimize the geometry according to the
    DFT forces and stresses, or to perform molecular dynamics
    simulations using these forces, or to generate dynamical matrices,
    Born effective charges, and dielectric tensors, based on Density-Functional
    Perturbation Theory, and many more properties. Excited states can be
    computed within the Many-Body Perturbation Theory (the GW approximation and
    the Bethe-Salpeter equation), and Time-Dependent Density Functional Theory
    (for molecules). In addition to the main ABINIT code, different utility
    programs are provided.
    """

    homepage = 'http://www.abinit.org'
    url      = 'https://www.abinit.org/sites/default/files/packages/abinit-8.6.3.tar.gz'

    version('8.10.3', sha256='ed626424b4472b93256622fbb9c7645fa3ffb693d4b444b07d488771ea7eaa75')
    version('8.10.2', sha256='4ee2e0329497bf16a9b2719fe0536cc50c5d5a07c65e18edaf15ba02251cbb73')
    version('8.8.2', sha256='15216703bd56a799a249a112b336d07d733627d3756487a4b1cb48ebb625c3e7')
    version('8.6.3', sha256='82e8d071088ab8dc1b3a24380e30b68c544685678314df1213180b449c84ca65')
    version('8.2.2', sha256='e43544a178d758b0deff3011c51ef7c957d7f2df2ce8543366d68016af9f3ea1')
    # Versions before 8.0.8b are not supported.
    version('8.0.8b', sha256='37ad5f0f215d2a36e596383cb6e54de3313842a0390ce8d6b48a423d3ee25af2')

    variant('mpi', default=True,
            description='Builds with MPI support. Requires MPI2+')
    variant('openmp', default=False,
            description='Enables OpenMP threads. Use threaded FFTW3')
    variant('scalapack', default=False,
            description='Enables scalapack support. Requires MPI')
    # variant('elpa', default=False,
    #         description='Uses elpa instead of scalapack. Requires MPI')

    # TODO: To be tested.
    # It was working before the last `git pull` but now all tests crash.
    # For the time being, the default is netcdf3 and the internal fallbacks
    # FIXME: rename (trio?) and use multivalued variants to cover
    # --with-trio-flavor={netcdf, none}
    # Note that Abinit@8: does not support etsf_io anymore because it is not
    # compatible with HDF5 and MPI-IO
    variant('hdf5', default=False,
            description='Enables HDF5+Netcdf4 with MPI. WARNING: experimental')

    variant('wannier90', default=False,
            description='Enables the Wannier90 library')

    # Add dependencies
    # currently one cannot forward options to virtual packages, see #1712.
    # depends_on('blas', when='~openmp')
    # depends_on('blas+openmp', when='+openmp')
    depends_on('blas')
    depends_on('lapack')

    # Require MPI2+
    depends_on('mpi@2:', when='+mpi')

    depends_on('scalapack', when='+scalapack+mpi')

    # depends_on('elpa~openmp', when='+elpa+mpi~openmp')
    # depends_on('elpa+openmp', when='+elpa+mpi+openmp')

    depends_on('fftw precision=float,double')
    depends_on('fftw~openmp', when='~openmp')
    depends_on('fftw+openmp', when='+openmp')

    depends_on('netcdf-fortran', when='+hdf5')
    depends_on('hdf5+mpi', when='+mpi+hdf5')  # required for NetCDF-4 support

    # pin libxc version
    depends_on("libxc@2.2.2")

    # Cannot ask for +scalapack if it does not depend on MPI
    conflicts('+scalapack', when='~mpi')

    depends_on("wannier90+shared", when='+wannier90')

    # Elpa is a substitute for scalapack and needs mpi
    # conflicts('+elpa', when='~mpi')
    # conflicts('+elpa', when='+scalapack')

    patch('rm_march_settings.patch')

    # Fix detection of Fujitsu compiler
    # Fix configure not to collect the option that causes an error
    # Fix intent(out) and unnecessary rewind to avoid compile error
    patch('fix_for_fujitsu.patch', when='%fj')

    def configure_args(self):

        spec = self.spec

        options = []
        oapp = options.append

        if '+wannier90' in spec:
            oapp('--with-wannier90-libs=-L{0}'
                 .format(spec['wannier90'].prefix.lib + ' -lwannier -lm'))
            oapp('--with-wannier90-incs=-I{0}'
                 .format(spec['wannier90'].prefix.modules))
            oapp('--with-wannier90-bins={0}'
                 .format(spec['wannier90'].prefix.bin))
            oapp('--enable-connectors')
            oapp('--with-dft-flavor=wannier90')

        if '+mpi' in spec:
            # MPI version:
            # let the configure script auto-detect MPI support from mpi_prefix
            oapp('--enable-mpi=yes')
            if self.spec.satisfies('%fj'):
                oapp('CC={0}'.format(spec['mpi'].mpicc))
                oapp('CXX={0}'.format(spec['mpi'].mpicxx))
                oapp('FC={0}'.format(spec['mpi'].mpifc))
            else:
                oapp('--with-mpi-prefix={0}'.format(spec['mpi'].prefix))
                oapp('--enable-mpi-io=yes')
                oapp('MPIFC={0}'.format(spec['mpi'].mpifc))
            if '~wannier90' in spec:
                oapp('--with-dft-flavor=atompaw+libxc')

        # Activate OpenMP in Abinit Fortran code.
        if '+openmp' in spec:
            oapp('--enable-openmp=yes')

        # BLAS/LAPACK/SCALAPACK-ELPA
        linalg = spec['lapack'].libs + spec['blas'].libs
        if '+scalapack' in spec:
            oapp('--with-linalg-flavor=custom+scalapack')
            linalg = spec['scalapack'].libs + linalg

        # elif '+elpa' in spec:
        else:
            oapp('--with-linalg-flavor=custom')

        oapp('--with-linalg-libs={0}'.format(linalg.ld_flags))

        # FFTW3: use sequential or threaded version if +openmp
        fftflavor, fftlibs = 'fftw3', '-lfftw3 -lfftw3f'
        if '+openmp' in spec:
            fftflavor = 'fftw3-threads'
            fftlibs = '-lfftw3_omp -lfftw3 -lfftw3f'

        options.extend([
            '--with-fft-flavor=%s' % fftflavor,
            '--with-fft-incs=-I%s' % spec['fftw'].prefix.include,
            '--with-fft-libs=-L%s %s' % (spec['fftw'].prefix.lib, fftlibs),
        ])

        # LibXC library
        libxc = spec['libxc:fortran']
        options.extend([
            'with_libxc_incs={0}'.format(libxc.headers.cpp_flags),
            'with_libxc_libs={0}'.format(libxc.libs.ld_flags + ' -lm')
        ])

        # Netcdf4/HDF5
        if '+hdf5' in spec:
            oapp('--with-trio-flavor=netcdf')
            # Since version 8, Abinit started to use netcdf4 + hdf5 and we have
            # to link with the high level HDF5 library
            hdf5 = spec['hdf5:hl']
            netcdff = spec['netcdf-fortran:shared']
            options.extend([
                '--with-netcdf-incs={0}'.format(netcdff.headers.cpp_flags),
                '--with-netcdf-libs={0}'.format(
                    netcdff.libs.ld_flags + ' ' + hdf5.libs.ld_flags
                ),
            ])
        else:
            # In Spack we do our best to avoid building any internally provided
            # dependencies, such as netcdf3 in this case.
            oapp('--with-trio-flavor=none')

        if self.spec.satisfies('%fj'):
            oapp('FCFLAGS_MODDIR=-M{0}'.format(join_path(
                 self.stage.source_path, 'src/mods')))

        return options

    def check(self):
        """This method is called after the build phase if tests have been
        explicitly activated by user.
        """
        make('check')
        make('tests_in')
