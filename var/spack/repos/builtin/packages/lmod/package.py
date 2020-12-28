# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from glob import glob

from spack.package import *


class Lmod(AutotoolsPackage):
    """Lmod is a Lua based module system that easily handles the MODULEPATH
    Hierarchical problem.

    Environment Modules provide a convenient way to dynamically change the
    users' environment through modulefiles. This includes easily adding or
    removing directories to the PATH environment variable. Modulefiles for
    Library packages provide environment variables that specify where the
    library and header files can be found.
    """

    homepage = 'https://www.tacc.utexas.edu/research-development/tacc-projects/lmod'
    url      = 'https://github.com/TACC/Lmod/archive/7.4.11.tar.gz'

    version('8.3',    sha256='c2c2e9e6b387b011ee617cb009a2199caac8bf200330cb8a065ceedee09e664a')
    version('8.2.10', sha256='15676d82235faf5c755a747f0e318badb1a5c3ff1552fa8022c67ff083ee9e2f')
    version('8.1.5',  sha256='3e5846d3d8e593cbcdfa0aed1474569bf5b5cfd19fd288de22051823d449d344')
    version('8.0.9',  sha256='9813c22ae4dd21eb3dc480f6ce307156512092b4bca954bf8aacc15944f23673')
    version('7.8.15', sha256='00a257f5073d656adc73045997c28f323b7a4f6d901f1c57b7db2b0cd6bee6e6')
    version('7.8.1',  sha256='74244c22cecd72777e75631f357d2e20ff7f2b9c2ef59e4e38b5a171b7b6eeea')
    version('7.8',    sha256='40388380a36a00c3ce929a9f88c8fffc93deeabf87a7c3f8864a82acad38c3ba')
    version('7.7.29', sha256='269235d07d8ea387a2578f90bb64cf8ad16b4f28dcce196b293eb48cf1f71fb4')
    version('7.7.13', sha256='6145f075e5d49e12fcf0e75bb38afb27f205d23ba3496c1ff6c8b2cbaa9908be')
    version('7.7',    sha256='090118fcecedbce5515cca8b77297f082686583aa06ca811b9703cd828f10e0a')
    version('7.6.14', sha256='f628ed2272bb26671d2c478afef2ddd88dce324748032bfe8d6f6c7747f00162')
    version('7.4.11', sha256='54c3629f6e455a4767dfb775e1b0ca46b8f217dcc0966bf0227c0ea11e0e0d62')
    version('7.4.10', sha256='7b37936ddbc574f03eb08579f1d1bb5fa8c476b55ee070dc3c432d96970e6562')
    version('7.4.9',  sha256='5aee6cc9cf0b27327c8b4f5fdfb9aa079d90aed685ee7853cbcc49c32b48a5d9')
    version('7.4.8',  sha256='a634989dcd34b0ad7bee95ca535765b7de886d9f9ef78cad5976122356d71169')
    version('7.4.5',  sha256='a4af6dcd3d9b209cc10467e6ce77301c0ec517437b70cfc567a3180030c4f404')
    version('7.4.1',  sha256='1d407c68a5a8c1ae9870a12303ba81d2a92b68f66ac7dd704ccffb65bfb873d9')
    version('7.3',    sha256='624e8ffb7527b380dc248cf7ddf36beecb91c762d840be447bc9a55bf8cd26c2')
    version('6.4.5',  sha256='741744a2837c9d92fceeccfebdc8e07ce4f4b7e56f67b214d317955bbd8786b7')
    version('6.4.1',  sha256='a260b4e42269a80b517c066ba8484658362ea095e80767a2376bbe33d9b070a5')
    version('6.3.7',  sha256='55ddb52cbdc0e2e389b3405229336df9aabfa582c874f5df2559ea264e2ee4ae')

    depends_on('lua@5.1:')
    depends_on('lua-luaposix', type=('build', 'run'))
    depends_on('lua-luafilesystem', type=('build', 'run'))
    depends_on('tcl', type=('build', 'link', 'run'))

    variant('auto_swap', default=True, description='Auto swapping of compilers, etc.')
    variant('redirect', default=False, description='Redirect messages to stdout (instead of stderr)')

    patch('fix_tclsh_paths.patch', when='@:6.4.3')
    patch('0001-fix-problem-with-MODULESHOME-and-issue-271.patch', when='@7.3.28:7.4.10')

    parallel = False

    def setup_build_environment(self, env):
        stage_lua_path = join_path(
            self.stage.source_path, 'src', '?.lua')
        env.append_path('LUA_PATH', stage_lua_path.format(
            version=self.version), separator=';')

    def patch(self):
        """The tcl scripts should use the tclsh that was discovered
           by the configure script.  Touch up their #! lines so that the
           sed in the Makefile's install step has something to work on.
           Requires the change in the associated patch file.fg"""
        if self.spec.version <= Version('6.4.3'):
            for tclscript in glob('src/*.tcl'):
                filter_file(r'^#!.*tclsh', '#!@path_to_tclsh@', tclscript)

    def configure_args(self):
        args = []

        if '+auto_swap' in self.spec:
            args.append('--with-autoSwap=yes')
        else:
            args.append('--with-autoSwap=no')

        if '+redirect' in self.spec:
            args.append('--with-redirect=yes')
        else:
            args.append('--with-redirect=no')

        return args
