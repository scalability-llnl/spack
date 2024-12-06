# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Otf(AutotoolsPackage):
    """To improve scalability for very large and massively parallel
    traces the Open Trace Format (OTF) is developed at ZIH as a
    successor format to the Vampir Trace Format (VTF3)."""

    homepage = "http://tu-dresden.de/die_tu_dresden/zentrale_einrichtungen/zih/forschung/projekte/otf/index_html/document_view?set_language=en"
    url = "https://wwwpub.zih.tu-dresden.de/%7Emlieber/dcount/dcount.php?package=otf&get=OTF-1.12.5salmon.tar.gz"

    maintainers("michaelkuhn")

    license("BSD-3-Clause")

    version(
        "1.12.5salmon", sha256="0a8427360dedb38e8ddca30f14d95f826420c550337c5a79dbb754904e194088"
    )

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("zlib-api")

    def configure_args(self):
        args = []

        args.append("--without-mpi")
        args.append("--without-vtf3")
        args.append("--without-zoidfs")

        args.append("--with-zlib")
        args.append("--with-zlib-dir={0}".format(self.spec["zlib-api"].prefix))

        return args
