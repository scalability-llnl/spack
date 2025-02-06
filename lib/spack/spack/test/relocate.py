# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import re
import shutil

import pytest

import spack.platforms
import spack.relocate
import spack.relocate_text as relocate_text
import spack.repo
import spack.util.executable

pytestmark = pytest.mark.not_on_windows("Tests fail on Windows")


def skip_unless_linux(f):
    return pytest.mark.skipif(
        str(spack.platforms.real_host()) != "linux",
        reason="implementation currently requires linux",
    )(f)


def rpaths_for(new_binary):
    """Return the RPATHs or RUNPATHs of a binary."""
    patchelf = spack.util.executable.which("patchelf")
    output = patchelf("--print-rpath", str(new_binary), output=str)
    return output.strip()


def text_in_bin(text, binary):
    with open(str(binary), "rb") as f:
        data = f.read()
        f.seek(0)
        pat = re.compile(text.encode("utf-8"))
        if not pat.search(data):
            return False
        return True


@pytest.fixture()
def make_dylib(tmpdir_factory):
    """Create a shared library with unfriendly qualities.

    - Writes the same rpath twice
    - Writes its install path as an absolute path
    """
    cc = spack.util.executable.which("cc")

    def _factory(abs_install_name="abs", extra_rpaths=[]):
        assert all(extra_rpaths)

        tmpdir = tmpdir_factory.mktemp(abs_install_name + "-".join(extra_rpaths).replace("/", ""))
        src = tmpdir.join("foo.c")
        src.write("int foo() { return 1; }\n")

        filename = "foo.dylib"
        lib = tmpdir.join(filename)

        args = ["-shared", str(src), "-o", str(lib)]
        rpaths = list(extra_rpaths)
        if abs_install_name.startswith("abs"):
            args += ["-install_name", str(lib)]
        else:
            args += ["-install_name", "@rpath/" + filename]

        if abs_install_name.endswith("rpath"):
            rpaths.append(str(tmpdir))

        args.extend("-Wl,-rpath," + s for s in rpaths)

        cc(*args)

        return (str(tmpdir), filename)

    return _factory


@pytest.fixture()
def make_object_file(tmpdir):
    cc = spack.util.executable.which("cc")

    def _factory():
        src = tmpdir.join("bar.c")
        src.write("int bar() { return 2; }\n")

        filename = "bar.o"
        lib = tmpdir.join(filename)

        args = ["-c", str(src), "-o", str(lib)]

        cc(*args)

        return (str(tmpdir), filename)

    return _factory


@pytest.fixture()
def copy_binary(prefix_like):
    """Returns a function that copies a binary somewhere and
    returns the new location.
    """

    def _copy_somewhere(orig_binary):
        new_root = orig_binary.mkdtemp().mkdir(prefix_like)
        new_binary = new_root.join("main.x")
        shutil.copy(str(orig_binary), str(new_binary))
        return new_binary

    return _copy_somewhere


@pytest.mark.requires_executables("patchelf", "gcc")
@skip_unless_linux
def test_relocate_text_bin(binary_with_rpaths, prefix_like):
    prefix = "/usr/" + prefix_like
    prefix_bytes = prefix.encode("utf-8")
    new_prefix = "/foo/" + prefix_like
    new_prefix_bytes = new_prefix.encode("utf-8")
    # Compile an "Hello world!" executable and set RPATHs
    executable = binary_with_rpaths(rpaths=[prefix + "/lib", prefix + "/lib64"])

    # Relocate the RPATHs
    spack.relocate.relocate_text_bin([str(executable)], {prefix_bytes: new_prefix_bytes})

    # Some compilers add rpaths so ensure changes included in final result
    assert "%s/lib:%s/lib64" % (new_prefix, new_prefix) in rpaths_for(executable)


@pytest.mark.requires_executables("patchelf", "gcc")
@skip_unless_linux
def test_relocate_elf_binaries_absolute_paths(binary_with_rpaths, copy_binary, prefix_tmpdir):
    # Create an executable, set some RPATHs, copy it to another location
    orig_binary = binary_with_rpaths(rpaths=[str(prefix_tmpdir.mkdir("lib")), "/usr/lib64"])
    new_binary = copy_binary(orig_binary)

    spack.relocate.relocate_elf_binaries(
        binaries=[str(new_binary)], prefix_to_prefix={str(orig_binary.dirpath()): "/foo"}
    )

    # Some compilers add rpaths so ensure changes included in final result
    assert "/foo/lib:/usr/lib64" in rpaths_for(new_binary)


@pytest.mark.requires_executables("patchelf", "gcc")
@skip_unless_linux
def test_relocate_text_bin_with_message(binary_with_rpaths, copy_binary, prefix_tmpdir):
    orig_binary = binary_with_rpaths(
        rpaths=[
            str(prefix_tmpdir.mkdir("lib")),
            str(prefix_tmpdir.mkdir("lib64")),
            "/opt/local/lib",
        ],
        message=str(prefix_tmpdir),
    )
    new_binary = copy_binary(orig_binary)

    # Check original directory is in the executable and the new one is not
    assert text_in_bin(str(prefix_tmpdir), new_binary)
    assert not text_in_bin(str(new_binary.dirpath()), new_binary)

    # Check this call succeed
    orig_path_bytes = str(orig_binary.dirpath()).encode("utf-8")
    new_path_bytes = str(new_binary.dirpath()).encode("utf-8")

    spack.relocate.relocate_text_bin([str(new_binary)], {orig_path_bytes: new_path_bytes})

    # Check original directory is not there anymore and it was
    # substituted with the new one
    assert not text_in_bin(str(prefix_tmpdir), new_binary)
    assert text_in_bin(str(new_binary.dirpath()), new_binary)


def test_relocate_text_bin_raise_if_new_prefix_is_longer(tmpdir):
    short_prefix = b"/short"
    long_prefix = b"/much/longer"
    fpath = str(tmpdir.join("fakebin"))
    with open(fpath, "w", encoding="utf-8") as f:
        f.write("/short")
    with pytest.raises(relocate_text.BinaryTextReplaceError):
        spack.relocate.relocate_text_bin([fpath], {short_prefix: long_prefix})


@pytest.mark.requires_executables("install_name_tool", "cc")
def test_fixup_macos_rpaths(make_dylib, make_object_file):
    compiler_cls = spack.repo.PATH.get_pkg_class("apple-clang")
    compiler_version = compiler_cls.determine_version("cc")
    try:
        # See https://forums.swift.org/t/xcode-ships-llvm-15-but-swift-builds-llvm-16/67377
        xcode_major_version = int(compiler_version.split(".")[0])
    except IndexError:
        pytest.xfail("cannot determine the major version of XCode")

    # For each of these tests except for the "correct" case, the first fixup
    # should make changes, and the second fixup should be a null-op.
    fixup_rpath = spack.relocate.fixup_macos_rpath

    no_rpath = []
    duplicate_rpaths = ["/usr", "/usr"]
    bad_rpath = ["/nonexistent/path"]

    # Non-relocatable library id and duplicate rpaths
    (root, filename) = make_dylib("abs", duplicate_rpaths)
    # XCode 15 ships a new linker that takes care of deduplication
    if xcode_major_version < 15:
        assert fixup_rpath(root, filename)
    assert not fixup_rpath(root, filename)

    # Hardcoded but relocatable library id (but we do NOT relocate)
    (root, filename) = make_dylib("abs_with_rpath", no_rpath)
    assert not fixup_rpath(root, filename)

    # Library id uses rpath but there are extra duplicate rpaths
    (root, filename) = make_dylib("rpath", duplicate_rpaths)
    # XCode 15 ships a new linker that takes care of deduplication
    if xcode_major_version < 15:
        assert fixup_rpath(root, filename)
    assert not fixup_rpath(root, filename)

    # Shared library was constructed with relocatable id from the get-go
    (root, filename) = make_dylib("rpath", no_rpath)
    assert not fixup_rpath(root, filename)

    # Non-relocatable library id
    (root, filename) = make_dylib("abs", no_rpath)
    assert not fixup_rpath(root, filename)

    # Relocatable with executable paths and loader paths
    (root, filename) = make_dylib("rpath", ["@executable_path/../lib", "@loader_path"])
    assert not fixup_rpath(root, filename)

    # Non-relocatable library id but nonexistent rpath
    (root, filename) = make_dylib("abs", bad_rpath)
    assert fixup_rpath(root, filename)
    assert not fixup_rpath(root, filename)

    # Duplicate nonexistent rpath will need *two* passes
    (root, filename) = make_dylib("rpath", bad_rpath * 2)
    assert fixup_rpath(root, filename)
    # XCode 15 ships a new linker that takes care of deduplication
    if xcode_major_version < 15:
        assert fixup_rpath(root, filename)
    assert not fixup_rpath(root, filename)

    # Test on an object file, which *also* has type 'application/x-mach-binary'
    # but should be ignored (no ID headers, no RPATH)
    # (this is a corner case for GCC installation)
    (root, filename) = make_object_file()
    assert not fixup_rpath(root, filename)
