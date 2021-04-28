# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import llnl.util.lang
import llnl.util.tty as tty


class ConcreteSpecRegistry(object):
    """
    The ConcreteSpecRegistry is just a dictionary containing all known
    concrete specs ever seen by spack, keyed by dag hash.
    """
    def __init__(self):
        self._registry = {}

    def populate(self):
        import spack.binary_distribution as bindist
        import spack.environment as ev
        import spack.store

        tty.debug('ConcreteSpecRegistry: populating')
        tty.debug('  db specs:')
        for key, spec in spack.store.db.all_specs():
            tty.debug('    {0} -> {1}'.format(key, spec.name))
            self._registry[key] = spec

        tty.debug('  buildcache specs:')
        bindist.binary_index.update()
        for spec in bindist.binary_index.get_all_built_specs():
            tty.debug('    {0} -> {1}'.format(spec.dag_hash(), spec.name))
            self._registry[spec.dag_hash()] = spec

        active_env = ev.get_env(None, None)
        if active_env:
            tty.debug('  environment specs:')
            for s in active_env.all_specs():
                tty.debug('    {0} -> {1}'.format(s.dag_hash(), s.name))
                self._registry[s.dag_hash()] = s

    def clear(self):
        # Seems to be needed by testing infrastructure so we are
        # forced to repopulate with relevant specs.
        self._registry = {}

    def get_by_hash(self, dag_hash):
        if not self._registry:
            self.populate()

        matches = [spec for h, spec in self._registry.items()
                   if h.startswith(dag_hash)]

        return matches


def _specs():
    return ConcreteSpecRegistry()


specs = llnl.util.lang.Singleton(_specs)
