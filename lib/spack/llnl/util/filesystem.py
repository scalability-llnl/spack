# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import collections
import collections.abc
import errno
import fnmatch
import glob
import hashlib
import itertools
import numbers
import os
import pathlib
import posixpath
import re
import shutil
import stat
import sys
import tempfile
from contextlib import contextmanager
from itertools import accumulate
from typing import (
    Callable,
    Deque,
    Dict,
    Generator,
    Iterable,
    List,
    Match,
    Optional,
    Sequence,
    Set,
    Tuple,
    Union,
)

import llnl.util.symlink
from llnl.util import tty
from llnl.util.lang import dedupe, fnmatch_translate_multiple, memoized
from llnl.util.symlink import islink, readlink, resolve_link_target_relative_to_the_link, symlink

from ..path import path_to_os_path, system_path_filter

if sys.platform != "win32":
    import grp
    import pwd
else:
    import win32security


__all__ = [
    "FileFilter",
    "FileList",
    "HeaderList",
    "LibraryList",
    "ancestor",
    "can_access",
    "change_sed_delimiter",
    "copy_mode",
    "filter_file",
    "find",
    "find_first",
    "find_headers",
    "find_all_headers",
    "find_libraries",
    "find_system_libraries",
    "force_remove",
    "force_symlink",
    "getuid",
    "chgrp",
    "chmod_x",
    "copy",
    "install",
    "copy_tree",
    "install_tree",
    "is_exe",
    "join_path",
    "last_modification_time_recursive",
    "library_extensions",
    "mkdirp",
    "partition_path",
    "prefixes",
    "remove_dead_links",
    "remove_directory_contents",
    "remove_if_dead_link",
    "remove_linked_tree",
    "rename",
    "set_executable",
    "set_install_permissions",
    "touch",
    "touchp",
    "traverse_tree",
    "unset_executable_mode",
    "working_dir",
    "keep_modification_time",
    "BaseDirectoryVisitor",
    "visit_directory_tree",
]

Path = Union[str, pathlib.Path]

if sys.version_info < (3, 7, 4):
    # monkeypatch shutil.copystat to fix PermissionError when copying read-only
    # files on Lustre when using Python < 3.7.4

    def copystat(src, dst, follow_symlinks=True):
        """Copy file metadata
        Copy the permission bits, last access time, last modification time, and
        flags from `src` to `dst`. On Linux, copystat() also copies the "extended
        attributes" where possible. The file contents, owner, and group are
        unaffected. `src` and `dst` are path names given as strings.
        If the optional flag `follow_symlinks` is not set, symlinks aren't
        followed if and only if both `src` and `dst` are symlinks.
        """

        def _nop(args, ns=None, follow_symlinks=None):
            pass

        # follow symlinks (aka don't not follow symlinks)
        follow = follow_symlinks or not (islink(src) and islink(dst))
        if follow:
            # use the real function if it exists
            def lookup(name):
                return getattr(os, name, _nop)

        else:
            # use the real function only if it exists
            # *and* it supports follow_symlinks
            def lookup(name):
                fn = getattr(os, name, _nop)
                if sys.version_info >= (3, 3):
                    if fn in os.supports_follow_symlinks:  # novermin
                        return fn
                return _nop

        st = lookup("stat")(src, follow_symlinks=follow)
        mode = stat.S_IMODE(st.st_mode)
        lookup("utime")(dst, ns=(st.st_atime_ns, st.st_mtime_ns), follow_symlinks=follow)

        # We must copy extended attributes before the file is (potentially)
        # chmod()'ed read-only, otherwise setxattr() will error with -EACCES.
        shutil._copyxattr(src, dst, follow_symlinks=follow)

        try:
            lookup("chmod")(dst, mode, follow_symlinks=follow)
        except NotImplementedError:
            # if we got a NotImplementedError, it's because
            #   * follow_symlinks=False,
            #   * lchown() is unavailable, and
            #   * either
            #       * fchownat() is unavailable or
            #       * fchownat() doesn't implement AT_SYMLINK_NOFOLLOW.
            #         (it returned ENOSUP.)
            # therefore we're out of options--we simply cannot chown the
            # symlink.  give up, suppress the error.
            # (which is what shutil always did in this circumstance.)
            pass
        if hasattr(st, "st_flags"):
            try:
                lookup("chflags")(dst, st.st_flags, follow_symlinks=follow)
            except OSError as why:
                for err in "EOPNOTSUPP", "ENOTSUP":
                    if hasattr(errno, err) and why.errno == getattr(errno, err):
                        break
                else:
                    raise

    shutil.copystat = copystat


def polite_path(components: Iterable[str]):
    """
    Given a list of strings which are intended to be path components,
    generate a path, and format each component to avoid generating extra
    path entries.

    For example all "/", "\", and ":" characters will be replaced with
    "_". Other characters like "=" will also be replaced.
    """
    return os.path.join(*[polite_filename(x) for x in components])


@memoized
def _polite_antipattern():
    # A regex of all the characters we don't want in a filename
    return re.compile(r"[^A-Za-z0-9_+.-]")


def polite_filename(filename: str) -> str:
    """
    Replace generally problematic filename characters with underscores.

    This differs from sanitize_filename in that it is more aggressive in
    changing characters in the name. For example it removes "=" which can
    confuse path parsing in external tools.
    """
    # This character set applies for both Windows and Linux. It does not
    # account for reserved filenames in Windows.
    return _polite_antipattern().sub("_", filename)


def getuid() -> Union[str, int]:
    """Returns os getuid on non Windows
    On Windows returns 0 for admin users, login string otherwise
    This is in line with behavior from get_owner_uid which
    always returns the login string on Windows
    """
    if sys.platform == "win32":
        import ctypes

        # If not admin, use the string name of the login as a unique ID
        if ctypes.windll.shell32.IsUserAnAdmin() == 0:
            return os.getlogin()
        return 0
    else:
        return os.getuid()


def _win_rename(src, dst):
    # os.replace will still fail if on Windows (but not POSIX) if the dst
    # is a symlink to a directory (all other cases have parity Windows <-> Posix)
    if os.path.islink(dst) and os.path.isdir(os.path.realpath(dst)):
        if os.path.samefile(src, dst):
            # src and dst are the same
            # do nothing and exit early
            return
        # If dst exists and is a symlink to a directory
        # we need to remove dst and then perform rename/replace
        # this is safe to do as there's no chance src == dst now
        os.remove(dst)
    os.replace(src, dst)


@system_path_filter
def msdos_escape_parens(path):
    """MS-DOS interprets parens as grouping parameters even in a quoted string"""
    if sys.platform == "win32":
        return path.replace("(", "^(").replace(")", "^)")
    else:
        return path


@system_path_filter
def rename(src, dst):
    # On Windows, os.rename will fail if the destination file already exists
    # os.replace is the same as os.rename on POSIX and is MoveFileExW w/
    # the MOVEFILE_REPLACE_EXISTING flag on Windows
    # Windows invocation is abstracted behind additonal logic handling
    # remaining cases of divergent behavior accross platforms
    if sys.platform == "win32":
        _win_rename(src, dst)
    else:
        os.replace(src, dst)


@system_path_filter
def path_contains_subdirectory(path, root):
    norm_root = os.path.abspath(root).rstrip(os.path.sep) + os.path.sep
    norm_path = os.path.abspath(path).rstrip(os.path.sep) + os.path.sep
    return norm_path.startswith(norm_root)


#: This generates the library filenames that may appear on any OS.
library_extensions = ["a", "la", "so", "tbd", "dylib"]


def possible_library_filenames(library_names):
    """Given a collection of library names like 'libfoo', generate the set of
    library filenames that may be found on the system (e.g. libfoo.so).
    """
    lib_extensions = library_extensions
    return set(
        ".".join((lib, extension))
        for lib, extension in itertools.product(library_names, lib_extensions)
    )


def paths_containing_libs(paths, library_names):
    """Given a collection of filesystem paths, return the list of paths that
    which include one or more of the specified libraries.
    """
    required_lib_fnames = possible_library_filenames(library_names)

    rpaths_to_include = []
    paths = path_to_os_path(*paths)
    for path in paths:
        fnames = set(os.listdir(path))
        if fnames & required_lib_fnames:
            rpaths_to_include.append(path)

    return rpaths_to_include


def filter_file(
    regex: str,
    repl: Union[str, Callable[[Match], str]],
    *filenames: str,
    string: bool = False,
    backup: bool = False,
    ignore_absent: bool = False,
    start_at: Optional[str] = None,
    stop_at: Optional[str] = None,
    encoding: Optional[str] = "utf-8",
) -> None:
    r"""Like sed, but uses python regular expressions.

    Filters every line of each file through regex and replaces the file with a filtered version.
    Preserves mode of filtered files.

    As with re.sub, ``repl`` can be either a string or a callable. If it is a callable, it is
    passed the match object and should return a suitable replacement string.  If it is a string, it
    can contain ``\1``, ``\2``, etc. to represent back-substitution as sed would allow.

    Args:
        regex: The regular expression to search for
        repl: The string to replace matches with
        *filenames: One or more files to search and replace string: Treat regex as a plain string.
            Default it False backup: Make backup file(s) suffixed with ``~``. Default is False
        ignore_absent: Ignore any files that don't exist. Default is False
        start_at: Marker used to start applying the replacements. If a text line matches this
            marker filtering is started at the next line. All contents before the marker and the
            marker itself are copied verbatim. Default is to start filtering from the first line of
            the file.
        stop_at: Marker used to stop scanning the file further. If a text line matches this marker
            filtering is stopped and the rest of the file is copied verbatim. Default is to filter
            until the end of the file.
        encoding: The encoding to use when reading and writing the files. Default is None, which
            uses the system's default encoding.
    """
    # Allow strings to use \1, \2, etc. for replacement, like sed
    if not callable(repl):
        unescaped = repl.replace(r"\\", "\\")

        def replace_groups_with_groupid(m: Match) -> str:
            def groupid_to_group(x):
                return m.group(int(x.group(1)))

            return re.sub(r"\\([1-9])", groupid_to_group, unescaped)

        repl = replace_groups_with_groupid

    if string:
        regex = re.escape(regex)
    regex_compiled = re.compile(regex)
    for path in path_to_os_path(*filenames):
        if ignore_absent and not os.path.exists(path):
            tty.debug(f'FILTER FILE: file "{path}" not found. Skipping to next file.')
            continue
        else:
            tty.debug(f'FILTER FILE: {path} [replacing "{regex}"]')

        fd, temp_path = tempfile.mkstemp(
            prefix=f"{os.path.basename(path)}.", dir=os.path.dirname(path)
        )
        os.close(fd)

        shutil.copy(path, temp_path)
        errored = False

        try:
            # Open as a text file and filter until the end of the file is reached, or we found a
            # marker in the line if it was specified. To avoid translating line endings (\n to
            # \r\n and vice-versa) use newline="".
            with open(
                temp_path, mode="r", errors="surrogateescape", newline="", encoding=encoding
            ) as input_file, open(
                path, mode="w", errors="surrogateescape", newline="", encoding=encoding
            ) as output_file:
                if start_at is None and stop_at is None:  # common case, avoids branching in loop
                    for line in input_file:
                        output_file.write(re.sub(regex_compiled, repl, line))
                else:
                    # state is -1 before start_at; 0 between; 1 after stop_at
                    state = 0 if start_at is None else -1
                    for line in input_file:
                        if state == 0:
                            if stop_at == line.strip():
                                state = 1
                            else:
                                line = re.sub(regex_compiled, repl, line)
                        elif state == -1 and start_at == line.strip():
                            state = 0
                        output_file.write(line)

        except BaseException:
            # restore the original file
            os.rename(temp_path, path)
            errored = True
            raise

        finally:
            if not errored and not backup:
                os.unlink(temp_path)


class FileFilter:
    """Convenience class for calling ``filter_file`` a lot."""

    def __init__(self, *filenames):
        self.filenames = filenames

    def filter(
        self,
        regex: str,
        repl: Union[str, Callable[[Match], str]],
        string: bool = False,
        backup: bool = False,
        ignore_absent: bool = False,
        start_at: Optional[str] = None,
        stop_at: Optional[str] = None,
    ) -> None:
        return filter_file(
            regex,
            repl,
            *self.filenames,
            string=string,
            backup=backup,
            ignore_absent=ignore_absent,
            start_at=start_at,
            stop_at=stop_at,
        )


def change_sed_delimiter(old_delim, new_delim, *filenames):
    """Find all sed search/replace commands and change the delimiter.

    e.g., if the file contains seds that look like ``'s///'``, you can
    call ``change_sed_delimiter('/', '@', file)`` to change the
    delimiter to ``'@'``.

    Note that this routine will fail if the delimiter is ``'`` or ``"``.
    Handling those is left for future work.

    Parameters:
        old_delim (str): The delimiter to search for
        new_delim (str): The delimiter to replace with
        *filenames: One or more files to search and replace
    """
    assert len(old_delim) == 1
    assert len(new_delim) == 1

    # TODO: handle these cases one day?
    assert old_delim != '"'
    assert old_delim != "'"
    assert new_delim != '"'
    assert new_delim != "'"

    whole_lines = "^s@([^@]*)@(.*)@[gIp]$"
    whole_lines = whole_lines.replace("@", old_delim)

    single_quoted = r"'s@((?:\\'|[^@'])*)@((?:\\'|[^'])*)@[gIp]?'"
    single_quoted = single_quoted.replace("@", old_delim)

    double_quoted = r'"s@((?:\\"|[^@"])*)@((?:\\"|[^"])*)@[gIp]?"'
    double_quoted = double_quoted.replace("@", old_delim)

    repl = r"s@\1@\2@g"
    repl = repl.replace("@", new_delim)
    filenames = path_to_os_path(*filenames)
    for f in filenames:
        filter_file(whole_lines, repl, f)
        filter_file(single_quoted, "'%s'" % repl, f)
        filter_file(double_quoted, '"%s"' % repl, f)


@contextmanager
def exploding_archive_catch(stage):
    # Check for an exploding tarball, i.e. one that doesn't expand to
    # a single directory.  If the tarball *didn't* explode, move its
    # contents to the staging source directory & remove the container
    # directory.  If the tarball did explode, just rename the tarball
    # directory to the staging source directory.
    #
    # NOTE: The tar program on Mac OS X will encode HFS metadata in
    # hidden files, which can end up *alongside* a single top-level
    # directory.  We initially ignore presence of hidden files to
    # accomodate these "semi-exploding" tarballs but ensure the files
    # are copied to the source directory.

    # Expand all tarballs in their own directory to contain
    # exploding tarballs.
    tarball_container = os.path.join(stage.path, "spack-expanded-archive")
    mkdirp(tarball_container)
    orig_dir = os.getcwd()
    os.chdir(tarball_container)
    try:
        yield
        # catch an exploding archive on sucessful extraction
        os.chdir(orig_dir)
        exploding_archive_handler(tarball_container, stage)
    except Exception as e:
        # return current directory context to previous on failure
        os.chdir(orig_dir)
        raise e


@system_path_filter
def exploding_archive_handler(tarball_container, stage):
    """
    Args:
        tarball_container: where the archive was expanded to
        stage: Stage object referencing filesystem location
            where archive is being expanded
    """
    files = os.listdir(tarball_container)
    non_hidden = [f for f in files if not f.startswith(".")]
    if len(non_hidden) == 1:
        src = os.path.join(tarball_container, non_hidden[0])
        if os.path.isdir(src):
            stage.srcdir = non_hidden[0]
            shutil.move(src, stage.source_path)
            if len(files) > 1:
                files.remove(non_hidden[0])
                for f in files:
                    src = os.path.join(tarball_container, f)
                    dest = os.path.join(stage.path, f)
                    shutil.move(src, dest)
            os.rmdir(tarball_container)
        else:
            # This is a non-directory entry (e.g., a patch file) so simply
            # rename the tarball container to be the source path.
            shutil.move(tarball_container, stage.source_path)
    else:
        shutil.move(tarball_container, stage.source_path)


@system_path_filter(arg_slice=slice(1))
def get_owner_uid(path, err_msg=None) -> Union[str, int]:
    """Returns owner UID of path destination
    On non Windows this is the value of st_uid
    On Windows this is the login string associated with the
     owning user.

    """
    if not os.path.exists(path):
        mkdirp(path, mode=stat.S_IRWXU)

        p_stat = os.stat(path)
        if p_stat.st_mode & stat.S_IRWXU != stat.S_IRWXU:
            tty.error(
                "Expected {0} to support mode {1}, but it is {2}".format(
                    path, stat.S_IRWXU, p_stat.st_mode
                )
            )

            raise OSError(errno.EACCES, err_msg.format(path, path) if err_msg else "")
    else:
        p_stat = os.stat(path)

    if sys.platform != "win32":
        owner_uid = p_stat.st_uid
    else:
        sid = win32security.GetFileSecurity(
            path, win32security.OWNER_SECURITY_INFORMATION
        ).GetSecurityDescriptorOwner()
        owner_uid = win32security.LookupAccountSid(None, sid)[0]
    return owner_uid


@system_path_filter
def set_install_permissions(path):
    """Set appropriate permissions on the installed file."""
    # If this points to a file maintained in a Spack prefix, it is assumed that
    # this function will be invoked on the target. If the file is outside a
    # Spack-maintained prefix, the permissions should not be modified.
    if islink(path):
        return
    if os.path.isdir(path):
        os.chmod(path, 0o755)
    else:
        os.chmod(path, 0o644)


def group_ids(uid=None):
    """Get group ids that a uid is a member of.

    Arguments:
        uid (int): id of user, or None for current user

    Returns:
        (list of int): gids of groups the user is a member of
    """
    if sys.platform == "win32":
        tty.warn("Function is not supported on Windows")
        return []

    if uid is None:
        uid = getuid()

    pwd_entry = pwd.getpwuid(uid)
    user = pwd_entry.pw_name

    # user's primary group id may not be listed in grp (i.e. /etc/group)
    # you have to check pwd for that, so start the list with that
    gids = [pwd_entry.pw_gid]

    return sorted(set(gids + [g.gr_gid for g in grp.getgrall() if user in g.gr_mem]))


@system_path_filter(arg_slice=slice(1))
def chgrp(path, group, follow_symlinks=True):
    """Implement the bash chgrp function on a single path"""
    if sys.platform == "win32":
        raise OSError("Function 'chgrp' is not supported on Windows")

    if isinstance(group, str):
        gid = grp.getgrnam(group).gr_gid
    else:
        gid = group
    if os.stat(path).st_gid == gid:
        return
    if follow_symlinks:
        os.chown(path, -1, gid)
    else:
        os.lchown(path, -1, gid)


@system_path_filter(arg_slice=slice(1))
def chmod_x(entry, perms):
    """Implements chmod, treating all executable bits as set using the chmod
    utility's `+X` option.
    """
    mode = os.stat(entry).st_mode
    if os.path.isfile(entry):
        if not mode & (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH):
            perms &= ~stat.S_IXUSR
            perms &= ~stat.S_IXGRP
            perms &= ~stat.S_IXOTH
    os.chmod(entry, perms)


@system_path_filter
def copy_mode(src, dest):
    """Set the mode of dest to that of src unless it is a link."""
    if islink(dest):
        return
    src_mode = os.stat(src).st_mode
    dest_mode = os.stat(dest).st_mode
    if src_mode & stat.S_IXUSR:
        dest_mode |= stat.S_IXUSR
    if src_mode & stat.S_IXGRP:
        dest_mode |= stat.S_IXGRP
    if src_mode & stat.S_IXOTH:
        dest_mode |= stat.S_IXOTH
    os.chmod(dest, dest_mode)


@system_path_filter
def unset_executable_mode(path):
    mode = os.stat(path).st_mode
    mode &= ~stat.S_IXUSR
    mode &= ~stat.S_IXGRP
    mode &= ~stat.S_IXOTH
    os.chmod(path, mode)


@system_path_filter
def copy(src, dest, _permissions=False):
    """Copy the file(s) *src* to the file or directory *dest*.

    If *dest* specifies a directory, the file will be copied into *dest*
    using the base filename from *src*.

    *src* may contain glob characters.

    Parameters:
        src (str): the file(s) to copy
        dest (str): the destination file or directory
        _permissions (bool): for internal use only

    Raises:
        IOError: if *src* does not match any files or directories
        ValueError: if *src* matches multiple files but *dest* is
            not a directory
    """
    if _permissions:
        tty.debug("Installing {0} to {1}".format(src, dest))
    else:
        tty.debug("Copying {0} to {1}".format(src, dest))

    files = glob.glob(src)
    if not files:
        raise IOError("No such file or directory: '{0}'".format(src))
    if len(files) > 1 and not os.path.isdir(dest):
        raise ValueError(
            "'{0}' matches multiple files but '{1}' is not a directory".format(src, dest)
        )

    for src in files:
        # Expand dest to its eventual full path if it is a directory.
        dst = dest
        if os.path.isdir(dest):
            dst = join_path(dest, os.path.basename(src))

        shutil.copy(src, dst)

        if _permissions:
            set_install_permissions(dst)
            copy_mode(src, dst)


@system_path_filter
def install(src, dest):
    """Install the file(s) *src* to the file or directory *dest*.

    Same as :py:func:`copy` with the addition of setting proper
    permissions on the installed file.

    Parameters:
        src (str): the file(s) to install
        dest (str): the destination file or directory

    Raises:
        IOError: if *src* does not match any files or directories
        ValueError: if *src* matches multiple files but *dest* is
            not a directory
    """
    copy(src, dest, _permissions=True)


@system_path_filter
def copy_tree(
    src: str,
    dest: str,
    symlinks: bool = True,
    ignore: Optional[Callable[[str], bool]] = None,
    _permissions: bool = False,
):
    """Recursively copy an entire directory tree rooted at *src*.

    If the destination directory *dest* does not already exist, it will
    be created as well as missing parent directories.

    *src* may contain glob characters.

    If *symlinks* is true, symbolic links in the source tree are represented
    as symbolic links in the new tree and the metadata of the original links
    will be copied as far as the platform allows; if false, the contents and
    metadata of the linked files are copied to the new tree.

    If *ignore* is set, then each path relative to *src* will be passed to
    this function; the function returns whether that path should be skipped.

    Parameters:
        src (str): the directory to copy
        dest (str): the destination directory
        symlinks (bool): whether or not to preserve symlinks
        ignore (typing.Callable): function indicating which files to ignore
        _permissions (bool): for internal use only

    Raises:
        IOError: if *src* does not match any files or directories
        ValueError: if *src* is a parent directory of *dest*
    """
    if _permissions:
        tty.debug("Installing {0} to {1}".format(src, dest))
    else:
        tty.debug("Copying {0} to {1}".format(src, dest))

    abs_dest = os.path.abspath(dest)
    if not abs_dest.endswith(os.path.sep):
        abs_dest += os.path.sep

    files = glob.glob(src)
    if not files:
        raise IOError("No such file or directory: '{0}'".format(src))

    # For Windows hard-links and junctions, the source path must exist to make a symlink. Add
    # all symlinks to this list while traversing the tree, then when finished, make all
    # symlinks at the end.
    links = []

    for src in files:
        abs_src = os.path.abspath(src)
        if not abs_src.endswith(os.path.sep):
            abs_src += os.path.sep

        # Stop early to avoid unnecessary recursion if being asked to copy
        # from a parent directory.
        if abs_dest.startswith(abs_src):
            raise ValueError(
                "Cannot copy ancestor directory {0} into {1}".format(abs_src, abs_dest)
            )

        mkdirp(abs_dest)

        for s, d in traverse_tree(
            abs_src,
            abs_dest,
            order="pre",
            follow_links=not symlinks,
            ignore=ignore,
            follow_nonexisting=True,
        ):
            if islink(s):
                link_target = resolve_link_target_relative_to_the_link(s)
                if symlinks:
                    target = readlink(s)
                    if os.path.isabs(target):

                        def escaped_path(path):
                            return path.replace("\\", r"\\")

                        new_target = re.sub(escaped_path(abs_src), escaped_path(abs_dest), target)
                        if new_target != target:
                            tty.debug("Redirecting link {0} to {1}".format(target, new_target))
                            target = new_target

                    links.append((target, d, s))
                    continue

                elif os.path.isdir(link_target):
                    mkdirp(d)
                else:
                    shutil.copyfile(s, d)
            else:
                if os.path.isdir(s):
                    mkdirp(d)
                else:
                    shutil.copy2(s, d)

            if _permissions:
                set_install_permissions(d)
                copy_mode(s, d)

    for target, d, s in links:
        symlink(target, d)
        if _permissions:
            set_install_permissions(d)
            copy_mode(s, d)


@system_path_filter
def install_tree(src, dest, symlinks=True, ignore=None):
    """Recursively install an entire directory tree rooted at *src*.

    Same as :py:func:`copy_tree` with the addition of setting proper
    permissions on the installed files and directories.

    Parameters:
        src (str): the directory to install
        dest (str): the destination directory
        symlinks (bool): whether or not to preserve symlinks
        ignore (typing.Callable): function indicating which files to ignore

    Raises:
        IOError: if *src* does not match any files or directories
        ValueError: if *src* is a parent directory of *dest*
    """
    copy_tree(src, dest, symlinks=symlinks, ignore=ignore, _permissions=True)


@system_path_filter
def is_exe(path):
    """True if path is an executable file."""
    return os.path.isfile(path) and os.access(path, os.X_OK)


def has_shebang(path):
    """Returns whether a path has a shebang line. Returns False if the file cannot be opened."""
    try:
        with open(path, "rb") as f:
            return f.read(2) == b"#!"
    except OSError:
        return False


@system_path_filter
def is_nonsymlink_exe_with_shebang(path):
    """Returns whether the path is an executable regular file with a shebang. Returns False too
    when the path is a symlink to a script, and also when the file cannot be opened."""
    try:
        st = os.lstat(path)
    except OSError:
        return False

    # Should not be a symlink
    if stat.S_ISLNK(st.st_mode):
        return False

    # Should be executable
    if not st.st_mode & (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH):
        return False

    return has_shebang(path)


@system_path_filter(arg_slice=slice(1))
def chgrp_if_not_world_writable(path, group):
    """chgrp path to group if path is not world writable"""
    mode = os.stat(path).st_mode
    if not mode & stat.S_IWOTH:
        chgrp(path, group)


def mkdirp(
    *paths: str,
    mode: Optional[int] = None,
    group: Optional[Union[str, int]] = None,
    default_perms: Optional[str] = None,
):
    """Creates a directory, as well as parent directories if needed.

    Arguments:
        paths: paths to create with mkdirp
        mode: optional permissions to set on the created directory -- use OS default
            if not provided
        group: optional group for permissions of final created directory -- use OS
            default if not provided. Only used if world write permissions are not set
        default_perms: one of 'parents' or 'args'. The default permissions that are set for
            directories that are not themselves an argument for mkdirp. 'parents' means
            intermediate directories get the permissions of their direct parent directory,
            'args' means intermediate get the same permissions specified in the arguments to
            mkdirp -- default value is 'args'
    """
    default_perms = default_perms or "args"
    paths = path_to_os_path(*paths)
    for path in paths:
        if not os.path.exists(path):
            try:
                last_parent, intermediate_folders = longest_existing_parent(path)

                # create folders
                os.makedirs(path)

                # leaf folder permissions
                if mode is not None:
                    os.chmod(path, mode)
                if group:
                    chgrp_if_not_world_writable(path, group)
                    if mode is not None:
                        os.chmod(path, mode)  # reset sticky grp bit post chgrp

                # for intermediate folders, change mode just for newly created
                # ones and if mode_intermediate has been specified, otherwise
                # intermediate folders list is not populated at all and default
                # OS mode will be used
                if default_perms == "args":
                    intermediate_mode = mode
                    intermediate_group = group
                elif default_perms == "parents":
                    stat_info = os.stat(last_parent)
                    intermediate_mode = stat_info.st_mode
                    intermediate_group = stat_info.st_gid
                else:
                    msg = "Invalid value: '%s'. " % default_perms
                    msg += "Choose from 'args' or 'parents'."
                    raise ValueError(msg)

                for intermediate_path in reversed(intermediate_folders):
                    if intermediate_mode is not None:
                        os.chmod(intermediate_path, intermediate_mode)
                    if intermediate_group is not None:
                        chgrp_if_not_world_writable(intermediate_path, intermediate_group)
                        if intermediate_mode is not None:
                            os.chmod(
                                intermediate_path, intermediate_mode
                            )  # reset sticky bit after

            except OSError as e:
                if e.errno != errno.EEXIST or not os.path.isdir(path):
                    raise e
        elif not os.path.isdir(path):
            raise OSError(errno.EEXIST, "File already exists", path)


def longest_existing_parent(path: str) -> Tuple[str, List[str]]:
    """Return the last existing parent and a list of all intermediate directories
    to be created for the directory passed as input.

    Args:
        path: directory to be created
    """
    # detect missing intermediate folders
    intermediate_folders = []
    last_parent = ""
    intermediate_path = os.path.dirname(path)
    while intermediate_path:
        if os.path.lexists(intermediate_path):
            last_parent = intermediate_path
            break

        intermediate_folders.append(intermediate_path)
        intermediate_path = os.path.dirname(intermediate_path)
    return last_parent, intermediate_folders


@system_path_filter
def force_remove(*paths):
    """Remove files without printing errors.  Like ``rm -f``, does NOT
    remove directories."""
    for path in paths:
        try:
            os.remove(path)
        except OSError:
            pass


@contextmanager
@system_path_filter
def working_dir(dirname: str, *, create: bool = False):
    if create:
        mkdirp(dirname)

    orig_dir = os.getcwd()
    os.chdir(dirname)
    try:
        yield
    finally:
        os.chdir(orig_dir)


class CouldNotRestoreDirectoryBackup(RuntimeError):
    def __init__(self, inner_exception, outer_exception):
        self.inner_exception = inner_exception
        self.outer_exception = outer_exception


@contextmanager
@system_path_filter
def replace_directory_transaction(directory_name):
    """Temporarily renames a directory in the same parent dir. If the operations
    executed within the context manager don't raise an exception, the renamed directory
    is deleted. If there is an exception, the move is undone.

    Args:
        directory_name (path): absolute path of the directory name

    Returns:
        temporary directory where ``directory_name`` has been moved
    """
    # Check the input is indeed a directory with absolute path.
    # Raise before anything is done to avoid moving the wrong directory
    directory_name = os.path.abspath(directory_name)
    assert os.path.isdir(directory_name), "Not a directory: " + directory_name

    # Note: directory_name is normalized here, meaning the trailing slash is dropped,
    # so dirname is the directory's parent not the directory itself.
    tmpdir = tempfile.mkdtemp(dir=os.path.dirname(directory_name), prefix=".backup")

    # We have to jump through hoops to support Windows, since
    # os.rename(directory_name, tmpdir) errors there.
    backup_dir = os.path.join(tmpdir, "backup")
    os.rename(directory_name, backup_dir)
    tty.debug("Directory moved [src={0}, dest={1}]".format(directory_name, backup_dir))

    try:
        yield backup_dir
    except (Exception, KeyboardInterrupt, SystemExit) as inner_exception:
        # Try to recover the original directory, if this fails, raise a
        # composite exception.
        try:
            # Delete what was there, before copying back the original content
            if os.path.exists(directory_name):
                shutil.rmtree(directory_name)
            os.rename(backup_dir, directory_name)
        except Exception as outer_exception:
            raise CouldNotRestoreDirectoryBackup(inner_exception, outer_exception)

        tty.debug("Directory recovered [{0}]".format(directory_name))
        raise
    else:
        # Otherwise delete the temporary directory
        shutil.rmtree(tmpdir, ignore_errors=True)
        tty.debug("Temporary directory deleted [{0}]".format(tmpdir))


@system_path_filter
def hash_directory(directory, ignore=[]):
    """Hashes recursively the content of a directory.

    Args:
        directory (path): path to a directory to be hashed

    Returns:
        hash of the directory content
    """
    assert os.path.isdir(directory), '"directory" must be a directory!'

    md5_hash = hashlib.md5()

    # Adapted from https://stackoverflow.com/a/3431835/771663
    for root, dirs, files in os.walk(directory):
        for name in sorted(files):
            filename = os.path.join(root, name)
            if filename not in ignore:
                # TODO: if caching big files becomes an issue, convert this to
                # TODO: read in chunks. Currently it's used only for testing
                # TODO: purposes.
                with open(filename, "rb") as f:
                    md5_hash.update(f.read())

    return md5_hash.hexdigest()


@contextmanager
@system_path_filter
def write_tmp_and_move(filename: str, *, encoding: Optional[str] = None):
    """Write to a temporary file, then move into place."""
    dirname = os.path.dirname(filename)
    basename = os.path.basename(filename)
    tmp = os.path.join(dirname, ".%s.tmp" % basename)
    with open(tmp, "w", encoding=encoding) as f:
        yield f
    shutil.move(tmp, filename)


@system_path_filter
def touch(path):
    """Creates an empty file at the specified path."""
    if sys.platform == "win32":
        perms = os.O_WRONLY | os.O_CREAT
    else:
        perms = os.O_WRONLY | os.O_CREAT | os.O_NONBLOCK | os.O_NOCTTY
    fd = None
    try:
        fd = os.open(path, perms)
        os.utime(path, None)
    finally:
        if fd is not None:
            os.close(fd)


@system_path_filter
def touchp(path):
    """Like ``touch``, but creates any parent directories needed for the file."""
    mkdirp(os.path.dirname(path))
    touch(path)


@system_path_filter
def force_symlink(src, dest):
    try:
        symlink(src, dest)
    except OSError:
        os.remove(dest)
        symlink(src, dest)


@system_path_filter
def join_path(prefix, *args):
    path = str(prefix)
    for elt in args:
        path = os.path.join(path, str(elt))
    return path


@system_path_filter
def ancestor(dir, n=1):
    """Get the nth ancestor of a directory."""
    parent = os.path.abspath(dir)
    for i in range(n):
        parent = os.path.dirname(parent)
    return parent


@system_path_filter
def get_single_file(directory):
    fnames = os.listdir(directory)
    if len(fnames) != 1:
        raise ValueError("Expected exactly 1 file, got {0}".format(str(len(fnames))))
    return fnames[0]


@system_path_filter
def windows_sfn(path: os.PathLike):
    """Returns 8.3 Filename (SFN) representation of
    path

    8.3 Filenames (SFN or short filename) is a file
    naming convention used prior to Win95 that Windows
    still (and will continue to) support. This convention
    caps filenames at 8 characters, and most importantly
    does not allow for spaces in addition to other specifications.
    The scheme is generally the same as a normal Windows
    file scheme, but all spaces are removed and the filename
    is capped at 6 characters. The remaining characters are
    replaced with ~N where N is the number file in a directory
    that a given file represents i.e. Program Files and Program Files (x86)
    would be PROGRA~1 and PROGRA~2 respectively.
    Further, all file/directory names are all caps (although modern Windows
    is case insensitive in practice).
    Conversion is accomplished by fileapi.h GetShortPathNameW

    Returns paths in 8.3 Filename form

    Note: this method is a no-op on Linux

    Args:
        path: Path to be transformed into SFN (8.3 filename) format
    """
    # This should not be run-able on linux/macos
    if sys.platform != "win32":
        return path
    path = str(path)
    import ctypes

    k32 = ctypes.WinDLL("kernel32", use_last_error=True)
    # Method with null values returns size of short path name
    sz = k32.GetShortPathNameW(path, None, 0)
    # stub Windows types TCHAR[LENGTH]
    TCHAR_arr = ctypes.c_wchar * sz
    ret_str = TCHAR_arr()
    k32.GetShortPathNameW(path, ctypes.byref(ret_str), sz)
    return ret_str.value


@contextmanager
def temp_cwd():
    tmp_dir = tempfile.mkdtemp()
    try:
        with working_dir(tmp_dir):
            yield tmp_dir
    finally:
        kwargs = {}
        if sys.platform == "win32":
            kwargs["ignore_errors"] = False
            kwargs["onerror"] = readonly_file_handler(ignore_errors=True)
        shutil.rmtree(tmp_dir, **kwargs)


@system_path_filter
def can_access(file_name):
    """True if we have read/write access to the file."""
    return os.access(file_name, os.R_OK | os.W_OK)


@system_path_filter
def traverse_tree(
    source_root: str,
    dest_root: str,
    rel_path: str = "",
    *,
    order: str = "pre",
    ignore: Optional[Callable[[str], bool]] = None,
    follow_nonexisting: bool = True,
    follow_links: bool = False,
):
    """Traverse two filesystem trees simultaneously.

    Walks the LinkTree directory in pre or post order.  Yields each
    file in the source directory with a matching path from the dest
    directory, along with whether the file is a directory.
    e.g., for this tree::

        root/
          a/
            file1
            file2
          b/
            file3

    When called on dest, this yields::

        ('root',         'dest')
        ('root/a',       'dest/a')
        ('root/a/file1', 'dest/a/file1')
        ('root/a/file2', 'dest/a/file2')
        ('root/b',       'dest/b')
        ('root/b/file3', 'dest/b/file3')

    Keyword Arguments:
        order (str): Whether to do pre- or post-order traversal. Accepted
            values are 'pre' and 'post'
        ignore (typing.Callable): function indicating which files to ignore. This will also
            ignore symlinks if they point to an ignored file (regardless of whether the symlink
            is explicitly ignored); note this only supports one layer of indirection (i.e. if
            you have x -> y -> z, and z is ignored but x/y are not, then y would be ignored
            but not x). To avoid this, make sure the ignore function also ignores the symlink
            paths too.
        follow_nonexisting (bool): Whether to descend into directories in
            ``src`` that do not exit in ``dest``. Default is True
        follow_links (bool): Whether to descend into symlinks in ``src``
    """
    if order not in ("pre", "post"):
        raise ValueError("Order must be 'pre' or 'post'.")

    # List of relative paths to ignore under the src root.
    ignore = ignore or (lambda filename: False)

    # Don't descend into ignored directories
    if ignore(rel_path):
        return

    source_path = os.path.join(source_root, rel_path)
    dest_path = os.path.join(dest_root, rel_path)

    # preorder yields directories before children
    if order == "pre":
        yield (source_path, dest_path)

    for f in os.listdir(source_path):
        source_child = os.path.join(source_path, f)
        dest_child = os.path.join(dest_path, f)
        rel_child = os.path.join(rel_path, f)

        # If the source path is a link and the link's source is ignored, then ignore the link too,
        # but only do this if the ignore is defined.
        if ignore is not None:
            if islink(source_child) and not follow_links:
                target = readlink(source_child)
                all_parents = accumulate(target.split(os.sep), lambda x, y: os.path.join(x, y))
                if any(map(ignore, all_parents)):
                    tty.warn(
                        f"Skipping {source_path} because the source or a part of the source's "
                        f"path is included in the ignores."
                    )
                    continue

        # Treat as a directory
        # TODO: for symlinks, os.path.isdir looks for the link target. If the
        # target is relative to the link, then that may not resolve properly
        # relative to our cwd - see resolve_link_target_relative_to_the_link
        if os.path.isdir(source_child) and (follow_links or not islink(source_child)):
            # When follow_nonexisting isn't set, don't descend into dirs
            # in source that do not exist in dest
            if follow_nonexisting or os.path.exists(dest_child):
                tuples = traverse_tree(
                    source_root,
                    dest_root,
                    rel_child,
                    order=order,
                    ignore=ignore,
                    follow_nonexisting=follow_nonexisting,
                    follow_links=follow_links,
                )
                for t in tuples:
                    yield t

        # Treat as a file.
        elif not ignore(os.path.join(rel_path, f)):
            yield (source_child, dest_child)

    if order == "post":
        yield (source_path, dest_path)


class BaseDirectoryVisitor:
    """Base class and interface for :py:func:`visit_directory_tree`."""

    def visit_file(self, root: str, rel_path: str, depth: int) -> None:
        """Handle the non-symlink file at ``os.path.join(root, rel_path)``

        Parameters:
            root: root directory
            rel_path: relative path to current file from ``root``
            depth (int): depth of current file from the ``root`` directory"""
        pass

    def visit_symlinked_file(self, root: str, rel_path: str, depth) -> None:
        """Handle the symlink to a file at ``os.path.join(root, rel_path)``. Note: ``rel_path`` is
        the location of the symlink, not to what it is pointing to. The symlink may be dangling.

        Parameters:
            root: root directory
            rel_path: relative path to current symlink from ``root``
            depth: depth of current symlink from the ``root`` directory"""
        pass

    def before_visit_dir(self, root: str, rel_path: str, depth: int) -> bool:
        """Return True from this function to recurse into the directory at
        os.path.join(root, rel_path). Return False in order not to recurse further.

        Parameters:
            root: root directory
            rel_path: relative path to current directory from ``root``
            depth: depth of current directory from the ``root`` directory

        Returns:
            bool: ``True`` when the directory should be recursed into. ``False`` when
            not"""
        return False

    def before_visit_symlinked_dir(self, root: str, rel_path: str, depth: int) -> bool:
        """Return ``True`` to recurse into the symlinked directory and ``False`` in order not to.
        Note: ``rel_path`` is the path to the symlink itself. Following symlinked directories
        blindly can cause infinite recursion due to cycles.

        Parameters:
            root: root directory
            rel_path: relative path to current symlink from ``root``
            depth: depth of current symlink from the ``root`` directory

        Returns:
            bool: ``True`` when the directory should be recursed into. ``False`` when
            not"""
        return False

    def after_visit_dir(self, root: str, rel_path: str, depth: int) -> None:
        """Called after recursion into ``rel_path`` finished. This function is not called when
        ``rel_path`` was not recursed into.

        Parameters:
            root: root directory
            rel_path: relative path to current directory from ``root``
            depth: depth of current directory from the ``root`` directory"""
        pass

    def after_visit_symlinked_dir(self, root: str, rel_path: str, depth: int) -> None:
        """Called after recursion into ``rel_path`` finished. This function is not called when
        ``rel_path`` was not recursed into.

        Parameters:
            root: root directory
            rel_path: relative path to current symlink from ``root``
            depth: depth of current symlink from the ``root`` directory"""
        pass


def visit_directory_tree(
    root: str, visitor: BaseDirectoryVisitor, rel_path: str = "", depth: int = 0
):
    """Recurses the directory root depth-first through a visitor pattern using the interface from
    :py:class:`BaseDirectoryVisitor`

    Parameters:
        root: path of directory to recurse into
        visitor: what visitor to use
        rel_path: current relative path from the root
        depth: current depth from the root
    """
    dir = os.path.join(root, rel_path)
    dir_entries = sorted(os.scandir(dir), key=lambda d: d.name)

    for f in dir_entries:
        rel_child = os.path.join(rel_path, f.name)
        islink = f.is_symlink()
        # On Windows, symlinks to directories are distinct from symlinks to files, and it is
        # possible to create a broken symlink to a directory (e.g. using os.symlink without
        # `target_is_directory=True`), invoking `isdir` on a symlink on Windows that is broken in
        # this manner will result in an error. In this case we can work around the issue by reading
        # the target and resolving the directory ourselves
        try:
            isdir = f.is_dir()
        except OSError as e:
            if sys.platform == "win32" and hasattr(e, "winerror") and e.winerror == 5 and islink:
                # if path is a symlink, determine destination and evaluate file vs directory
                link_target = resolve_link_target_relative_to_the_link(f)
                # link_target might be relative but resolve_link_target_relative_to_the_link
                # will ensure that if so, that it is relative to the CWD and therefore makes sense
                isdir = os.path.isdir(link_target)
            else:
                raise e

        if not isdir and not islink:
            # handle non-symlink files
            visitor.visit_file(root, rel_child, depth)
        elif not isdir:
            visitor.visit_symlinked_file(root, rel_child, depth)
        elif not islink and visitor.before_visit_dir(root, rel_child, depth):
            # Handle ordinary directories
            visit_directory_tree(root, visitor, rel_child, depth + 1)
            visitor.after_visit_dir(root, rel_child, depth)
        elif islink and visitor.before_visit_symlinked_dir(root, rel_child, depth):
            # Handle symlinked directories
            visit_directory_tree(root, visitor, rel_child, depth + 1)
            visitor.after_visit_symlinked_dir(root, rel_child, depth)


@system_path_filter
def set_executable(path):
    mode = os.stat(path).st_mode
    if mode & stat.S_IRUSR:
        mode |= stat.S_IXUSR
    if mode & stat.S_IRGRP:
        mode |= stat.S_IXGRP
    if mode & stat.S_IROTH:
        mode |= stat.S_IXOTH
    os.chmod(path, mode)


@system_path_filter
def last_modification_time_recursive(path):
    path = os.path.abspath(path)
    times = [os.stat(path).st_mtime]
    times.extend(
        os.lstat(os.path.join(root, name)).st_mtime
        for root, dirs, files in os.walk(path)
        for name in dirs + files
    )
    return max(times)


@system_path_filter
def remove_empty_directories(root):
    """Ascend up from the leaves accessible from `root` and remove empty
    directories.

    Parameters:
        root (str): path where to search for empty directories
    """
    for dirpath, subdirs, files in os.walk(root, topdown=False):
        for sd in subdirs:
            sdp = os.path.join(dirpath, sd)
            try:
                os.rmdir(sdp)
            except OSError:
                pass


@system_path_filter
def remove_dead_links(root):
    """Recursively removes any dead link that is present in root.

    Parameters:
        root (str): path where to search for dead links
    """
    for dirpath, subdirs, files in os.walk(root, topdown=False):
        for f in files:
            path = join_path(dirpath, f)
            remove_if_dead_link(path)


@system_path_filter
def remove_if_dead_link(path):
    """Removes the argument if it is a dead link.

    Parameters:
        path (str): The potential dead link
    """
    if islink(path) and not os.path.exists(path):
        os.unlink(path)


def readonly_file_handler(ignore_errors=False):
    # TODO: generate stages etc. with write permissions wherever
    # so this callback is no-longer required
    """
    Generate callback for shutil.rmtree to handle permissions errors on
    Windows. Some files may unexpectedly lack write permissions even
    though they were generated by Spack on behalf of the user (e.g. the
    stage), so this callback will detect such cases and modify the
    permissions if that is the issue. For other errors, the fallback
    is either to raise (if ignore_errors is False) or ignore (if
    ignore_errors is True). This is only intended for Windows systems
    and will raise a separate error if it is ever invoked (by accident)
    on a non-Windows system.
    """

    def error_remove_readonly(func, path, exc):
        if sys.platform != "win32":
            raise RuntimeError("This method should only be invoked on Windows")
        excvalue = exc[1]
        if (
            sys.platform == "win32"
            and func in (os.rmdir, os.remove, os.unlink)
            and excvalue.errno == errno.EACCES
        ):
            # change the file to be readable,writable,executable: 0777
            os.chmod(path, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
            # retry
            func(path)
        elif not ignore_errors:
            raise

    return error_remove_readonly


@system_path_filter
def remove_linked_tree(path):
    """Removes a directory and its contents.

    If the directory is a symlink, follows the link and removes the real
    directory before removing the link.

    This method will force-delete files on Windows

    Parameters:
        path (str): Directory to be removed
    """
    kwargs = {"ignore_errors": True}

    # Windows readonly files cannot be removed by Python
    # directly.
    if sys.platform == "win32":
        kwargs["ignore_errors"] = False
        kwargs["onerror"] = readonly_file_handler(ignore_errors=True)

    if os.path.exists(path):
        if islink(path):
            shutil.rmtree(os.path.realpath(path), **kwargs)
            os.unlink(path)
        else:
            if sys.platform == "win32":
                # Adding this prefix allows shutil to remove long paths on windows
                # https://learn.microsoft.com/en-us/windows/win32/fileio/maximum-file-path-limitation?tabs=registry
                long_path_pfx = "\\\\?\\"
                if not path.startswith(long_path_pfx):
                    path = long_path_pfx + path
            shutil.rmtree(path, **kwargs)


@contextmanager
@system_path_filter
def safe_remove(*files_or_dirs):
    """Context manager to remove the files passed as input, but restore
    them in case any exception is raised in the context block.

    Args:
        *files_or_dirs: glob expressions for files or directories
            to be removed

    Returns:
        Dictionary that maps deleted files to their temporary copy
        within the context block.
    """
    # Find all the files or directories that match
    glob_matches = [glob.glob(x) for x in files_or_dirs]
    # Sort them so that shorter paths like "/foo/bar" come before
    # nested paths like "/foo/bar/baz.yaml". This simplifies the
    # handling of temporary copies below
    sorted_matches = sorted([os.path.abspath(x) for x in itertools.chain(*glob_matches)], key=len)

    # Copy files and directories in a temporary location
    removed, dst_root = {}, tempfile.mkdtemp()
    try:
        for id, file_or_dir in enumerate(sorted_matches):
            # The glob expression at the top ensures that the file/dir exists
            # at the time we enter the loop. Double check here since it might
            # happen that a previous iteration of the loop already removed it.
            # This is the case, for instance, if we remove the directory
            # "/foo/bar" before the file "/foo/bar/baz.yaml".
            if not os.path.exists(file_or_dir):
                continue
            # The monotonic ID is a simple way to make the filename
            # or directory name unique in the temporary folder
            basename = os.path.basename(file_or_dir) + "-{0}".format(id)
            temporary_path = os.path.join(dst_root, basename)
            shutil.move(file_or_dir, temporary_path)
            removed[file_or_dir] = temporary_path
        yield removed
    except BaseException:
        # Restore the files that were removed
        for original_path, temporary_path in removed.items():
            shutil.move(temporary_path, original_path)
        raise


def find_first(root: str, files: Union[Iterable[str], str], bfs_depth: int = 2) -> Optional[str]:
    """Find the first file matching a pattern.

    The following

    .. code-block:: console

       $ find /usr -name 'abc*' -o -name 'def*' -quit

    is equivalent to:

    >>> find_first("/usr", ["abc*", "def*"])

    Any glob pattern supported by fnmatch can be used.

    The search order of this method is breadth-first over directories,
    until depth bfs_depth, after which depth-first search is used.

    Parameters:
        root (str): The root directory to start searching from
        files (str or Iterable): File pattern(s) to search for
        bfs_depth (int): (advanced) parameter that specifies at which
            depth to switch to depth-first search.

    Returns:
        str or None: The matching file or None when no file is found.
    """
    if isinstance(files, str):
        files = [files]
    return FindFirstFile(root, *files, bfs_depth=bfs_depth).find()


def find(
    root: Union[Path, Sequence[Path]],
    files: Union[str, Sequence[str]],
    recursive: bool = True,
    max_depth: Optional[int] = None,
) -> List[str]:
    """Finds all files matching the patterns from ``files`` starting from ``root``. This function
    returns a deterministic result for the same input and directory structure when run multiple
    times. Symlinked directories are followed, and unique directories are searched only once. Each
    matching file is returned only once at lowest depth in case multiple paths exist due to
    symlinked directories.

    Accepts any glob characters accepted by fnmatch:

    ==========  ====================================
    Pattern     Meaning
    ==========  ====================================
    ``*``       matches one or more characters
    ``?``       matches any single character
    ``[seq]``   matches any character in ``seq``
    ``[!seq]``  matches any character not in ``seq``
    ==========  ====================================

    Examples:

    >>> find("/usr", "*.txt", recursive=True, max_depth=2)

    finds all files with the extension ``.txt`` in the directory ``/usr`` and subdirectories up to
    depth 2.

    >>> find(["/usr", "/var"], ["*.txt", "*.log"], recursive=True)

    finds all files with the extension ``.txt`` or ``.log`` in the directories ``/usr`` and
    ``/var`` at any depth.

    >>> find("/usr", "GL/*.h", recursive=True)

    finds all header files in a directory GL at any depth in the directory ``/usr``.

    Parameters:
        root: One or more root directories to start searching from
        files: One or more filename patterns to search for
        recursive: if False search only root, if True descends from roots. Defaults to True.
        max_depth: if set, don't search below this depth. Cannot be set if recursive is False

    Returns a list of absolute, matching file paths.
    """
    if isinstance(root, (str, pathlib.Path)):
        root = [root]
    elif not isinstance(root, collections.abc.Sequence):
        raise TypeError(f"'root' arg must be a path or a sequence of paths, not '{type(root)}']")

    if isinstance(files, str):
        files = [files]
    elif not isinstance(files, collections.abc.Sequence):
        raise TypeError(f"'files' arg must be str or a sequence of str, not '{type(files)}']")

    # If recursive is false, max_depth can only be None or 0
    if max_depth and not recursive:
        raise ValueError(f"max_depth ({max_depth}) cannot be set if recursive is False")

    tty.debug(f"Find (max depth = {max_depth}): {root} {files}")
    if not recursive:
        max_depth = 0
    elif max_depth is None:
        max_depth = sys.maxsize
    result = _find_max_depth(root, files, max_depth)
    tty.debug(f"Find complete: {root} {files}")
    return result


def _log_file_access_issue(e: OSError, path: str) -> None:
    tty.debug(f"find must skip {path}: {e}")


def _file_id(s: os.stat_result) -> Tuple[int, int]:
    # Note: on windows, st_ino is the file index and st_dev is the volume serial number. See
    # https://github.com/python/cpython/blob/3.9/Python/fileutils.c
    return (s.st_ino, s.st_dev)


def _dedupe_files(paths: List[str]) -> List[str]:
    """Deduplicate files by inode and device, dropping files that cannot be accessed."""
    unique_files: List[str] = []
    # tuple of (inode, device) for each file without following symlinks
    visited: Set[Tuple[int, int]] = set()
    for path in paths:
        try:
            stat_info = os.lstat(path)
        except OSError as e:
            _log_file_access_issue(e, path)
            continue
        file_id = _file_id(stat_info)
        if file_id not in visited:
            unique_files.append(path)
            visited.add(file_id)
    return unique_files


def _find_max_depth(
    roots: Sequence[Path], globs: Sequence[str], max_depth: int = sys.maxsize
) -> List[str]:
    """See ``find`` for the public API."""
    # We optimize for the common case of simple filename only patterns: a single, combined regex
    # is used. For complex patterns that include path components, we use a slower glob call from
    # every directory we visit within max_depth.
    filename_only_patterns = {
        f"pattern_{i}": os.path.normcase(x) for i, x in enumerate(globs) if "/" not in x
    }
    complex_patterns = {f"pattern_{i}": x for i, x in enumerate(globs) if "/" in x}
    regex = re.compile(fnmatch_translate_multiple(filename_only_patterns))
    # Ordered dictionary that keeps track of what pattern found which files
    matched_paths: Dict[str, List[str]] = {f"pattern_{i}": [] for i, _ in enumerate(globs)}
    # Ensure returned paths are always absolute
    roots = [os.path.abspath(r) for r in roots]
    # Breadth-first search queue. Each element is a tuple of (depth, dir)
    dir_queue: Deque[Tuple[int, str]] = collections.deque()
    # Set of visited directories. Each element is a tuple of (inode, device)
    visited_dirs: Set[Tuple[int, int]] = set()

    for root in roots:
        try:
            stat_root = os.stat(root)
        except OSError as e:
            _log_file_access_issue(e, root)
            continue
        dir_id = _file_id(stat_root)
        if dir_id not in visited_dirs:
            dir_queue.appendleft((0, root))
            visited_dirs.add(dir_id)

    while dir_queue:
        depth, curr_dir = dir_queue.pop()
        try:
            dir_iter = os.scandir(curr_dir)
        except OSError as e:
            _log_file_access_issue(e, curr_dir)
            continue

        # Use glob.glob for complex patterns.
        for pattern_name, pattern in complex_patterns.items():
            matched_paths[pattern_name].extend(
                path for path in glob.glob(os.path.join(curr_dir, pattern))
            )

        # List of subdirectories by path and (inode, device) tuple
        subdirs: List[Tuple[str, Tuple[int, int]]] = []

        with dir_iter:
            for dir_entry in dir_iter:

                # Match filename only patterns
                if filename_only_patterns:
                    m = regex.match(os.path.normcase(dir_entry.name))
                    if m:
                        for pattern_name in filename_only_patterns:
                            if m.group(pattern_name):
                                matched_paths[pattern_name].append(dir_entry.path)
                                break

                # Collect subdirectories
                if depth >= max_depth:
                    continue

                try:
                    if not dir_entry.is_dir(follow_symlinks=True):
                        continue
                    if sys.platform == "win32":
                        # Note: st_ino/st_dev on DirEntry.stat are not set on Windows, so we have
                        # to call os.stat
                        stat_info = os.stat(dir_entry.path, follow_symlinks=True)
                    else:
                        stat_info = dir_entry.stat(follow_symlinks=True)
                except OSError as e:
                    # Possible permission issue, or a symlink that cannot be resolved (ELOOP).
                    _log_file_access_issue(e, dir_entry.path)
                    continue

                subdirs.append((dir_entry.path, _file_id(stat_info)))

        # Enqueue subdirectories in a deterministic order
        if subdirs:
            subdirs.sort(key=lambda s: os.path.basename(s[0]))
            for subdir, subdir_id in subdirs:
                if subdir_id not in visited_dirs:
                    dir_queue.appendleft((depth + 1, subdir))
                    visited_dirs.add(subdir_id)

    # Sort the matched paths for deterministic output
    for paths in matched_paths.values():
        paths.sort()
    all_matching_paths = [path for paths in matched_paths.values() for path in paths]

    # We only dedupe files if we have any complex patterns, since only they can match the same file
    # multiple times
    return _dedupe_files(all_matching_paths) if complex_patterns else all_matching_paths


# Utilities for libraries and headers


class FileList(collections.abc.Sequence):
    """Sequence of absolute paths to files.

    Provides a few convenience methods to manipulate file paths.
    """

    def __init__(self, files):
        if isinstance(files, str):
            files = [files]

        self.files = list(dedupe(files))

    @property
    def directories(self):
        """Stable de-duplication of the directories where the files reside.

        >>> l = LibraryList(['/dir1/liba.a', '/dir2/libb.a', '/dir1/libc.a'])
        >>> l.directories
        ['/dir1', '/dir2']
        >>> h = HeaderList(['/dir1/a.h', '/dir1/b.h', '/dir2/c.h'])
        >>> h.directories
        ['/dir1', '/dir2']

        Returns:
            list: A list of directories
        """
        return list(dedupe(os.path.dirname(x) for x in self.files if os.path.dirname(x)))

    @property
    def basenames(self):
        """Stable de-duplication of the base-names in the list

        >>> l = LibraryList(['/dir1/liba.a', '/dir2/libb.a', '/dir3/liba.a'])
        >>> l.basenames
        ['liba.a', 'libb.a']
        >>> h = HeaderList(['/dir1/a.h', '/dir2/b.h', '/dir3/a.h'])
        >>> h.basenames
        ['a.h', 'b.h']

        Returns:
            list: A list of base-names
        """
        return list(dedupe(os.path.basename(x) for x in self.files))

    def __getitem__(self, item):
        cls = type(self)
        if isinstance(item, numbers.Integral):
            return self.files[item]
        return cls(self.files[item])

    def __add__(self, other):
        return self.__class__(dedupe(self.files + list(other)))

    def __radd__(self, other):
        return self.__add__(other)

    def __eq__(self, other):
        return self.files == other.files

    def __len__(self):
        return len(self.files)

    def joined(self, separator=" "):
        return separator.join(self.files)

    def __repr__(self):
        return self.__class__.__name__ + "(" + repr(self.files) + ")"

    def __str__(self):
        return self.joined()


class HeaderList(FileList):
    """Sequence of absolute paths to headers.

    Provides a few convenience methods to manipulate header paths and get
    commonly used compiler flags or names.
    """

    # Make sure to only match complete words, otherwise path components such
    # as "xinclude" will cause false matches.
    # Avoid matching paths such as <prefix>/include/something/detail/include,
    # e.g. in the CUDA Toolkit which ships internal libc++ headers.
    include_regex = re.compile(r"(.*?)(\binclude\b)(.*)")

    def __init__(self, files):
        super().__init__(files)

        self._macro_definitions = []
        self._directories = None

    @property
    def directories(self):
        """Directories to be searched for header files."""
        values = self._directories
        if values is None:
            values = self._default_directories()
        return list(dedupe(values))

    @directories.setter
    def directories(self, value):
        value = value or []
        # Accept a single directory as input
        if isinstance(value, str):
            value = [value]

        self._directories = [path_to_os_path(os.path.normpath(x))[0] for x in value]

    def _default_directories(self):
        """Default computation of directories based on the list of
        header files.
        """
        dir_list = super().directories
        values = []
        for d in dir_list:
            # If the path contains a subdirectory named 'include' then stop
            # there and don't add anything else to the path.
            m = self.include_regex.match(d)
            value = os.path.join(*m.group(1, 2)) if m else d
            values.append(value)
        return values

    @property
    def headers(self):
        """Stable de-duplication of the headers.

        Returns:
            list: A list of header files
        """
        return self.files

    @property
    def names(self):
        """Stable de-duplication of header names in the list without extensions

        >>> h = HeaderList(['/dir1/a.h', '/dir2/b.h', '/dir3/a.h'])
        >>> h.names
        ['a', 'b']

        Returns:
            list: A list of files without extensions
        """
        names = []

        for x in self.basenames:
            name = x

            # Valid extensions include: ['.cuh', '.hpp', '.hh', '.h']
            for ext in [".cuh", ".hpp", ".hh", ".h"]:
                i = name.rfind(ext)
                if i != -1:
                    names.append(name[:i])
                    break
            else:
                # No valid extension, should we still include it?
                names.append(name)

        return list(dedupe(names))

    @property
    def include_flags(self):
        """Include flags

        >>> h = HeaderList(['/dir1/a.h', '/dir1/b.h', '/dir2/c.h'])
        >>> h.include_flags
        '-I/dir1 -I/dir2'

        Returns:
            str: A joined list of include flags
        """
        return " ".join(["-I" + x for x in self.directories])

    @property
    def macro_definitions(self):
        """Macro definitions

        >>> h = HeaderList(['/dir1/a.h', '/dir1/b.h', '/dir2/c.h'])
        >>> h.add_macro('-DBOOST_LIB_NAME=boost_regex')
        >>> h.add_macro('-DBOOST_DYN_LINK')
        >>> h.macro_definitions
        '-DBOOST_LIB_NAME=boost_regex -DBOOST_DYN_LINK'

        Returns:
            str: A joined list of macro definitions
        """
        return " ".join(self._macro_definitions)

    @property
    def cpp_flags(self):
        """Include flags + macro definitions

        >>> h = HeaderList(['/dir1/a.h', '/dir1/b.h', '/dir2/c.h'])
        >>> h.cpp_flags
        '-I/dir1 -I/dir2'
        >>> h.add_macro('-DBOOST_DYN_LINK')
        >>> h.cpp_flags
        '-I/dir1 -I/dir2 -DBOOST_DYN_LINK'

        Returns:
            str: A joined list of include flags and macro definitions
        """
        cpp_flags = self.include_flags
        if self.macro_definitions:
            cpp_flags += " " + self.macro_definitions
        return cpp_flags

    def add_macro(self, macro):
        """Add a macro definition

        Parameters:
            macro (str): The macro to add
        """
        self._macro_definitions.append(macro)


def find_headers(headers, root, recursive=False):
    """Returns an iterable object containing a list of full paths to
    headers if found.

    Accepts any glob characters accepted by fnmatch:

    =======  ====================================
    Pattern  Meaning
    =======  ====================================
    *        matches everything
    ?        matches any single character
    [seq]    matches any character in ``seq``
    [!seq]   matches any character not in ``seq``
    =======  ====================================

    Parameters:
        headers (str or list): Header name(s) to search for
        root (str): The root directory to start searching from
        recursive (bool): if False search only root folder,
            if True descends top-down from the root. Defaults to False.

    Returns:
        HeaderList: The headers that have been found
    """
    if isinstance(headers, str):
        headers = [headers]
    elif not isinstance(headers, collections.abc.Sequence):
        message = "{0} expects a string or sequence of strings as the "
        message += "first argument [got {1} instead]"
        message = message.format(find_headers.__name__, type(headers))
        raise TypeError(message)

    # Construct the right suffix for the headers
    suffixes = [
        # C
        "h",
        # C++
        "hpp",
        "hxx",
        "hh",
        "H",
        "txx",
        "tcc",
        "icc",
        # Fortran
        "mod",
        "inc",
    ]

    # List of headers we are searching with suffixes
    headers = ["{0}.{1}".format(header, suffix) for header in headers for suffix in suffixes]

    return HeaderList(find(root, headers, recursive))


@system_path_filter
def find_all_headers(root):
    """Convenience function that returns the list of all headers found
    in the directory passed as argument.

    Args:
        root (str): directory where to look recursively for header files

    Returns:
        List of all headers found in ``root`` and subdirectories.
    """
    return find_headers("*", root=root, recursive=True)


class LibraryList(FileList):
    """Sequence of absolute paths to libraries

    Provides a few convenience methods to manipulate library paths and get
    commonly used compiler flags or names
    """

    @property
    def libraries(self):
        """Stable de-duplication of library files.

        Returns:
            list: A list of library files
        """
        return self.files

    @property
    def names(self):
        """Stable de-duplication of library names in the list

        >>> l = LibraryList(['/dir1/liba.a', '/dir2/libb.a', '/dir3/liba.so'])
        >>> l.names
        ['a', 'b']

        Returns:
            list: A list of library names
        """
        names = []

        for x in self.basenames:
            name = x
            if x.startswith("lib"):
                name = x[3:]

            # Valid extensions include: ['.dylib', '.so', '.a']
            # on non Windows platform
            # Windows valid library extensions are:
            # ['.dll', '.lib']
            valid_exts = [".dll", ".lib"] if sys.platform == "win32" else [".dylib", ".so", ".a"]
            for ext in valid_exts:
                i = name.rfind(ext)
                if i != -1:
                    names.append(name[:i])
                    break
            else:
                # No valid extension, should we still include it?
                names.append(name)

        return list(dedupe(names))

    @property
    def search_flags(self):
        """Search flags for the libraries

        >>> l = LibraryList(['/dir1/liba.a', '/dir2/libb.a', '/dir1/liba.so'])
        >>> l.search_flags
        '-L/dir1 -L/dir2'

        Returns:
            str: A joined list of search flags
        """
        return " ".join(["-L" + x for x in self.directories])

    @property
    def link_flags(self):
        """Link flags for the libraries

        >>> l = LibraryList(['/dir1/liba.a', '/dir2/libb.a', '/dir1/liba.so'])
        >>> l.link_flags
        '-la -lb'

        Returns:
            str: A joined list of link flags
        """
        return " ".join(["-l" + name for name in self.names])

    @property
    def ld_flags(self):
        """Search flags + link flags

        >>> l = LibraryList(['/dir1/liba.a', '/dir2/libb.a', '/dir1/liba.so'])
        >>> l.ld_flags
        '-L/dir1 -L/dir2 -la -lb'

        Returns:
            str: A joined list of search flags and link flags
        """
        return self.search_flags + " " + self.link_flags


def find_system_libraries(libraries, shared=True):
    """Searches the usual system library locations for ``libraries``.

    Search order is as follows:

    1. ``/lib64``
    2. ``/lib``
    3. ``/usr/lib64``
    4. ``/usr/lib``
    5. ``/usr/local/lib64``
    6. ``/usr/local/lib``

    Accepts any glob characters accepted by fnmatch:

    =======  ====================================
    Pattern  Meaning
    =======  ====================================
    *        matches everything
    ?        matches any single character
    [seq]    matches any character in ``seq``
    [!seq]   matches any character not in ``seq``
    =======  ====================================

    Parameters:
        libraries (str or list): Library name(s) to search for
        shared (bool): if True searches for shared libraries,
            otherwise for static. Defaults to True.

    Returns:
        LibraryList: The libraries that have been found
    """
    if isinstance(libraries, str):
        libraries = [libraries]
    elif not isinstance(libraries, collections.abc.Sequence):
        message = "{0} expects a string or sequence of strings as the "
        message += "first argument [got {1} instead]"
        message = message.format(find_system_libraries.__name__, type(libraries))
        raise TypeError(message)

    libraries_found = []
    search_locations = [
        "/lib64",
        "/lib",
        "/usr/lib64",
        "/usr/lib",
        "/usr/local/lib64",
        "/usr/local/lib",
    ]

    for library in libraries:
        for root in search_locations:
            result = find_libraries(library, root, shared, recursive=True)
            if result:
                libraries_found += result
                break

    return libraries_found


def find_libraries(
    libraries, root, shared=True, recursive=False, runtime=True, max_depth: Optional[int] = None
):
    """Returns an iterable of full paths to libraries found in a root dir.

    Accepts any glob characters accepted by fnmatch:

    =======  ====================================
    Pattern  Meaning
    =======  ====================================
    *        matches everything
    ?        matches any single character
    [seq]    matches any character in ``seq``
    [!seq]   matches any character not in ``seq``
    =======  ====================================

    Parameters:
        libraries (str or list): Library name(s) to search for
        root (str): The root directory to start searching from
        shared (bool): if True searches for shared libraries,
            otherwise for static. Defaults to True.
        recursive (bool): if False search only root folder,
            if True descends top-down from the root. Defaults to False.
        max_depth (int): if set, don't search below this depth. Cannot be set
            if recursive is False
        runtime (bool): Windows only option, no-op elsewhere. If true,
            search for runtime shared libs (.DLL), otherwise, search
            for .Lib files. If shared is false, this has no meaning.
            Defaults to True.

    Returns:
        LibraryList: The libraries that have been found
    """

    if isinstance(libraries, str):
        libraries = [libraries]
    elif not isinstance(libraries, collections.abc.Sequence):
        message = "{0} expects a string or sequence of strings as the "
        message += "first argument [got {1} instead]"
        message = message.format(find_libraries.__name__, type(libraries))
        raise TypeError(message)

    if sys.platform == "win32":
        static_ext = "lib"
        # For linking (runtime=False) you need the .lib files regardless of
        # whether you are doing a shared or static link
        shared_ext = "dll" if runtime else "lib"
    else:
        # Used on both Linux and macOS
        static_ext = "a"
        shared_ext = "so"

    # Construct the right suffix for the library
    if shared:
        # Used on both Linux and macOS
        suffixes = [shared_ext]
        if sys.platform == "darwin":
            # Only used on macOS
            suffixes.append("dylib")
    else:
        suffixes = [static_ext]

    # List of libraries we are searching with suffixes
    libraries = ["{0}.{1}".format(lib, suffix) for lib in libraries for suffix in suffixes]

    if not recursive:
        if max_depth:
            raise ValueError(f"max_depth ({max_depth}) cannot be set if recursive is False")
        # If not recursive, look for the libraries directly in root
        return LibraryList(find(root, libraries, recursive=False))

    # To speedup the search for external packages configured e.g. in /usr,
    # perform first non-recursive search in root/lib then in root/lib64 and
    # finally search all of root recursively. The search stops when the first
    # match is found.
    common_lib_dirs = ["lib", "lib64"]
    if sys.platform == "win32":
        common_lib_dirs.extend(["bin", "Lib"])

    for subdir in common_lib_dirs:
        dirname = join_path(root, subdir)
        if not os.path.isdir(dirname):
            continue
        found_libs = find(dirname, libraries, False)
        if found_libs:
            break
    else:
        found_libs = find(root, libraries, recursive=True, max_depth=max_depth)

    return LibraryList(found_libs)


def find_all_shared_libraries(root, recursive=False, runtime=True):
    """Convenience function that returns the list of all shared libraries found
    in the directory passed as argument.

    See documentation for `llnl.util.filesystem.find_libraries` for more information
    """
    return find_libraries("*", root=root, shared=True, recursive=recursive, runtime=runtime)


def find_all_static_libraries(root, recursive=False):
    """Convenience function that returns the list of all static libraries found
    in the directory passed as argument.

    See documentation for `llnl.util.filesystem.find_libraries` for more information
    """
    return find_libraries("*", root=root, shared=False, recursive=recursive)


def find_all_libraries(root, recursive=False):
    """Convenience function that returns the list of all libraries found
    in the directory passed as argument.

    See documentation for `llnl.util.filesystem.find_libraries` for more information
    """

    return find_all_shared_libraries(root, recursive=recursive) + find_all_static_libraries(
        root, recursive=recursive
    )


class WindowsSimulatedRPath:
    """Class representing Windows filesystem rpath analog

    One instance of this class is associated with a package (only on Windows)
    For each lib/binary directory in an associated package, this class introduces
    a symlink to any/all dependent libraries/binaries. This includes the packages
    own bin/lib directories, meaning the libraries are linked to the bianry directory
    and vis versa.
    """

    def __init__(self, package, link_install_prefix=True):
        """
        Args:
            package (spack.package_base.PackageBase): Package requiring links
            link_install_prefix (bool): Link against package's own install or stage root.
                Packages that run their own executables during build and require rpaths to
                the build directory during build time require this option. Default: install
                root
        """
        self.pkg = package
        self._addl_rpaths = set()
        self.link_install_prefix = link_install_prefix
        self._additional_library_dependents = set()

    @property
    def library_dependents(self):
        """
        Set of directories where package binaries/libraries are located.
        """
        return set([pathlib.Path(self.pkg.prefix.bin)]) | self._additional_library_dependents

    def add_library_dependent(self, *dest):
        """
        Add paths to directories or libraries/binaries to set of
        common paths that need to link against other libraries

        Specified paths should fall outside of a package's common
        link paths, i.e. the bin
        directories.
        """
        for pth in dest:
            if os.path.isfile(pth):
                new_pth = pathlib.Path(pth).parent
            else:
                new_pth = pathlib.Path(pth)
            self._additional_library_dependents.add(new_pth)

    @property
    def rpaths(self):
        """
        Set of libraries this package needs to link against during runtime
        These packages will each be symlinked into the packages lib and binary dir
        """
        dependent_libs = []
        for path in self.pkg.rpath:
            dependent_libs.extend(list(find_all_shared_libraries(path, recursive=True)))
        for extra_path in self._addl_rpaths:
            dependent_libs.extend(list(find_all_shared_libraries(extra_path, recursive=True)))
        return set([pathlib.Path(x) for x in dependent_libs])

    def add_rpath(self, *paths):
        """
        Add libraries found at the root of provided paths to runtime linking

        These are libraries found outside of the typical scope of rpath linking
        that require manual inclusion in a runtime linking scheme.
        These links are unidirectional, and are only
        intended to bring outside dependencies into this package

        Args:
            *paths (str): arbitrary number of paths to be added to runtime linking
        """
        self._addl_rpaths = self._addl_rpaths | set(paths)

    def _link(self, path: pathlib.Path, dest_dir: pathlib.Path):
        """Perform link step of simulated rpathing, installing
        simlinks of file in path to the dest_dir
        location. This method deliberately prevents
        the case where a path points to a file inside the dest_dir.
        This is because it is both meaningless from an rpath
        perspective, and will cause an error when Developer
        mode is not enabled"""

        def report_already_linked():
            # We have either already symlinked or we are encoutering a naming clash
            # either way, we don't want to overwrite existing libraries
            already_linked = islink(str(dest_file))
            tty.debug(
                "Linking library %s to %s failed, " % (str(path), str(dest_file))
                + "already linked."
                if already_linked
                else "library with name %s already exists at location %s."
                % (str(file_name), str(dest_dir))
            )

        file_name = path.name
        dest_file = dest_dir / file_name
        if not dest_file.exists() and dest_dir.exists() and not dest_file == path:
            try:
                symlink(str(path), str(dest_file))
            # For py2 compatibility, we have to catch the specific Windows error code
            # associate with trying to create a file that already exists (winerror 183)
            # Catch OSErrors missed by the SymlinkError checks
            except OSError as e:
                if sys.platform == "win32" and (e.winerror == 183 or e.errno == errno.EEXIST):
                    report_already_linked()
                else:
                    raise e
            # catch errors we raise ourselves from Spack
            except llnl.util.symlink.AlreadyExistsError:
                report_already_linked()

    def establish_link(self):
        """
        (sym)link packages to runtime dependencies based on RPath configuration for
        Windows heuristics
        """
        # from build_environment.py:463
        # The top-level package is always RPATHed. It hasn't been installed yet
        # so the RPATHs are added unconditionally

        # for each binary install dir in self.pkg (i.e. pkg.prefix.bin, pkg.prefix.lib)
        # install a symlink to each dependent library

        # do not rpath for system libraries included in the dag
        # we should not be modifying libraries managed by the Windows system
        # as this will negatively impact linker behavior and can result in permission
        # errors if those system libs are not modifiable by Spack
        if "windows-system" not in getattr(self.pkg, "tags", []):
            for library, lib_dir in itertools.product(self.rpaths, self.library_dependents):
                self._link(library, lib_dir)


@system_path_filter
@memoized
def can_access_dir(path):
    """Returns True if the argument is an accessible directory.

    Args:
        path: path to be tested

    Returns:
        True if ``path`` is an accessible directory, else False
    """
    return os.path.isdir(path) and os.access(path, os.R_OK | os.X_OK)


@system_path_filter
@memoized
def can_write_to_dir(path):
    """Return True if the argument is a directory in which we can write.

    Args:
        path: path to be tested

    Returns:
        True if ``path`` is an writeable directory, else False
    """
    return os.path.isdir(path) and os.access(path, os.R_OK | os.X_OK | os.W_OK)


@system_path_filter
@memoized
def files_in(*search_paths):
    """Returns all the files in paths passed as arguments.

    Caller must ensure that each path in ``search_paths`` is a directory.

    Args:
        *search_paths: directories to be searched

    Returns:
        List of (file, full_path) tuples with all the files found.
    """
    files = []
    for d in filter(can_access_dir, search_paths):
        files.extend(
            filter(
                lambda x: os.path.isfile(x[1]), [(f, os.path.join(d, f)) for f in os.listdir(d)]
            )
        )
    return files


def is_readable_file(file_path):
    """Return True if the path passed as argument is readable"""
    return os.path.isfile(file_path) and os.access(file_path, os.R_OK)


@system_path_filter
def search_paths_for_executables(*path_hints):
    """Given a list of path hints returns a list of paths where
    to search for an executable.

    Args:
        *path_hints (list of paths): list of paths taken into
            consideration for a search

    Returns:
        A list containing the real path of every existing directory
        in `path_hints` and its `bin` subdirectory if it exists.
    """
    executable_paths = []
    for path in path_hints:
        if not os.path.isdir(path):
            continue

        path = os.path.abspath(path)
        executable_paths.append(path)

        bin_dir = os.path.join(path, "bin")
        if os.path.isdir(bin_dir):
            executable_paths.append(bin_dir)

    return executable_paths


@system_path_filter
def search_paths_for_libraries(*path_hints):
    """Given a list of path hints returns a list of paths where
    to search for a shared library.

    Args:
        *path_hints (list of paths): list of paths taken into
            consideration for a search

    Returns:
        A list containing the real path of every existing directory
        in `path_hints` and its `lib` and `lib64` subdirectory if it exists.
    """
    library_paths = []
    for path in path_hints:
        if not os.path.isdir(path):
            continue

        path = os.path.abspath(path)
        library_paths.append(path)

        lib_dir = os.path.join(path, "lib")
        if os.path.isdir(lib_dir):
            library_paths.append(lib_dir)

        lib64_dir = os.path.join(path, "lib64")
        if os.path.isdir(lib64_dir):
            library_paths.append(lib64_dir)

    return library_paths


@system_path_filter
def partition_path(path, entry=None):
    """
    Split the prefixes of the path at the first occurrence of entry and
    return a 3-tuple containing a list of the prefixes before the entry, a
    string of the prefix ending with the entry, and a list of the prefixes
    after the entry.

    If the entry is not a node in the path, the result will be the prefix list
    followed by an empty string and an empty list.
    """
    paths = prefixes(path)

    if entry is not None:
        # Derive the index of entry within paths, which will correspond to
        # the location of the entry in within the path.
        try:
            sep = os.sep
            entries = path.split(sep)
            if entries[0].endswith(":"):
                # Handle drive letters e.g. C:/ on Windows
                entries[0] = entries[0] + sep
            i = entries.index(entry)
            if "" in entries:
                i -= 1
            return paths[:i], paths[i], paths[i + 1 :]
        except ValueError:
            pass

    return paths, "", []


@system_path_filter
def prefixes(path):
    """
    Returns a list containing the path and its ancestors, top-to-bottom.

    The list for an absolute path will not include an ``os.sep`` entry.
    For example, assuming ``os.sep`` is ``/``, given path ``/ab/cd/efg``
    the resulting paths will be, in order: ``/ab``, ``/ab/cd``, and
    ``/ab/cd/efg``

    The list for a relative path starting ``./`` will not include ``.``.
    For example, path ``./hi/jkl/mn`` results in a list with the following
    paths, in order: ``./hi``, ``./hi/jkl``, and ``./hi/jkl/mn``.

    On Windows, paths will be normalized to use ``/`` and ``/`` will always
    be used as the separator instead of ``os.sep``.

    Parameters:
        path (str): the string used to derive ancestor paths

    Returns:
        A list containing ancestor paths in order and ending with the path
    """
    if not path:
        return []
    sep = os.sep
    parts = path.strip(sep).split(sep)
    if path.startswith(sep):
        parts.insert(0, sep)
    elif parts[0].endswith(":"):
        # Handle drive letters e.g. C:/ on Windows
        parts[0] = parts[0] + sep
    paths = [os.path.join(*parts[: i + 1]) for i in range(len(parts))]

    try:
        paths.remove(sep)
    except ValueError:
        pass

    try:
        paths.remove(".")
    except ValueError:
        pass

    return paths


@system_path_filter
def remove_directory_contents(dir):
    """Remove all contents of a directory."""
    if os.path.exists(dir):
        for entry in [os.path.join(dir, entry) for entry in os.listdir(dir)]:
            if os.path.isfile(entry) or islink(entry):
                os.unlink(entry)
            else:
                shutil.rmtree(entry)


@contextmanager
@system_path_filter
def keep_modification_time(*filenames):
    """
    Context manager to keep the modification timestamps of the input files.
    Tolerates and has no effect on non-existent files and files that are
    deleted by the nested code.

    Parameters:
        *filenames: one or more files that must have their modification
            timestamps unchanged
    """
    mtimes = {}
    for f in filenames:
        if os.path.exists(f):
            mtimes[f] = os.path.getmtime(f)
    yield
    for f, mtime in mtimes.items():
        if os.path.exists(f):
            os.utime(f, (os.path.getatime(f), mtime))


@contextmanager
def temporary_dir(
    suffix: Optional[str] = None, prefix: Optional[str] = None, dir: Optional[str] = None
):
    """Create a temporary directory and cd's into it. Delete the directory
    on exit.

    Takes the same arguments as tempfile.mkdtemp()
    """
    tmp_dir = tempfile.mkdtemp(suffix=suffix, prefix=prefix, dir=dir)
    try:
        with working_dir(tmp_dir):
            yield tmp_dir
    finally:
        remove_directory_contents(tmp_dir)


@contextmanager
def edit_in_place_through_temporary_file(file_path: str) -> Generator[str, None, None]:
    """Context manager for modifying ``file_path`` in place, preserving its inode and hardlinks,
    for functions or external tools that do not support in-place editing. Notice that this function
    is unsafe in that it works with paths instead of a file descriptors, but this is by design,
    since we assume the call site will create a new inode at the same path."""
    tmp_fd, tmp_path = tempfile.mkstemp(
        dir=os.path.dirname(file_path), prefix=f"{os.path.basename(file_path)}."
    )
    # windows cannot replace a file with open fds, so close since the call site needs to replace.
    os.close(tmp_fd)
    try:
        shutil.copyfile(file_path, tmp_path, follow_symlinks=True)
        yield tmp_path
        shutil.copyfile(tmp_path, file_path, follow_symlinks=True)
    finally:
        os.unlink(tmp_path)


def filesummary(path, print_bytes=16) -> Tuple[int, bytes]:
    """Create a small summary of the given file. Does not error
    when file does not exist.

    Args:
        print_bytes (int): Number of bytes to print from start/end of file

    Returns:
        Tuple of size and byte string containing first n .. last n bytes.
        Size is 0 if file cannot be read."""
    try:
        n = print_bytes
        with open(path, "rb") as f:
            size = os.fstat(f.fileno()).st_size
            if size <= 2 * n:
                short_contents = f.read(2 * n)
            else:
                short_contents = f.read(n)
                f.seek(-n, 2)
                short_contents += b"..." + f.read(n)
        return size, short_contents
    except OSError:
        return 0, b""


class FindFirstFile:
    """Uses hybrid iterative deepening to locate the first matching
    file. Up to depth ``bfs_depth`` it uses iterative deepening, which
    mimics breadth-first with the same memory footprint as depth-first
    search, after which it switches to ordinary depth-first search using
    ``os.walk``."""

    def __init__(self, root: str, *file_patterns: str, bfs_depth: int = 2):
        """Create a small summary of the given file. Does not error
        when file does not exist.

        Args:
            root (str): directory in which to recursively search
            file_patterns (str): glob file patterns understood by fnmatch
            bfs_depth (int): until this depth breadth-first traversal is used,
                when no match is found, the mode is switched to depth-first search.
        """
        self.root = root
        self.bfs_depth = bfs_depth
        self.match: Callable

        # normcase is trivial on posix
        regex = re.compile("|".join(fnmatch.translate(os.path.normcase(p)) for p in file_patterns))

        # On case sensitive filesystems match against normcase'd paths.
        if os.path is posixpath:
            self.match = regex.match
        else:
            self.match = lambda p: regex.match(os.path.normcase(p))

    def find(self) -> Optional[str]:
        """Run the file search

        Returns:
            str or None: path of the matching file
        """
        self.file = None

        # First do iterative deepening (i.e. bfs through limited depth dfs)
        for i in range(self.bfs_depth + 1):
            if self._find_at_depth(self.root, i):
                return self.file

        # Then fall back to depth-first search
        return self._find_dfs()

    def _find_at_depth(self, path, max_depth, depth=0) -> bool:
        """Returns True when done. Notice search can be done
        either because a file was found, or because it recursed
        through all directories."""
        try:
            entries = os.scandir(path)
        except OSError:
            return True

        done = True

        with entries:
            # At max depth we look for matching files.
            if depth == max_depth:
                for f in entries:
                    # Exit on match
                    if self.match(f.name):
                        self.file = os.path.join(path, f.name)
                        return True

                    # is_dir should not require a stat call, so it's a good optimization.
                    if self._is_dir(f):
                        done = False
                return done

            # At lower depth only recurse into subdirs
            for f in entries:
                if not self._is_dir(f):
                    continue

                # If any subdir is not fully traversed, we're not done yet.
                if not self._find_at_depth(os.path.join(path, f.name), max_depth, depth + 1):
                    done = False

                # Early exit when we've found something.
                if self.file:
                    return True

            return done

    def _is_dir(self, f: os.DirEntry) -> bool:
        """Returns True when f is dir we can enter (and not a symlink)."""
        try:
            return f.is_dir(follow_symlinks=False)
        except OSError:
            return False

    def _find_dfs(self) -> Optional[str]:
        """Returns match or None"""
        for dirpath, _, filenames in os.walk(self.root):
            for file in filenames:
                if self.match(file):
                    return os.path.join(dirpath, file)
        return None
