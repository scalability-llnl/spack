# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os
import re
import sys

import spack.build_environment
import spack.config
import spack.spec
import spack.util.environment as environment
from spack import traverse
from spack.context import Context

#: Environment variable name Spack uses to track individually loaded packages
spack_loaded_hashes_var = "SPACK_LOADED_HASHES"


def prefix_inspections(platform):
    """Get list of prefix inspections for platform

    Arguments:
        platform (str): the name of the platform to consider. The platform
            determines what environment variables Spack will use for some
            inspections.

    Returns:
        A dictionary mapping subdirectory names to lists of environment
            variables to modify with that directory if it exists.
    """
    inspections = spack.config.get("modules:prefix_inspections")
    if isinstance(inspections, dict):
        return inspections

    inspections = {
        "bin": ["PATH"],
        "man": ["MANPATH"],
        "share/man": ["MANPATH"],
        "share/aclocal": ["ACLOCAL_PATH"],
        "lib/pkgconfig": ["PKG_CONFIG_PATH"],
        "lib64/pkgconfig": ["PKG_CONFIG_PATH"],
        "share/pkgconfig": ["PKG_CONFIG_PATH"],
        "": ["CMAKE_PREFIX_PATH"],
    }

    if platform == "darwin":
        inspections["lib"] = ["DYLD_FALLBACK_LIBRARY_PATH"]
        inspections["lib64"] = ["DYLD_FALLBACK_LIBRARY_PATH"]

    return inspections


def unconditional_environment_modifications(view):
    """List of environment (shell) modifications to be processed for view.

    This list does not depend on the specs in this environment"""
    env = environment.EnvironmentModifications()

    for subdir, vars in prefix_inspections(sys.platform).items():
        full_subdir = os.path.join(view.root, subdir)
        for var in vars:
            env.prepend_path(var, full_subdir)

    return env


def project_env_mods(
    *specs: spack.spec.Spec, view, env: environment.EnvironmentModifications
) -> None:
    """Given a list of environment modifications, project paths changes to the view."""
    prefix_to_prefix = {s.prefix: view.get_projection_for_spec(s) for s in specs if not s.external}
    # Avoid empty regex if all external
    if not prefix_to_prefix:
        return
    prefix_regex = re.compile("|".join(re.escape(p) for p in prefix_to_prefix.keys()))
    for mod in env.env_modifications:
        if isinstance(mod, environment.NameValueModifier):
            mod.value = prefix_regex.sub(lambda m: prefix_to_prefix[m.group(0)], mod.value)


def environment_modifications_for_specs(
    *specs: spack.spec.Spec, view=None, set_package_py_globals: bool = True
):
    """List of environment (shell) modifications to be processed for spec.

    This list is specific to the location of the spec or its projection in
    the view.

    Args:
        specs: spec(s) for which to list the environment modifications
        view: view associated with the spec passed as first argument
        set_package_py_globals: whether or not to set the global variables in the
            package.py files (this may be problematic when using buildcaches that have
            been built on a different but compatible OS)
    """
    env = environment.EnvironmentModifications()
    topo_ordered = list(
        traverse.traverse_nodes(specs, root=True, deptype=("run", "link"), order="topo")
    )

    # Static environment changes (prefix inspections)
    for s in reversed(topo_ordered):
        static = environment.inspect_path(
            s.prefix, prefix_inspections(s.platform), exclude=environment.is_system_path
        )
        env.extend(static)

    # Dynamic environment changes (setup_run_environment etc)
    setup_context = spack.build_environment.SetupContext(*specs, context=Context.RUN)
    if set_package_py_globals:
        setup_context.set_all_package_py_globals()
    env.extend(setup_context.get_env_modifications())

    # Apply view projections if any.
    if view:
        project_env_mods(*topo_ordered, view=view, env=env)

    return env
