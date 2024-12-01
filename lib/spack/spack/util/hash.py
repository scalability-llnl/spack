# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import base64
import hashlib

import spack.util.crypto


def b32_hash(content):
    """Return the b32 encoded sha1 hash of the input string as a string."""
    sha = hashlib.sha1(content.encode("utf-8"))
    b32_hash = base64.b32encode(sha.digest()).lower()
    b32_hash = b32_hash.decode("utf-8")
    return b32_hash


def base32_prefix_bits(hash_string, bits):
    """Return the first <bits> bits of a base32 string as an integer."""
    if bits > len(hash_string) * 5:
        raise ValueError("Too many bits! Requested %d bit prefix of '%s'." % (bits, hash_string))

    hash_bytes = base64.b32decode(hash_string, casefold=True)
    return spack.util.crypto.prefix_bits(hash_bytes, bits)
