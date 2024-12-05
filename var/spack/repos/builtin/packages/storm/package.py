# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Storm(Package):
    """
    Storm is a distributed realtime computation system. Similar to how
    Hadoop provides a set of general primitives for doing batch processing,
    Storm provides a set of general primitives for doing realtime computation.
    """

    homepage = "https://storm.apache.org/"
    url = "https://archive.apache.org/dist/storm/apache-storm-2.2.0/apache-storm-2.2.0.tar.gz"
    list_url = "https://archive.apache.org/dist/storm/"
    list_depth = 1

    license("CC-BY-4.0")

    version("2.6.2", sha256="640c2c54a593cdcffef9441336738774ae618830d3e63eb8e770c22d68beed30")
    version("2.3.0", sha256="49c2255b26633c6fd96399c520339e459fcda29a0e7e6d0c8775cefcff6c3636")
    version("2.2.0", sha256="f621163f349a8e85130bc3d2fbb34e3b08f9c039ccac5474f3724e47a3a38675")
    version("2.1.0", sha256="e279a495dda42af7d9051543989f74a1435a5bda53e795a1de4a1def32027fc4")
    version("2.0.0", sha256="0a4a6f985242a99f899a01bd01dacf9365f381e2acc473caa84073fbe84f6703")
    version("1.2.3", sha256="d45322253db06353a521284f31b30bd964dab859f3a279a305bd79112803425a")

    depends_on("java@8:", type=("build", "run"))
    depends_on("zookeeper", type="run")

    def install(self, spec, prefix):
        install_tree(".", prefix)
