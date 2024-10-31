# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import contextlib
import errno
import functools
import os
import re
from typing import List

import llnl.util.filesystem

import spack.error
import spack.paths
import spack.util.executable
import spack.version

#: Executable instance for "gpg", initialized lazily
GPG = None
#: Executable instance for "gpgconf", initialized lazily
GPGCONF = None
#: Socket directory required if a non default home directory is used
SOCKET_DIR = None
#: GNUPGHOME environment variable in the context of this Python module
GNUPGHOME = None


def clear():
    """Reset the global state to uninitialized."""
    global GPG, GPGCONF, SOCKET_DIR, GNUPGHOME
    GPG, GPGCONF, SOCKET_DIR, GNUPGHOME = None, None, None, None


def init(gnupghome=None, force=False):
    """Initialize the global objects in the module, if not set.

    When calling any gpg executable, the GNUPGHOME environment
    variable is set to:

    1. The value of the `gnupghome` argument, if not None
    2. The value of the "SPACK_GNUPGHOME" environment variable, if set
    3. The default gpg path for Spack otherwise

    Args:
        gnupghome (str): value to be used for GNUPGHOME when calling
            GnuPG executables
        force (bool): if True forces the re-initialization even if the
            global objects are set already
    """
    global GPG, GPGCONF, SOCKET_DIR, GNUPGHOME
    import spack.bootstrap

    if force:
        clear()

    # If the executables are already set, there's nothing to do
    if GPG and GNUPGHOME:
        return

    # Set the value of GNUPGHOME to be used in this module
    GNUPGHOME = gnupghome or os.getenv("SPACK_GNUPGHOME") or spack.paths.gpg_path

    # Set the executable objects for "gpg" and "gpgconf"
    with spack.bootstrap.ensure_bootstrap_configuration():
        spack.bootstrap.ensure_gpg_in_path_or_raise()
        GPG, GPGCONF = _gpg(), _gpgconf()

    GPG.add_default_env("GNUPGHOME", GNUPGHOME)
    if GPGCONF:
        GPGCONF.add_default_env("GNUPGHOME", GNUPGHOME)
        # Set the socket dir if not using GnuPG defaults
        SOCKET_DIR = _socket_dir(GPGCONF)

    # Make sure that the GNUPGHOME exists
    if not os.path.exists(GNUPGHOME):
        os.makedirs(GNUPGHOME)
        os.chmod(GNUPGHOME, 0o700)

    if not os.path.isdir(GNUPGHOME):
        msg = 'GNUPGHOME "{0}" exists and is not a directory'.format(GNUPGHOME)
        raise SpackGPGError(msg)

    if SOCKET_DIR is not None:
        GPGCONF("--create-socketdir")


def _autoinit(func):
    """Decorator to ensure that global variables have been initialized before
    running the decorated function.

    Args:
        func (callable): decorated function
    """

    @functools.wraps(func)
    def _wrapped(*args, **kwargs):
        init()
        return func(*args, **kwargs)

    return _wrapped


@contextlib.contextmanager
def gnupghome_override(dir):
    """Set the GNUPGHOME to a new location for this context.

    Args:
        dir (str): new value for GNUPGHOME
    """
    global GPG, GPGCONF, SOCKET_DIR, GNUPGHOME

    # Store backup values
    _GPG, _GPGCONF = GPG, GPGCONF
    _SOCKET_DIR, _GNUPGHOME = SOCKET_DIR, GNUPGHOME
    clear()

    # Clear global state
    init(gnupghome=dir, force=True)

    yield

    clear()
    GPG, GPGCONF = _GPG, _GPGCONF
    SOCKET_DIR, GNUPGHOME = _SOCKET_DIR, _GNUPGHOME


def _parse_secret_keys_output(output: str) -> List[str]:
    keys: List[str] = []
    found_sec = False
    for line in output.split("\n"):
        if found_sec:
            if line.startswith("fpr"):
                keys.append(line.split(":")[9])
                found_sec = False
            elif line.startswith("ssb"):
                found_sec = False
        elif line.startswith("sec"):
            found_sec = True
    return keys


def _parse_public_keys_output(output):
    """
    Returns a list of public keys with their fingerprints
    """
    keys = []
    found_pub = False
    current_pub_key = ""
    for line in output.split("\n"):
        if found_pub:
            if line.startswith("fpr"):
                keys.append((current_pub_key, line.split(":")[9]))
                found_pub = False
            elif line.startswith("ssb"):
                found_pub = False
        elif line.startswith("pub"):
            current_pub_key = line.split(":")[4]
            found_pub = True
    return keys


def _get_unimported_public_keys(output):
    keys = []
    for line in output.split("\n"):
        if line.startswith("pub"):
            keys.append(line.split(":")[4])
    return keys


class SpackGPGError(spack.error.SpackError):
    """Class raised when GPG errors are detected."""


@_autoinit
def create(**kwargs):
    """Create a new key pair."""
    r, w = os.pipe()
    with contextlib.closing(os.fdopen(r, "r")) as r:
        with contextlib.closing(os.fdopen(w, "w")) as w:
            w.write(
                """
Key-Type: rsa
Key-Length: 4096
Key-Usage: sign
Name-Real: %(name)s
Name-Email: %(email)s
Name-Comment: %(comment)s
Expire-Date: %(expires)s
%%no-protection
%%commit
"""
                % kwargs
            )
        GPG("--gen-key", "--batch", input=r)


@_autoinit
def signing_keys(*args) -> List[str]:
    """Return the keys that can be used to sign binaries."""
    assert GPG
    output: str = GPG("--list-secret-keys", "--with-colons", "--fingerprint", *args, output=str)
    return _parse_secret_keys_output(output)


@_autoinit
def public_keys_to_fingerprint(*args):
    """Return the keys that can be used to verify binaries."""
    output = GPG("--list-public-keys", "--with-colons", "--fingerprint", *args, output=str)
    return _parse_public_keys_output(output)


@_autoinit
def public_keys(*args):
    """Return a list of fingerprints"""
    keys_and_fpr = public_keys_to_fingerprint(*args)
    return [key_and_fpr[1] for key_and_fpr in keys_and_fpr]


@_autoinit
def export_keys(location, keys, secret=False):
    """Export public keys to a location passed as argument.

    Args:
        location (str): where to export the keys
        keys (list): keys to be exported
        secret (bool): whether to export secret keys or not
    """
    if secret:
        GPG("--export-secret-keys", "--armor", "--output", location, *keys)
    else:
        GPG("--batch", "--yes", "--armor", "--export", "--output", location, *keys)


@_autoinit
def trust(keyfile):
    """Import a public key from a file and trust it.

    Args:
        keyfile (str): file with the public key
    """
    # Get the public keys we are about to import
    output = GPG("--with-colons", keyfile, output=str, error=str)
    keys = _get_unimported_public_keys(output)

    # Import them
    GPG("--batch", "--import", keyfile)

    # Set trust to ultimate
    key_to_fpr = dict(public_keys_to_fingerprint())
    for key in keys:
        # Skip over keys we cannot find a fingerprint for.
        if key not in key_to_fpr:
            continue

        fpr = key_to_fpr[key]
        r, w = os.pipe()
        with contextlib.closing(os.fdopen(r, "r")) as r:
            with contextlib.closing(os.fdopen(w, "w")) as w:
                w.write("{0}:6:\n".format(fpr))
            GPG("--import-ownertrust", input=r)


@_autoinit
def untrust(signing, *keys):
    """Delete known keys.

    Args:
        signing (bool): if True deletes the secret keys
        *keys: keys to be deleted
    """
    if signing:
        skeys = signing_keys(*keys)
        GPG("--batch", "--yes", "--delete-secret-keys", *skeys)

    pkeys = public_keys(*keys)
    GPG("--batch", "--yes", "--delete-keys", *pkeys)


@_autoinit
def sign(key, file, output, clearsign=False):
    """Sign a file with a key.

    Args:
        key: key to be used to sign
        file (str): file to be signed
        output (str): output file (either the clearsigned file or
            the detached signature)
        clearsign (bool): if True wraps the document in an ASCII-armored
            signature, if False creates a detached signature
    """
    signopt = "--clearsign" if clearsign else "--detach-sign"
    GPG(signopt, "--armor", "--local-user", key, "--output", output, file)


@_autoinit
def verify(signature, file=None, suppress_warnings=False):
    """Verify the signature on a file.

    Args:
        signature (str): signature of the file (or clearsigned file)
        file (str): file to be verified.  If None, then signature is
            assumed to be a clearsigned file.
        suppress_warnings (bool): whether or not to suppress warnings
            from GnuPG
    """
    args = [signature]
    if file:
        args.append(file)
    kwargs = {"error": str} if suppress_warnings else {}
    GPG("--verify", *args, **kwargs)


@_autoinit
def list(trusted, signing):
    """List known keys.

    Args:
        trusted (bool): if True list public keys
        signing (bool): if True list private keys
    """
    if trusted:
        GPG("--list-public-keys")

    if signing:
        GPG("--list-secret-keys")


def _verify_exe_or_raise(exe):
    msg = (
        "Spack requires gpgconf version >= 2\n"
        "  To install a suitable version using Spack, run\n"
        "    spack install gnupg@2:\n"
        "  and load it by running\n"
        "    spack load gnupg@2:"
    )
    if not exe:
        raise SpackGPGError(msg)

    output = exe("--version", output=str)
    match = re.search(r"^gpg(conf)? \(GnuPG(?:/MacGPG2)?\) (.*)$", output, re.M)
    if not match:
        raise SpackGPGError('Could not determine "{0}" version'.format(exe.name))

    if spack.version.Version(match.group(2)) < spack.version.Version("2"):
        raise SpackGPGError(msg)


def _gpgconf():
    exe = spack.util.executable.which("gpgconf", "gpg2conf", "gpgconf2")
    _verify_exe_or_raise(exe)

    # ensure that the gpgconf we found can run "gpgconf --create-socketdir"
    try:
        exe("--dry-run", "--create-socketdir", output=os.devnull, error=os.devnull)
    except spack.util.executable.ProcessError:
        # no dice
        exe = None

    return exe


def _gpg():
    exe = spack.util.executable.which("gpg2", "gpg")
    _verify_exe_or_raise(exe)
    return exe


def _socket_dir(gpgconf):
    # Try to ensure that (/var)/run/user/$(id -u) exists so that
    # `gpgconf --create-socketdir` can be run later.
    #
    # NOTE(opadron): This action helps prevent a large class of
    #                "file-name-too-long" errors in gpg.

    # If there is no suitable gpgconf, don't even bother trying to
    # pre-create a user run dir.
    if not gpgconf:
        return None

    result = None
    for var_run in ("/run", "/var/run"):
        if not os.path.exists(var_run):
            continue

        var_run_user = os.path.join(var_run, "user")
        try:
            if not os.path.exists(var_run_user):
                os.mkdir(var_run_user)
                os.chmod(var_run_user, 0o777)

            user_dir = os.path.join(var_run_user, str(llnl.util.filesystem.getuid()))

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
