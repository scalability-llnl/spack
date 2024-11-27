# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

import spack.util.ld_so_conf as ld_so_conf


def test_ld_so_conf_parsing(tmpdir):
    cwd = os.getcwd()
    tmpdir.ensure("subdir", dir=True)

    # Entrypoint config file
    with open(str(tmpdir.join("main.conf")), "wb") as f:
        f.write(b"  \n")
        f.write(b"include subdir/*.conf\n")
        f.write(b"include non-existent/file\n")
        f.write(b"include #nope\n")
        f.write(b"include     \n")
        f.write(b"include\t\n")
        f.write(b"include\n")
        f.write(b"/main.conf/lib # and a comment\n")
        f.write(b"relative/path\n\n")
        f.write(b"#/skip/me\n")

    # Should be parsed: subdir/first.conf
    with open(str(tmpdir.join("subdir", "first.conf")), "wb") as f:
        f.write(b"/first.conf/lib")

    # Should be parsed: subdir/second.conf
    with open(str(tmpdir.join("subdir", "second.conf")), "wb") as f:
        f.write(b"/second.conf/lib")

    # Not matching subdir/*.conf
    with open(str(tmpdir.join("subdir", "third")), "wb") as f:
        f.write(b"/third/lib")

    paths = ld_so_conf.parse_ld_so_conf(str(tmpdir.join("main.conf")))

    assert len(paths) == 3
    assert "/main.conf/lib" in paths
    assert "/first.conf/lib" in paths
    assert "/second.conf/lib" in paths

    # Make sure globbing didn't change the working dir
    assert os.getcwd() == cwd


def test_host_dynamic_linker_search_paths():
    assert {"/usr/lib", "/usr/lib64", "/lib", "/lib64"}.issubset(
        ld_so_conf.host_dynamic_linker_search_paths()
    )
