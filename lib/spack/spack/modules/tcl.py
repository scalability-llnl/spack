# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""This module implements the classes necessary to generate TCL
non-hierarchical modules.
"""
import os.path
import string
from typing import Dict, Any  # novm

import llnl.util.tty as tty

import spack.config
import spack.projections as proj
import spack.tengine as tengine
from .common import BaseConfiguration, BaseFileLayout
from .common import BaseContext, BaseModuleFileWriter


#: TCL specific part of the configuration
def configuration(module_set_name):
    config_path = 'modules:%s:tcl' % module_set_name
    config = spack.config.get(config_path, {})
    if not config and module_set_name == 'default':
        # return old format for backward compatibility
        return spack.config.get('modules:tcl', {})
    return config


#: Caches the configuration {spec_hash: configuration}
configuration_registry = {}  # type: Dict[str, Any]


def make_configuration(spec, module_set_name):
    """Returns the tcl configuration for spec"""
    key = (spec.dag_hash(), module_set_name)
    try:
        return configuration_registry[key]
    except KeyError:
        return configuration_registry.setdefault(
            key, TclConfiguration(spec, module_set_name))


def make_layout(spec, module_set_name):
    """Returns the layout information for spec """
    conf = make_configuration(spec, module_set_name)
    return TclFileLayout(conf)


def make_context(spec, module_set_name):
    """Returns the context information for spec"""
    conf = make_configuration(spec, module_set_name)
    return TclContext(conf)


class TclConfiguration(BaseConfiguration):
    """Configuration class for tcl module files."""

    @property
    def conflicts(self):
        """Conflicts for this module file"""
        return self.conf.get('conflict', [])


class TclFileLayout(BaseFileLayout):
    """File layout for tcl module files."""


class TclContext(BaseContext):
    """Context class for tcl module files."""

    @tengine.context_property
    def prerequisites(self):
        """List of modules that needs to be loaded automatically."""
        return self._create_module_list_of('specs_to_prereq')

    @tengine.context_property
    def conflicts(self):
        """List of conflicts for the tcl module file."""
        fmts = []
        projection = proj.get_projection(self.conf.projections, self.spec)
        f = string.Formatter()
        for item in self.conf.conflicts:
            if len([x for x in f.parse(item)]) > 1:
                for naming_dir, conflict_dir in zip(
                        projection.split('/'), item.split('/')
                ):
                    if naming_dir != conflict_dir:
                        message = 'conflict scheme does not match naming '
                        message += 'scheme [{spec}]\n\n'
                        message += 'naming scheme   : "{nformat}"\n'
                        message += 'conflict scheme : "{cformat}"\n\n'
                        message += '** You may want to check your '
                        message += '`modules.yaml` configuration file **\n'
                        tty.error(message.format(spec=self.spec,
                                                 nformat=projection,
                                                 cformat=item))
                        raise SystemExit('Module generation aborted.')
                item = self.spec.format(item)
            fmts.append(item)
        # Substitute spec tokens if present
        return [self.spec.format(x) for x in fmts]


class TclModulefileWriter(BaseModuleFileWriter):
    """Writer class for tcl module files."""
    default_template = os.path.join('modules', 'modulefile.tcl')
