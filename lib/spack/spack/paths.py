# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
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


class Paths:
    #: This file lives in $prefix/lib/spack/spack/__file__
    prefix = ancestor(__file__, 4)

    #: synonym for prefix
    spack_root = prefix

    #: bin directory in the spack prefix
    bin_path = os.path.join(prefix, "bin")

    #: The spack script itself
    spack_script = os.path.join(bin_path, "spack")

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
    share_path            = os.path.join(prefix, "share", "spack")

    # Paths to built-in Spack repositories.
    packages_path      = os.path.join(repos_path, "builtin")
    mock_packages_path = os.path.join(repos_path, "builtin.mock")

    #: User configuration location
    _user_config_path = os.path.expanduser('~/.spack')

    opt_path        = os.path.join(prefix, "opt")
    etc_path        = os.path.join(prefix, "etc")
    system_etc_path = '/etc'

    # GPG paths.
    gpg_keys_path      = os.path.join(var_path, "gpg")
    mock_gpg_data_path = os.path.join(var_path, "gpg.mock", "data")
    mock_gpg_keys_path = os.path.join(var_path, "gpg.mock", "keys")
    gpg_path           = os.path.join(opt_path, "spack", "gpg")

    @property
    def user_config_path(self):
        """Return the path to the user configuration directory"""
        return self._user_config_path

    @user_config_path.setter
    def user_config_path(self, arg):
        """Set the user_config_path"""
        self._user_config_path = arg


# The following allows the Paths() class to replace this module in sys.modules:
#
# From Guido van Rossum:
#   (https://mail.python.org/pipermail/python-ideas/2012-May/014969.html)
# There is actually a hack that is occasionally used and recommended: a module
# can define a class with the desired functionality, and then at the end,
# replace itself in sys.modules with an instance of that class (or with the
# class, if you insist, but that's generally less useful). E.g.:
#
#  # module foo.py
#
#    import sys
#
#    class Foo:
#        def funct1(self, <args>): <code>
#        def funct2(self, <args>): <code>
#
#    sys.modules[__name__] = Foo()
#
# This works because the import machinery is actively enabling this hack, and
# as its final step pulls the actual module out of sys.modules, after loading
# it. (This is no accident. The hack was proposed long ago and we decided we
# liked enough to support it in the import machinery.)

# But why? We want user_config_path to provide an API for modifying the
# user_config_path
import sys  # noqa: E402

sys.modules[__name__] = Paths()
