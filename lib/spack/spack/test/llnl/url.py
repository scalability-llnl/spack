# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Tests for llnl.url functions"""
import itertools

import pytest

import llnl.url


@pytest.fixture(params=llnl.url.ALLOWED_ARCHIVE_TYPES)
def archive_and_expected(request):
    archive_name = ".".join(["Foo", request.param])
    return archive_name, request.param


def test_get_extension(archive_and_expected):
    """Tests that we can predict correctly known extensions for simple cases."""
    archive, expected = archive_and_expected
    result = llnl.url.extension_from_path(archive)
    assert result == expected


def test_get_bad_extension():
    """Tests that a bad extension returns None"""
    result = llnl.url.extension_from_path("Foo.cxx")
    assert result is None


@pytest.mark.parametrize(
    "url,expected",
    [
        # No suffix
        ("rgb-1.0.6", "rgb-1.0.6"),
        # Misleading prefix
        ("jpegsrc.v9b", "jpegsrc.v9b"),
        ("turbolinux702", "turbolinux702"),
        ("converge_install_2.3.16", "converge_install_2.3.16"),
        # Download type - code, source
        ("cistem-1.0.0-beta-source-code", "cistem-1.0.0-beta"),
        # Download type - src
        ("apache-ant-1.9.7-src", "apache-ant-1.9.7"),
        ("go1.7.4.src", "go1.7.4"),
        # Download type - source
        ("bowtie2-2.2.5-source", "bowtie2-2.2.5"),
        ("grib_api-1.17.0-Source", "grib_api-1.17.0"),
        # Download type - full
        ("julia-0.4.3-full", "julia-0.4.3"),
        # Download type - bin
        ("apache-maven-3.3.9-bin", "apache-maven-3.3.9"),
        # Download type - binary
        ("Jmol-14.8.0-binary", "Jmol-14.8.0"),
        # Download type - gem
        ("rubysl-date-2.0.9.gem", "rubysl-date-2.0.9"),
        # Download type - tar
        ("gromacs-4.6.1-tar", "gromacs-4.6.1"),
        # Download type - sh
        ("Miniconda2-4.3.11-Linux-x86_64.sh", "Miniconda2-4.3.11"),
        # Download version - release
        ("v1.0.4-release", "v1.0.4"),
        # Download version - stable
        ("libevent-2.0.21-stable", "libevent-2.0.21"),
        # Download version - final
        ("2.6.7-final", "2.6.7"),
        # Download version - rel
        ("v1.9.5.1rel", "v1.9.5.1"),
        # Download version - orig
        ("dash_0.5.5.1.orig", "dash_0.5.5.1"),
        # Download version - plus
        ("ncbi-blast-2.6.0+-src", "ncbi-blast-2.6.0"),
        # License
        ("cppad-20170114.gpl", "cppad-20170114"),
        # Arch
        ("pcraster-4.1.0_x86-64", "pcraster-4.1.0"),
        ("dislin-11.0.linux.i586_64", "dislin-11.0"),
        ("PAGIT.V1.01.64bit", "PAGIT.V1.01"),
        # OS - linux
        ("astyle_2.04_linux", "astyle_2.04"),
        # OS - unix
        ("install-tl-unx", "install-tl"),
        # OS - macos
        ("astyle_1.23_macosx", "astyle_1.23"),
        ("haxe-2.08-osx", "haxe-2.08"),
        # PyPI - wheel
        ("wheel-1.2.3-py3-none-any", "wheel-1.2.3"),
        ("wheel-1.2.3-py2.py3-none-any", "wheel-1.2.3"),
        ("wheel-1.2.3-cp38-abi3-macosx_10_12_x86_64", "wheel-1.2.3"),
        ("entrypoints-0.2.2-py2.py3-none-any", "entrypoints-0.2.2"),
        (
            "numpy-1.12.0-cp27-cp27m-macosx_10_6_intel.macosx_10_9_intel."
            "macosx_10_9_x86_64.macosx_10_10_intel.macosx_10_10_x86_64",
            "numpy-1.12.0",
        ),
        # Combinations of multiple patterns - bin, release
        ("rocketmq-all-4.5.2-bin-release", "rocketmq-all-4.5.2"),
        # Combinations of multiple patterns - all
        ("p7zip_9.04_src_all", "p7zip_9.04"),
        # Combinations of multiple patterns - run
        ("cuda_8.0.44_linux.run", "cuda_8.0.44"),
        # Combinations of multiple patterns - file
        ("ack-2.14-single-file", "ack-2.14"),
        # Combinations of multiple patterns - jar
        ("antlr-3.4-complete.jar", "antlr-3.4"),
        # Combinations of multiple patterns - oss
        ("tbb44_20160128oss_src_0", "tbb44_20160128"),
        # Combinations of multiple patterns - darwin
        ("ghc-7.0.4-x86_64-apple-darwin", "ghc-7.0.4"),
        ("ghc-7.0.4-i386-apple-darwin", "ghc-7.0.4"),
        # Combinations of multiple patterns - centos
        ("sratoolkit.2.8.2-1-centos_linux64", "sratoolkit.2.8.2-1"),
        # Combinations of multiple patterns - arch
        (
            "VizGlow_v2.2alpha17-R21November2016-Linux-x86_64-Install",
            "VizGlow_v2.2alpha17-R21November2016",
        ),
        ("jdk-8u92-linux-x64", "jdk-8u92"),
        ("cuda_6.5.14_linux_64.run", "cuda_6.5.14"),
        ("Mathematica_12.0.0_LINUX.sh", "Mathematica_12.0.0"),
        ("trf407b.linux64", "trf407b"),
        # Combinations of multiple patterns - with
        ("mafft-7.221-with-extensions-src", "mafft-7.221"),
        ("spark-2.0.0-bin-without-hadoop", "spark-2.0.0"),
        ("conduit-v0.3.0-src-with-blt", "conduit-v0.3.0"),
        # Combinations of multiple patterns - rock
        ("bitlib-23-2.src.rock", "bitlib-23-2"),
        # Combinations of multiple patterns - public
        ("dakota-6.3-public.src", "dakota-6.3"),
        # Combinations of multiple patterns - universal
        ("synergy-1.3.6p2-MacOSX-Universal", "synergy-1.3.6p2"),
        # Combinations of multiple patterns - dynamic
        ("snptest_v2.5.2_linux_x86_64_dynamic", "snptest_v2.5.2"),
        # Combinations of multiple patterns - other
        ("alglib-3.11.0.cpp.gpl", "alglib-3.11.0"),
        ("hpcviewer-2019.08-linux.gtk.x86_64", "hpcviewer-2019.08"),
        ("apache-mxnet-src-1.3.0-incubating", "apache-mxnet-src-1.3.0"),
    ],
)
def test_url_strip_version_suffixes(url, expected):
    stripped = llnl.url.strip_version_suffixes(url)
    assert stripped == expected


def test_strip_compression_extension(archive_and_expected):
    archive, extension = archive_and_expected
    stripped = llnl.url.strip_compression_extension(archive)
    if extension == "zip":
        assert stripped == "Foo.zip"
        stripped = llnl.url.strip_compression_extension(archive, "zip")
        assert stripped == "Foo"
    elif extension == "whl":
        assert stripped == "Foo.whl"
    elif (
        extension.lower() == "tar"
        or extension in llnl.url.CONTRACTION_MAP
        or extension
        in [
            ".".join(ext)
            for ext in itertools.product(llnl.url.PREFIX_EXTENSIONS, llnl.url.EXTENSIONS)
        ]
    ):
        assert stripped == "Foo.tar" or stripped == "Foo.TAR"
    else:
        assert stripped == "Foo"


def test_allowed_archive(archive_and_expected):
    archive, _ = archive_and_expected
    assert llnl.url.allowed_archive(archive)
