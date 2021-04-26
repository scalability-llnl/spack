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
      * on_install_failure(exception)

   This can be used to implement support for things like module
   systems (e.g. modules, lmod, etc.) or to add other custom
   features.
"""
import os.path

import llnl.util.lang
import spack.paths


@llnl.util.lang.memoized
def all_hook_modules():
    modules, last_module = [], None
    for name in llnl.util.lang.list_modules(spack.paths.hooks_path):
        module_name = __name__ + '.' + name
        module_path = os.path.join(spack.paths.hooks_path, name) + ".py"

        module_obj = llnl.util.lang.load_module_from_file(
            module_name, module_path
        )
        if name == 'write_install_manifest':
            last_module = module_obj
        else:
            modules.append(module_obj)

    # put `write_install_manifest` as the last hook to run
    if last_module:
        modules.append(last_module)

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


# pre/post install and run by the install subprocess
pre_install = HookRunner('pre_install')
post_install = HookRunner('post_install')

# These hooks are run within an install subprocess
pre_uninstall = HookRunner('pre_uninstall')
post_uninstall = HookRunner('post_uninstall')
on_phase_success = HookRunner('on_phase_success')
on_phase_error = HookRunner('on_phase_error')

# These are hooks in installer.py, before starting install subprocess
on_install_start = HookRunner('on_install_start')
on_install_success = HookRunner('on_install_success')
on_install_failure = HookRunner('on_install_failure')

# Analyzer hooks
on_analyzer_save = HookRunner('on_analyzer_save')
