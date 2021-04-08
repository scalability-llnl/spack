# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""This package contains modules with hooks for various stages in the
   Spack install process.  You can add modules here and they'll be
   executed by package at various times during the package lifecycle.

   Each hook is just a function that takes a package as a parameter.
   Hooks are not executed in any particular order.

   Currently the following hooks are supported:

      * pre_install(spec)
      * post_install(spec)
      * pre_uninstall(spec)
      * post_uninstall(spec)

   This can be used to implement support for things like module
   systems (e.g. modules, lmod, etc.) or to add other custom
   features.
"""
import os.path

import spack.paths
import spack.util.imp as simp
from llnl.util.lang import memoized, list_modules


@memoized
def all_hook_modules():
    modules = []
    for name in list_modules(spack.paths.hooks_path):
        mod_name = __name__ + '.' + name
        path = os.path.join(spack.paths.hooks_path, name) + ".py"
        mod = simp.load_source(mod_name, path)

        if name == 'write_install_manifest':
            last_mod = mod
        else:
            modules.append(mod)

    # put `write_install_manifest` as the last hook to run
    modules.append(last_mod)
    return modules


class HookRunner(object):

    def __init__(self, hook_name):
        self.hook_name = hook_name

    def __call__(self, *args, **kwargs):
        for module in all_hook_modules():
            if hasattr(module, self.hook_name):
                hook = getattr(module, self.hook_name)
                if hasattr(hook, '__call__'):
                    hook(*args, **kwargs)


pre_install = HookRunner('pre_install')
post_install = HookRunner('post_install')

pre_uninstall = HookRunner('pre_uninstall')
post_uninstall = HookRunner('post_uninstall')

on_install_success = HookRunner('on_install_success')
