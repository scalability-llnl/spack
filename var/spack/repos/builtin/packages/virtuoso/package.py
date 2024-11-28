# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Virtuoso(AutotoolsPackage):
    """Virtuoso is a high-performance and scalable Multi-Model RDBMS,
    Data Integration Middleware, Linked Data Deployment, and HTTP
    Application Server Platform"""

    homepage = "https://github.com/openlink/virtuoso-opensource"
    git = "https://github.com/openlink/virtuoso-opensource.git"

    version("7.2.5.1-dev", commit="3ff1d4b3de3977337baf909c264968b9f70b7d2c")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant("dbpedia-vad", default=False, description="DBpedia vad package")
    variant("demo-vad", default=False, description="Demo vad package")
    variant("fct-vad", default=True, description="Facet Browser vad package")
    variant("ods-vad", default=True, description="ODS vad package")
    variant("sparqldemo-vad", default=False, description="Sparql Demo vad package")
    variant("tutorial-vad", default=False, description="Tutorial vad package")
    variant("isparql-vad", default=True, description="iSPARQL vad package")
    variant("rdfmappers-vad", default=True, description="RDF Mappers vad package")

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")

    depends_on("bison", type="build")
    depends_on("flex", type="build")
    depends_on("gperf")
    depends_on("readline")
    depends_on("openssl@0.9.8:1.1")

    def autoreconf(self, spec, prefix):
        bash = which("bash")
        bash("./autogen.sh")

    def configure_args(self):
        readlinep = self.spec["readline"].prefix.lib
        args = [
            "--with-layout=opt",
            "--program-transform-name=s/isql/isql-v/",
            "--with-readline={0}".format(readlinep),
        ]
        args.extend(self.enable_or_disable("dbpedia-vad"))
        args.extend(self.enable_or_disable("demo-vad"))
        args.extend(self.enable_or_disable("fct-vad"))
        args.extend(self.enable_or_disable("ods-vad"))
        args.extend(self.enable_or_disable("sparqldemo-vad"))
        args.extend(self.enable_or_disable("tutorial-vad"))
        args.extend(self.enable_or_disable("isparql-vad"))
        args.extend(self.enable_or_disable("rdfmappers-vad"))
        return args
