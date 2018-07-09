##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
import re
import os
from itertools import product
from spack.util.executable import which

# Supported archive extensions.
PRE_EXTS = ["tar", "TAR"]
EXTS     = ["gz", "bz2", "xz", "Z", "zip", "tgz"]

# Add PRE_EXTS and EXTS last so that .tar.gz is matched *before* .tar or .gz
ALLOWED_ARCHIVE_TYPES = [".".join(l) for l in product(
    PRE_EXTS, EXTS)] + PRE_EXTS + EXTS


def allowed_archive(path):
    return any(path.endswith(t) for t in ALLOWED_ARCHIVE_TYPES)


def decompressor_for(path, extension=None):
    """Get the appropriate decompressor for a path."""
    if ((extension and re.match(r'\.?zip$', extension)) or
            path.endswith('.zip')):
        unzip = which('unzip', required=True)
        unzip.add_default_arg('-q')
        return unzip
    if extension and re.match(r'gz', extension):
        gunzip = which('gunzip', required=True)
        return Gunzip(gunzip)
    tar = which('tar', required=True)
    tar.add_default_arg('-xf')
    return tar


class Gunzip(object):
    """gunzip (and gzip in decompression mode) don't operate on symlinks to
       archives without additional arguments. This invokes the gunzip exe
       to write to stdout, and redirects stdout to an automatically-chosen
       filename (derived from stripping the extension from the archive name).
    """
    def __init__(self, gunzip_exe):
        self.gunzip_exe = gunzip_exe

    def __call__(self, archive_path):
        args = ['-c', archive_path]
        target_name = os.path.basename(strip_extension(archive_path))
        target_path = os.path.join(os.getcwd(), target_name)
        self.gunzip_exe(*args, output=target_path)


def strip_extension(path):
    """Get the part of a path that does not include its compressed
       type extension."""
    for type in ALLOWED_ARCHIVE_TYPES:
        suffix = r'\.%s$' % type
        if re.search(suffix, path):
            return re.sub(suffix, "", path)
    return path


def extension(path):
    """Get the archive extension for a path."""
    if path is None:
        raise ValueError("Can't call extension() on None")

    # Strip sourceforge suffix.
    if re.search(r'((?:sourceforge.net|sf.net)/.*)/download$', path):
        path = os.path.dirname(path)

    for t in ALLOWED_ARCHIVE_TYPES:
        suffix = r'\.%s$' % t
        if re.search(suffix, path):
            return t
    return None
