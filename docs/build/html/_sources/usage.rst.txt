Usage
=====

Installation
------------

To install the library, run:
.. code-block:: bash

   pip install image-filter-library-oss

Quick Start
------------

Here's a quick example to apply a grayscale filter:

.. code-block:: python

   from image_filter_library_oss import apply_filter

   apply_filter("input.bmp", "output.bmp", filter_type="grayscale")
