# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from os import symlink

from spack.package import *


class Circos(Package):
    """Circos is a software package for visualizing data and information."""

    homepage = "http://circos.ca/"
    url = "http://circos.ca/distribution/circos-0.69-6.tgz"

    license("GPL-3.0-only")

    version("0.69-9", sha256="34d8d7ebebf3f553d62820f8f4a0a57814b610341f836b4740c46c3057f789d2")
    version("0.69-6", sha256="52d29bfd294992199f738a8d546a49754b0125319a1685a28daca71348291566")

    depends_on("perl", type="run")
    depends_on("perl-clone", type="run")
    depends_on("perl-config-general", type="run")
    depends_on("perl-exporter-tiny", type="run")
    depends_on("perl-font-ttf", type="run")
    depends_on("perl-gd", type="run")
    depends_on("perl-io-string", type="run")
    depends_on("perl-list-moreutils", type="run")
    depends_on("perl-math-round", type="run")
    depends_on("perl-math-bezier", type="run")
    depends_on("perl-math-vecstat", type="run")
    depends_on("perl-params-validate", type="run")
    depends_on("perl-readonly", type="run")
    depends_on("perl-regexp-common", type="run")
    depends_on("perl-set-intspan", type="run")
    depends_on("perl-statistics-basic", type="run")
    depends_on("perl-svg", type="run")
    depends_on("perl-text-format", type="run")

    def install(self, spec, prefix):
        basedir = prefix.lib.circos
        install_tree(".", basedir)

        mkdirp(prefix.bin)
        symlink(basedir.bin.circos, prefix.bin.circos)
