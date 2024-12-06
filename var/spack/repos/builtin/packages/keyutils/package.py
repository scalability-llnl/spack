# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Keyutils(MakefilePackage):
    """These tools are used to control the key management system built
    into the Linux kernel."""

    homepage = "https://git.kernel.org/pub/scm/linux/kernel/git/dhowells/keyutils.git/"
    url = "https://git.kernel.org/pub/scm/linux/kernel/git/dhowells/keyutils.git/snapshot/keyutils-1.6.1.tar.gz"

    license("GPL-2.0-or-later AND LGPL-2.0-or-later")

    version("1.6.1", sha256="3c71dcfc6900d07b02f4e061d8fb218a4ae6519c1d283d6a57b8e27718e2f557")
    version("1.6", sha256="c6a27b4e3d0122d921f3dcea4b1f02a8616ca844535960d6af76ef67d015b5cf")
    version("1.5.10", sha256="e1fdbde234c786b65609a4cf080a2c5fbdb57f049249c139160c85fc3dfa7da9")
    version("1.5.9", sha256="2dc0bdb099ab8331e02e5dbbce320359bef76eda0a4ddbd2ba1d1b9d3a8cdff8")

    depends_on("c", type="build")  # generated

    conflicts("platform=darwin", msg="Linux-only")

    def install(self, spec, prefix):
        install_tree(".", prefix)
        mkdirp(prefix.include)
        install(join_path(prefix, "*.h"), prefix.include)
