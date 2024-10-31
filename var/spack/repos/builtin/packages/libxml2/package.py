# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os

import llnl.util.filesystem as fs

import spack.builder
from spack.build_systems import autotools, nmake
from spack.package import *


class Libxml2(AutotoolsPackage, NMakePackage):
    """Libxml2 is the XML C parser and toolkit developed for the Gnome
    project (but usable outside of the Gnome platform), it is free
    software available under the MIT License."""

    homepage = "https://gitlab.gnome.org/GNOME/libxml2/-/wikis"
    url = "https://download.gnome.org/sources/libxml2/2.9/libxml2-2.9.13.tar.xz"
    list_url = "https://gitlab.gnome.org/GNOME/libxml2/-/releases"

    maintainers("AlexanderRichert-NOAA")

    def url_for_version(self, version):
        if version >= Version("2.9.13"):
            url = "https://download.gnome.org/sources/libxml2/{0}/libxml2-{1}.tar.xz"
            return url.format(version.up_to(2), version)
        return "http://xmlsoft.org/sources/libxml2-{0}.tar.gz".format(version)

    license("MIT")

    version("2.10.3", sha256="5d2cc3d78bec3dbe212a9d7fa629ada25a7da928af432c93060ff5c17ee28a9c")
    version("2.10.2", sha256="d240abe6da9c65cb1900dd9bf3a3501ccf88b3c2a1cb98317d03f272dda5b265")
    version("2.10.1", sha256="21a9e13cc7c4717a6c36268d0924f92c3f67a1ece6b7ff9d588958a6db9fb9d8")
    version("2.9.14", sha256="60d74a257d1ccec0475e749cba2f21559e48139efba6ff28224357c7c798dfee")
    version("2.9.13", sha256="276130602d12fe484ecc03447ee5e759d0465558fbc9d6bd144e3745306ebf0e")
    version("2.9.12", sha256="c8d6681e38c56f172892c85ddc0852e1fd4b53b4209e7f4ebf17f7e2eae71d92")
    version("2.9.11", sha256="886f696d5d5b45d780b2880645edf9e0c62a4fd6841b853e824ada4e02b4d331")
    version("2.9.10", sha256="aafee193ffb8fe0c82d4afef6ef91972cbaf5feea100edc2f262750611b4be1f")
    version("2.9.9", sha256="94fb70890143e3c6549f265cee93ec064c80a84c42ad0f23e85ee1fd6540a871")
    version("2.9.8", sha256="0b74e51595654f958148759cfef0993114ddccccbb6f31aee018f3558e8e2732")
    version("2.9.4", sha256="ffb911191e509b966deb55de705387f14156e1a56b21824357cdf0053233633c")
    version("2.9.2", sha256="5178c30b151d044aefb1b08bf54c3003a0ac55c59c866763997529d60770d5bc")
    version("2.7.8", sha256="cda23bc9ebd26474ca8f3d67e7d1c4a1f1e7106364b690d822e009fdc3c417ec")

    depends_on("c", type="build")  # generated

    variant("python", default=False, description="Enable Python support")
    variant("shared", default=True, description="Build shared library")
    variant("pic", default=True, description="Enable position-independent code (PIC)")

    conflicts("~pic+shared")

    depends_on("pkgconfig@0.9.0:", type="build", when="build_system=autotools")
    # conditional on non Windows, but rather than specify for each platform
    # specify for non Windows builder, which has equivalent effect
    depends_on("iconv", when="build_system=autotools")
    depends_on("zlib-api")
    depends_on("xz")

    # avoid cycle dependency for concretizer
    with when("+python"):
        extends("python")
        depends_on("python+shared~libxml2")
        # A note about python versions: libxml 2.10.1 (and presumably earlier) has
        # a bug in its configure script that fails to properly parse python
        # version strings with more than one character for the minor version.
        depends_on("python@:3.9", when="@:2.10.1")

    # XML Conformance Test Suites
    # See https://www.w3.org/XML/Test/ for information
    resource(
        name="xmlts",
        url="https://www.w3.org/XML/Test/xmlts20080827.tar.gz",
        sha256="96151685cec997e1f9f3387e3626d61e6284d4d6e66e0e440c209286c03e9cc7",
    )

    patch("nvhpc-elfgcchack.patch", when="@:2.9 %nvhpc")

    # Use NAN/INFINITY if available to avoid SIGFPE
    # See https://gitlab.gnome.org/GNOME/libxml2/-/merge_requests/186
    patch(
        "https://gitlab.gnome.org/GNOME/libxml2/-/commit/c9925454fd384a17c8c03d358c6778a552e9287b.diff",
        sha256="5dc43fed02b443d2563a502a52caafe39477c06fc30b70f786d5ed3eb5aea88d",
        when="@2.9.11:2.9.14",
    )
    build_system(conditional("nmake", when="platform=windows"), "autotools", default="autotools")

    def flag_handler(self, name, flags):
        if name == "cflags" and self.spec.satisfies("+pic"):
            flags.append(self.compiler.cc_pic_flag)
            flags.append("-DPIC")
        return (flags, None, None)

    @property
    def command(self):
        return Executable(self.prefix.bin.join("xml2-config"))

    @property
    def headers(self):
        include_dir = self.spec.prefix.include.libxml2
        hl = find_all_headers(include_dir)
        hl.directories = [include_dir, self.spec.prefix.include]
        return hl

    def patch(self):
        # Remove flags not recognized by the NVIDIA compiler
        if self.spec.satisfies("%nvhpc"):
            filter_file(
                "-pedantic -Wall -Wextra -Wshadow -Wpointer-arith "
                "-Wcast-align -Wwrite-strings -Waggregate-return "
                "-Wstrict-prototypes -Wmissing-prototypes "
                "-Wnested-externs -Winline -Wredundant-decls",
                "-Wall",
                "configure",
            )
            filter_file("-Wno-long-long -Wno-format-extra-args", "", "configure")

    def test_import(self):
        """import module test"""
        if "+python" not in self.spec:
            raise SkipTest("Package must be built with +python")

        with working_dir("spack-test", create=True):
            python("-c", "import libxml2")

    def test_xmlcatalog(self):
        """check minimal creation output"""
        path = self.prefix.bin.xmlcatalog
        if not os.path.exists(path):
            raise SkipTest("xmlcatalog is not installed")

        xmlcatalog = which(path)
        out = xmlcatalog("--create", output=str.split, error=str.split)

        expected = [r"<catalog xmlns", r'catalog"/>']
        check_outputs(expected, out)

    def test_xml2_config(self):
        """check version output"""
        path = join_path(self.prefix.bin, "xml2-config")
        if not os.path.exists(path):
            raise SkipTest("xml2-config is not installed")

        xml2_config = which(path)
        out = xml2_config("--version", output=str.split, error=str.split)
        assert str(self.spec.version) in out

    def test_xmllint(self):
        """run xmllint generation and validation checks"""
        path = self.prefix.bin.xmllint
        if not os.path.exists(path):
            raise SkipTest("xmllint is not installed")

        test_filename = "test.xml"
        xmllint = which(path)

        with test_part(self, "test_xmllint_auto", purpose="generate {0}".format(test_filename)):
            xmllint("--auto", "-o", test_filename)

        with test_part(
            self,
            "test_xmllint_validate_no_dtd",
            purpose="validate {0} without a DTD".format(test_filename),
        ):
            out = xmllint(
                "--postvalid",
                test_filename,
                output=str.split,
                error=str.split,
                fail_on_error=False,
            )

            expected = [r"validity error", r"no DTD found", r"does not validate"]
            check_outputs(expected, out)

        data_dir = self.test_suite.current_test_data_dir
        dtd_path = data_dir.join("info.dtd")

        with test_part(
            self,
            "test_xmllint_validate_with_dtd",
            purpose="validate {0} with a DTD".format(test_filename),
        ):
            out = xmllint(
                "--dtdvalid",
                dtd_path,
                test_filename,
                output=str.split,
                error=str.split,
                fail_on_error=False,
            )

            expected = [r"validity error", r"does not follow the DTD"]
            check_outputs(expected, out)

        test_filename = data_dir.join("info.xml")
        with test_part(
            self,
            "test_xmllint_validate_works",
            purpose="validate {0} with a DTD".format(test_filename),
        ):
            xmllint("--dtdvalid", dtd_path, data_dir.join("info.xml"))


class BaseBuilder(metaclass=spack.builder.PhaseCallbacksMeta):
    @run_after("install")
    @on_package_attributes(run_tests=True)
    def import_module_test(self):
        if self.spec.satisfies("+python"):
            with working_dir("spack-test", create=True):
                python("-c", "import libxml2")


class AutotoolsBuilder(BaseBuilder, autotools.AutotoolsBuilder):
    def configure_args(self):
        spec = self.spec

        args = [
            "--with-lzma={0}".format(spec["xz"].prefix),
            "--with-iconv={0}".format(spec["iconv"].prefix),
        ]

        if spec.satisfies("+python"):
            args.extend(
                [
                    "--with-python={0}".format(spec["python"].home),
                    "--with-python-install-dir={0}".format(python_platlib),
                ]
            )
        else:
            args.append("--without-python")

        args.extend(self.enable_or_disable("shared"))
        # PIC setting is taken care of above by self.flag_handler()
        args.append("--without-pic")

        return args


class NMakeBuilder(BaseBuilder, nmake.NMakeBuilder):
    phases = ("configure", "build", "install")

    @property
    def makefile_name(self):
        return "Makefile.msvc"

    @property
    def build_directory(self):
        return fs.windows_sfn(os.path.join(self.stage.source_path, "win32"))

    def configure(self, pkg, spec, prefix):
        with working_dir(self.build_directory):
            opts = [
                "prefix=%s" % fs.windows_sfn(prefix),
                "compiler=msvc",
                "iconv=no",
                "zlib=yes",
                "lzma=yes",
                "lib=%s"
                % ";".join(
                    (
                        fs.windows_sfn(spec["zlib-api"].prefix.lib),
                        fs.windows_sfn(spec["xz"].prefix.lib),
                    )
                ),
                "include=%s"
                % ";".join(
                    (
                        fs.windows_sfn(spec["zlib-api"].prefix.include),
                        fs.windows_sfn(spec["xz"].prefix.include),
                    )
                ),
            ]
            if spec.satisfies("+python"):
                opts.append("python=yes")
            cscript("configure.js", *opts)
