# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import spack.config
import spack.modules
import spack.modules.common
import llnl.util.tty as tty


def _for_each_enabled(spec, method_name):
    """Calls a method for each enabled module"""
    for name in spack.config.get('modules', {}):
        enabled = spack.config.get('modules:%s:enable' % name)
        if not enabled:
            tty.debug('NO MODULE WRITTEN: list of enabled module files is empty')
            return

        for type in enabled:
            generator = spack.modules.module_types[type](spec, name)
            try:
                getattr(generator, method_name)()
            except RuntimeError as e:
                msg = 'cannot perform the requested {0} operation on module files'
                msg += ' [{1}]'
                tty.warn(msg.format(method_name, str(e)))


def post_install(spec):
    # If the spec is installed through an environment, we delegate to
    # the post_env_write hook so that spack can manage interactions between
    # env views and modules
    import spack.environment  # break import cycle
    env = spack.environment.get_env({}, '')
    if not env:
        _for_each_enabled(spec, 'write')


def post_uninstall(spec):
    _for_each_enabled(spec, 'remove')


def post_env_write(env):
    for spec in env.new_installs:
        _for_each_enabled(spec, 'write')
