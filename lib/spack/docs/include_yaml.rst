.. Copyright Spack Project Developers. See COPYRIGHT file for details.

   SPDX-License-Identifier: (Apache-2.0 OR MIT)

.. _include-yaml:

===============================
Include Settings (include.yaml)
===============================

Spack allows you to include configuration files through ``include.yaml``.
Using the ``include:`` heading results in pulling in external configuration
information to be used by any Spack command.

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
the path is only included if it exists. The condition ``os == "ventura"``
in the ``when`` clause for ``/path/to/os-specific/config-dir`` means the
path is only included when the operating system (``os``) is ``ventura``.

The same conditions and variables in `Spec List References 
<https://spack.readthedocs.io/en/latest/environments.html#spec-list-references>`_
can be used for conditional activation in the ``when`` clauses.

Included files can be specified by path or by their parent directory.
Paths may be absolute, relative (to the configuration file including the path), 
or specified as URLs. Only the ``file``, ``ftp``, ``http`` and ``https`` protocols (or
schemes) are supported. Spack-specific, environment and user path variables
can be used. (See :ref:`config-file-variables` for more information.)
