.. Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
   Spack Project Developers. See the top-level COPYRIGHT file for details.

   SPDX-License-Identifier: (Apache-2.0 OR MIT)

==========================
Frequently Asked Questions
==========================

This page contains answers to frequently asked questions about Spack.
If you have questions that are not answered here, feel free to ask on
`Slack <https://slack.spack.io>`_ or `GitHub Discussions
<https://github.com/spack/spack/discussions>`_. If you've learned the
answer to a question that you think should be here, please consider
contributing to this page.

.. _faq-concretizer-precedence:

-----------------------------------------------------
Why does Spack pick particular versions and variants?
-----------------------------------------------------

This question comes up in a variety of forms:

 1. Why does Spack seem to ignore my package preferences from ``packages.yaml`` config?
 2. Why does Spack toggle a variant instead of using the default from the ``package.py`` file?

The short answer is that Spack always picks an optimal configuration
based on a complex set of criteria\ [#f1]_. These criteria are more nuanced
than always choosing the latest versions or default variants.

.. note::

    As a rule of thumb: requirements + constraints > reuse > preferences > defaults.

The following set of criteria (from lowest to highest precedence) explain
common cases where concretization output may seem surprising at first.

1. :ref:`Package preferences <package-preferences>` configured in ``packages.yaml``
   override variant defaults from ``package.py`` files, and influence the optimal
   ordering of versions. Preferences are specified as follows:

   .. code-block:: yaml

      packages:
        foo:
          version: [1.0, 1.1]
          variants: ~mpi

2. :ref:`Reuse concretization <concretizer-options>` configured in ``concretizer.yaml``
   overrides preferences, since it's typically faster to reuse an existing spec than to
   build a preferred one from sources. When build caches are enabled, specs may be reused
   from a remote location too. Reuse concretization is configured as follows:

   .. code-block:: yaml

      concretizer:
        reuse: dependencies  # other options are 'true' and 'false'

3. :ref:`Package requirements <package-requirements>` configured in ``packages.yaml``,
   and constraints from the command line as well as ``package.py`` files override all
   of the above. Requirements are specified as follows:

   .. code-block:: yaml

      packages:
        foo:
          require:
          - "@1.2: +mpi"

Requirements and constraints restrict the set of possible solutions, while reuse
behavior and preferences influence what an optimal solution looks like.


.. rubric:: Footnotes

.. [#f1] The exact list of criteria can be retrieved with the ``spack solve`` command
