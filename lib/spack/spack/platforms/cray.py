# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os
import os.path
import re
import platform

import archspec.cpu

import llnl.util.tty as tty
from spack.paths import build_env_path
from spack.util.executable import Executable
from spack.architecture import Platform, Target, NoPlatformError
from spack.operating_systems.cray_frontend import CrayFrontend
from spack.operating_systems.cray_backend import CrayBackend
from spack.util.module_cmd import module


_craype_name_to_target_name = {
    'x86-cascadelake': 'cascadelake',
    'x86-naples': 'zen',
    'x86-rome': 'zen2',
    'x86-skylake': 'skylake_avx512',
    'mic-knl': 'mic_knl',
    'interlagos': 'bulldozer',
    'abudhabi': 'piledriver',
}


def _target_name_from_craype_target_name(name):
    return _craype_name_to_target_name.get(name, name)


class Cray(Platform):
    priority = 10

    def __init__(self):
        ''' Create a Cray system platform.

        Target names should use craype target names but not include the
        'craype-' prefix. Uses first viable target from:
          self
          envars [SPACK_FRONT_END, SPACK_BACK_END]
          configuration file "targets.yaml" with keys 'front_end', 'back_end'
          scanning /etc/bash/bashrc.local for back_end only
        '''
        super(Cray, self).__init__('cray')

        # Make all craype targets available.
        for target in self._avail_targets():
            name = _target_name_from_craype_target_name(target)
            self.add_target(name, Target(name, 'craype-%s' % target))

        self.back_end = os.environ.get('SPACK_BACK_END',
                                       self._default_target_from_env())
        self.default = self.back_end
        if self.back_end not in self.targets:
            # We didn't find a target module for the backend
            raise NoPlatformError()

        # Setup frontend targets
        for name in archspec.cpu.TARGETS:
            if name not in self.targets:
                self.add_target(name, Target(name))
        self.front_end = os.environ.get(
            'SPACK_FRONT_END', archspec.cpu.host().name
        )
        if self.front_end not in self.targets:
            self.add_target(self.front_end, Target(self.front_end))

        front_distro = CrayFrontend()
        back_distro = CrayBackend()

        self.default_os = str(back_distro)
        self.back_os = self.default_os
        self.front_os = str(front_distro)

        self.add_operating_system(self.back_os, back_distro)
        if self.front_os != self.back_os:
            self.add_operating_system(self.front_os, front_distro)

    @classmethod
    def setup_platform_environment(cls, pkg, env):
        """ Change the linker to default dynamic to be more
            similar to linux/standard linker behavior
        """
        # Unload these modules to prevent any silent linking or unnecessary
        # I/O profiling in the case of darshan.
        modules_to_unload = ["cray-mpich", "darshan", "cray-libsci", "altd"]
        for mod in modules_to_unload:
            module('unload', mod)

        env.set('CRAYPE_LINK_TYPE', 'dynamic')
        cray_wrapper_names = os.path.join(build_env_path, 'cray')

        if os.path.isdir(cray_wrapper_names):
            env.prepend_path('PATH', cray_wrapper_names)
            env.prepend_path('SPACK_ENV_PATH', cray_wrapper_names)

        # Makes spack installed pkg-config work on Crays
        env.append_path("PKG_CONFIG_PATH", "/usr/lib64/pkgconfig")
        env.append_path("PKG_CONFIG_PATH", "/usr/local/lib64/pkgconfig")

        # CRAY_LD_LIBRARY_PATH is used at build time by the cray compiler
        # wrappers to augment LD_LIBRARY_PATH. This is to avoid long load
        # times at runtime. This behavior is not always respected on cray
        # "cluster" systems, so we reproduce it here.
        if os.environ.get('CRAY_LD_LIBRARY_PATH'):
            env.prepend_path('LD_LIBRARY_PATH',
                             os.environ['CRAY_LD_LIBRARY_PATH'])

    @classmethod
    def detect(cls):
        """
        Detect whether this system is a Cray machine.

        We detect the Cray platform based on the availability through `module`
        of the Cray programming environment. If this environment is available,
        we can use it to find compilers, target modules, etc. If the Cray
        programming environment is not available via modules, then we will
        treat it as a standard linux system, as the Cray compiler wrappers
        and other components of the Cray programming environment are
        irrelevant without module support.
        """
        return 'opt/cray' in os.environ.get('MODULEPATH', '')

    def _default_target_from_env(self):
        '''Set and return the default CrayPE target loaded in a clean login
        session.

        A bash subshell is launched with a wiped environment and the list of
        loaded modules is parsed for the first acceptable CrayPE target.
        '''
        # env -i /bin/bash -lc echo $CRAY_CPU_TARGET 2> /dev/null
        if getattr(self, 'default', None) is None:
            bash = Executable('/bin/bash')
            output = bash(
                '--norc', '--noprofile', '-lc', 'echo $CRAY_CPU_TARGET',
                env={'TERM': os.environ.get('TERM', '')},
                output=str, error=os.devnull
            )
            default_from_module = ''.join(output.split())  # rm all whitespace
            if default_from_module:
                tty.debug("Found default module:%s" % default_from_module)
                return default_from_module
            else:
                front_end = archspec.cpu.host().name
                if front_end in list(
                        map(lambda x: _target_name_from_craype_target_name(x),
                            self._avail_targets())
                ):
                    tty.debug("default to front-end architecture")
                    return archspec.cpu.host().name
                else:
                    return platform.machine()

    def _avail_targets(self):
        '''Return a list of available CrayPE CPU targets.'''

        def modules_in_output(output):
            """Returns a list of valid modules parsed from modulecmd output"""
            return [i for i in re.split(r'\s\s+|\n', output)]

        def target_names_from_modules(modules):
            # Craype- module prefixes that are not valid CPU targets.
            targets = []
            for mod in modules:
                if 'craype-' in mod:
                    name = mod[7:]
                    _n = name.replace('-', '_')  # test for mic-knl/mic_knl
                    is_target_name = (name in archspec.cpu.TARGETS or
                                      _n in archspec.cpu.TARGETS)
                    is_cray_target_name = name in _craype_name_to_target_name
                    if is_target_name or is_cray_target_name:
                        targets.append(name)

            return targets

        def modules_from_listdir():
            craype_default_path = '/opt/cray/pe/craype/default/modulefiles'
            if os.path.isdir(craype_default_path):
                return os.listdir(craype_default_path)
            return []

        if getattr(self, '_craype_targets', None) is None:
            strategies = [
                lambda: modules_in_output(module('avail', '-t', 'craype-')),
                modules_from_listdir
            ]
            for available_craype_modules in strategies:
                craype_modules = available_craype_modules()
                craype_targets = target_names_from_modules(craype_modules)
                if craype_targets:
                    self._craype_targets = craype_targets
                    break
            else:
                # If nothing is found add platform.machine()
                # to avoid Spack erroring out
                self._craype_targets = [platform.machine()]

        return self._craype_targets
