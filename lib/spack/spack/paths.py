# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Defines paths that are part of Spack's directory structure.

Do not import other ``spack`` modules here. This module is used
throughout Spack and should bring in a minimal number of external
dependencies.
"""
import os
import pathlib
from pathlib import PurePath

import llnl.util.filesystem

import spack.util.hash as hash

#: This file lives in $prefix/lib/spack/spack/__file__
prefix = str(PurePath(llnl.util.filesystem.ancestor(__file__, 4)))


# User configuration and caches in $HOME/.spack
# Override w/ `SPACK_USER_CONFIG_PATH`
def _get_user_config_path():
    return os.path.expanduser(os.getenv("SPACK_USER_CONFIG_PATH") or "~%s.spack" % os.sep)


# Configuration in /etc/spack on the system
# Override w/ `SPACK_SYSTEM_CONFIG_PATH`
def _get_system_config_path():
    return os.path.expanduser(
        os.getenv("SPACK_SYSTEM_CONFIG_PATH") or os.sep + os.path.join("etc", "spack")
    )


def dir_is_occupied(x, except_for=None):
    x = pathlib.Path(x)
    except_for = except_for or set()
    return x.is_dir() and bool(set(x.iterdir()) - except_for)


#: User configuration location
user_config_path = _get_user_config_path()

#: System configuration location
system_config_path = _get_system_config_path()

#: When Spack is provided by an admin to a user, the admin can
#: provide a config that only applies for the end-users
admin_customer_cfg = os.path.join(system_config_path, "admin-customer")

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
share_path = os.path.join(prefix, "share", "spack")
etc_path = os.path.join(prefix, "etc", "spack")
default_license_dir = os.path.join(etc_path, "licenses")
var_path = os.path.join(prefix, "var", "spack")


internal_install_tree_root = os.path.join(prefix, "opt", "spack")


def user_root():
    """Default install tree and config scope.

    Applies when $spack/opt is not an install tree.

    ~/<spack-prefix-hash>/
    """
    spack_prefix = prefix
    return pathlib.Path(user_config_path, hash.b32_hash(spack_prefix)[:7])


per_spack_user_root = str(user_root())

#: transient caches for Spack data (virtual cache, patch sha256 lookup, etc.)
#: placed in per-spack-instance user root
default_misc_cache_path = os.path.join(per_spack_user_root, "cache")

modules_base = None
for module_dir in ["lmod", "modules"]:
    if dir_is_occupied(os.path.join(share_path, module_dir)):
        modules_base = share_path
if not modules_base:
    modules_base = os.path.join(per_spack_user_root, "modules")

old_envs_path = os.path.join(var_path, "environments")
if dir_is_occupied(old_envs_path):
    envs_path = old_envs_path
else:
    envs_path = os.path.join(per_spack_user_root, "environments")

# TODO: we could shutil.mv resources from old paths to new paths

# $spack/var/spack is generally read-only. Older instances may
# write gpg keys or environments into ...var/
repos_path = os.path.join(var_path, "repos")
packages_path = os.path.join(repos_path, "builtin")
mock_packages_path = os.path.join(repos_path, "builtin.mock")

mock_gpg_data_path = os.path.join(var_path, "gpg.mock", "data")
mock_gpg_keys_path = os.path.join(var_path, "gpg.mock", "keys")


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

default_fetch_cache_path = os.path.join(user_cache_path, "downloads")

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

old_gpg_path = os.path.join("prefix", "opt" "spack", "gpg")
if dir_is_occupied(old_gpg_path):
    gpg_path = old_gpg_path
else:
    gpg_path = os.path.join(user_cache_path, "gpg")

old_gpg_keys_path = os.path.join(var_path, "gpg")
if dir_is_occupied(old_gpg_keys_path):
    gpg_keys_path = old_gpg_keys_path
else:
    gpg_keys_path = os.path.join(user_cache_path, "gpg-keys")

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
