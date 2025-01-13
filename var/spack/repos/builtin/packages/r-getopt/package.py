# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RGetopt(RPackage):
    """C-Like 'getopt' Behavior.

    Package designed to be used with Rscript to write "#!" shebang scripts that
    accept short and long flags/options. Many users will prefer using instead
    the packages optparse or argparse which add extra features like
    automatically generated help option and usage, support for default values,
    positional argument support, etc."""

    cran = "getopt"

    license("GPL-2.0-or-later")

    version("1.20.4", sha256="87d36cbe6dba41dbc1d78d845210266cdd08c7440d977d738a6e45db14221e8b")
    version("1.20.3", sha256="531f5fdfdcd6b96a73df2b39928418de342160ac1b0043861e9ea844f9fbf57f")
    version("1.20.2", sha256="3d6c12d32d6cd4b2909be626e570e158b3ed960e4739510e3a251e7f172de38e")
    version("1.20.1", sha256="1522c35b13e8546979725a68b75e3bc9d156fb06569067472405f6b8591d8654")
