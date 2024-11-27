# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Sabre(MakefilePackage):
    """Sabre is a tool that will demultiplex barcoded reads into separate
    files. It will work on both single-end and paired-end data in fastq
    format. It simply compares the provided barcodes with each read and
    separates the read into its appropriate barcode file, after stripping
    the barcode from the read (and also stripping the quality values of
    the barcode bases). If a read does not have a recognized barcode,
    then it is put into the unknown file.
    """

    homepage = "https://github.com/najoshi/sabre"
    git = "https://github.com/najoshi/sabre.git"

    license("MIT")

    version("2013-09-27", commit="039a55e500ba07b7e6432ea6ec2ddcfb3471d949")

    depends_on("c", type="build")  # generated

    depends_on("zlib-api")

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install("sabre", prefix.bin)
