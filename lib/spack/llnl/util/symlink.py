# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os
import re
import shutil
import subprocess
import sys
import tempfile
from typing import Union

from llnl.util import lang, tty

from ..path import sanitize_win_longpath, system_path_filter

if sys.platform == "win32":
    from win32file import CreateHardLink


def _windows_symlink(
    src: str, dst: str, target_is_directory: bool = False, *, dir_fd: Union[int, None] = None
):
    """On Windows with System Administrator privileges this will be a normal symbolic link via
    os.symlink. On Windows without privledges the link will be a junction for a directory and a
    hardlink for a file. On Windows the various link types are:

    Symbolic Link: A link to a file or directory on the same or different volume (drive letter) or
    even to a remote file or directory (using UNC in its path). Need System Administrator
    privileges to make these.

    Hard Link: A link to a file on the same volume (drive letter) only. Every file (file's data)
    has at least 1 hard link (file's name). But when this method creates a new hard link there will
    be 2. Deleting all hard links effectively deletes the file. Don't need System Administrator
    privileges.

    Junction: A link to a directory on the same or different volume (drive letter) but not to a
    remote directory. Don't need System Administrator privileges."""
    source_path = os.path.normpath(src)
    win_source_path = source_path
    link_path = os.path.normpath(dst)

    # Perform basic checks to make sure symlinking will succeed
    if os.path.lexists(link_path):
        raise AlreadyExistsError(f"Link path ({link_path}) already exists. Cannot create link.")

    if not os.path.exists(source_path):
        if os.path.isabs(source_path):
            # An absolute source path that does not exist will result in a broken link.
            raise SymlinkError(
                f"Source path ({source_path}) is absolute but does not exist. Resulting "
                f"link would be broken so not making link."
            )
        else:
            # os.symlink can create a link when the given source path is relative to
            # the link path. Emulate this behavior and check to see if the source exists
            # relative to the link path ahead of link creation to prevent broken
            # links from being made.
            link_parent_dir = os.path.dirname(link_path)
            relative_path = os.path.join(link_parent_dir, source_path)
            if os.path.exists(relative_path):
                # In order to work on windows, the source path needs to be modified to be
                # relative because hardlink/junction dont resolve relative paths the same
                # way as os.symlink. This is ignored on other operating systems.
                win_source_path = relative_path
            else:
                raise SymlinkError(
                    f"The source path ({source_path}) is not relative to the link path "
                    f"({link_path}). Resulting link would be broken so not making link."
                )

    # Create the symlink
    if not _windows_can_symlink():
        _windows_create_link(win_source_path, link_path)
    else:
        os.symlink(source_path, link_path, target_is_directory=os.path.isdir(source_path))


def _windows_islink(path: str) -> bool:
    """Override os.islink to give correct answer for spack logic.

    For Non-Windows: a link can be determined with the os.path.islink method.
    Windows-only methods will return false for other operating systems.

    For Windows: spack considers symlinks, hard links, and junctions to
    all be links, so if any of those are True, return True.

    Args:
        path (str): path to check if it is a link.

    Returns:
         bool - whether the path is any kind link or not.
    """
    return any([os.path.islink(path), _windows_is_junction(path), _windows_is_hardlink(path)])


def _windows_is_hardlink(path: str) -> bool:
    """Determines if a path is a windows hard link. This is accomplished
    by looking at the number of links using os.stat. A non-hard-linked file
    will have a st_nlink value of 1, whereas a hard link will have a value
    larger than 1. Note that both the original and hard-linked file will
    return True because they share the same inode.

    Args:
        path (str): Windows path to check for a hard link

    Returns:
         bool - Whether the path is a hard link or not.
    """
    if sys.platform != "win32" or os.path.islink(path) or not os.path.exists(path):
        return False

    return os.stat(path).st_nlink > 1


def _windows_is_junction(path: str) -> bool:
    """Determines if a path is a windows junction. A junction can be
    determined using a bitwise AND operation between the file's
    attribute bitmask and the known junction bitmask (0x400).

    Args:
        path (str): A non-file path

    Returns:
        bool - whether the path is a junction or not.
    """
    if sys.platform != "win32" or os.path.islink(path) or os.path.isfile(path):
        return False

    import ctypes.wintypes

    get_file_attributes = ctypes.windll.kernel32.GetFileAttributesW  # type: ignore[attr-defined]
    get_file_attributes.argtypes = (ctypes.wintypes.LPWSTR,)
    get_file_attributes.restype = ctypes.wintypes.DWORD

    invalid_file_attributes = 0xFFFFFFFF
    reparse_point = 0x400
    file_attr = get_file_attributes(str(path))

    if file_attr == invalid_file_attributes:
        return False

    return file_attr & reparse_point > 0


@lang.memoized
def _windows_can_symlink() -> bool:
    """
    Determines if windows is able to make a symlink depending on
    the system configuration and the level of the user's permissions.
    """
    if sys.platform != "win32":
        tty.warn("windows_can_symlink method can't be used on non-Windows OS.")
        return False

    tempdir = tempfile.mkdtemp()

    dpath = os.path.join(tempdir, "dpath")
    fpath = os.path.join(tempdir, "fpath.txt")

    dlink = os.path.join(tempdir, "dlink")
    flink = os.path.join(tempdir, "flink.txt")

    import llnl.util.filesystem as fs

    fs.touchp(fpath)
    fs.mkdirp(dpath)

    try:
        os.symlink(dpath, dlink)
        can_symlink_directories = os.path.islink(dlink)
    except OSError:
        can_symlink_directories = False

    try:
        os.symlink(fpath, flink)
        can_symlink_files = os.path.islink(flink)
    except OSError:
        can_symlink_files = False

    # Cleanup the test directory
    shutil.rmtree(tempdir)

    return can_symlink_directories and can_symlink_files


def _windows_create_link(source: str, link: str):
    """
    Attempts to create a Hard Link or Junction as an alternative
    to a symbolic link. This is called when symbolic links cannot
    be created.
    """
    if sys.platform != "win32":
        raise SymlinkError("windows_create_link method can't be used on non-Windows OS.")
    elif os.path.isdir(source):
        _windows_create_junction(source=source, link=link)
    elif os.path.isfile(source):
        _windows_create_hard_link(path=source, link=link)
    else:
        raise SymlinkError(
            f"Cannot create link from {source}. It is neither a file nor a directory."
        )


def _windows_create_junction(source: str, link: str):
    """Duly verify that the path and link are eligible to create a junction,
    then create the junction.
    """
    if sys.platform != "win32":
        raise SymlinkError("windows_create_junction method can't be used on non-Windows OS.")
    elif not os.path.exists(source):
        raise SymlinkError("Source path does not exist, cannot create a junction.")
    elif os.path.lexists(link):
        raise AlreadyExistsError("Link path already exists, cannot create a junction.")
    elif not os.path.isdir(source):
        raise SymlinkError("Source path is not a directory, cannot create a junction.")

    import subprocess

    cmd = ["cmd", "/C", "mklink", "/J", link, source]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = proc.communicate()
    tty.debug(out.decode())
    if proc.returncode != 0:
        err_str = err.decode()
        tty.error(err_str)
        raise SymlinkError("Make junction command returned a non-zero return code.", err_str)


def _windows_create_hard_link(path: str, link: str):
    """Duly verify that the path and link are eligible to create a hard
    link, then create the hard link.
    """
    if sys.platform != "win32":
        raise SymlinkError("windows_create_hard_link method can't be used on non-Windows OS.")
    elif not os.path.exists(path):
        raise SymlinkError(f"File path {path} does not exist. Cannot create hard link.")
    elif os.path.lexists(link):
        raise AlreadyExistsError(f"Link path ({link}) already exists. Cannot create hard link.")
    elif not os.path.isfile(path):
        raise SymlinkError(f"File path ({link}) is not a file. Cannot create hard link.")
    else:
        tty.debug(f"Creating hard link {link} pointing to {path}")
        CreateHardLink(link, path)


def _windows_readlink(path: str, *, dir_fd=None):
    """Spack utility to override of os.readlink method to work cross platform"""
    if _windows_is_hardlink(path):
        return _windows_read_hard_link(path)
    elif _windows_is_junction(path):
        return _windows_read_junction(path)
    else:
        return sanitize_win_longpath(os.readlink(path, dir_fd=dir_fd))


def _windows_read_hard_link(link: str) -> str:
    """Find all of the files that point to the same inode as the link"""
    if sys.platform != "win32":
        raise SymlinkError("Can't read hard link on non-Windows OS.")
    link = os.path.abspath(link)
    fsutil_cmd = ["fsutil", "hardlink", "list", link]
    proc = subprocess.Popen(fsutil_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    out, err = proc.communicate()
    if proc.returncode != 0:
        raise SymlinkError(f"An error occurred while reading hard link: {err.decode()}")

    # fsutil response does not include the drive name, so append it back to each linked file.
    drive, link_tail = os.path.splitdrive(os.path.abspath(link))
    links = set([os.path.join(drive, p) for p in out.decode().splitlines()])
    links.remove(link)
    if len(links) == 1:
        return links.pop()
    elif len(links) > 1:
        # TODO: How best to handle the case where 3 or more paths point to a single inode?
        raise SymlinkError(f"Found multiple paths pointing to the same inode {links}")
    else:
        raise SymlinkError("Cannot determine hard link source path.")


def _windows_read_junction(link: str):
    """Find the path that a junction points to."""
    if sys.platform != "win32":
        raise SymlinkError("Can't read junction on non-Windows OS.")

    link = os.path.abspath(link)
    link_basename = os.path.basename(link)
    link_parent = os.path.dirname(link)
    fsutil_cmd = ["dir", "/a:l", link_parent]
    proc = subprocess.Popen(fsutil_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    out, err = proc.communicate()
    if proc.returncode != 0:
        raise SymlinkError(f"An error occurred while reading junction: {err.decode()}")
    matches = re.search(rf"<JUNCTION>\s+{link_basename} \[(.*)]", out.decode())
    if matches:
        return matches.group(1)
    else:
        raise SymlinkError("Could not find junction path.")


@system_path_filter
def resolve_link_target_relative_to_the_link(link):
    """
    os.path.isdir uses os.path.exists, which for links will check
    the existence of the link target. If the link target is relative to
    the link, we need to construct a pathname that is valid from
    our cwd (which may not be the same as the link's directory)
    """
    target = readlink(link)
    if os.path.isabs(target):
        return target
    link_dir = os.path.dirname(os.path.abspath(link))
    return os.path.join(link_dir, target)


if sys.platform == "win32":
    symlink = _windows_symlink
    readlink = _windows_readlink
    islink = _windows_islink
else:
    symlink = os.symlink
    readlink = os.readlink
    islink = os.path.islink


class SymlinkError(RuntimeError):
    """Exception class for errors raised while creating symlinks,
    junctions and hard links
    """


class AlreadyExistsError(SymlinkError):
    """Link path already exists."""
