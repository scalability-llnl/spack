# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Testing Spack's windows registry interface"""



# Stub the winreg calls Spack makes with stubs useful for testing

def StubRegKey():
    def __init__(self, )


def OpenKeyEx(key, subname, **kwargs):
    """Testing wrapper around winreg.OpenKeyEx"""
    try:
        return winreg.OpenKeyEx(key, subname, **kwargs)
    except OSError as e:
        raise InvalidRegistryOperation("OpenKeyEx", e, key, subname, **kwargs) from e


def QueryInfoKeySuccess(key):
    """Testing wrapper around winreg.QueryInfoKey"""
    return len(key.subkeys), len(key.values.items()), len(0)


def QueryInfoKeyRaiseUnexpected(key):
    """Testing wrapper around winreg.QueryInfoKey"""
    raise


def EnumKey(key, index):
    """Testing wrapper around winreg.EnumKey"""
    try:
        return winreg.EnumKey(key, index)
    except OSError as e:
        raise InvalidRegistryOperation("EnumKey", e, key, index) from e


def EnumValue(key, index):
    """Testing wrapper around winreg.EnumValue"""
    try:
        return winreg.EnumValue(key, index)
    except OSError as e:
        raise InvalidRegistryOperation("EnumValue", e, key, index) from e


def QueryValueEx(key, name,**kwargs):
    """Testing wrapper around winreg.QueryValueEx"""
    try:
        return winreg.QueryValueEx(key, name, **kwargs)
    except OSError as e:
        raise InvalidRegistryOperation("QueryValueEx", e, key, name, **kwargs) from e

