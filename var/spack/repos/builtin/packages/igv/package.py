# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Igv(Package):
    """The Integrative Genomics Viewer (IGV) is a high-performance visualization
    tool for interactive exploration of large, integrated genomic datasets.
    It supports a wide variety of data types, including array-based and
    next-generation sequence data, and genomic annotations."""

    homepage = "https://software.broadinstitute.org/software/igv/home"
    url = "https://data.broadinstitute.org/igv/projects/downloads/2.8/IGV_2.8.0.zip"

    maintainers("snehring")

    version("2.16.2", sha256="489d34ed4e807a3d32a3720f11248d2ddf1e21d264b06bea44fbe1ccb74b3aa2")
    version("2.12.3", sha256="c87a109deb35994e1b28dee80b5acfd623ec3257f031fcd9cfce008cd32a4cf2")
    version("2.8.0", sha256="33f3ac57017907b931f90c35b63b2de2e4f8d2452f0fbb5be39d30288fc9b2c6")

    depends_on("java@11:", type="run")

    variant("igvtools", default=False, description="Include igvtools")

    def url_for_version(self, version):
        url = "https://data.broadinstitute.org/igv/projects/downloads/{0}/IGV_{1}.zip"
        return url.format(version.up_to(2), version)

    def install(self, spec, prefix):
        install_tree("lib", prefix.lib)
        mkdirp(prefix.bin)
        install("igv.args", prefix)
        files = ["igv.sh", "igv_hidpi.sh"]
        if spec.satisfies("+igvtools"):
            files.extend(["igvtools", "igvtools_gui", "igvtools_gui_hidpi"])
        for f in files:
            filter_file("^prefix=.*$", "prefix=" + prefix, f)
            filter_file(" java ", " {0} ".format(spec["java"].prefix.bin.java), f)
            set_executable(f)
            install(f, prefix.bin)
