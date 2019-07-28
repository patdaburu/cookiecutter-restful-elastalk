.. _publishing:

**********************
Publishing the Package
**********************

As you make changes to the project, you'll probably want to publish new version of the package.
*(That's the point, right?)*

Gemfury
=======

This project's packages are hosted in a private repository at `Gemfury <https://gemfury.com/>`_, so
you will need have have your `Github <https://github.com/>`_ credentials added to the group's
account.

The ``.gemfury`` File
---------------------

The project's :ref:`Makefile <using-the-makefile>` contains a :ref:`publish <make-publish>`
target that uses `curl <https://en.wikipedia.org/wiki/CURL>`_ to upload packages.  Part of the
upload command includes a secret which shoul **never** be included in any project files.

Instead, create a file in your home directory called ``.gemfury`` that contains only the
`repository URL <https://manage.fury.io/dashboard/geocomm/intro?kind=python>`_ on the first line.
The file will look something like the example below.

.. code-block:: bash

    https://ASECRETKEY@push.fury.io/geocomm/

Protect the ``.gemfury`` File
-----------------------------

The ``.gemfury`` file contains a sensitive key.  Since you'll be storing it in a file, let's make
sure only you have the ability to access its contents.

.. code-block:: bash

    chown $USER:$USER ~/.gemfury
    chmod 400 ~/.gemfury

Publishing
==========

The actual process of publishing the project is just a matter of running the
:ref:`publish <make-publish>` target.

.. code-block:: bash

    make publish

Installing
==========

If you just need to install the library in your project, have a look at
the :ref:`general tutorial <getting-started>` and the :ref:`pip.conf <pip>` article.












