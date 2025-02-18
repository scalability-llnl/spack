# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

#: PEP440 canonical <major>.<minor>.<micro>.<devN> string
__version__ = "0.22.4"
spack_version = __version__


def __try_int(v):
    try:
        return int(v)
    except ValueError:
        return v


#: (major, minor, micro, dev release) tuple
spack_version_info = tuple([__try_int(v) for v in __version__.split(".")])


__all__ = ["spack_version_info", "spack_version"]
