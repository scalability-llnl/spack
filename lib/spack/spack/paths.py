# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Defines paths that are part of Spack's directory structure.

Do not import other ``spack`` modules here. This module is used
throughout Spack and should bring in a minimal number of external
dependencies.
"""
import os
from llnl.util.filesystem import ancestor

#: This file lives in $prefix/lib/spack/spack/__file__
prefix = ancestor(__file__, 4)

#: synonym for prefix
spack_root = prefix

#: bin directory in the spack prefix
bin_path = os.path.join(prefix, "bin")

#: The spack script itself
spack_script = os.path.join(bin_path, "spack")

#: The sbang script in the spack installation
sbang_script = os.path.join(bin_path, "sbang")

# spack directory hierarchy
lib_path              = os.path.join(prefix, "lib", "spack")
external_path         = os.path.join(lib_path, "external")
build_env_path        = os.path.join(lib_path, "env")
module_path           = os.path.join(lib_path, "spack")
command_path          = os.path.join(module_path, "cmd")
platform_path         = os.path.join(module_path, 'platforms')
compilers_path        = os.path.join(module_path, "compilers")
build_systems_path    = os.path.join(module_path, 'build_systems')
operating_system_path = os.path.join(module_path, 'operating_systems')
test_path             = os.path.join(module_path, "test")
hooks_path            = os.path.join(module_path, "hooks")
var_path              = os.path.join(prefix, "var", "spack")
repos_path            = os.path.join(var_path, "repos")
tests_path            = os.path.join(var_path, "tests")
share_path            = os.path.join(prefix, "share", "spack")

# Paths to built-in Spack repositories.
packages_path      = os.path.join(repos_path, "builtin")
mock_packages_path = os.path.join(repos_path, "builtin.mock")

#: User configuration location
user_config_path = os.path.expanduser('~/.spack')
user_bootstrap_path = os.path.join(user_config_path, 'bootstrap')
user_bootstrap_store = os.path.join(user_bootstrap_path, 'store')

opt_path        = os.path.join(prefix, "opt")
etc_path        = os.path.join(prefix, "etc")
system_etc_path = '/etc'

# GPG paths.
gpg_keys_path      = os.path.join(var_path, "gpg")
mock_gpg_data_path = os.path.join(var_path, "gpg.mock", "data")
mock_gpg_keys_path = os.path.join(var_path, "gpg.mock", "keys")
gpg_path           = os.path.join(opt_path, "spack", "gpg")
