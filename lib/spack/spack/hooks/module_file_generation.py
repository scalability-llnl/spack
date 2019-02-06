# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import spack.modules
import spack.modules.common
import llnl.util.tty as tty

try:
    enabled = spack.config.get('modules:enable')
except KeyError:
    tty.debug('NO MODULE WRITTEN: list of enabled module files is empty')
    enabled = []


def _for_each_enabled(spec, method_name):
    """Calls a method for each enabled module"""
    if spec.external_module:
        tty.debug("Skip module generation for external with"
                  " preexisting module: " + spec.format())
        return
    for name in enabled:
        generator = spack.modules.module_types[name](spec)
        try:
            getattr(generator, method_name)()
        except RuntimeError as e:
            msg = 'cannot perform the requested {0} operation on module files'
            msg += ' [{1}]'
            tty.warn(msg.format(method_name, str(e)))


post_install = lambda spec: _for_each_enabled(spec, 'write')
post_uninstall = lambda spec: _for_each_enabled(spec, 'remove')
