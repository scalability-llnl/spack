# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import re

import pytest

import spack.repo
from spack.cmd.url import name_parsed_correctly, url_summary, version_parsed_correctly
from spack.main import SpackCommand
from spack.url import UndetectableVersionError

url = SpackCommand("url")


class MyPackage:
    def __init__(self, name, versions):
        self.name = name
        self.versions = versions


def test_name_parsed_correctly():
    # Expected True
    assert name_parsed_correctly(MyPackage("netcdf", []), "netcdf")
    assert name_parsed_correctly(MyPackage("r-devtools", []), "devtools")
    assert name_parsed_correctly(MyPackage("py-numpy", []), "numpy")
    assert name_parsed_correctly(MyPackage("octave-splines", []), "splines")
    assert name_parsed_correctly(MyPackage("th-data", []), "TH.data")
    assert name_parsed_correctly(MyPackage("imagemagick", []), "ImageMagick")

    # Expected False
    assert not name_parsed_correctly(MyPackage("", []), "hdf5")
    assert not name_parsed_correctly(MyPackage("hdf5", []), "")
    assert not name_parsed_correctly(MyPackage("yaml-cpp", []), "yamlcpp")
    assert not name_parsed_correctly(MyPackage("yamlcpp", []), "yaml-cpp")
    assert not name_parsed_correctly(MyPackage("r-py-parser", []), "parser")
    assert not name_parsed_correctly(MyPackage("oce", []), "oce-0.18.0")


def test_version_parsed_correctly():
    # Expected True
    assert version_parsed_correctly(MyPackage("", ["1.2.3"]), "1.2.3")
    assert version_parsed_correctly(MyPackage("", ["5.4a", "5.4b"]), "5.4a")
    assert version_parsed_correctly(MyPackage("", ["5.4a", "5.4b"]), "5.4b")
    assert version_parsed_correctly(MyPackage("", ["1.63.0"]), "1_63_0")
    assert version_parsed_correctly(MyPackage("", ["0.94h"]), "094h")

    # Expected False
    assert not version_parsed_correctly(MyPackage("", []), "1.2.3")
    assert not version_parsed_correctly(MyPackage("", ["1.2.3"]), "")
    assert not version_parsed_correctly(MyPackage("", ["1.2.3"]), "1.2.4")
    assert not version_parsed_correctly(MyPackage("", ["3.4a"]), "3.4")
    assert not version_parsed_correctly(MyPackage("", ["3.4"]), "3.4b")
    assert not version_parsed_correctly(MyPackage("", ["0.18.0"]), "oce-0.18.0")


def test_url_parse():
    url("parse", "http://zlib.net/fossils/zlib-1.2.10.tar.gz")


def test_url_with_no_version_fails():
    # No version in URL
    with pytest.raises(UndetectableVersionError):
        url("parse", "http://www.netlib.org/voronoi/triangle.zip")


def test_url_list(mock_packages):
    out = url("list")
    total_urls = len(out.split("\n"))

    # The following two options should not change the number of URLs printed.
    out = url("list", "--color", "--extrapolation")
    colored_urls = len(out.split("\n"))
    assert colored_urls == total_urls

    # The following options should print fewer URLs than the default.
    # If they print the same number of URLs, something is horribly broken.
    # If they say we missed 0 URLs, something is probably broken too.
    out = url("list", "--incorrect-name")
    incorrect_name_urls = len(out.split("\n"))
    assert 0 < incorrect_name_urls < total_urls

    out = url("list", "--incorrect-version")
    incorrect_version_urls = len(out.split("\n"))
    assert 0 < incorrect_version_urls < total_urls

    out = url("list", "--correct-name")
    correct_name_urls = len(out.split("\n"))
    assert 0 < correct_name_urls < total_urls

    out = url("list", "--correct-version")
    correct_version_urls = len(out.split("\n"))
    assert 0 < correct_version_urls < total_urls


def test_url_summary(mock_packages):
    """Test the URL summary command."""
    # test url_summary, the internal function that does the work
    (total_urls, correct_names, correct_versions, name_count_dict, version_count_dict) = (
        url_summary(None)
    )

    assert 0 < correct_names <= sum(name_count_dict.values()) <= total_urls
    assert 0 < correct_versions <= sum(version_count_dict.values()) <= total_urls

    # make sure it agrees with the actual command.
    out = url("summary")
    out_total_urls = int(re.search(r"Total URLs found:\s*(\d+)", out).group(1))
    assert out_total_urls == total_urls

    out_correct_names = int(re.search(r"Names correctly parsed:\s*(\d+)", out).group(1))
    assert out_correct_names == correct_names

    out_correct_versions = int(re.search(r"Versions correctly parsed:\s*(\d+)", out).group(1))
    assert out_correct_versions == correct_versions


def test_url_stats(capfd, mock_packages):
    with capfd.disabled():
        output = url("stats")
        npkgs = "%d packages" % len(spack.repo.all_package_names())
        assert npkgs in output
        assert "url" in output
        assert "git" in output
        assert "schemes" in output
        assert "versions" in output
        assert "resources" in output

        output = url("stats", "--show-issues")
        npkgs = "%d packages" % len(spack.repo.all_package_names())
        assert npkgs in output
        assert "url" in output
        assert "git" in output
        assert "schemes" in output
        assert "versions" in output
        assert "resources" in output

        assert "Package URLs with md5 hashes" in output
        assert "needs-relocation" in output
        assert "https://cmake.org/files/v3.4/cmake-0.0.0.tar.gz" in output

        assert "Package URLs with http urls" in output
        assert "zmpi" in output
        assert "http://www.spack-fake-zmpi.org/downloads/zmpi-1.0.tar.gz" in output
