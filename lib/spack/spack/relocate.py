# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import collections
import itertools
import os
import re
import sys
from collections import OrderedDict
from typing import List, Optional

import macholib.mach_o
import macholib.MachO

import llnl.util.filesystem as fs
import llnl.util.lang
import llnl.util.tty as tty
from llnl.util.lang import memoized
from llnl.util.symlink import readlink, symlink

import spack.error
import spack.store
import spack.util.elf as elf
import spack.util.executable as executable

from .relocate_text import BinaryFilePrefixReplacer, TextFilePrefixReplacer


class InstallRootStringError(spack.error.SpackError):
    def __init__(self, file_path, root_path):
        """Signal that the relocated binary still has the original
        Spack's store root string

        Args:
            file_path (str): path of the binary
            root_path (str): original Spack's store root string
        """
        super().__init__(
            "\n %s \ncontains string\n %s \n"
            "after replacing it in rpaths.\n"
            "Package should not be relocated.\n Use -a to override." % (file_path, root_path)
        )


@memoized
def _patchelf() -> Optional[executable.Executable]:
    """Return the full path to the patchelf binary, if available, else None."""
    import spack.bootstrap

    if sys.platform == "darwin":
        return None

    with spack.bootstrap.ensure_bootstrap_configuration():
        return spack.bootstrap.ensure_patchelf_in_path_or_raise()


def _decode_macho_data(bytestring):
    return bytestring.rstrip(b"\x00").decode("ascii")


def macho_find_paths(orig_rpaths, deps, idpath, prefix_to_prefix):
    """
    Inputs
    original rpaths from mach-o binaries
    dependency libraries for mach-o binaries
    id path of mach-o libraries
    old install directory layout root
    prefix_to_prefix dictionary which maps prefixes in the old directory layout
    to directories in the new directory layout
    Output
    paths_to_paths dictionary which maps all of the old paths to new paths
    """
    paths_to_paths = dict()
    # Sort from longest path to shortest, to ensure we try /foo/bar/baz before /foo/bar
    prefix_iteration_order = sorted(prefix_to_prefix, key=len, reverse=True)
    for orig_rpath in orig_rpaths:
        for old_prefix in prefix_iteration_order:
            new_prefix = prefix_to_prefix[old_prefix]
            if orig_rpath.startswith(old_prefix):
                new_rpath = re.sub(re.escape(old_prefix), new_prefix, orig_rpath)
                paths_to_paths[orig_rpath] = new_rpath
                break
        else:
            paths_to_paths[orig_rpath] = orig_rpath

    if idpath:
        for old_prefix in prefix_iteration_order:
            new_prefix = prefix_to_prefix[old_prefix]
            if idpath.startswith(old_prefix):
                paths_to_paths[idpath] = re.sub(re.escape(old_prefix), new_prefix, idpath)
                break

    for dep in deps:
        for old_prefix in prefix_iteration_order:
            new_prefix = prefix_to_prefix[old_prefix]
            if dep.startswith(old_prefix):
                paths_to_paths[dep] = re.sub(re.escape(old_prefix), new_prefix, dep)
                break

        if dep.startswith("@"):
            paths_to_paths[dep] = dep

    return paths_to_paths


def modify_macho_object(cur_path, rpaths, deps, idpath, paths_to_paths):
    """
    This function is used to make machO buildcaches on macOS by
    replacing old paths with new paths using install_name_tool
    Inputs:
    mach-o binary to be modified
    original rpaths
    original dependency paths
    original id path if a mach-o library
    dictionary mapping paths in old install layout to new install layout
    """
    # avoid error message for libgcc_s
    if "libgcc_" in cur_path:
        return
    args = []

    if idpath:
        new_idpath = paths_to_paths.get(idpath, None)
        if new_idpath and not idpath == new_idpath:
            args += [("-id", new_idpath)]

    for dep in deps:
        new_dep = paths_to_paths.get(dep)
        if new_dep and dep != new_dep:
            args += [("-change", dep, new_dep)]

    new_rpaths = []
    for orig_rpath in rpaths:
        new_rpath = paths_to_paths.get(orig_rpath)
        if new_rpath and not orig_rpath == new_rpath:
            args_to_add = ("-rpath", orig_rpath, new_rpath)
            if args_to_add not in args and new_rpath not in new_rpaths:
                args += [args_to_add]
                new_rpaths.append(new_rpath)

    # Deduplicate and flatten
    args = list(itertools.chain.from_iterable(llnl.util.lang.dedupe(args)))
    install_name_tool = executable.Executable("install_name_tool")
    if args:
        with fs.edit_in_place_through_temporary_file(cur_path) as temp_path:
            install_name_tool(*args, temp_path)


def macholib_get_paths(cur_path):
    """Get rpaths, dependent libraries, and library id of mach-o objects."""
    headers = []
    try:
        headers = macholib.MachO.MachO(cur_path).headers
    except ValueError:
        pass
    if not headers:
        tty.warn("Failed to read Mach-O headers: {0}".format(cur_path))
        commands = []
    else:
        if len(headers) > 1:
            # Reproduce original behavior of only returning the last mach-O
            # header section
            tty.warn("Encountered fat binary: {0}".format(cur_path))
        if headers[-1].filetype == "dylib_stub":
            tty.warn("File is a stub, not a full library: {0}".format(cur_path))
        commands = headers[-1].commands

    LC_ID_DYLIB = macholib.mach_o.LC_ID_DYLIB
    LC_LOAD_DYLIB = macholib.mach_o.LC_LOAD_DYLIB
    LC_RPATH = macholib.mach_o.LC_RPATH

    ident = None
    rpaths = []
    deps = []
    for load_command, dylib_command, data in commands:
        cmd = load_command.cmd
        if cmd == LC_RPATH:
            rpaths.append(_decode_macho_data(data))
        elif cmd == LC_LOAD_DYLIB:
            deps.append(_decode_macho_data(data))
        elif cmd == LC_ID_DYLIB:
            ident = _decode_macho_data(data)

    return (rpaths, deps, ident)


def _set_elf_rpaths_and_interpreter(
    target: str, rpaths: List[str], interpreter: Optional[str] = None
) -> Optional[str]:
    """Replace the original RPATH of the target with the paths passed as arguments.

    Args:
        target: target executable. Must be an ELF object.
        rpaths: paths to be set in the RPATH
        interpreter: optionally set the interpreter

    Returns:
        A string concatenating the stdout and stderr of the call to ``patchelf`` if it was invoked
    """
    # Join the paths using ':' as a separator
    rpaths_str = ":".join(rpaths)

    try:
        # TODO: error handling is not great here?
        # TODO: revisit the use of --force-rpath as it might be conditional
        # TODO: if we want to support setting RUNPATH from binary packages
        args = ["--force-rpath", "--set-rpath", rpaths_str]
        if interpreter:
            args.extend(["--set-interpreter", interpreter])
        args.append(target)
        return _patchelf()(*args, output=str, error=str)
    except executable.ProcessError as e:
        tty.warn(str(e))
        return None


def relocate_macho_binaries(path_names, prefix_to_prefix):
    """
    Use macholib python package to get the rpaths, depedent libraries
    and library identity for libraries from the MachO object. Modify them
    with the replacement paths queried from the dictionary mapping old layout
    prefixes to hashes and the dictionary mapping hashes to the new layout
    prefixes.
    """

    for path_name in path_names:
        # Corner case where macho object file ended up in the path name list
        if path_name.endswith(".o"):
            continue
        # get the paths in the old prefix
        rpaths, deps, idpath = macholib_get_paths(path_name)
        # get the mapping of paths in the old prerix to the new prefix
        paths_to_paths = macho_find_paths(rpaths, deps, idpath, prefix_to_prefix)
        # replace the old paths with new paths
        modify_macho_object(path_name, rpaths, deps, idpath, paths_to_paths)


def relocate_elf_binaries(binaries, prefix_to_prefix):
    """Take a list of binaries, and an ordered dictionary of
    prefix to prefix mapping, and update the rpaths accordingly."""

    # Transform to binary string
    prefix_to_prefix = OrderedDict(
        (k.encode("utf-8"), v.encode("utf-8")) for (k, v) in prefix_to_prefix.items()
    )

    for path in binaries:
        try:
            elf.substitute_rpath_and_pt_interp_in_place_or_raise(path, prefix_to_prefix)
        except elf.ElfCStringUpdatesFailed as e:
            # Fall back to `patchelf --set-rpath ... --set-interpreter ...`
            rpaths = e.rpath.new_value.decode("utf-8").split(":") if e.rpath else []
            interpreter = e.pt_interp.new_value.decode("utf-8") if e.pt_interp else None
            _set_elf_rpaths_and_interpreter(path, rpaths=rpaths, interpreter=interpreter)


def warn_if_link_cant_be_relocated(link, target):
    if not os.path.isabs(target):
        return
    tty.warn('Symbolic link at "{}" to "{}" cannot be relocated'.format(link, target))


def relocate_links(links, prefix_to_prefix):
    """Relocate links to a new install prefix."""
    regex = re.compile("|".join(re.escape(p) for p in prefix_to_prefix.keys()))
    for link in links:
        old_target = readlink(link)
        match = regex.match(old_target)

        # No match.
        if match is None:
            warn_if_link_cant_be_relocated(link, old_target)
            continue

        new_target = prefix_to_prefix[match.group()] + old_target[match.end() :]
        os.unlink(link)
        symlink(new_target, link)


def relocate_text(files, prefixes):
    """Relocate text file from the original installation prefix to the
    new prefix.

    Relocation also affects the the path in Spack's sbang script.

    Args:
        files (list): Text files to be relocated
        prefixes (OrderedDict): String prefixes which need to be changed
    """
    TextFilePrefixReplacer.from_strings_or_bytes(prefixes).apply(files)


def relocate_text_bin(binaries, prefixes):
    """Replace null terminated path strings hard-coded into binaries.

    The new install prefix must be shorter than the original one.

    Args:
        binaries (list): binaries to be relocated
        prefixes (OrderedDict): String prefixes which need to be changed.

    Raises:
      spack.relocate_text.BinaryTextReplaceError: when the new path is longer than the old path
    """
    return BinaryFilePrefixReplacer.from_strings_or_bytes(prefixes).apply(binaries)


def is_macho_magic(magic: bytes) -> bool:
    return (
        # In order of popularity: 64-bit mach-o le/be, 32-bit mach-o le/be.
        magic.startswith(b"\xCF\xFA\xED\xFE")
        or magic.startswith(b"\xFE\xED\xFA\xCF")
        or magic.startswith(b"\xCE\xFA\xED\xFE")
        or magic.startswith(b"\xFE\xED\xFA\xCE")
        # universal binaries: 0xcafebabe be (most common?) or 0xbebafeca le (not sure if exists).
        # Here we need to disambiguate mach-o and JVM class files. In mach-o the next 4 bytes are
        # the number of binaries; in JVM class files it's the java version number. We assume there
        # are less than 10 binaries in a universal binary.
        or (magic.startswith(b"\xCA\xFE\xBA\xBE") and int.from_bytes(magic[4:8], "big") < 10)
        or (magic.startswith(b"\xBE\xBA\xFE\xCA") and int.from_bytes(magic[4:8], "little") < 10)
    )


def is_elf_magic(magic: bytes) -> bool:
    return magic.startswith(b"\x7FELF")


def is_binary(filename: str) -> bool:
    """Returns true iff a file is likely binary"""
    with open(filename, "rb") as f:
        magic = f.read(8)

    return is_macho_magic(magic) or is_elf_magic(magic)


# Memoize this due to repeated calls to libraries in the same directory.
@llnl.util.lang.memoized
def _exists_dir(dirname):
    return os.path.isdir(dirname)


def is_macho_binary(path):
    try:
        with open(path, "rb") as f:
            return is_macho_magic(f.read(4))
    except OSError:
        return False


def fixup_macos_rpath(root, filename):
    """Apply rpath fixups to the given file.

    Args:
        root: absolute path to the parent directory
        filename: relative path to the library or binary

    Returns:
        True if fixups were applied, else False
    """
    abspath = os.path.join(root, filename)

    if not is_macho_binary(abspath):
        return False

    # Get Mach-O header commands
    (rpath_list, deps, id_dylib) = macholib_get_paths(abspath)

    # Convert rpaths list to (name -> number of occurrences)
    add_rpaths = set()
    del_rpaths = set()
    rpaths = collections.defaultdict(int)
    for rpath in rpath_list:
        rpaths[rpath] += 1

    args = []

    # Check dependencies for non-rpath entries
    spack_root = spack.store.STORE.layout.root
    for name in deps:
        if name.startswith(spack_root):
            tty.debug("Spack-installed dependency for {0}: {1}".format(abspath, name))
            (dirname, basename) = os.path.split(name)
            if dirname != root or dirname in rpaths:
                # Only change the rpath if it's a dependency *or* if the root
                # rpath was already added to the library (this is to prevent
                # GCC or similar getting rpaths when they weren't at all
                # configured)
                args += ["-change", name, "@rpath/" + basename]
                add_rpaths.add(dirname.rstrip("/"))

    # Check for nonexistent rpaths (often added by spack linker overzealousness
    # with both lib/ and lib64/) and duplicate rpaths
    for rpath, count in rpaths.items():
        if rpath.startswith("@loader_path") or rpath.startswith("@executable_path"):
            # Allowable relative paths
            pass
        elif not _exists_dir(rpath):
            tty.debug("Nonexistent rpath in {0}: {1}".format(abspath, rpath))
            del_rpaths.add(rpath)
        elif count > 1:
            # Rpath should only be there once, but it can sometimes be
            # duplicated between Spack's compiler and libtool. If there are
            # more copies of the same one, something is very odd....
            tty_debug = tty.debug if count == 2 else tty.warn
            tty_debug("Rpath appears {0} times in {1}: {2}".format(count, abspath, rpath))
            del_rpaths.add(rpath)

    # Delete bad rpaths
    for rpath in del_rpaths:
        args += ["-delete_rpath", rpath]

    # Add missing rpaths that are not set for deletion
    for rpath in add_rpaths - del_rpaths - set(rpaths):
        args += ["-add_rpath", rpath]

    if not args:
        # No fixes needed
        return False

    with fs.edit_in_place_through_temporary_file(abspath) as temp_path:
        executable.Executable("install_name_tool")(*args, temp_path)
    return True


def fixup_macos_rpaths(spec):
    """Remove duplicate and nonexistent rpaths.

    Some autotools packages write their own ``-rpath`` entries in addition to
    those implicitly added by the Spack compiler wrappers. On Linux these
    duplicate rpaths are eliminated, but on macOS they result in multiple
    entries which makes it harder to adjust with ``install_name_tool
    -delete_rpath``.
    """
    if spec.external or spec.virtual:
        tty.warn("external or virtual package cannot be fixed up: {0!s}".format(spec))
        return False

    if "platform=darwin" not in spec:
        raise NotImplementedError("fixup_macos_rpaths requires macOS")

    applied = 0

    libs = frozenset(["lib", "lib64", "libexec", "plugins", "Library", "Frameworks"])
    prefix = spec.prefix

    if not os.path.exists(prefix):
        raise RuntimeError(
            "Could not fix up install prefix spec {0} because it does "
            "not exist: {1!s}".format(prefix, spec.name)
        )

    # Explore the installation prefix of the spec
    for root, dirs, files in os.walk(prefix, topdown=True):
        dirs[:] = set(dirs) & libs
        for name in files:
            try:
                needed_fix = fixup_macos_rpath(root, name)
            except Exception as e:
                tty.warn("Failed to apply library fixups to: {0}/{1}: {2!s}".format(root, name, e))
                needed_fix = False
            if needed_fix:
                applied += 1

    specname = spec.format("{name}{/hash:7}")
    if applied:
        tty.info(
            "Fixed rpaths for {0:d} {1} installed to {2}".format(
                applied, "binary" if applied == 1 else "binaries", specname
            )
        )
    else:
        tty.debug("No rpath fixup needed for " + specname)
