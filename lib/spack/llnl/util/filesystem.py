# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import collections
import errno
import hashlib
import glob
import grp
import itertools
import numbers
import os
import pwd
import re
import shutil
import stat
import sys
import tempfile
from contextlib import contextmanager

import six
from compat import Sequence
from llnl.util import tty
from llnl.util.lang import dedupe, memoized
from spack.util.executable import Executable


__all__ = [
    'FileFilter',
    'FileList',
    'HeaderList',
    'LibraryList',
    'ancestor',
    'can_access',
    'change_sed_delimiter',
    'copy_mode',
    'filter_file',
    'find',
    'find_headers',
    'find_all_headers',
    'find_libraries',
    'find_system_libraries',
    'fix_darwin_install_name',
    'force_remove',
    'force_symlink',
    'chgrp',
    'chmod_x',
    'copy',
    'install',
    'copy_tree',
    'install_tree',
    'is_exe',
    'join_path',
    'last_modification_time_recursive',
    'mkdirp',
    'partition_path',
    'prefixes',
    'remove_dead_links',
    'remove_directory_contents',
    'remove_if_dead_link',
    'remove_linked_tree',
    'set_executable',
    'set_install_permissions',
    'touch',
    'touchp',
    'traverse_tree',
    'unset_executable_mode',
    'working_dir',
    'keep_modification_time'
]


def path_contains_subdirectory(path, root):
    norm_root = os.path.abspath(root).rstrip(os.path.sep) + os.path.sep
    norm_path = os.path.abspath(path).rstrip(os.path.sep) + os.path.sep
    return norm_path.startswith(norm_root)


def possible_library_filenames(library_names):
    """Given a collection of library names like 'libfoo', generate the set of
    library filenames that may be found on the system (e.g. libfoo.so). This
    generates the library filenames that may appear on any OS.
    """
    lib_extensions = ['a', 'la', 'so', 'tbd', 'dylib']
    return set(
        '.'.join((lib, extension)) for lib, extension in
        itertools.product(library_names, lib_extensions))


def paths_containing_libs(paths, library_names):
    """Given a collection of filesystem paths, return the list of paths that
    which include one or more of the specified libraries.
    """
    required_lib_fnames = possible_library_filenames(library_names)

    rpaths_to_include = []
    for path in paths:
        fnames = set(os.listdir(path))
        if fnames & required_lib_fnames:
            rpaths_to_include.append(path)

    return rpaths_to_include


def same_path(path1, path2):
    norm1 = os.path.abspath(path1).rstrip(os.path.sep)
    norm2 = os.path.abspath(path2).rstrip(os.path.sep)
    return norm1 == norm2


def filter_file(regex, repl, *filenames, **kwargs):
    r"""Like sed, but uses python regular expressions.

    Filters every line of each file through regex and replaces the file
    with a filtered version.  Preserves mode of filtered files.

    As with re.sub, ``repl`` can be either a string or a callable.
    If it is a callable, it is passed the match object and should
    return a suitable replacement string.  If it is a string, it
    can contain ``\1``, ``\2``, etc. to represent back-substitution
    as sed would allow.

    Parameters:
        regex (str): The regular expression to search for
        repl (str): The string to replace matches with
        *filenames: One or more files to search and replace

    Keyword Arguments:
        string (bool): Treat regex as a plain string. Default it False
        backup (bool): Make backup file(s) suffixed with ``~``. Default is True
        ignore_absent (bool): Ignore any files that don't exist.
            Default is False
        stop_at (str): Marker used to stop scanning the file further. If a text
            line matches this marker filtering is stopped and the rest of the
            file is copied verbatim. Default is to filter until the end of the
            file.
    """
    string = kwargs.get('string', False)
    backup = kwargs.get('backup', True)
    ignore_absent = kwargs.get('ignore_absent', False)
    stop_at = kwargs.get('stop_at', None)

    # Allow strings to use \1, \2, etc. for replacement, like sed
    if not callable(repl):
        unescaped = repl.replace(r'\\', '\\')

        def replace_groups_with_groupid(m):
            def groupid_to_group(x):
                return m.group(int(x.group(1)))
            return re.sub(r'\\([1-9])', groupid_to_group, unescaped)
        repl = replace_groups_with_groupid

    if string:
        regex = re.escape(regex)

    for filename in filenames:

        msg = 'FILTER FILE: {0} [replacing "{1}"]'
        tty.debug(msg.format(filename, regex))

        backup_filename = filename + "~"
        tmp_filename = filename + ".spack~"

        if ignore_absent and not os.path.exists(filename):
            msg = 'FILTER FILE: file "{0}" not found. Skipping to next file.'
            tty.debug(msg.format(filename))
            continue

        # Create backup file. Don't overwrite an existing backup
        # file in case this file is being filtered multiple times.
        if not os.path.exists(backup_filename):
            shutil.copy(filename, backup_filename)

        # Create a temporary file to read from. We cannot use backup_filename
        # in case filter_file is invoked multiple times on the same file.
        shutil.copy(filename, tmp_filename)

        try:
            extra_kwargs = {}
            if sys.version_info > (3, 0):
                extra_kwargs = {'errors': 'surrogateescape'}

            # Open as a text file and filter until the end of the file is
            # reached or we found a marker in the line if it was specified
            with open(tmp_filename, mode='r', **extra_kwargs) as input_file:
                with open(filename, mode='w', **extra_kwargs) as output_file:
                    # Using iter and readline is a workaround needed not to
                    # disable input_file.tell(), which will happen if we call
                    # input_file.next() implicitly via the for loop
                    for line in iter(input_file.readline, ''):
                        if stop_at is not None:
                            current_position = input_file.tell()
                            if stop_at == line.strip():
                                output_file.write(line)
                                break
                        filtered_line = re.sub(regex, repl, line)
                        output_file.write(filtered_line)
                    else:
                        current_position = None

            # If we stopped filtering at some point, reopen the file in
            # binary mode and copy verbatim the remaining part
            if current_position and stop_at:
                with open(tmp_filename, mode='rb') as input_file:
                    input_file.seek(current_position)
                    with open(filename, mode='ab') as output_file:
                        output_file.writelines(input_file.readlines())

        except BaseException:
            # clean up the original file on failure.
            shutil.move(backup_filename, filename)
            raise

        finally:
            os.remove(tmp_filename)
            if not backup and os.path.exists(backup_filename):
                os.remove(backup_filename)


class FileFilter(object):
    """Convenience class for calling ``filter_file`` a lot."""

    def __init__(self, *filenames):
        self.filenames = filenames

    def filter(self, regex, repl, **kwargs):
        return filter_file(regex, repl, *self.filenames, **kwargs)


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
    assert(len(old_delim) == 1)
    assert(len(new_delim) == 1)

    # TODO: handle these cases one day?
    assert(old_delim != '"')
    assert(old_delim != "'")
    assert(new_delim != '"')
    assert(new_delim != "'")

    whole_lines = "^s@([^@]*)@(.*)@[gIp]$"
    whole_lines = whole_lines.replace('@', old_delim)

    single_quoted = r"'s@((?:\\'|[^@'])*)@((?:\\'|[^'])*)@[gIp]?'"
    single_quoted = single_quoted.replace('@', old_delim)

    double_quoted = r'"s@((?:\\"|[^@"])*)@((?:\\"|[^"])*)@[gIp]?"'
    double_quoted = double_quoted.replace('@', old_delim)

    repl = r's@\1@\2@g'
    repl = repl.replace('@', new_delim)

    for f in filenames:
        filter_file(whole_lines, repl, f)
        filter_file(single_quoted, "'%s'" % repl, f)
        filter_file(double_quoted, '"%s"' % repl, f)


def set_install_permissions(path):
    """Set appropriate permissions on the installed file."""
    # If this points to a file maintained in a Spack prefix, it is assumed that
    # this function will be invoked on the target. If the file is outside a
    # Spack-maintained prefix, the permissions should not be modified.
    if os.path.islink(path):
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
    if uid is None:
        uid = os.getuid()
    user = pwd.getpwuid(uid).pw_name
    return [g.gr_gid for g in grp.getgrall() if user in g.gr_mem]


def chgrp(path, group):
    """Implement the bash chgrp function on a single path"""
    if isinstance(group, six.string_types):
        gid = grp.getgrnam(group).gr_gid
    else:
        gid = group
    os.chown(path, -1, gid)


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


def copy_mode(src, dest):
    """Set the mode of dest to that of src unless it is a link.
    """
    if os.path.islink(dest):
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


def unset_executable_mode(path):
    mode = os.stat(path).st_mode
    mode &= ~stat.S_IXUSR
    mode &= ~stat.S_IXGRP
    mode &= ~stat.S_IXOTH
    os.chmod(path, mode)


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
        tty.debug('Installing {0} to {1}'.format(src, dest))
    else:
        tty.debug('Copying {0} to {1}'.format(src, dest))

    files = glob.glob(src)
    if not files:
        raise IOError("No such file or directory: '{0}'".format(src))
    if len(files) > 1 and not os.path.isdir(dest):
        raise ValueError(
            "'{0}' matches multiple files but '{1}' is not a directory".format(
                src, dest))

    for src in files:
        # Expand dest to its eventual full path if it is a directory.
        dst = dest
        if os.path.isdir(dest):
            dst = join_path(dest, os.path.basename(src))

        shutil.copy(src, dst)

        if _permissions:
            set_install_permissions(dst)
            copy_mode(src, dst)


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


def resolve_link_target_relative_to_the_link(link):
    """
    os.path.isdir uses os.path.exists, which for links will check
    the existence of the link target. If the link target is relative to
    the link, we need to construct a pathname that is valid from
    our cwd (which may not be the same as the link's directory)
    """
    target = os.readlink(link)
    if os.path.isabs(target):
        return target
    link_dir = os.path.dirname(os.path.abspath(link))
    return os.path.join(link_dir, target)


def copy_tree(src, dest, symlinks=True, ignore=None, _permissions=False):
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
        ignore (function): function indicating which files to ignore
        _permissions (bool): for internal use only

    Raises:
        IOError: if *src* does not match any files or directories
        ValueError: if *src* is a parent directory of *dest*
    """
    if _permissions:
        tty.debug('Installing {0} to {1}'.format(src, dest))
    else:
        tty.debug('Copying {0} to {1}'.format(src, dest))

    abs_dest = os.path.abspath(dest)
    if not abs_dest.endswith(os.path.sep):
        abs_dest += os.path.sep

    files = glob.glob(src)
    if not files:
        raise IOError("No such file or directory: '{0}'".format(src))

    for src in files:
        abs_src = os.path.abspath(src)
        if not abs_src.endswith(os.path.sep):
            abs_src += os.path.sep

        # Stop early to avoid unnecessary recursion if being asked to copy
        # from a parent directory.
        if abs_dest.startswith(abs_src):
            raise ValueError('Cannot copy ancestor directory {0} into {1}'.
                             format(abs_src, abs_dest))

        mkdirp(abs_dest)

        for s, d in traverse_tree(abs_src, abs_dest, order='pre',
                                  follow_symlinks=not symlinks,
                                  ignore=ignore,
                                  follow_nonexisting=True):
            if os.path.islink(s):
                link_target = resolve_link_target_relative_to_the_link(s)
                if symlinks:
                    target = os.readlink(s)
                    if os.path.isabs(target):
                        new_target = re.sub(abs_src, abs_dest, target)
                        if new_target != target:
                            tty.debug("Redirecting link {0} to {1}"
                                      .format(target, new_target))
                            target = new_target

                    os.symlink(target, d)
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


def install_tree(src, dest, symlinks=True, ignore=None):
    """Recursively install an entire directory tree rooted at *src*.

    Same as :py:func:`copy_tree` with the addition of setting proper
    permissions on the installed files and directories.

    Parameters:
        src (str): the directory to install
        dest (str): the destination directory
        symlinks (bool): whether or not to preserve symlinks
        ignore (function): function indicating which files to ignore

    Raises:
        IOError: if *src* does not match any files or directories
        ValueError: if *src* is a parent directory of *dest*
    """
    copy_tree(src, dest, symlinks=symlinks, ignore=ignore, _permissions=True)


def is_exe(path):
    """True if path is an executable file."""
    return os.path.isfile(path) and os.access(path, os.X_OK)


def get_filetype(path_name):
    """
    Return the output of file path_name as a string to identify file type.
    """
    file = Executable('file')
    file.add_default_env('LC_ALL', 'C')
    output = file('-b', '-h', '%s' % path_name,
                  output=str, error=str)
    return output.strip()


def chgrp_if_not_world_writable(path, group):
    """chgrp path to group if path is not world writable"""
    mode = os.stat(path).st_mode
    if not mode & stat.S_IWOTH:
        chgrp(path, group)


def mkdirp(*paths, **kwargs):
    """Creates a directory, as well as parent directories if needed.

    Arguments:
        paths (str): paths to create with mkdirp

    Keyword Aguments:
        mode (permission bits or None, optional): optional permissions to set
            on the created directory -- use OS default if not provided
        group (group name or None, optional): optional group for permissions of
            final created directory -- use OS default if not provided. Only
            used if world write permissions are not set
        default_perms ('parents' or 'args', optional): The default permissions
            that are set for directories that are not themselves an argument
            for mkdirp. 'parents' means intermediate directories get the
            permissions of their direct parent directory, 'args' means
            intermediate get the same permissions specified in the arguments to
            mkdirp -- default value is 'args'
    """
    mode = kwargs.get('mode', None)
    group = kwargs.get('group', None)
    default_perms = kwargs.get('default_perms', 'args')

    for path in paths:
        if not os.path.exists(path):
            try:
                # detect missing intermediate folders
                intermediate_folders = []
                last_parent = ''

                intermediate_path = os.path.dirname(path)

                while intermediate_path:
                    if os.path.exists(intermediate_path):
                        last_parent = intermediate_path
                        break

                    intermediate_folders.append(intermediate_path)
                    intermediate_path = os.path.dirname(intermediate_path)

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
                if default_perms == 'args':
                    intermediate_mode = mode
                    intermediate_group = group
                elif default_perms == 'parents':
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
                        chgrp_if_not_world_writable(intermediate_path,
                                                    intermediate_group)
                        os.chmod(intermediate_path,
                                 intermediate_mode)  # reset sticky bit after

            except OSError as e:
                if e.errno != errno.EEXIST or not os.path.isdir(path):
                    raise e
        elif not os.path.isdir(path):
            raise OSError(errno.EEXIST, "File already exists", path)


def force_remove(*paths):
    """Remove files without printing errors.  Like ``rm -f``, does NOT
       remove directories."""
    for path in paths:
        try:
            os.remove(path)
        except OSError:
            pass


@contextmanager
def working_dir(dirname, **kwargs):
    if kwargs.get('create', False):
        mkdirp(dirname)

    orig_dir = os.getcwd()
    os.chdir(dirname)
    try:
        yield
    finally:
        os.chdir(orig_dir)


@contextmanager
def replace_directory_transaction(directory_name, tmp_root=None):
    """Moves a directory to a temporary space. If the operations executed
    within the context manager don't raise an exception, the directory is
    deleted. If there is an exception, the move is undone.

    Args:
        directory_name (path): absolute path of the directory name
        tmp_root (path): absolute path of the parent directory where to create
            the temporary

    Returns:
        temporary directory where ``directory_name`` has been moved
    """
    # Check the input is indeed a directory with absolute path.
    # Raise before anything is done to avoid moving the wrong directory
    assert os.path.isdir(directory_name), \
        'Invalid directory: ' + directory_name
    assert os.path.isabs(directory_name), \
        '"directory_name" must contain an absolute path: ' + directory_name

    directory_basename = os.path.basename(directory_name)

    if tmp_root is not None:
        assert os.path.isabs(tmp_root)

    tmp_dir = tempfile.mkdtemp(dir=tmp_root)
    tty.debug('TEMPORARY DIRECTORY CREATED [{0}]'.format(tmp_dir))

    shutil.move(src=directory_name, dst=tmp_dir)
    tty.debug('DIRECTORY MOVED [src={0}, dest={1}]'.format(
        directory_name, tmp_dir
    ))

    try:
        yield tmp_dir
    except (Exception, KeyboardInterrupt, SystemExit) as e:
        # Delete what was there, before copying back the original content
        if os.path.exists(directory_name):
            shutil.rmtree(directory_name)
        shutil.move(
            src=os.path.join(tmp_dir, directory_basename),
            dst=os.path.dirname(directory_name)
        )
        tty.debug('DIRECTORY RECOVERED [{0}]'.format(directory_name))

        msg = 'the transactional move of "{0}" failed.'
        msg += '\n    ' + str(e)
        raise RuntimeError(msg.format(directory_name))
    else:
        # Otherwise delete the temporary directory
        shutil.rmtree(tmp_dir)
        tty.debug('TEMPORARY DIRECTORY DELETED [{0}]'.format(tmp_dir))


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
                with open(filename, 'rb') as f:
                    md5_hash.update(f.read())

    return md5_hash.hexdigest()


@contextmanager
def write_tmp_and_move(filename):
    """Write to a temporary file, then move into place."""
    dirname = os.path.dirname(filename)
    basename = os.path.basename(filename)
    tmp = os.path.join(dirname, '.%s.tmp' % basename)
    with open(tmp, 'w') as f:
        yield f
    shutil.move(tmp, filename)


@contextmanager
def open_if_filename(str_or_file, mode='r'):
    """Takes either a path or a file object, and opens it if it is a path.

    If it's a file object, just yields the file object.
    """
    if isinstance(str_or_file, six.string_types):
        with open(str_or_file, mode) as f:
            yield f
    else:
        yield str_or_file


def touch(path):
    """Creates an empty file at the specified path."""
    perms = (os.O_WRONLY | os.O_CREAT | os.O_NONBLOCK | os.O_NOCTTY)
    fd = None
    try:
        fd = os.open(path, perms)
        os.utime(path, None)
    finally:
        if fd is not None:
            os.close(fd)


def touchp(path):
    """Like ``touch``, but creates any parent directories needed for the file.
    """
    mkdirp(os.path.dirname(path))
    touch(path)


def force_symlink(src, dest):
    try:
        os.symlink(src, dest)
    except OSError:
        os.remove(dest)
        os.symlink(src, dest)


def join_path(prefix, *args):
    path = str(prefix)
    for elt in args:
        path = os.path.join(path, str(elt))
    return path


def ancestor(dir, n=1):
    """Get the nth ancestor of a directory."""
    parent = os.path.abspath(dir)
    for i in range(n):
        parent = os.path.dirname(parent)
    return parent


def get_single_file(directory):
    fnames = os.listdir(directory)
    if len(fnames) != 1:
        raise ValueError("Expected exactly 1 file, got {0}"
                         .format(str(len(fnames))))
    return fnames[0]


@contextmanager
def temp_cwd():
    tmp_dir = tempfile.mkdtemp()
    try:
        with working_dir(tmp_dir):
            yield tmp_dir
    finally:
        shutil.rmtree(tmp_dir)


@contextmanager
def temp_rename(orig_path, temp_path):
    same_path = os.path.realpath(orig_path) == os.path.realpath(temp_path)
    if not same_path:
        shutil.move(orig_path, temp_path)
    try:
        yield
    finally:
        if not same_path:
            shutil.move(temp_path, orig_path)


def can_access(file_name):
    """True if we have read/write access to the file."""
    return os.access(file_name, os.R_OK | os.W_OK)


def traverse_tree(source_root, dest_root, rel_path='', **kwargs):
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
        ignore (function): function indicating which files to ignore
        follow_nonexisting (bool): Whether to descend into directories in
            ``src`` that do not exit in ``dest``. Default is True
        follow_links (bool): Whether to descend into symlinks in ``src``
    """
    follow_nonexisting = kwargs.get('follow_nonexisting', True)
    follow_links = kwargs.get('follow_link', False)

    # Yield in pre or post order?
    order = kwargs.get('order', 'pre')
    if order not in ('pre', 'post'):
        raise ValueError("Order must be 'pre' or 'post'.")

    # List of relative paths to ignore under the src root.
    ignore = kwargs.get('ignore', None) or (lambda filename: False)

    # Don't descend into ignored directories
    if ignore(rel_path):
        return

    source_path = os.path.join(source_root, rel_path)
    dest_path = os.path.join(dest_root, rel_path)

    # preorder yields directories before children
    if order == 'pre':
        yield (source_path, dest_path)

    for f in os.listdir(source_path):
        source_child = os.path.join(source_path, f)
        dest_child = os.path.join(dest_path, f)
        rel_child = os.path.join(rel_path, f)

        # Treat as a directory
        # TODO: for symlinks, os.path.isdir looks for the link target. If the
        # target is relative to the link, then that may not resolve properly
        # relative to our cwd - see resolve_link_target_relative_to_the_link
        if os.path.isdir(source_child) and (
                follow_links or not os.path.islink(source_child)):

            # When follow_nonexisting isn't set, don't descend into dirs
            # in source that do not exist in dest
            if follow_nonexisting or os.path.exists(dest_child):
                tuples = traverse_tree(
                    source_root, dest_root, rel_child, **kwargs)
                for t in tuples:
                    yield t

        # Treat as a file.
        elif not ignore(os.path.join(rel_path, f)):
            yield (source_child, dest_child)

    if order == 'post':
        yield (source_path, dest_path)


def set_executable(path):
    mode = os.stat(path).st_mode
    if mode & stat.S_IRUSR:
        mode |= stat.S_IXUSR
    if mode & stat.S_IRGRP:
        mode |= stat.S_IXGRP
    if mode & stat.S_IROTH:
        mode |= stat.S_IXOTH
    os.chmod(path, mode)


def last_modification_time_recursive(path):
    path = os.path.abspath(path)
    times = [os.stat(path).st_mtime]
    times.extend(os.stat(os.path.join(root, name)).st_mtime
                 for root, dirs, files in os.walk(path)
                 for name in dirs + files)
    return max(times)


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


def remove_dead_links(root):
    """Recursively removes any dead link that is present in root.

    Parameters:
        root (str): path where to search for dead links
    """
    for dirpath, subdirs, files in os.walk(root, topdown=False):
        for f in files:
            path = join_path(dirpath, f)
            remove_if_dead_link(path)


def remove_if_dead_link(path):
    """Removes the argument if it is a dead link.

    Parameters:
        path (str): The potential dead link
    """
    if os.path.islink(path) and not os.path.exists(path):
        os.unlink(path)


def remove_linked_tree(path):
    """Removes a directory and its contents.

    If the directory is a symlink, follows the link and removes the real
    directory before removing the link.

    Parameters:
        path (str): Directory to be removed
    """
    if os.path.exists(path):
        if os.path.islink(path):
            shutil.rmtree(os.path.realpath(path), True)
            os.unlink(path)
        else:
            shutil.rmtree(path, True)


@contextmanager
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
    sorted_matches = sorted([
        os.path.abspath(x) for x in itertools.chain(*glob_matches)
    ], key=len)

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
            basename = os.path.basename(file_or_dir) + '-{0}'.format(id)
            temporary_path = os.path.join(dst_root, basename)
            shutil.move(file_or_dir, temporary_path)
            removed[file_or_dir] = temporary_path
        yield removed
    except BaseException:
        # Restore the files that were removed
        for original_path, temporary_path in removed.items():
            shutil.move(temporary_path, original_path)
        raise


def fix_darwin_install_name(path):
    """Fix install name of dynamic libraries on Darwin to have full path.

    There are two parts of this task:

    1. Use ``install_name('-id', ...)`` to change install name of a single lib
    2. Use ``install_name('-change', ...)`` to change the cross linking between
       libs. The function assumes that all libraries are in one folder and
       currently won't follow subfolders.

    Parameters:
        path (str): directory in which .dylib files are located
    """
    libs = glob.glob(join_path(path, "*.dylib"))
    for lib in libs:
        # fix install name first:
        install_name_tool = Executable('install_name_tool')
        install_name_tool('-id', lib, lib)
        otool = Executable('otool')
        long_deps = otool('-L', lib, output=str).split('\n')
        deps = [dep.partition(' ')[0][1::] for dep in long_deps[2:-1]]
        # fix all dependencies:
        for dep in deps:
            for loc in libs:
                # We really want to check for either
                #     dep == os.path.basename(loc)   or
                #     dep == join_path(builddir, os.path.basename(loc)),
                # but we don't know builddir (nor how symbolic links look
                # in builddir). We thus only compare the basenames.
                if os.path.basename(dep) == os.path.basename(loc):
                    install_name_tool('-change', dep, loc, lib)
                    break


def find(root, files, recursive=True):
    """Search for ``files`` starting from the ``root`` directory.

    Like GNU/BSD find but written entirely in Python.

    Examples:

    .. code-block:: console

       $ find /usr -name python

    is equivalent to:

    >>> find('/usr', 'python')

    .. code-block:: console

       $ find /usr/local/bin -maxdepth 1 -name python

    is equivalent to:

    >>> find('/usr/local/bin', 'python', recursive=False)

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
        root (str): The root directory to start searching from
        files (str or Sequence): Library name(s) to search for
        recurse (bool, optional): if False search only root folder,
            if True descends top-down from the root. Defaults to True.

    Returns:
        list of strings: The files that have been found
    """
    if isinstance(files, six.string_types):
        files = [files]

    if recursive:
        return _find_recursive(root, files)
    else:
        return _find_non_recursive(root, files)


def _find_recursive(root, search_files):

    # The variable here is **on purpose** a defaultdict. The idea is that
    # we want to poke the filesystem as little as possible, but still maintain
    # stability in the order of the answer. Thus we are recording each library
    # found in a key, and reconstructing the stable order later.
    found_files = collections.defaultdict(list)

    # Make the path absolute to have os.walk also return an absolute path
    root = os.path.abspath(root)

    for path, _, list_files in os.walk(root):
        for search_file in search_files:
            matches = glob.glob(os.path.join(path, search_file))
            matches = [os.path.join(path, x) for x in matches]
            found_files[search_file].extend(matches)

    answer = []
    for search_file in search_files:
        answer.extend(found_files[search_file])

    return answer


def _find_non_recursive(root, search_files):
    # The variable here is **on purpose** a defaultdict as os.list_dir
    # can return files in any order (does not preserve stability)
    found_files = collections.defaultdict(list)

    # Make the path absolute to have absolute path returned
    root = os.path.abspath(root)

    for search_file in search_files:
        matches = glob.glob(os.path.join(root, search_file))
        matches = [os.path.join(root, x) for x in matches]
        found_files[search_file].extend(matches)

    answer = []
    for search_file in search_files:
        answer.extend(found_files[search_file])

    return answer


# Utilities for libraries and headers


class FileList(Sequence):
    """Sequence of absolute paths to files.

    Provides a few convenience methods to manipulate file paths.
    """

    def __init__(self, files):
        if isinstance(files, six.string_types):
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
            list of strings: A list of directories
        """
        return list(dedupe(
            os.path.dirname(x) for x in self.files if os.path.dirname(x)
        ))

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
            list of strings: A list of base-names
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

    def joined(self, separator=' '):
        return separator.join(self.files)

    def __repr__(self):
        return self.__class__.__name__ + '(' + repr(self.files) + ')'

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
    include_regex = re.compile(r'(.*?)(\binclude\b)(.*)')

    def __init__(self, files):
        super(HeaderList, self).__init__(files)

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
        if isinstance(value, six.string_types):
            value = [value]

        self._directories = [os.path.normpath(x) for x in value]

    def _default_directories(self):
        """Default computation of directories based on the list of
        header files.
        """
        dir_list = super(HeaderList, self).directories
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
            list of strings: A list of header files
        """
        return self.files

    @property
    def names(self):
        """Stable de-duplication of header names in the list without extensions

        >>> h = HeaderList(['/dir1/a.h', '/dir2/b.h', '/dir3/a.h'])
        >>> h.names
        ['a', 'b']

        Returns:
            list of strings: A list of files without extensions
        """
        names = []

        for x in self.basenames:
            name = x

            # Valid extensions include: ['.cuh', '.hpp', '.hh', '.h']
            for ext in ['.cuh', '.hpp', '.hh', '.h']:
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
        return ' '.join(['-I' + x for x in self.directories])

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
        return ' '.join(self._macro_definitions)

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
            cpp_flags += ' ' + self.macro_definitions
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
        headers (str or list of str): Header name(s) to search for
        root (str): The root directory to start searching from
        recursive (bool, optional): if False search only root folder,
            if True descends top-down from the root. Defaults to False.

    Returns:
        HeaderList: The headers that have been found
    """
    if isinstance(headers, six.string_types):
        headers = [headers]
    elif not isinstance(headers, Sequence):
        message = '{0} expects a string or sequence of strings as the '
        message += 'first argument [got {1} instead]'
        message = message.format(find_headers.__name__, type(headers))
        raise TypeError(message)

    # Construct the right suffix for the headers
    suffixes = [
        # C
        'h',
        # C++
        'hpp', 'hxx', 'hh', 'H', 'txx', 'tcc', 'icc',
        # Fortran
        'mod', 'inc',
    ]

    # List of headers we are searching with suffixes
    headers = ['{0}.{1}'.format(header, suffix) for header in headers
               for suffix in suffixes]

    return HeaderList(find(root, headers, recursive))


def find_all_headers(root):
    """Convenience function that returns the list of all headers found
    in the directory passed as argument.

    Args:
        root (path): directory where to look recursively for header files

    Returns:
        List of all headers found in ``root`` and subdirectories.
    """
    return find_headers('*', root=root, recursive=True)


class LibraryList(FileList):
    """Sequence of absolute paths to libraries

    Provides a few convenience methods to manipulate library paths and get
    commonly used compiler flags or names
    """

    @property
    def libraries(self):
        """Stable de-duplication of library files.

        Returns:
            list of strings: A list of library files
        """
        return self.files

    @property
    def names(self):
        """Stable de-duplication of library names in the list

        >>> l = LibraryList(['/dir1/liba.a', '/dir2/libb.a', '/dir3/liba.so'])
        >>> l.names
        ['a', 'b']

        Returns:
            list of strings: A list of library names
        """
        names = []

        for x in self.basenames:
            name = x
            if x.startswith('lib'):
                name = x[3:]

            # Valid extensions include: ['.dylib', '.so', '.a']
            for ext in ['.dylib', '.so', '.a']:
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
        return ' '.join(['-L' + x for x in self.directories])

    @property
    def link_flags(self):
        """Link flags for the libraries

        >>> l = LibraryList(['/dir1/liba.a', '/dir2/libb.a', '/dir1/liba.so'])
        >>> l.link_flags
        '-la -lb'

        Returns:
            str: A joined list of link flags
        """
        return ' '.join(['-l' + name for name in self.names])

    @property
    def ld_flags(self):
        """Search flags + link flags

        >>> l = LibraryList(['/dir1/liba.a', '/dir2/libb.a', '/dir1/liba.so'])
        >>> l.ld_flags
        '-L/dir1 -L/dir2 -la -lb'

        Returns:
            str: A joined list of search flags and link flags
        """
        return self.search_flags + ' ' + self.link_flags


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
        libraries (str or list of str): Library name(s) to search for
        shared (bool, optional): if True searches for shared libraries,
            otherwise for static. Defaults to True.

    Returns:
        LibraryList: The libraries that have been found
    """
    if isinstance(libraries, six.string_types):
        libraries = [libraries]
    elif not isinstance(libraries, Sequence):
        message = '{0} expects a string or sequence of strings as the '
        message += 'first argument [got {1} instead]'
        message = message.format(find_system_libraries.__name__,
                                 type(libraries))
        raise TypeError(message)

    libraries_found = []
    search_locations = [
        '/lib64',
        '/lib',
        '/usr/lib64',
        '/usr/lib',
        '/usr/local/lib64',
        '/usr/local/lib',
    ]

    for library in libraries:
        for root in search_locations:
            result = find_libraries(library, root, shared, recursive=True)
            if result:
                libraries_found += result
                break

    return libraries_found


def find_libraries(libraries, root, shared=True, recursive=False):
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
        libraries (str or list of str): Library name(s) to search for
        root (str): The root directory to start searching from
        shared (bool, optional): if True searches for shared libraries,
            otherwise for static. Defaults to True.
        recursive (bool, optional): if False search only root folder,
            if True descends top-down from the root. Defaults to False.

    Returns:
        LibraryList: The libraries that have been found
    """
    if isinstance(libraries, six.string_types):
        libraries = [libraries]
    elif not isinstance(libraries, Sequence):
        message = '{0} expects a string or sequence of strings as the '
        message += 'first argument [got {1} instead]'
        message = message.format(find_libraries.__name__, type(libraries))
        raise TypeError(message)

    # Construct the right suffix for the library
    if shared is True:
        suffix = 'dylib' if sys.platform == 'darwin' else 'so'
    else:
        suffix = 'a'
    # List of libraries we are searching with suffixes
    libraries = ['{0}.{1}'.format(lib, suffix) for lib in libraries]

    if not recursive:
        # If not recursive, look for the libraries directly in root
        return LibraryList(find(root, libraries, False))

    # To speedup the search for external packages configured e.g. in /usr,
    # perform first non-recursive search in root/lib then in root/lib64 and
    # finally search all of root recursively. The search stops when the first
    # match is found.
    for subdir in ('lib', 'lib64'):
        dirname = join_path(root, subdir)
        if not os.path.isdir(dirname):
            continue
        found_libs = find(dirname, libraries, False)
        if found_libs:
            break
    else:
        found_libs = find(root, libraries, True)

    return LibraryList(found_libs)


@memoized
def can_access_dir(path):
    """Returns True if the argument is an accessible directory.

    Args:
        path: path to be tested

    Returns:
        True if ``path`` is an accessible directory, else False
    """
    return os.path.isdir(path) and os.access(path, os.R_OK | os.X_OK)


@memoized
def can_write_to_dir(path):
    """Return True if the argument is a directory in which we can write.

    Args:
        path: path to be tested

    Returns:
        True if ``path`` is an writeable directory, else False
    """
    return os.path.isdir(path) and os.access(path, os.R_OK | os.X_OK | os.W_OK)


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
        files.extend(filter(
            lambda x: os.path.isfile(x[1]),
            [(f, os.path.join(d, f)) for f in os.listdir(d)]
        ))
    return files


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

        bin_dir = os.path.join(path, 'bin')
        if os.path.isdir(bin_dir):
            executable_paths.append(bin_dir)

    return executable_paths


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
            entries = path.split(os.sep)
            i = entries.index(entry)
            if '' in entries:
                i -= 1
            return paths[:i], paths[i], paths[i + 1:]
        except ValueError:
            pass

    return paths, '', []


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

    Parameters:
        path (str): the string used to derive ancestor paths

    Returns:
        A list containing ancestor paths in order and ending with the path
    """
    if not path:
        return []

    parts = path.strip(os.sep).split(os.sep)
    if path.startswith(os.sep):
        parts.insert(0, os.sep)
    paths = [os.path.join(*parts[:i + 1]) for i in range(len(parts))]

    try:
        paths.remove(os.sep)
    except ValueError:
        pass

    try:
        paths.remove('.')
    except ValueError:
        pass

    return paths


def md5sum(file):
    """Compute the MD5 sum of a file.

    Args:
        file (str): file to be checksummed

    Returns:
        MD5 sum of the file's content
    """
    md5 = hashlib.md5()
    with open(file, "rb") as f:
        md5.update(f.read())
    return md5.digest()


def remove_directory_contents(dir):
    """Remove all contents of a directory."""
    if os.path.exists(dir):
        for entry in [os.path.join(dir, entry) for entry in os.listdir(dir)]:
            if os.path.isfile(entry) or os.path.islink(entry):
                os.unlink(entry)
            else:
                shutil.rmtree(entry)


@contextmanager
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
