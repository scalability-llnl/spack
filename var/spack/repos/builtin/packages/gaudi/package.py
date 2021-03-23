# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
from spack.pkg.builtin.boost import Boost


class Gaudi(CMakePackage):
    """An experiment-independent HEP event data processing framework"""

    homepage = "http://gaudi.web.cern.ch/gaudi/"
    git      = "https://gitlab.cern.ch/gaudi/Gaudi.git"
    url      = "https://gitlab.cern.ch/gaudi/Gaudi/-/archive/v33r1/Gaudi-v33r1.tar.gz"

    tags = ['hep']

    version('master', branch='master')
    version('35.0', sha256='c01b822f9592a7bf875b9997cbeb3c94dea97cb13d523c12649dbbf5d69b5fa6')
    version('34.0', sha256='28fc4abb5a6b08da5a6b1300451c7e8487f918b055939877219d454abf7668ae')
    version('33.2', sha256='26aaf9c4ff237a60ec79af9bd18ad249fc91c16e297ba77e28e4a256123db6e5')
    version('33.1', sha256='7eb6b2af64aeb965228d4b6ea66c7f9f57f832f93d5b8ad55c9105235af5b042')
    version('33.0', sha256='76a967c41f579acc432593d498875dd4dc1f8afd5061e692741a355a9cf233c8')
    version('32.2', sha256='e9ef3eb57fd9ac7b9d5647e278a84b2e6263f29f0b14dbe1321667d44d969d2e')
    version('31.0',    commit='aeb156f0c40571b5753a9e1dab31e331491b2f3e')
    version('30.5',    commit='2c70e73ee5b543b26197b90dd59ea4e4d359d230')

    maintainers = ['drbenmorgan', "vvolkl"]

    variant('optional', default=False,
            description='Build most optional components and tests')
    variant('docs', default=False,
            description='Build documentation with Doxygen')
    variant('vtune', default=False,
            description='Build with Intel VTune profiler support')

    # only build subdirectory GaudiExamples when +optional
    patch("build_testing.patch", when="@:34.99")
    # fixes for the cmake config which could not find newer boost versions
    patch("link_target_fixes.patch", when="@33.0:34.99")
    patch("link_target_fixes32.patch", when="@:32.2")

    # These dependencies are needed for a minimal Gaudi build
    depends_on('aida')
    depends_on('boost@1.67.0: +python')

    # TODO: replace this with an explicit list of components of Boost,
    # for instance depends_on('boost +filesystem')
    # See https://github.com/spack/spack/pull/22303 for reference
    depends_on(Boost.with_default_variants)
    depends_on('clhep')
    depends_on('cmake', type='build')
    depends_on('cppgsl')
    depends_on('fmt', when='@33.2:')
    depends_on('intel-tbb')
    depends_on('uuid')
    depends_on('nlohmann-json', when="@35.0:")
    depends_on('python', type=('build', 'run'))
    depends_on('python@:3.7.99', when='@32.2:34.99', type=('build', 'run'))
    depends_on('python@:2.99.99', when='@:32.1', type=('build', 'run'))
    depends_on('py-setuptools@:45.99.99', when='^python@:2.7.99', type='build')
    depends_on('py-six', type=('build', 'run'))
    depends_on('py-xenv@1:', type=('build', 'run'))
    depends_on('range-v3')
    depends_on('root +python +root7 +ssl +tbb +threads')
    depends_on('zlib')

    # todo: this should be a test dependency only,
    depends_on('py-nose', when="@35.0", type=('build', 'run'))

    # Adding these dependencies triggers the build of most optional components
    depends_on('cppgsl', when='+optional')
    depends_on('cppunit', when='+optional')
    depends_on('doxygen +graphviz', when='+docs')
    depends_on('gperftools', when='+optional')
    depends_on('gdb', when='+optional')
    depends_on('gsl', when='+optional')
    depends_on('heppdt@:2.99.99', when='+optional')
    depends_on('jemalloc', when='+optional')
    depends_on('libpng', when='+optional')
    depends_on('libunwind', when='+optional')
    depends_on('py-networkx@:2.2', when='+optional ^python@:2.7.99')
    depends_on('py-networkx', when='+optional ^python@3.0.0:')
    depends_on('py-setuptools', when='+optional')
    depends_on('py-nose', when='+optional')
    depends_on('relax', when='@:33.99 +optional')
    depends_on('xerces-c', when='+optional')
    # NOTE: pocl cannot be added as a minimal OpenCL implementation because
    #       ROOT does not like being exposed to LLVM symbols.

    # The Intel VTune dependency is taken aside because it requires a license
    depends_on('intel-parallel-studio -mpi +vtune', when='+vtune')

    def cmake_args(self):
        args = [
            self.define_from_variant("BUILD_TESTING",             "optional"),
            self.define_from_variant("GAUDI_USE_AIDA",            "optional"),
            self.define_from_variant("GAUDI_USE_CPPUNIT",         "optional"),
            self.define_from_variant("GAUDI_USE_HEPPDT",          "optional"),
            self.define_from_variant("GAUDI_USE_JEMALLOC",        "optional"),
            self.define_from_variant("GAUDI_USE_UNWIND",          "optional"),
            self.define_from_variant("GAUDI_USE_XERCESC",         "optional"),
            self.define_from_variant("GAUDI_USE_DOXYGEN",         "docs"),
            # needed to build core services like rndmsvc
            self.define("GAUDI_USE_CLHEP", True),
            self.define("GAUDI_USE_PYTHON_MAJOR",
                        str(self.spec['python'].version.up_to(1))),
            # todo:
            self.define("GAUDI_USE_INTELAMPLIFIER",  False),
            self.define("GAUDI_USE_GPERFTOOLS",      False), ]
        # this is not really used in spack builds, but needs to be set
        if self.spec.version < Version('34.99'):
            args.append("-DHOST_BINARY_TAG=x86_64-linux-gcc9-opt")
        return args

    def setup_run_environment(self, env):
        # environment as in Gaudi.xenv
        env.prepend_path('PATH', self.prefix.scripts)
        env.prepend_path('PYTHONPATH', self.prefix.python)
        env.prepend_path('ROOT_INCLUDE_PATH', self.prefix.include)

    def url_for_version(self, version):
        major = str(version[0])
        minor = str(version[1])
        url = "https://gitlab.cern.ch/gaudi/Gaudi/-/archive/v{0}r{1}/Gaudi-v{0}r{1}.tar.gz".format(major, minor)
        return url
