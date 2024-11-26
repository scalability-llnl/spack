# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Dicom3tools(MakefilePackage):
    """Command line utilities for creating, modifying, dumping and validating
    files of DICOM attributes, and conversion of proprietary image formats to
    DICOM. Can handle older ACR/NEMA format data, and some proprietary versions
    of that such as SPI."""

    homepage = "https://www.dclunie.com/dicom3tools.html"
    url = "https://www.dclunie.com/dicom3tools/workinprogress/dicom3tools_1.00.snapshot.20210306100017.tar.bz2"

    version(
        "1.00.snapshot.20210306100017",
        sha256="3cc2d6056e349e0ac6a093d231d8f4dd7a77e26ed29c1ebaca945dd5e56c1520",
    )

    depends_on("cxx", type="build")  # generated

    variant(
        "uid_root",
        default="0.0.0.0",
        values=lambda x: True,
        description="default UID Root assignment",
    )

    depends_on("bzip2", type="build")
    depends_on("imake", type="build")
    depends_on("libx11")

    def edit(self, spec, prefix):
        defines = [
            '#define InstallBinDir "{0}"'.format(prefix.bin),
            '#define InstallIncDir "{0}"'.format(prefix.include),
            '#define InstallLibDir "{0}"'.format(prefix.lib),
            '#define InstallManDir "{0}"'.format(prefix.man),
            '#define X11LibraryPath "{0}"'.format(spec["libx11"].prefix.lib),
            '#define X11IncludePath "{0}"'.format(spec["libx11"].prefix.include),
        ]

        with working_dir("config"):
            with open("site.p-def", "a") as inc:
                for define in defines:
                    inc.write("{0}\n".format(define))

            configure = FileFilter("Configure")
            configure.filter("usegcc=.*", "usegcc={0}".format(spack_cc))
            configure.filter("usegpp=.*", "usegpp={0}".format(spack_cxx))

    def build(self, spec, prefix):
        uid_root = spec.variants["uid_root"].value
        configure = Executable(join_path(".", "Configure"))
        configure()

        if spec.satisfies("%fj"):
            filter_file(
                "#define UseStandardHeadersWithoutExtension 0",
                "#define UseStandardHeadersWithoutExtension 1",
                "config/generic.cf",
            )
            filter_file(
                "#define EmitUsingStdNameSpace 0",
                "#define EmitUsingStdNameSpace 1",
                "config/generic.cf",
            )

        imake = which("imake")
        imake("-I./config", "-DDefaultUIDRoot={0}".format(uid_root))
        make("World")

    def install(self, spec, prefix):
        make("install")
        make("install.man")
