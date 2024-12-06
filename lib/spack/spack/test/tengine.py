# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import pytest

import spack.config
import spack.tengine as tengine
from spack.util.path import canonicalize_path


class TestContext:
    class A(tengine.Context):
        @tengine.context_property
        def foo(self):
            return 1

    class B(tengine.Context):
        @tengine.context_property
        def bar(self):
            return 2

    class C(A, B):
        @tengine.context_property
        def foobar(self):
            return 3

        @tengine.context_property
        def foo(self):
            return 10

    def test_to_dict(self):
        """Tests that all the context properties in a hierarchy are considered
        when building the context dictionary.
        """

        # A derives directly from Context
        a = TestContext.A()
        d = a.to_dict()

        assert len(d) == 1
        assert "foo" in d
        assert d["foo"] == 1

        # So does B
        b = TestContext.B()
        d = b.to_dict()

        assert len(d) == 1
        assert "bar" in d
        assert d["bar"] == 2

        # C derives from both and overrides 'foo'
        c = TestContext.C()
        d = c.to_dict()

        assert len(d) == 3
        for x in ("foo", "bar", "foobar"):
            assert x in d

        assert d["foo"] == 10
        assert d["bar"] == 2
        assert d["foobar"] == 3


@pytest.mark.usefixtures("config")
class TestTengineEnvironment:
    def test_template_retrieval(self):
        """Tests the template retrieval mechanism hooked into config files"""
        # Check the directories are correct
        template_dirs = spack.config.get("config:template_dirs")
        template_dirs = tuple([canonicalize_path(x) for x in template_dirs])
        assert len(template_dirs) == 3

        env = tengine.make_environment(template_dirs)

        # Retrieve a.txt, which resides in the second
        # template directory specified in the mock configuration
        template = env.get_template("a.txt")
        text = template.render({"word": "world"})
        assert "Hello world!" == text

        # Retrieve b.txt, which resides in the third
        # template directory specified in the mock configuration
        template = env.get_template("b.txt")
        text = template.render({"word": "world"})
        assert "Howdy world!" == text
