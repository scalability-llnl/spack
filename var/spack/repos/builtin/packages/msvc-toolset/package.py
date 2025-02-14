# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class MsvcToolset(BundlePackage):
    """Msvc Toolset - high level representation of the suite 
    of tools containing Microsofts Visual C/C++ compilers, linkers
    and other tools/libraries

    Cannot be installed via Spack
    """

    homepage = "https://learn.microsoft.com/en-us/cpp/"


    maintainers("johnwparent")

    license("Microsoft Product Terms", checked_by="johnwparent")

    # Each of these correspond to a specific version of VS
    # There is technically a 144 but that's a part of VS 2022
    # and is therefor still version 143
    version("143") # VS 22
    version("142") # VS 19
    version("141") # VS 17
    # Spack does not support VS older than 17

    provides("msvc-runtime")

    @property
    def libs(self):
        return LibraryList([])

    @property
    def headers(self):
        return HeaderList([])