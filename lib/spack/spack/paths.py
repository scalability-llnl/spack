# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Defines paths that are part of Spack's directory structure.

Do not import other ``spack`` modules here. This module is used
throughout Spack and should bring in a minimal number of external
dependencies.
"""
import os
from pathlib import PurePath

import llnl.util.filesystem

#: This file lives in $prefix/lib/spack/spack/__file__
prefix = str(PurePath(llnl.util.filesystem.ancestor(__file__, 4)))

#: synonym for prefix
spack_root = prefix

#: bin directory in the spack prefix
bin_path = os.path.join(prefix, "bin")

#: The spack script itself
spack_script = os.path.join(bin_path, "spack")

#: The sbang script in the spack installation
sbang_script = os.path.join(bin_path, "sbang")

# spack directory hierarchy
lib_path = os.path.join(prefix, "lib", "spack")
external_path = os.path.join(lib_path, "external")
build_env_path = os.path.join(lib_path, "env")
module_path = os.path.join(lib_path, "spack")
command_path = os.path.join(module_path, "cmd")
analyzers_path = os.path.join(module_path, "analyzers")
platform_path = os.path.join(module_path, "platforms")
compilers_path = os.path.join(module_path, "compilers")
build_systems_path = os.path.join(module_path, "build_systems")
operating_system_path = os.path.join(module_path, "operating_systems")
test_path = os.path.join(module_path, "test")
hooks_path = os.path.join(module_path, "hooks")
opt_path = os.path.join(prefix, "opt")
share_path = os.path.join(prefix, "share", "spack")
etc_path = os.path.join(prefix, "etc", "spack")

#
# Things in $spack/etc/spack
#
default_license_dir = os.path.join(etc_path, "licenses")

#
# Things in $spack/var/spack
#
var_path = os.path.join(prefix, "var", "spack")

# read-only things in $spack/var/spack
repos_path = os.path.join(var_path, "repos")
packages_path = os.path.join(repos_path, "builtin")
mock_packages_path = os.path.join(repos_path, "builtin.mock")

#
# Writable things in $spack/var/spack
# TODO: Deprecate these, as we want a read-only spack prefix by default.
# TODO: These should probably move to user cache, or some other location.
#
# fetch cache for downloaded files
default_fetch_cache_path = os.path.join(var_path, "cache")

# GPG paths.
gpg_keys_path = os.path.join(var_path, "gpg")
mock_gpg_data_path = os.path.join(var_path, "gpg.mock", "data")
mock_gpg_keys_path = os.path.join(var_path, "gpg.mock", "keys")
gpg_path = os.path.join(opt_path, "spack", "gpg")


# Below paths are where Spack can write information for the user.
# Some are caches, some are not exactly caches.
#
# The options that start with `default_` below are overridable in
# `config.yaml`, but they default to use `user_cache_path/<location>`.
#
# You can override the top-level directory (the user cache path) by
# setting `SPACK_USER_CACHE_PATH`. Otherwise it defaults to ~/.spack.
#
def _get_user_cache_path():
    return os.path.expanduser(os.getenv("SPACK_USER_CACHE_PATH") or "~%s.spack" % os.sep)


user_cache_path = str(PurePath(_get_user_cache_path()))

#: junit, cdash, etc. reports about builds
reports_path = os.path.join(user_cache_path, "reports")

#: installation test (spack test) output
default_test_path = os.path.join(user_cache_path, "test")

#: spack monitor analysis directories
default_monitor_path = os.path.join(reports_path, "monitor")

#: git repositories fetched to compare commits to versions
user_repos_cache_path = os.path.join(user_cache_path, "git_repos")

#: bootstrap store for bootstrapping clingo and other tools
default_user_bootstrap_path = os.path.join(user_cache_path, "bootstrap")

#: transient caches for Spack data (virtual cache, patch sha256 lookup, etc.)
default_misc_cache_path = os.path.join(user_cache_path, "cache")


# Below paths pull configuration from the host environment.
#
# There are three environment variables you can use to isolate spack from
# the host environment:
# - `SPACK_USER_CONFIG_PATH`: override `~/.spack` location (for config and caches)
# - `SPACK_SYSTEM_CONFIG_PATH`: override `/etc/spack` configuration scope.
# - `SPACK_DISABLE_LOCAL_CONFIG`: disable both of these locations.


# User configuration and caches in $HOME/.spack
def _get_user_config_path():
    return os.path.expanduser(os.getenv("SPACK_USER_CONFIG_PATH") or "~%s.spack" % os.sep)


# Configuration in /etc/spack on the system
def _get_system_config_path():
    return os.path.expanduser(
        os.getenv("SPACK_SYSTEM_CONFIG_PATH") or os.sep + os.path.join("etc", "spack")
    )


#: User configuration location
user_config_path = _get_user_config_path()

#: System configuration location
system_config_path = _get_system_config_path()

#: Recorded directory where spack command was originally invoked
spack_working_dir = None


def set_working_dir():
    """Change the working directory to getcwd, or spack prefix if no cwd."""
    global spack_working_dir
    try:
        spack_working_dir = os.getcwd()
    except OSError:
        os.chdir(prefix)
        spack_working_dir = prefix
