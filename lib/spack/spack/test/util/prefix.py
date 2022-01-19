# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Tests various features of :py:class:`spack.util.prefix.Prefix`"""

from spack.util.prefix import Prefix


def test_prefix_attributes():
    """Test normal prefix attributes like ``prefix.bin``"""
    prefix = Prefix('/usr')

    assert prefix.bin     == '/usr/bin'
    assert prefix.lib     == '/usr/lib'
    assert prefix.include == '/usr/include'


def test_prefix_join():
    """Test prefix join  ``prefix.join(...)``"""
    prefix = Prefix('/usr')

    a1 = prefix.join('a_{0}'.format(1)).lib64
    a2 = prefix.join('a-{0}'.format(1)).lib64
    a3 = prefix.join('a.{0}'.format(1)).lib64

    assert a1 == '/usr/a_1/lib64'
    assert a2 == '/usr/a-1/lib64'
    assert a3 == '/usr/a.1/lib64'

    assert isinstance(a1, Prefix)
    assert isinstance(a2, Prefix)
    assert isinstance(a3, Prefix)

    p1 = prefix.bin.join('executable.sh')
    p2 = prefix.share.join('pkg-config').join('foo.pc')
    p3 = prefix.join('dashed-directory').foo

    assert p1 == '/usr/bin/executable.sh'
    assert p2 == '/usr/share/pkg-config/foo.pc'
    assert p3 == '/usr/dashed-directory/foo'

    assert isinstance(p1, Prefix)
    assert isinstance(p2, Prefix)
    assert isinstance(p3, Prefix)


def test_multilevel_attributes():
    """Test attributes of attributes, like ``prefix.share.man``"""
    prefix = Prefix('/usr/')

    assert prefix.share.man   == '/usr/share/man'
    assert prefix.man.man8    == '/usr/man/man8'
    assert prefix.foo.bar.baz == '/usr/foo/bar/baz'

    share = prefix.share

    assert isinstance(share, Prefix)
    assert share.man == '/usr/share/man'


def test_string_like_behavior():
    """Test string-like behavior of the prefix object"""
    prefix = Prefix('/usr')

    assert prefix == '/usr'
    assert isinstance(prefix, str)

    assert prefix + '/bin' == '/usr/bin'
    assert '--prefix=%s' % prefix == '--prefix=/usr'
    assert '--prefix={0}'.format(prefix) == '--prefix=/usr'

    assert prefix.find('u', 1)
    assert prefix.upper() == '/USR'
    assert prefix.lstrip('/') == 'usr'
