# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import sys
import functools
from types import MethodType

from spack.package import PackageBase, InstallPhase, run_after


class DynamicInheritancePackage(PackageBase):
    build_system_class = 'DynamicInheritancePackage'

    # Classes from which to inherit install methods. Must be set by packager
    classes = {}

    # Selected class to inherit. Will be set dynamically
    cls = None

    # Some inheritance affects the package class. We will reset after install.
    old_cls_dict = {}

    # All phase names from all build system classes
    phases = ['set_build_system',
              'autoreconf',
              'configure', 'cmake', 'meson', 'edit', 'build_ext', 'qmake',
              'build', 'install', 'bdist',
              'unset_build_system']

    # Users can request non-standard phases available from a build system
    include_phases = []

    def set_build_system(self, spec, prefix):
        # Save old class information to restore later
        self.old_cls_dict = self.__class__.__dict__

        # get class and setup class variables
        for cls, when in self.classes.items():
            if spec.satisfies(when):
                self.cls = cls
                make_package_build_system(self, cls)

        # Remove phases not used by this build system
        # keep phases we have methods for and build system phases
        for ph in self.phases:
            if ph not in self.include_phases and ph not in self.cls.phases:
                setattr(self, '_InstallPhase_%s' % ph, None)

    def unset_build_system(self, spec, prefix):
        # This probably doesn't overwrite InstallPhase objects properly.
        # However, they are only used at build time, so we will call
        # set_build_system before attempting to use any of them. The
        # InstallPhase objects set to None are on the package, not the class,
        # so they don't need to be restored.
        self.__class__.__dict__ = self.old_cls_dict
        self.cls = None

    # Check that self.prefix is there after installation
    run_after('unset_build_system')(PackageBase.sanity_check_prefix)


def get_func_from_method(method):
    """Get the underlying function of a python method in a manner agnostic to
    the python version."""
    if sys.version_info >= (3, 0):
        func = method.__func__
    else:
        func = method.im_func
    return func


def steal_attribute(pkg, attribute):
    """
    Attaches attribute to pkg, while maintaining type information.

    Methods are turned to functions and attached via MethodType
    Properties are captured using fget and attached to the package class
    All others are attached directly.

    This will need to be revisited if/when a build system adds a multimethod
    function.
    """
    if isinstance(attribute, property):
        return property(attribute.fget)
    elif isinstance(attribute, MethodType):
        func = get_func_from_method(attribute)
        new_method = MethodType(func, pkg, pkg.__class__)
        return new_method
    elif isinstance(attribute, InstallPhase):
        name = '_InstallPhase_%s' % attribute.name
        pkg_attr = getattr(pkg.__class__, name)
        pkg_attr.run_before.extend(attribute.run_before)
        pkg_attr.run_after.extend(attribute.run_after)
        return pkg_attr
    else:
        return attribute


def make_package_build_system(pkg, build_system):
    """
    Attach all properties of build_system to pkg necessary to use build_system
    install phases.

    If the property already exists, no change is necessary for that attribute.
    It is up to the package writer to ensure the overriding property is of the
    appropriate type.
    """
    for name in build_system.__dict__:
        if not hasattr(pkg, name):
            new_attr = steal_attribute(pkg, getattr(build_system, name))
            if isinstance(new_attr, InstallPhase):
                # InstallPhse attributes update in place
                pass
            elif isinstance(new_attr, property):
                setattr(pkg.__class__, name, new_attr)
            else:
                setattr(pkg, name, new_attr)
        else:
            # special handling for multimethods that are overidden for some
            # specs but not for default. This will need updating if any build
            # system classes add multimethods.
            cur_attr = getattr(pkg, name)
            if isinstance(cur_attr, functools.partial):
                try:
                    multimethod = pkg.__class__.__dict__[name]
                except Exception:
                    continue
                new_attr = get_func_from_method(
                    steal_attribute(pkg,
                                    getattr(build_system, name))
                )
                if not multimethod.default:
                    multimethod.default = new_attr
                    functools.update_wrapper(multimethod, new_attr)
