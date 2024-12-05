# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Testdfsio(MavenPackage):
    """A corrected and enhanced version of Apache Hadoop TestDFSIO"""

    homepage = "https://github.com/asotirov0/testdfsio"
    url = "https://github.com/asotirov0/testdfsio/archive/0.0.1.tar.gz"

    version(
        "0.0.1",
        sha256="fe8cc47260ffb3e3ac90e0796ebfe73eb4dac64964ab77671e5d32435339dd09",
        deprecated=True,
    )

    depends_on("hadoop@3.2.1:", type="run")
