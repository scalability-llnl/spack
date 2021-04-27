# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Qgis(CMakePackage):
    """QGIS is a free and open-source cross-platform desktop geographic
    information system application that supports viewing, editing, and
    analysis of geospatial data.
    """

    homepage = "https://qgis.org"
    url      = "https://qgis.org/downloads/qgis-3.8.1.tar.bz2"

    maintainers = ['adamjstewart', 'Sinan81']

    version('3.18.2',   sha256='1913e4d5596bbc8b7d143f3defb18bf376f750a71f334f69d76af5deca7ecc5d')
    # Prefer latest long term release
    version('3.16.5',   sha256='525f469ad6e40dd7a8f09ebab5eb6a2dffc45939b99b7d937750cc04ed78d61c', preferred=True)
    version('3.14.16',  sha256='c9915c2e577f1812a2b35b678b123c58407e07824d73e5ec0dda13db7ca75c04')
    version('3.14.0',   sha256='1b76c5278def0c447c3d354149a2afe2562ac26cf0bcbe69b9e0528356d407b8')
    version('3.12.3',   sha256='c2b53815f9b994e1662995d1f25f90628156b996758f5471bffb74ab29a95220')
    version('3.12.2',   sha256='501f81715672205afd2c1a289ffc765aff96eaa8ecb49d079a58ef4d907467b8')
    version('3.12.1',   sha256='a7dc7af768b8960c08ce72a06c1f4ca4664f4197ce29c7fe238429e48b2881a8')
    version('3.12.0',   sha256='19e9c185dfe88cad7ee6e0dcf5ab7b0bbfe1672307868a53bf771e0c8f9d5e9c')
    version('3.10.10',  sha256='e21a778139823fb6cf12e4a38f00984fcc060f41abcd4f0af83642d566883839')
    version('3.10.7',   sha256='f6c02489e065bae355d2f4374b84a1624379634c34a770b6d65bf38eb7e71564')
    version('3.10.6',   sha256='a96791bf6615e4f8ecdbbb9a90a8ef14a12459d8c5c374ab22eb5f776f864bb5')
    version('3.10.5',   sha256='f3e1cc362941ec69cc21062eeaea160354ef71382b21dc4b3191c315447b4ce1')
    version('3.10.4',   sha256='a032e2b8144c2fd825bc26766f586cfb1bd8574bc72efd1aa8ce18dfff8b6c9f')
    version('3.10.3',   sha256='0869704df9120dd642996ff1ed50213ac8247650aa0640b62f8c9c581c05d7a7')
    version('3.10.2',   sha256='381cb01a8ac2f5379a915b124e9c830d727d2c67775ec49609c7153fe765a6f7')
    version('3.10.1',   sha256='466ac9fad91f266cf3b9d148f58e2adebd5b9fcfc03e6730eb72251e6c34c8ab')
    version('3.10.0',   sha256='25eb1c41d9fb922ffa337a720dfdceee43cf2d38409923f087c2010c9742f012')
    version('3.8.3',    sha256='3cca3e8483bc158cb8e972eb819a55a5734ba70f2c7da28ebc485864aafb17bd')
    version('3.8.2',    sha256='4d682f7625465a5b3596b3f7e83eddad86a60384fead9c81a6870704baffaddd')
    version('3.8.1',    sha256='d65c8e1c7471bba46f5017f261ebbef81dffb5843a24f0e7713a00f70785ea99')
    version('3.4.15',   sha256='81c93b72adbea41bd765294c0cdb09476a632d8b3f90101abc409ca9ea7fb04d')
    version('3.4.14',   sha256='e138716c7ea84011d3b28fb9c75e6a79322fb66f532246393571906a595d7261')

    variant('3d',               default=False,  description='Build QGIS 3D library')
    variant('analysis',         default=True,   description='Build QGIS analysis library')
    variant('apidoc',           default=False,  description='Build QGIS API doxygen documentation')
    variant('astyle',           default=False,  description='Contribute QGIS with astyle')
    variant('bindings',         default=True,   description='Build Python bindings')
    variant('clang_tidy',       default=False,  description='Use Clang tidy')
    variant('core',             default=True,   description='Build QGIS Core')
    variant('custom_widgets',   default=False,  description='Build QGIS custom widgets for Qt Designer')
    variant('desktop',          default=True,   description='Build QGIS desktop')
    variant('georeferencer',    default=True,   description='Build GeoReferencer plugin')
    variant('globe',            default=False,  description='Build Globe plugin')
    variant('grass7',           default=False,  description='Build with GRASS providers and plugin')
    variant('gui',              default=True,   description='Build QGIS GUI library and everything built on top of it')
    variant('internal_mdal',    default=True,   description='Build with MDAl support')
    variant('internal_o2',      default=True,   description='Download and locally include source of o2 library')
    variant('oauth2_plugin',    default=True,   description='Build OAuth2 authentication method plugin')
    variant('oracle',           default=False,  description='Build with Oracle support')
    variant('postgresql',       default=True,   description='Build with PostreSQL support')
    variant('py_compile',       default=False,  description='Byte compile Python modules in staged or installed locations')
    variant('qsciapi',          default=True,   description='Generate PyQGIS QScintilla2 API')
    variant('qspatialite',      default=False,  description='Build QSpatialite sql driver')
    variant('qt5serialport',    default=True,   description='Try Qt5SerialPort for GPS positioning')
    variant('qtmobility',       default=False,  description='Build QtMobility related code')
    variant('qtwebkit',         default=False,  description='Enable QtWebkit Support')
    variant('quick',            default=False,  description='Build QGIS Quick library')
    variant('qwtpolar',         default=False,  description='Build QwtPolar')
    variant('server',           default=False,  description='Build QGIS server')
    variant('staged_plugins',   default=True,   description='Stage-install core Python plugins to run from build directory')
    variant('thread_local',     default=True,   description='Use std::thread_local')
    variant('txt2tags',         default=False,  description='Generate PDF for txt2tags documentation')

    # Ref. for dependencies:
    # https://github.com/qgis/QGIS/blob/master/INSTALL.md
    depends_on('exiv2')
    depends_on('expat@1.95:')
    depends_on('gdal@2.1.0: +python', type=('build', 'link', 'run'))
    depends_on('geos@3.4.0:')
    depends_on('libspatialindex')
    depends_on('libspatialite@4.2.0:')
    depends_on('libzip')
    depends_on('libtasn1')
    depends_on('proj@4.4.0:')
    depends_on('py-psycopg2', type=('build', 'run'))  # TODO: is build dependency necessary?
    depends_on('py-pyqt4', when='@2')
    depends_on('py-pyqt5@5.3:', when='@3')
    depends_on('py-requests', type=('build', 'run'))  # TODO: is build dependency necessary?
    depends_on('python@2.7:2.8', type=('build', 'run'), when='@2')
    depends_on('python@3.0.0:', type=('build', 'run'), when='@3')
    depends_on('qca@2.2.1')
    depends_on('qjson')
    depends_on('qscintilla +python')
    depends_on('qt+dbus')
    depends_on('qtkeychain@0.5:', when='@3:')
    depends_on('qwt@5:')
    depends_on('qwtpolar')
    depends_on('sqlite@3.0.0: +column_metadata')
    depends_on('protobuf', when='@3.16.4:')

    # Runtime python dependencies, not mentioned in install instructions
    depends_on('py-pyyaml', type='run')
    depends_on('py-owslib', type='run')
    depends_on('py-jinja2', type='run')
    depends_on('py-pygments', type='run')

    # optionals
    depends_on('postgresql@8:', when='+postgresql')  # for PostGIS support
    depends_on('gsl', when='+georeferencer')  # for georeferencer
    # grass@7.8.1 is the first version that supports proj@6
    depends_on('grass@7:', type=('build', 'link', 'run'), when='+grass7')  # for georeferencer

    # The below dependencies are shown in cmake config
    # hdf5 and netcdf-c together run afoul of a concretizer bug.
    # netcdf-c already depends on hdf5
    # depends_on('hdf5').
    depends_on('netcdf-c')

    # build
    depends_on('cmake@3.0.0:', type='build')
    depends_on('flex@2.5.6:', type='build')
    depends_on('bison@2.4:', type='build')
    depends_on('pkgconfig', type='build')

    # Take care of conflicts using depends_on
    depends_on('qt@5.9.0:5.12.99', when='@3.8')
    depends_on('qt@5.9.0:', when='@3.10.0:')
    depends_on('qtkeychain@:1.5.99', when='^qt@4')
    depends_on('qt@:4', when='@2')
    # Help concretizer
    # +qsci_api is implied by qscintilla+python dependency
    depends_on('py-pyqt4 +qsci_api', when='@2')
    depends_on('py-pyqt5@5.3: +qsci_api', when='@3')

    patch('pyqt5.patch', when='@:3.14 ^qt@5')
    patch('pyqt5_3165x.patch', when='@3.16.5: ^qt@5')

    def cmake_args(self):
        spec = self.spec
        args = []
        # qtwebkit module was removed from qt as of version 5.6
        # needs to be compiled as a separate package
        args.extend([
                    '-DUSE_OPENCL=OFF',
                    # cmake couldn't determine the following paths
                    '-DEXPAT_LIBRARY={0}'.format(self.spec['expat'].libs),
                    '-DPOSTGRESQL_PREFIX={0}'.format(
                        self.spec['postgresql'].prefix),
                    '-DQSCINTILLA_INCLUDE_DIR=' +
                    self.spec['qscintilla'].prefix.include,
                    '-DQSCINTILLA_LIBRARY=' + self.spec['qscintilla'].prefix +
                    '/lib/libqscintilla2_qt5.so',
                    '-DLIBZIP_INCLUDE_DIR=' +
                    self.spec['libzip'].prefix.include,
                    '-DLIBZIP_CONF_INCLUDE_DIR=' +
                    self.spec['libzip'].prefix.lib.libzip.include,
                    '-DGDAL_CONFIG_PREFER_PATH=' +
                    self.spec['gdal'].prefix.bin,
                    '-DGEOS_CONFIG_PREFER_PATH=' +
                    self.spec['geos'].prefix.bin,
                    '-DGSL_CONFIG_PREFER_PATH=' + self.spec['gsl'].prefix.bin,
                    '-DPOSTGRES_CONFIG_PREFER_PATH=' +
                    self.spec['postgresql'].prefix.bin
                    ])

        args.extend([
            '-DWITH_3D={0}'.format(
                'TRUE' if '+3d' in spec else 'FALSE'),
            '-DWITH_ANALYSIS={0}'.format(
                'TRUE' if '+analysis' in spec else 'FALSE'),
            '-DWITH_APIDOC={0}'.format(
                'TRUE' if '+apidoc' in spec else 'FALSE'),
            '-DWITH_ASTYLE={0}'.format(
                'TRUE' if '+astyle' in spec else 'FALSE'),
            '-DWITH_BINDINGS={0}'.format(
                'TRUE' if '+bindings' in spec else 'FALSE'),
            '-DWITH_CLANG_TIDY={0}'.format(
                'TRUE' if '+clang_tidy' in spec else 'FALSE'),
            '-DWITH_CORE={0}'.format(
                'TRUE' if '+core' in spec else 'FALSE'),
            '-DWITH_CUSTOM_WIDGETS={0}'.format(
                'TRUE' if '+custom_widgets' in spec else 'FALSE'),
            '-DWITH_DESKTOP={0}'.format(
                'TRUE' if '+desktop' in spec else 'FALSE'),
            '-DWITH_GEOREFERENCER={0}'.format(
                'TRUE' if '+georeferencer' in spec else 'FALSE'),
            '-DWITH_GLOBE={0}'.format(
                'TRUE' if '+globe' in spec else 'FALSE'),
            '-DWITH_GUI={0}'.format(
                'TRUE' if '+gui' in spec else 'FALSE'),
            '-DWITH_INTERNAL_MDAL={0}'.format(
                'TRUE' if '+internal_mdal' in spec else 'FALSE'),
            '-DWITH_INTERNAL_O2={0}'.format(
                'ON' if '+internal_o2' in spec else 'OFF'),
            '-DWITH_OAUTH2_PLUGIN={0}'.format(
                'TRUE' if '+oauth2_plugin' in spec else 'FALSE'),
            '-DWITH_ORACLE={0}'.format(
                'TRUE' if '+oracle' in spec else 'FALSE'),
            '-DWITH_POSTGRESQL={0}'.format(
                'TRUE' if '+postgresql' in spec else 'FALSE'),
            '-DWITH_PY_COMPILE={0}'.format(
                'TRUE' if '+py_compile' in spec else 'FALSE'),
            '-DWITH_QSCIAPI={0}'.format(
                'TRUE' if '+qsciapi' in spec else 'FALSE'),
            '-DWITH_QSPATIALITE={0}'.format(
                'ON' if '+qspatialite' in spec else 'OFF'),
            '-DWITH_QT5SERIALPORT={0}'.format(
                'TRUE' if '+qt5serialport' in spec else 'FALSE'),
            '-DWITH_QTMOBILITY={0}'.format(
                'TRUE' if '+qtmobility' in spec else 'FALSE'),
            '-DWITH_QTWEBKIT={0}'.format(
                'ON' if '+qtwebkit' in spec else 'OFF'),
            '-DWITH_QUICK={0}'.format(
                'TRUE' if '+quick' in spec else 'FALSE'),
            '-DWITH_QWTPOLAR={0}'.format(
                'TRUE' if '+qwtpolar' in spec else 'FALSE'),
            '-DWITH_SERVER={0}'.format(
                'TRUE' if '+server' in spec else 'FALSE'),
            '-DWITH_STAGED_PLUGINS={0}'.format(
                'TRUE' if '+staged_plugins' in spec else 'FALSE'),
            '-DWITH_THREAD_LOCAL={0}'.format(
                'TRUE' if '+thread_local' in spec else 'FALSE'),
            '-DWITH_TXT2TAGS_PDF={0}'.format(
                'TRUE' if '+txt2tags_pdf' in spec else 'FALSE'),
        ])

        if '+grass7' in self.spec:
            args.extend([
                '-DWITH_GRASS7=ON',
                '-DGRASS_PREFIX7={0}'.format(self.spec['grass'].prefix),
                '-DGRASS_INCLUDE_DIR7={0}'.format(
                    self.spec['grass'].prefix.include)
            ])
        else:
            args.append('-DWITH_GRASS7=OFF')
        return args
