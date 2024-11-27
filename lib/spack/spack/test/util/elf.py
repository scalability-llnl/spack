# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import io

import pytest

import llnl.util.filesystem as fs

import spack.platforms
import spack.util.elf as elf
import spack.util.executable
from spack.hooks.drop_redundant_rpaths import drop_redundant_rpaths


# note that our elf parser is platform independent... but I guess creating an elf file
# is slightly more difficult with system tools on non-linux.
def skip_unless_linux(f):
    return pytest.mark.skipif(
        str(spack.platforms.real_host()) != "linux",
        reason="implementation currently requires linux",
    )(f)


@pytest.mark.requires_executables("gcc")
@skip_unless_linux
@pytest.mark.parametrize(
    "linker_flag,is_runpath",
    [("-Wl,--disable-new-dtags", False), ("-Wl,--enable-new-dtags", True)],
)
def test_elf_parsing_shared_linking(linker_flag, is_runpath, tmpdir):
    gcc = spack.util.executable.which("gcc")

    with fs.working_dir(str(tmpdir)):
        # Create a library to link to so we can force a dynamic section in an ELF file
        with open("foo.c", "w") as f:
            f.write("int foo(){return 0;}")
        with open("bar.c", "w") as f:
            f.write("int foo(); int _start(){return foo();}")

        # Create library and executable linking to it.
        gcc("-shared", "-o", "libfoo.so", "-Wl,-soname,libfoo.so.1", "-nostdlib", "foo.c")
        gcc(
            "-o",
            "bar",
            linker_flag,
            "-Wl,-rpath,/first",
            "-Wl,-rpath,/second",
            "-Wl,--no-as-needed",
            "-nostdlib",
            "libfoo.so",
            "bar.c",
            "-o",
            "bar",
        )

        with open("libfoo.so", "rb") as f:
            foo_parsed = elf.parse_elf(f, interpreter=True, dynamic_section=True)

        assert not foo_parsed.has_pt_interp
        assert foo_parsed.has_pt_dynamic
        assert not foo_parsed.has_rpath
        assert not foo_parsed.has_needed
        assert foo_parsed.has_soname
        assert foo_parsed.dt_soname_str == b"libfoo.so.1"

        with open("bar", "rb") as f:
            bar_parsed = elf.parse_elf(f, interpreter=True, dynamic_section=True)

        assert bar_parsed.has_pt_interp
        assert bar_parsed.has_pt_dynamic
        assert bar_parsed.has_rpath
        assert bar_parsed.has_needed
        assert not bar_parsed.has_soname
        assert bar_parsed.dt_rpath_str == b"/first:/second"
        assert bar_parsed.dt_needed_strs == [b"libfoo.so.1"]


def test_broken_elf():
    # No elf magic
    with pytest.raises(elf.ElfParsingError, match="Not an ELF file"):
        elf.parse_elf(io.BytesIO(b"x"))

    # Incomplete ELF header
    with pytest.raises(elf.ElfParsingError, match="Not an ELF file"):
        elf.parse_elf(io.BytesIO(b"\x7fELF"))

    # Invalid class
    with pytest.raises(elf.ElfParsingError, match="Invalid class"):
        elf.parse_elf(io.BytesIO(b"\x7fELF\x09\x01" + b"\x00" * 10))

    # Invalid data type
    with pytest.raises(elf.ElfParsingError, match="Invalid data type"):
        elf.parse_elf(io.BytesIO(b"\x7fELF\x01\x09" + b"\x00" * 10))

    # 64-bit needs at least 64 bytes of header; this is only 56 bytes
    with pytest.raises(elf.ElfParsingError, match="ELF header malformed"):
        elf.parse_elf(io.BytesIO(b"\x7fELF\x02\x01" + b"\x00" * 50))

    # 32-bit needs at least 52 bytes of header; this is only 46 bytes
    with pytest.raises(elf.ElfParsingError, match="ELF header malformed"):
        elf.parse_elf(io.BytesIO(b"\x7fELF\x01\x01" + b"\x00" * 40))

    # Not a ET_DYN/ET_EXEC on a 32-bit LE ELF
    with pytest.raises(elf.ElfParsingError, match="Not an ET_DYN or ET_EXEC"):
        elf.parse_elf(io.BytesIO(b"\x7fELF\x01\x01" + (b"\x00" * 10) + b"\x09" + (b"\x00" * 35)))


def test_parser_doesnt_deal_with_nonzero_offset():
    # Currently we don't have logic to parse ELF files at nonzero offsets in a file
    # This could be useful when e.g. modifying an ELF file inside a tarball or so,
    # but currently we cannot.
    elf_at_offset_one = io.BytesIO(b"\x00\x7fELF\x01\x01" + b"\x00" * 10)
    elf_at_offset_one.read(1)
    with pytest.raises(elf.ElfParsingError, match="Cannot parse at a nonzero offset"):
        elf.parse_elf(elf_at_offset_one)


def test_only_header():
    # When passing only_header=True parsing a file that is literally just a header
    # without any sections/segments should not error.

    # 32 bit
    elf_32 = elf.parse_elf(io.BytesIO(b"\x7fELF\x01\x01" + b"\x00" * 46), only_header=True)
    assert not elf_32.is_64_bit
    assert elf_32.is_little_endian

    # 64 bit
    elf_64 = elf.parse_elf(io.BytesIO(b"\x7fELF\x02\x01" + b"\x00" * 58), only_header=True)
    assert elf_64.is_64_bit
    assert elf_64.is_little_endian


@pytest.mark.requires_executables("gcc")
@skip_unless_linux
def test_elf_get_and_replace_rpaths_and_pt_interp(binary_with_rpaths):
    long_paths = ["/very/long/prefix-a/x", "/very/long/prefix-b/y"]
    executable = str(
        binary_with_rpaths(rpaths=long_paths, dynamic_linker="/very/long/prefix-b/lib/ld.so")
    )

    # Before
    assert elf.get_rpaths(executable) == long_paths

    replacements = {
        b"/very/long/prefix-a": b"/short-a",
        b"/very/long/prefix-b": b"/short-b",
        b"/very/long": b"/dont",
    }

    # Replace once: should modify the file.
    assert elf.substitute_rpath_and_pt_interp_in_place_or_raise(executable, replacements)

    # Replace twice: nothing to be done.
    assert not elf.substitute_rpath_and_pt_interp_in_place_or_raise(executable, replacements)

    # Verify the rpaths were modified correctly
    assert elf.get_rpaths(executable) == ["/short-a/x", "/short-b/y"]
    assert elf.get_interpreter(executable) == "/short-b/lib/ld.so"

    # Going back to long rpaths should fail, since we've added trailing \0
    # bytes, and replacement can't assume it can write back in repeated null
    # bytes -- it may correspond to zero-length strings for example.
    with pytest.raises(elf.ElfCStringUpdatesFailed) as info:
        elf.substitute_rpath_and_pt_interp_in_place_or_raise(
            executable, {b"/short-a": b"/very/long/prefix-a", b"/short-b": b"/very/long/prefix-b"}
        )

    assert info.value.rpath is not None
    assert info.value.pt_interp is not None
    assert info.value.rpath.old_value == b"/short-a/x:/short-b/y"
    assert info.value.rpath.new_value == b"/very/long/prefix-a/x:/very/long/prefix-b/y"
    assert info.value.pt_interp.old_value == b"/short-b/lib/ld.so"
    assert info.value.pt_interp.new_value == b"/very/long/prefix-b/lib/ld.so"


@pytest.mark.requires_executables("gcc")
@skip_unless_linux
def test_drop_redundant_rpath(tmpdir, binary_with_rpaths):
    """Test the post install hook that drops redundant rpath entries"""

    # Use existing and non-existing dirs in tmpdir
    non_existing_dirs = [str(tmpdir.join("a")), str(tmpdir.join("b"))]
    existing_dirs = [str(tmpdir.join("c")), str(tmpdir.join("d"))]
    all_dirs = non_existing_dirs + existing_dirs

    tmpdir.ensure("c", dir=True)
    tmpdir.ensure("d", dir=True)

    # Create a binary with rpaths to both existing and non-existing dirs
    binary = binary_with_rpaths(rpaths=all_dirs)

    # Verify that the binary has all the rpaths
    # sometimes compilers add extra rpaths, so we test for a subset
    assert set(all_dirs).issubset(elf.get_rpaths(binary))

    # Test whether the right rpaths are dropped
    drop_redundant_rpaths(binary)
    new_rpaths = elf.get_rpaths(binary)
    assert set(existing_dirs).issubset(new_rpaths)
    assert set(non_existing_dirs).isdisjoint(new_rpaths)
