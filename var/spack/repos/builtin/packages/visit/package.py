# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Visit(CMakePackage):
    """VisIt is an Open Source, interactive, scalable, visualization,
       animation and analysis tool. See comments in VisIt's package.py
       for tips about building VisIt with spack. Building VisIt with
       Spack is still experimental and many standard features are likely
       disabled
       LINUX-------------------------------------------------------------------
       spack install visit ^python+shared ^glib@2.56.3 ^py-setuptools@44.1.0
       LINUX-W/O-OPENGL--------------------------------------------------------
       spack install visit ^python+shared ^glib@2.56.3 ^py-setuptools@44.1.0 \\
       ^mesa+opengl
       MACOS-------------------------------------------------------------------
       spack install visit ^python+shared ^glib@2.56.3 ^py-setuptools@44.1.0 \\
       ^qt~framework

    """
    ############################
    # Suggestions for building:
    ############################
    # cyrush note:
    #
    # Out of the box, VisIt's python 2 requirement will cause
    # spack spec constraint errors due Qt + Mesa build
    # dependencies.
    #
    # You can avoid this using:
    #
    # linux:
    #  spack install visit ^python+shared ^glib@2.56.3 ^py-setuptools@44.1.0
    #
    # linux w/o opengl: (add mesa as opengl if system lacks system opengl )
    #
    #  spack install visit ^python+shared ^glib@2.56.3 ^py-setuptools@44.1.0 \
    #                      ^mesa+opengl
    #
    # macOS:
    #  spack install visit ^python+shared ^glib@2.56.3 ^py-setuptools@44.1.0 \
    #                      ^qt~framework
    #
    # Rpath issues undermine qwt (not qt) when a build as a framework
    # VisIt's osxfixup resolves this for us in other cases,
    # but we can't use osxfixup with spack b/c it will undermine other libs.
    #
    # Even with these changes, VisIt's Python CLI does not work on macOS,
    # there is a linking issue related to OpenSSL.
    # (dyld: Symbol not found: _GENERAL_NAME_free - which comes from OpenSSL)
    #
    ############################
    homepage = "https://wci.llnl.gov/simulation/computer-codes/visit/"
    git      = "https://github.com/visit-dav/visit.git"
    url = "https://github.com/visit-dav/visit/releases/download/v3.1.1/visit3.1.1.tar.gz"

    maintainers = ['cyrush']

    extendable = True

    version('develop', branch='develop')
    version('3.1.1', sha256='0b60ac52fd00aff3cf212a310e36e32e13ae3ca0ddd1ea3f54f75e4d9b6c6cf0')
    version('3.0.1', sha256='a506d4d83b8973829e68787d8d721199523ce7ec73e7594e93333c214c2c12bd')
    version('2.13.3', sha256='cf0b3d2e39e1cd102dd886d3ef6da892733445e362fc28f24d9682012cccf2e5')
    version('2.13.0', sha256='716644b8e78a00ff82691619d4d1e7a914965b6535884890b667b97ba08d6a0f')
    version('2.12.3', sha256='2dd351a291ee3e79926bc00391ca89b202cfa4751331b0fdee1b960c7922161f')
    version('2.12.2', sha256='55897d656ac2ea4eb87a30118b2e3963d6c8a391dda0790268426a73e4b06943')
    version('2.10.3', sha256='05018215c4727eb42d47bb5cc4ff937b2a2ccaca90d141bc7fa426a0843a5dbc')
    version('2.10.2', sha256='89ecdfaf197ef431685e31b75628774deb6cd75d3e332ef26505774403e8beff')
    version('2.10.1', sha256='6b53dea89a241fd03300a7a3a50c0f773e2fb8458cd3ad06816e9bd2f0337cd8')

    variant('gui',    default=True, description='Enable VisIt\'s GUI')
    variant('adios2', default=False, description='Enable ADIOS2 file format')
    variant('hdf5',   default=True, description='Enable HDF5 file format')
    variant('silo',   default=True, description='Enable Silo file format')
    variant('python', default=True, description='Enable Python support')
    variant('mpi',    default=True, description='Enable parallel engine')

    patch('spack-changes-3.1.patch', when="@3.1.0:,develop")
    patch('spack-changes-3.0.1.patch', when="@3.0.1")
    patch('nonframework-qwt.patch', when='^qt~framework platform=darwin')
    patch('parallel-hdf5.patch', when='+hdf5+mpi')

    #############################################
    # Full List of dependencies from build_visit
    #############################################
    # cyrush note:
    #  I added these here to give folks details
    #  to help eventually build up to full
    #  support for visit
    #############################################
    # =====================================
    # core:
    # =====================================
    #  cmake (build)
    #  vtk
    #  qt
    #  qwt
    #  python
    #  mpi
    #
    # =====================================
    # rendering (optional):
    # =====================================
    # icet
    # vtk-m
    # vtk-h
    # llvm
    # mesagl
    # osmesa
    # tbb
    # embree
    # ispc
    # ospray
    #
    # =====================================
    # python modules:
    # =====================================
    # numpy
    # pillow
    # mpi4py
    # seedme
    # sphinx (build, docs)
    # sphinx rtd theme (build, docs)
    # pyqt (visit support deprecated)
    # pyside (note: we want pyside 2)
    #
    # =====================================
    # testing related:
    # =====================================
    # p7zip (build, test)
    #
    # =====================================
    # io libs:
    # =====================================
    # adios
    # adios2
    # advio
    # boost
    # boxlib
    # cfitsio
    # cgns
    # conduit
    # damaris
    # fastbit
    # fastquery
    # gdal
    # h5part
    # hdf4
    # hdf5
    # mdsplus
    # mfem
    # mili
    # moab
    # mxml
    # nektarpp
    # netcdf
    # openexr
    # pidx
    # silo
    # stripack
    # szip
    # tbb
    # uintah
    # xdmf
    # xercesc
    # xsd
    # zlib
    #
    # =====================================

    depends_on('cmake@3.0:', type='build')
    # https://github.com/visit-dav/visit/issues/3498
    depends_on('vtk@8.1.0:8.1.999+opengl2~python', when='~python @3.0:3.999,develop')
    depends_on('vtk@8.1.0:8.1.999+opengl2+python', when='+python @3.0:3.999,develop')
    depends_on('glu', when='platform=linux')
    depends_on('vtk@6.1.0~opengl2', when='@:2.999')
    depends_on('vtk+python', when='+python @3.0:,develop')
    depends_on('vtk~mpi', when='~mpi')
    depends_on('vtk+qt', when='+gui')
    depends_on('qt+gui@4.8.6:4.999', when='+gui @:2.999')
    depends_on('qt+gui@5.10:', when='+gui @3.0:,develop')
    depends_on('qwt', when='+gui')
    depends_on('python@2.6:2.8', when='+python')
    # VisIt uses Silo's 'ghost zone' data structures, which are only available
    # in v4.10+ releases: https://wci.llnl.gov/simulation/computer-codes/silo/releases/release-notes-4.10
    depends_on('silo@4.10:+shared', when='+silo')
    depends_on('silo~mpi', when='+silo~mpi')
    depends_on('silo+mpi', when='+silo+mpi')
    depends_on('hdf5~mpi', when='+hdf5~mpi')
    depends_on('hdf5+mpi', when='+hdf5+mpi')
    depends_on('mpi', when='+mpi')
    depends_on('adios2', when='+adios2')

    conflicts('+adios2', when='@:2.999')
    conflicts('+hdf5', when='~gui @:2.999')
    conflicts('+silo', when='~gui @:2.999')

    root_cmakelists_dir = 'src'

    @when('@3.0.0:3.999,develop')
    def patch(self):
        # Some of VTK's targets don't create explicit libraries, so there is no
        # 'vtktiff'. Instead, replace with the library variable defined from
        # VTK's module flies (e.g. lib/cmake/vtk-8.1/Modules/vtktiff.cmake)
        for filename in find('src', 'CMakeLists.txt'):
            filter_file(r'\bvtk(tiff|jpeg|png)', r'${vtk\1_LIBRARIES}',
                        filename)

    def cmake_args(self):
        spec = self.spec

        cxx_flags = [self.compiler.cxx_pic_flag]
        cc_flags = [self.compiler.cc_pic_flag]

        # NOTE: This is necessary in order to allow VisIt to compile a couple
        # of lines of code with 'const char*' to/from 'char*' conversions.
        if spec.satisfies('@3:%gcc'):
            cxx_flags.append('-fpermissive')
            cc_flags.append('-fpermissive')

        args = [
            '-DVTK_MAJOR_VERSION=' + str(spec['vtk'].version[0]),
            '-DVTK_MINOR_VERSION=' + str(spec['vtk'].version[1]),
            '-DVISIT_VTK_DIR:PATH=' + spec['vtk'].prefix,
            '-DVISIT_ZLIB_DIR:PATH=' + spec['zlib'].prefix,
            '-DVISIT_USE_GLEW=OFF',
            '-DCMAKE_CXX_FLAGS=' + ' '.join(cxx_flags),
            '-DCMAKE_C_FLAGS=' + ' '.join(cc_flags),
        ]

        # Provide the plugin compilation environment so as to extend VisIt
        args.append('-DVISIT_INSTALL_THIRD_PARTY=ON')

        if spec.satisfies('@3.1:'):
            args.append('-DFIXUP_OSX=OFF')

        if '+python' in spec:
            args.append('-DVISIT_PYTHON_SCRIPTING=ON')
            # keep this off, we have an openssl + python linking issue
            # that appears in spack
            args.append('-DVISIT_PYTHON_FILTERS=OFF')
            args.append('-DPYTHON_DIR:PATH={0}'.format(spec['python'].home))
        else:
            args.append('-DVISIT_PYTHON_SCRIPTING=OFF')
            # keep this off, we have an openssl + python linking issue
            # that appears in spack
            args.append('-DVISIT_PYTHON_FILTERS=OFF')

        if '+gui' in spec:
            qt_bin = spec['qt'].prefix.bin
            args.extend([
                '-DVISIT_LOC_QMAKE_EXE:FILEPATH={0}/qmake'.format(qt_bin),
                '-DVISIT_QT_DIR:PATH=' + spec['qt'].prefix,
                '-DVISIT_QWT_DIR:PATH=' + spec['qwt'].prefix
            ])
        else:
            args.append('-DVISIT_SERVER_COMPONENTS_ONLY=ON')
            args.append('-DVISIT_ENGINE_ONLY=ON')

        if '+hdf5' in spec:
            args.append(
                '-DVISIT_HDF5_DIR:PATH={0}'.format(spec['hdf5'].prefix))
            if '+mpi' in spec:
                args.append('-DVISIT_HDF5_MPI_DIR:PATH={0}'.format(
                    spec['hdf5'].prefix))

        if '+silo' in spec:
            args.append(
                '-DVISIT_SILO_DIR:PATH={0}'.format(spec['silo'].prefix))

        if '+mpi' in spec:
            args.append('-DVISIT_PARALLEL=ON')
            args.append('-DVISIT_C_COMPILER={0}'.format(spec['mpi'].mpicc))
            args.append('-DVISIT_CXX_COMPILER={0}'.format(spec['mpi'].mpicxx))
            args.append('-DVISIT_MPI_COMPILER={0}'.format(spec['mpi'].mpicxx))

        return args
