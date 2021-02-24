from spack import *


class Mdsplus(AutotoolsPackage):
    """A set of software tools for data acquisition and storage and a
    methodology for management of complex scientific data."""
    homepage = "https://mdsplus.org"
    git      = "https://github.com/MDSplus/mdsplus.git"

    maintainers = ['wmvanvliet']

    parallel = False

    version('stable', commit='83928a157ee0a5875135aeee0996634ecb802523',
            submodules=True)

    # Autotools needed for building
    depends_on('autoconf', type='build')
    depends_on('autoconf-archive', type='build')
    depends_on('automake', type='build')
    depends_on('libtool', type='build')
    depends_on('m4', type='build')
    depends_on('pkgconfig', type='build')

    # Libs needed for building and linking
    depends_on('libxml2')
    depends_on('readline')

    # GUI bindings
    depends_on('motif')

    # Language bindings
    depends_on('java', type=('build', 'run'))
    depends_on('python', type='run')
    depends_on('py-numpy', type='run')

    def autoreconf(self, spec, prefix):
        bash = which('bash')
        bash('./bootstrap')

    def setup_run_environment(self, env):
        env.set('MDSPLUS_DIR', self.prefix)
        env.prepend_path('PYTHONPATH', '{0}/python'.format(self.prefix))
