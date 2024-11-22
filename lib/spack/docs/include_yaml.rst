.. Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
   Spack Project Developers. See the top-level COPYRIGHT file for details.

   SPDX-License-Identifier: (Apache-2.0 OR MIT)

.. _include-yaml:

===============================
Include Settings (include.yaml)
===============================

Spack allows you to include configuration files through ``include.yaml``.
Using the ``include:`` heading results in pulling in external configuration
information to be used by any Spack command. The syntax is:

Included configuration files are required *unless* they are explicitly optional
or the entry's condition evaluates to ``false``. Optional includes are specified
with the ``optional`` clause and conditional with the ``when`` clause. For
example,

.. code-block:: yaml

   include:
   - /path/to/a/required/config.yaml
   - path: /path/to/$os/$target/config
     optional: true
   - path: /path/to/os-specific/config-dir
     when: os == "ventura"

shows all three. The first entry, ``/path/to/a/required/config.yaml``,
indicates that included ``config.yaml`` file is required (so must exist).
Use of ``optional: true`` for ``/path/to/$os/$target/config`` means
the path is only applied if it exists. The condition ``os == "ventura"``
in the ``when`` clause for ``/path/to/os-specific/config-dir`` means the
path is only applied when the operating system (``os``) is ``ventura``.

The same conditions and variables in `Spec List References 
<https://spack.readthedocs.io/en/latest/environments.html#spec-list-references>`_
can be used for conditional activation in the ``when`` clauses.
