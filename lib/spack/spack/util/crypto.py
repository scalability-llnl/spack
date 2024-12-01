# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import hashlib
from typing import BinaryIO, Callable, Dict, Optional

import llnl.util.tty as tty

HashFactory = Callable[[], "hashlib._Hash"]

#: Set of hash algorithms that Spack can use, mapped to digest size in bytes
hashes = {"sha256": 32, "md5": 16, "sha1": 20, "sha224": 28, "sha384": 48, "sha512": 64}
# Note: keys are ordered by popularity for earliest return in ``hash_key in version_dict`` checks.


#: size of hash digests in bytes, mapped to algoritm names
_size_to_hash = dict((v, k) for k, v in hashes.items())


#: List of deprecated hash functions. On some systems, these cannot be
#: used without special options to hashlib.
_deprecated_hash_algorithms = ["md5"]


#: cache of hash functions generated
_hash_functions: Dict[str, HashFactory] = {}


class DeprecatedHash:
    def __init__(self, hash_alg, alert_fn, disable_security_check):
        self.hash_alg = hash_alg
        self.alert_fn = alert_fn
        self.disable_security_check = disable_security_check

    def __call__(self, disable_alert=False):
        if not disable_alert:
            self.alert_fn(
                "Deprecation warning: {0} checksums will not be"
                " supported in future Spack releases.".format(self.hash_alg)
            )
        if self.disable_security_check:
            return hashlib.new(self.hash_alg, usedforsecurity=False)  # novermin
        else:
            return hashlib.new(self.hash_alg)


def hash_fun_for_algo(algo: str) -> HashFactory:
    """Get a function that can perform the specified hash algorithm."""
    fun = _hash_functions.get(algo)
    if fun:
        return fun
    elif algo not in _deprecated_hash_algorithms:
        _hash_functions[algo] = getattr(hashlib, algo)
    else:
        try:
            deprecated_fun = DeprecatedHash(algo, tty.debug, disable_security_check=False)

            # call once to get a ValueError if usedforsecurity is needed
            deprecated_fun(disable_alert=True)
        except ValueError:
            # Some systems may support the 'usedforsecurity' option
            # so try with that (but display a warning when it is used)
            deprecated_fun = DeprecatedHash(algo, tty.warn, disable_security_check=True)
        _hash_functions[algo] = deprecated_fun
    return _hash_functions[algo]


def hash_algo_for_digest(hexdigest: str) -> str:
    """Gets name of the hash algorithm for a hex digest."""
    algo = _size_to_hash.get(len(hexdigest) // 2)
    if algo is None:
        raise ValueError(f"Spack knows no hash algorithm for this digest: {hexdigest}")
    return algo


def hash_fun_for_digest(hexdigest: str) -> HashFactory:
    """Gets a hash function corresponding to a hex digest."""
    return hash_fun_for_algo(hash_algo_for_digest(hexdigest))


def checksum_stream(hashlib_algo: HashFactory, fp: BinaryIO, *, block_size: int = 2**20) -> str:
    """Returns a hex digest of the stream generated using given algorithm from hashlib."""
    hasher = hashlib_algo()
    while True:
        data = fp.read(block_size)
        if not data:
            break
        hasher.update(data)
    return hasher.hexdigest()


def checksum(hashlib_algo: HashFactory, filename: str, *, block_size: int = 2**20) -> str:
    """Returns a hex digest of the filename generated using an algorithm from hashlib."""
    with open(filename, "rb") as f:
        return checksum_stream(hashlib_algo, f, block_size=block_size)


class Checker:
    """A checker checks files against one particular hex digest.
    It will automatically determine what hashing algorithm
    to used based on the length of the digest it's initialized
    with.  e.g., if the digest is 32 hex characters long this will
    use md5.

    Example: know your tarball should hash to 'abc123'.  You want
    to check files against this.  You would use this class like so::

       hexdigest = 'abc123'
       checker = Checker(hexdigest)
       success = checker.check('downloaded.tar.gz')

    After the call to check, the actual checksum is available in
    checker.sum, in case it's needed for error output.

    You can trade read performance and memory usage by
    adjusting the block_size optional arg.  By default it's
    a 1MB (2**20 bytes) buffer.
    """

    def __init__(self, hexdigest: str, **kwargs) -> None:
        self.block_size = kwargs.get("block_size", 2**20)
        self.hexdigest = hexdigest
        self.sum: Optional[str] = None
        self.hash_fun = hash_fun_for_digest(hexdigest)

    @property
    def hash_name(self) -> str:
        """Get the name of the hash function this Checker is using."""
        return self.hash_fun().name.lower()

    def check(self, filename: str) -> bool:
        """Read the file with the specified name and check its checksum
        against self.hexdigest.  Return True if they match, False
        otherwise.  Actual checksum is stored in self.sum.
        """
        self.sum = checksum(self.hash_fun, filename, block_size=self.block_size)
        return self.sum == self.hexdigest


def prefix_bits(byte_array, bits):
    """Return the first <bits> bits of a byte array as an integer."""
    b2i = lambda b: b  # In Python 3, indexing byte_array gives int
    result = 0
    n = 0
    for i, b in enumerate(byte_array):
        n += 8
        result = (result << 8) | b2i(b)
        if n >= bits:
            break

    result >>= n - bits
    return result


def bit_length(num):
    """Number of bits required to represent an integer in binary."""
    s = bin(num)
    s = s.lstrip("-0b")
    return len(s)
