# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Fastqc(Package):
    """A quality control tool for high throughput sequence data."""

    homepage = "https://www.bioinformatics.babraham.ac.uk/projects/fastqc/"
    url = "https://www.bioinformatics.babraham.ac.uk/projects/fastqc/fastqc_v0.11.5.zip"

    license("GPL-3.0-or-later")

    version("0.12.1", sha256="5f4dba8780231a25a6b8e11ab2c238601920c9704caa5458d9de559575d58aa7")
    version("0.11.9", sha256="15510a176ef798e40325b717cac556509fb218268cfdb9a35ea6776498321369")
    version("0.11.7", sha256="59cf50876bbe5f363442eb989e43ae3eaab8d932c49e8cff2c1a1898dd721112")
    version("0.11.5", sha256="dd7a5ad80ceed2588cf6d6ffe35e0f161c0d9977ed08355f5e4d9473282cbd66")
    version("0.11.4", sha256="adb233f9fae7b02fe99e716664502adfec1b9a3fbb84eed4497122d6d33d1fe7")

    depends_on("java", type="run")
    depends_on("perl")  # for fastqc "script", any perl will do

    patch("fastqc_0.12.x.patch", level=0, when="@0.12:")
    patch("fastqc_0.11.x.patch", level=0, when="@:0.11.9")

    def patch(self):
        filter_file("/usr/bin/perl", self.spec["perl"].command.path, "fastqc", backup=False)

    def install(self, spec, prefix):
        mkdir(prefix.bin)
        mkdir(prefix.lib)
        install("fastqc", prefix.bin)
        install("cisd-jhdf5.jar", prefix.lib)
        install("jbzip2-0.9.jar", prefix.lib)
        if self.spec.satisfies("@:0.11.9"):
            install("sam-1.103.jar", prefix.lib)
        else:
            install("htsjdk.jar", prefix.lib)
        for d in ["Configuration", "net", "org", "Templates", "uk"]:
            install_tree(d, join_path(prefix.lib, d))
        chmod = which("chmod")
        chmod("+x", prefix.bin.fastqc)
