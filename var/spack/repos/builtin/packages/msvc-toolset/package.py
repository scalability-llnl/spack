# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class MsvcToolset(BundlePackage):
    """Msvc Toolset - high level representation of the suite 
    of tools containing Microsofts Visual C/C++ compilers, linkers
    and other tools/libraries
    """

    homepage = "https://learn.microsoft.com/en-us/cpp/"


    maintainers("johnwparent")

    license("Microsoft Product Terms", checked_by="johnwparent")

    # FIXME: Add proper versions here.
    # version("1.2.4")


    provides("msvc-runtime")

    @property
    def libs(self):
        return LibraryList([])

    @property
    def headers(self):
        return HeaderList([])