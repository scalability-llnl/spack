# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Paraver(Package):
    """ "A very powerful performance visualization and analysis tool
    based on traces that can be used to analyse any information that
    is expressed on its input trace format.  Traces for parallel MPI,
    OpenMP and other programs can be genereated with Extrae.

    Note: This package is deprecated in favor of wxparaver"""

    homepage = "https://tools.bsc.es/paraver"
    url = "https://ftp.tools.bsc.es/wxparaver/wxparaver-4.6.3-src.tar.bz2"

    # NOTE: Paraver provides only latest version for download.
    #       Don't keep/add older versions.
    version(
        "4.6.3",
        sha256="ac6025eec5419e1060967eab71dfd123e585be5b5f3ac3241085895dbeca255a",
        deprecated=True,
    )
    version(
        "4.6.2",
        sha256="74b85bf9e6570001d372b376b58643526e349b1d2f1e7633ca38bb0800ecf929",
        deprecated=True,
    )

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("boost@1.36: +serialization")
    depends_on("wxwidgets@2.8:")  # NOTE: using external for this one is usually simpler
    depends_on("wxpropgrid@1.4:")
    depends_on("libxml2")
    depends_on("zlib-api")

    def install(self, spec, prefix):
        os.chdir("ptools_common_files")
        configure("--prefix=%s" % prefix)
        make()
        make("install")

        os.chdir("../paraver-kernel")
        # "--with-extrae=%s" % spec['extrae'].prefix,
        configure(
            "--prefix=%s" % prefix,
            "--with-ptools-common-files=%s" % prefix,
            "--with-boost=%s" % spec["boost"].prefix,
            "--with-boost-serialization=boost_serialization",
        )
        make()
        make("install")

        os.chdir("../paraver-toolset")
        configure("--prefix=%s" % prefix)
        make()
        make("install")

        os.chdir("../wxparaver")
        # "--with-extrae=%s" % spec['extrae'].prefix,
        configure(
            "--prefix=%s" % prefix,
            "--with-paraver=%s" % prefix,
            "--with-boost=%s" % spec["boost"].prefix,
            "--with-boost-serialization=boost_serialization",
            "--with-wxdir=%s" % spec["wxwidgets"].prefix.bin,
        )
        make()
        make("install")
