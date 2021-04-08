# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import contextlib
import errno
import functools
import os
import re

import llnl.util.lang

import spack.error
import spack.paths
import spack.util.executable
import spack.version


_gnupg_version_re = r"^gpg(conf)? \(GnuPG\) (.*)$"
_gnupg_home_override = None
_global_gpg_instance = None


def get_gnupg_home(gnupg_home=None):
    """Returns the directory that should be used as the GNUPGHOME environment
    variable when calling gpg.

    If a [gnupg_home] is passed directly (and not None), that value will be
    used.

    Otherwise, if there is an override set (and it is not None), then that
    value will be used.

    Otherwise, if the environment variable "SPACK_GNUPGHOME" is set, then that
    value will be used.

    Otherwise, the default gpg path for Spack will be used.

    See also: gnupg_home_override()
    """
    return (gnupg_home or
            _gnupg_home_override or
            os.getenv('SPACK_GNUPGHOME') or
            spack.paths.gpg_path)


@contextlib.contextmanager
def gnupg_home_override(new_gnupg_home):
    global _gnupg_home_override
    global _global_gpg_instance

    old_gnupg_home_override = _gnupg_home_override
    old_global_gpg_instance = _global_gpg_instance

    _gnupg_home_override = new_gnupg_home
    _global_gpg_instance = None

    yield

    _gnupg_home_override = old_gnupg_home_override
    _global_gpg_instance = old_global_gpg_instance


def get_global_gpg_instance():
    global _global_gpg_instance
    if _global_gpg_instance is None:
        _global_gpg_instance = Gpg()
    return _global_gpg_instance


def parse_secret_keys_output(output):
    keys = []
    found_sec = False
    for line in output.split('\n'):
        if found_sec:
            if line.startswith('fpr'):
                keys.append(line.split(':')[9])
                found_sec = False
            elif line.startswith('ssb'):
                found_sec = False
        elif line.startswith('sec'):
            found_sec = True
    return keys


def parse_public_keys_output(output):
    keys = []
    found_pub = False
    for line in output.split('\n'):
        if found_pub:
            if line.startswith('fpr'):
                keys.append(line.split(':')[9])
                found_pub = False
            elif line.startswith('ssb'):
                found_pub = False
        elif line.startswith('pub'):
            found_pub = True
    return keys


cached_property = getattr(functools, 'cached_property', None)

# If older python version has no cached_property, emulate it here.
# TODO(opadron): maybe this shim should be moved to llnl.util.lang?
if not cached_property:
    def cached_property(*args, **kwargs):
        result = property(llnl.util.lang.memoized(*args, **kwargs))
        attr = result.fget.__name__

        @result.deleter
        def result(self):
            getattr(type(self), attr).fget.cache.pop((self,), None)

        return result


class _GpgConstants(object):
    @cached_property
    def target_version(self):
        return spack.version.Version('2')

    @cached_property
    def gpgconf_string(self):
        exe_str = spack.util.executable.which_string(
            'gpgconf', 'gpg2conf', 'gpgconf2')

        no_gpgconf_msg = (
            'Spack requires gpgconf version >= 2\n'
            '  To install a suitable version using Spack, run\n'
            '    spack install gnupg@2:\n'
            '  and load it by running\n'
            '    spack load gnupg@2:')

        if not exe_str:
            raise SpackGPGError(no_gpgconf_msg)

        exe = spack.util.executable.Executable(exe_str)
        output = exe('--version', output=str)
        match = re.search(_gnupg_version_re, output, re.M)

        if not match:
            raise SpackGPGError('Could not determine gpgconf version')

        if spack.version.Version(match.group(2)) < self.target_version:
            raise SpackGPGError(no_gpgconf_msg)

        # ensure that the gpgconf we found can run "gpgconf --create-socketdir"
        try:
            exe('--dry-run', '--create-socketdir')
        except spack.util.executable.ProcessError:
            # no dice
            exe_str = None

        return exe_str

    @cached_property
    def gpg_string(self):
        exe_str = spack.util.executable.which_string('gpg2', 'gpg')

        no_gpg_msg = (
            'Spack requires gpg version >= 2\n'
            '  To install a suitable version using Spack, run\n'
            '    spack install gnupg@2:\n'
            '  and load it by running\n'
            '    spack load gnupg@2:')

        if not exe_str:
            raise SpackGPGError(no_gpg_msg)

        exe = spack.util.executable.Executable(exe_str)
        output = exe('--version', output=str)
        match = re.search(_gnupg_version_re, output, re.M)

        if not match:
            raise SpackGPGError('Could not determine gpg version')

        if spack.version.Version(match.group(2)) < self.target_version:
            raise SpackGPGError(no_gpg_msg)

        return exe_str

    @cached_property
    def user_run_dir(self):
        # Try to ensure that (/var)/run/user/$(id -u) exists so that
        #  `gpgconf --create-socketdir` can be run later.
        #
        # NOTE(opadron): This action helps prevent a large class of
        #                "file-name-too-long" errors in gpg.

        try:
            has_suitable_gpgconf = bool(GpgConstants.gpgconf_string)
        except SpackGPGError:
            has_suitable_gpgconf = False

        # If there is no suitable gpgconf, don't even bother trying to
        # precreate a user run dir.
        if not has_suitable_gpgconf:
            return None

        result = None
        for var_run in ('/run', '/var/run'):
            if not os.path.exists(var_run):
                continue

            var_run_user = os.path.join(var_run, 'user')
            try:
                if not os.path.exists(var_run_user):
                    os.mkdir(var_run_user)
                    os.chmod(var_run_user, 0o777)

                user_dir = os.path.join(var_run_user, str(os.getuid()))

                if not os.path.exists(user_dir):
                    os.mkdir(user_dir)
                    os.chmod(user_dir, 0o700)

            # If the above operation fails due to lack of permissions, then
            # just carry on without running gpgconf and hope for the best.
            #
            # NOTE(opadron): Without a dir in which to create a socket for IPC,
            #                gnupg may fail if GNUPGHOME is set to a path that
            #                is too long, where "too long" in this context is
            #                actually quite short; somewhere in the
            #                neighborhood of more than 100 characters.
            #
            # TODO(opadron): Maybe a warning should be printed in this case?
            except OSError as exc:
                if exc.errno not in (errno.EPERM, errno.EACCES):
                    raise
                user_dir = None

            # return the last iteration that provides a usable user run dir
            if user_dir is not None:
                result = user_dir

        return result

    def clear(self):
        for attr in ('gpgconf_string', 'gpg_string', 'user_run_dir'):
            try:
                delattr(self, attr)
            except AttributeError:
                pass


GpgConstants = _GpgConstants()


def ensure_gpg(reevaluate=False):
    if reevaluate:
        GpgConstants.clear()

    if GpgConstants.user_run_dir is not None:
        GpgConstants.gpgconf_string

    GpgConstants.gpg_string
    return True


def has_gpg(*args, **kwargs):
    try:
        return ensure_gpg(*args, **kwargs)
    except SpackGPGError:
        return False


# NOTE(opadron): When adding methods to this class, consider adding convenience
#                wrapper functions further down in this file.
class Gpg(object):
    def __init__(self, gnupg_home=None):
        self.gnupg_home = get_gnupg_home(gnupg_home)

    @cached_property
    def prep(self):
        # Make sure that suitable versions of gpgconf and gpg are available
        ensure_gpg()

        # Make sure that the GNUPGHOME exists
        if not os.path.exists(self.gnupg_home):
            os.makedirs(self.gnupg_home)
            os.chmod(self.gnupg_home, 0o700)

        if not os.path.isdir(self.gnupg_home):
            raise SpackGPGError(
                'GNUPGHOME "{0}" exists and is not a directory'.format(
                    self.gnupg_home))

        if GpgConstants.user_run_dir is not None:
            self.gpgconf_exe('--create-socketdir')

        return True

    @cached_property
    def gpgconf_exe(self):
        exe = spack.util.executable.Executable(GpgConstants.gpgconf_string)
        exe.add_default_env('GNUPGHOME', self.gnupg_home)
        return exe

    @cached_property
    def gpg_exe(self):
        exe = spack.util.executable.Executable(GpgConstants.gpg_string)
        exe.add_default_env('GNUPGHOME', self.gnupg_home)
        return exe

    def __call__(self, *args, **kwargs):
        if self.prep:
            return self.gpg_exe(*args, **kwargs)

    def create(self, **kwargs):
        r, w = os.pipe()
        r = os.fdopen(r, 'r')
        w = os.fdopen(w, 'w')
        w.write('''
        Key-Type: rsa
        Key-Length: 4096
        Key-Usage: sign
        Name-Real: %(name)s
        Name-Email: %(email)s
        Name-Comment: %(comment)s
        Expire-Date: %(expires)s
        %%no-protection
        %%commit
        ''' % kwargs)
        w.close()
        self('--gen-key', '--batch', input=r)
        r.close()

    def signing_keys(self, *args):
        output = self('--list-secret-keys', '--with-colons', '--fingerprint',
                      *args, output=str)
        return parse_secret_keys_output(output)

    def public_keys(self, *args):
        output = self('--list-public-keys', '--with-colons', '--fingerprint',
                      *args, output=str)
        return parse_public_keys_output(output)

    def export_keys(self, location, keys, secret=False):
        if secret:
            self("--export-secret-keys", "--armor", "--output", location, *keys)
        else:
            self('--batch', '--yes', '--armor', '--export', '--output',
                 location, *keys)

    def trust(self, keyfile):
        self('--import', keyfile)

    def untrust(self, signing, *keys):
        if signing:
            skeys = self.signing_keys(*keys)
            self('--batch', '--yes', '--delete-secret-keys', *skeys)

        pkeys = self.public_keys(*keys)
        self('--batch', '--yes', '--delete-keys', *pkeys)

    def sign(self, key, file, output, clearsign=False):
        self(('--clearsign' if clearsign else '--detach-sign'),
             '--armor', '--default-key', key,
             '--output', output, file)

    def verify(self, signature, file, suppress_warnings=False):
        self('--verify', signature, file,
             **({'error': str} if suppress_warnings else {}))

    def list(self, trusted, signing):
        if trusted:
            self('--list-public-keys')

        if signing:
            self('--list-secret-keys')


class SpackGPGError(spack.error.SpackError):
    """Class raised when GPG errors are detected."""


# Convenience wrappers for methods of the Gpg class

# __call__ is a bit of a special case, since the Gpg instance is, itself, the
# "thing" that is being called.
@functools.wraps(Gpg.__call__)
def gpg(*args, **kwargs):
    return get_global_gpg_instance()(*args, **kwargs)


gpg.name = 'gpg'  # type: ignore[attr-defined]


@functools.wraps(Gpg.create)
def create(*args, **kwargs):
    return get_global_gpg_instance().create(*args, **kwargs)


@functools.wraps(Gpg.signing_keys)
def signing_keys(*args, **kwargs):
    return get_global_gpg_instance().signing_keys(*args, **kwargs)


@functools.wraps(Gpg.public_keys)
def public_keys(*args, **kwargs):
    return get_global_gpg_instance().public_keys(*args, **kwargs)


@functools.wraps(Gpg.export_keys)
def export_keys(*args, **kwargs):
    return get_global_gpg_instance().export_keys(*args, **kwargs)


@functools.wraps(Gpg.trust)
def trust(*args, **kwargs):
    return get_global_gpg_instance().trust(*args, **kwargs)


@functools.wraps(Gpg.untrust)
def untrust(*args, **kwargs):
    return get_global_gpg_instance().untrust(*args, **kwargs)


@functools.wraps(Gpg.sign)
def sign(*args, **kwargs):
    return get_global_gpg_instance().sign(*args, **kwargs)


@functools.wraps(Gpg.verify)
def verify(*args, **kwargs):
    return get_global_gpg_instance().verify(*args, **kwargs)


@functools.wraps(Gpg.list)
def list(*args, **kwargs):
    return get_global_gpg_instance().list(*args, **kwargs)
