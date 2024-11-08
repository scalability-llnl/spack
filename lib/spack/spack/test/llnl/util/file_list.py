# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import fnmatch
import os.path
import sys

import pytest

from llnl.util.filesystem import HeaderList, LibraryList, find, find_headers, find_libraries

import spack.paths


@pytest.fixture()
def library_list():
    """Returns an instance of LibraryList."""
    # Test all valid extensions: ['.a', '.dylib', '.so']
    libs = (
        [
            "/dir1/liblapack.a",
            "/dir2/libpython3.6.dylib",  # name may contain periods
            "/dir1/libblas.a",
            "/dir3/libz.so",
            "libmpi.so.20.10.1",  # shared object libraries may be versioned
        ]
        if sys.platform != "win32"
        else [
            "/dir1/liblapack.lib",
            "/dir2/libpython3.6.dll",
            "/dir1/libblas.lib",
            "/dir3/libz.dll",
            "libmpi.dll.20.10.1",
        ]
    )

    return LibraryList(libs)


@pytest.fixture()
def header_list():
    """Returns an instance of header list"""
    # Test all valid extensions: ['.h', '.hpp', '.hh', '.cuh']
    headers = [
        "/dir1/Python.h",
        "/dir2/date.time.h",
        "/dir1/pyconfig.hpp",
        "/dir3/core.hh",
        "pymem.cuh",
    ]
    h = HeaderList(headers)
    h.add_macro("-DBOOST_LIB_NAME=boost_regex")
    h.add_macro("-DBOOST_DYN_LINK")
    return h


# TODO: Remove below when llnl.util.filesystem.find_libraries becomes spec aware
plat_static_ext = "lib" if sys.platform == "win32" else "a"


plat_shared_ext = "dll" if sys.platform == "win32" else "so"


plat_apple_shared_ext = "dylib"


class TestLibraryList:
    def test_repr(self, library_list):
        x = eval(repr(library_list))
        assert library_list == x

    def test_joined_and_str(self, library_list):
        s1 = library_list.joined()
        expected = " ".join(
            [
                "/dir1/liblapack.%s" % plat_static_ext,
                "/dir2/libpython3.6.%s"
                % (plat_apple_shared_ext if sys.platform != "win32" else "dll"),
                "/dir1/libblas.%s" % plat_static_ext,
                "/dir3/libz.%s" % plat_shared_ext,
                "libmpi.%s.20.10.1" % plat_shared_ext,
            ]
        )
        assert s1 == expected

        s2 = str(library_list)
        assert s1 == s2

        s3 = library_list.joined(";")
        expected = ";".join(
            [
                "/dir1/liblapack.%s" % plat_static_ext,
                "/dir2/libpython3.6.%s"
                % (plat_apple_shared_ext if sys.platform != "win32" else "dll"),
                "/dir1/libblas.%s" % plat_static_ext,
                "/dir3/libz.%s" % plat_shared_ext,
                "libmpi.%s.20.10.1" % plat_shared_ext,
            ]
        )
        assert s3 == expected

    def test_flags(self, library_list):
        search_flags = library_list.search_flags
        assert "-L/dir1" in search_flags
        assert "-L/dir2" in search_flags
        assert "-L/dir3" in search_flags
        assert isinstance(search_flags, str)
        assert search_flags == "-L/dir1 -L/dir2 -L/dir3"

        link_flags = library_list.link_flags
        assert "-llapack" in link_flags
        assert "-lpython3.6" in link_flags
        assert "-lblas" in link_flags
        assert "-lz" in link_flags
        assert "-lmpi" in link_flags
        assert isinstance(link_flags, str)
        assert link_flags == "-llapack -lpython3.6 -lblas -lz -lmpi"

        ld_flags = library_list.ld_flags
        assert isinstance(ld_flags, str)
        assert ld_flags == search_flags + " " + link_flags

    def test_paths_manipulation(self, library_list):
        names = library_list.names
        assert names == ["lapack", "python3.6", "blas", "z", "mpi"]

        directories = library_list.directories
        assert directories == ["/dir1", "/dir2", "/dir3"]

    def test_get_item(self, library_list):
        a = library_list[0]
        assert a == "/dir1/liblapack.%s" % plat_static_ext

        b = library_list[:]
        assert type(b) is type(library_list)
        assert library_list == b
        assert library_list is not b

    def test_add(self, library_list):
        pylist = [
            "/dir1/liblapack.%s" % plat_static_ext,  # removed from the final list
            "/dir2/libmpi.%s" % plat_shared_ext,
            "/dir4/libnew.%s" % plat_static_ext,
        ]
        another = LibraryList(pylist)
        both = library_list + another
        assert len(both) == 7

        # Invariant
        assert both == both + both

        # Always produce an instance of LibraryList
        assert type(library_list + pylist) is type(library_list)
        assert type(pylist + library_list) is type(library_list)


class TestHeaderList:
    def test_repr(self, header_list):
        x = eval(repr(header_list))
        assert header_list == x

    def test_joined_and_str(self, header_list):
        s1 = header_list.joined()
        expected = " ".join(
            [
                "/dir1/Python.h",
                "/dir2/date.time.h",
                "/dir1/pyconfig.hpp",
                "/dir3/core.hh",
                "pymem.cuh",
            ]
        )
        assert s1 == expected

        s2 = str(header_list)
        assert s1 == s2

        s3 = header_list.joined(";")
        expected = ";".join(
            [
                "/dir1/Python.h",
                "/dir2/date.time.h",
                "/dir1/pyconfig.hpp",
                "/dir3/core.hh",
                "pymem.cuh",
            ]
        )
        assert s3 == expected

    def test_flags(self, header_list):
        include_flags = header_list.include_flags
        assert "-I/dir1" in include_flags
        assert "-I/dir2" in include_flags
        assert "-I/dir3" in include_flags
        assert isinstance(include_flags, str)
        assert include_flags == "-I/dir1 -I/dir2 -I/dir3"

        macros = header_list.macro_definitions
        assert "-DBOOST_LIB_NAME=boost_regex" in macros
        assert "-DBOOST_DYN_LINK" in macros
        assert isinstance(macros, str)
        assert macros == "-DBOOST_LIB_NAME=boost_regex -DBOOST_DYN_LINK"

        cpp_flags = header_list.cpp_flags
        assert isinstance(cpp_flags, str)
        assert cpp_flags == include_flags + " " + macros

    def test_paths_manipulation(self, header_list):
        names = header_list.names
        assert names == ["Python", "date.time", "pyconfig", "core", "pymem"]

        directories = header_list.directories
        assert directories == ["/dir1", "/dir2", "/dir3"]

    def test_get_item(self, header_list):
        a = header_list[0]
        assert a == "/dir1/Python.h"

        b = header_list[:]
        assert type(b) is type(header_list)
        assert header_list == b
        assert header_list is not b

    def test_add(self, header_list):
        pylist = [
            "/dir1/Python.h",  # removed from the final list
            "/dir2/pyconfig.hpp",
            "/dir4/date.time.h",
        ]
        another = HeaderList(pylist)
        h = header_list + another
        assert len(h) == 7

        # Invariant : l == l + l
        assert h == h + h

        # Always produce an instance of HeaderList
        assert type(header_list + pylist) is type(header_list)
        assert type(pylist + header_list) is type(header_list)


#: Directory where the data for the test below is stored
search_dir = os.path.join(spack.paths.test_path, "data", "directory_search")


@pytest.mark.parametrize(
    "lib_list,kwargs",
    [
        (["liba"], {"shared": True, "recursive": True}),
        (["liba"], {"shared": False, "recursive": True}),
        (["libc", "liba"], {"shared": True, "recursive": True}),
        (["liba", "libc"], {"shared": False, "recursive": True}),
        (["libc", "libb", "liba"], {"shared": True, "recursive": True}),
        (["liba", "libb", "libc"], {"shared": False, "recursive": True}),
    ],
)
def test_library_type_search(lib_list, kwargs):
    results = find_libraries(lib_list, search_dir, **kwargs)
    assert len(results) != 0
    for result in results:
        lib_type_ext = plat_shared_ext
        if not kwargs["shared"]:
            lib_type_ext = plat_static_ext
        assert result.endswith(lib_type_ext) or (
            kwargs["shared"] and result.endswith(plat_apple_shared_ext)
        )


@pytest.mark.parametrize(
    "search_fn,search_list,root,kwargs",
    [
        (find_libraries, "liba", search_dir, {"recursive": True}),
        (find_libraries, ["liba"], search_dir, {"recursive": True}),
        (find_libraries, "libb", search_dir, {"recursive": True}),
        (find_libraries, ["libc"], search_dir, {"recursive": True}),
        (find_libraries, ["libc", "liba"], search_dir, {"recursive": True}),
        (find_libraries, ["liba", "libc"], search_dir, {"recursive": True}),
        (find_libraries, ["libc", "libb", "liba"], search_dir, {"recursive": True}),
        (find_libraries, ["liba", "libc"], search_dir, {"recursive": True}),
        (
            find_libraries,
            ["libc", "libb", "liba"],
            search_dir,
            {"recursive": True, "shared": False},
        ),
        (find_headers, "a", search_dir, {"recursive": True}),
        (find_headers, ["a"], search_dir, {"recursive": True}),
        (find_headers, "b", search_dir, {"recursive": True}),
        (find_headers, ["c"], search_dir, {"recursive": True}),
        (find_headers, ["c", "a"], search_dir, {"recursive": True}),
        (find_headers, ["a", "c"], search_dir, {"recursive": True}),
        (find_headers, ["c", "b", "a"], search_dir, {"recursive": True}),
        (find_headers, ["a", "c"], search_dir, {"recursive": True}),
        (find_libraries, ["liba", "libd"], os.path.join(search_dir, "b"), {"recursive": False}),
        (find_headers, ["b", "d"], os.path.join(search_dir, "b"), {"recursive": False}),
    ],
)
def test_searching_order(search_fn, search_list, root, kwargs):
    # Test search
    result = search_fn(search_list, root, **kwargs)

    # The tests are set-up so that something is always found
    assert len(result) != 0

    # Now reverse the result and start discarding things
    # as soon as you have matches. In the end the list should
    # be emptied.
    rlist = list(reversed(result))

    # At this point make sure the search list is a sequence
    if isinstance(search_list, str):
        search_list = [search_list]

    # Discard entries in the order they appear in search list
    for x in search_list:
        try:
            while fnmatch.fnmatch(rlist[-1], x) or x in rlist[-1]:
                rlist.pop()
        except IndexError:
            # List is empty
            pass

    # List should be empty here
    assert len(rlist) == 0


@pytest.mark.parametrize(
    "root,search_list,kwargs,expected",
    [
        (
            search_dir,
            "*/*bar.tx?",
            {"recursive": False},
            [
                os.path.join(search_dir, os.path.join("a", "foobar.txt")),
                os.path.join(search_dir, os.path.join("b", "bar.txp")),
                os.path.join(search_dir, os.path.join("c", "bar.txt")),
            ],
        ),
        (
            search_dir,
            "*/*bar.tx?",
            {"recursive": True},
            [
                os.path.join(search_dir, os.path.join("a", "foobar.txt")),
                os.path.join(search_dir, os.path.join("b", "bar.txp")),
                os.path.join(search_dir, os.path.join("c", "bar.txt")),
            ],
        ),
    ],
)
def test_find_with_globbing(root, search_list, kwargs, expected):
    matches = find(root, search_list, **kwargs)
    assert sorted(matches) == sorted(expected)
