`Sparse List <https://pypi.org/project/sparse_list/>`__ |Build Status|
=========================================================================

Inspired by the post `Populating a sparse list with random
1's <http://stackoverflow.com/q/17522753/78845>`__ on
`StackOverflow <http://stackoverflow.com/>`__.

A "sparse list" is a list where most values will be None (or some other default)
and for reasons of memory efficiency you don't wish to store these (cf. `Sparse
array <http://en.wikipedia.org/wiki/Sparse_array>`__).

This implementation has a similar interface to Python's built-in list
but stores the data in a dictionary to conserve memory.

Installation
------------

`sparse_list <https://pypi.org/project/sparse_list/>`__ is
available from `The Python Package Index (PyPI) <https://pypi.org/>`__ .

Installation is simply:

::

    $ pip install sparse_list

Usage
-----

See the
`unit-tests <https://github.com/johnsyweb/python_sparse_list/blob/HEAD/test_sparse_list.py>`__!

Contributing
------------

1. Fork it
2. Create your feature branch (``git checkout -b my-new-feature``)
3. Commit your changes (``git commit -am 'Add some feature'``)
4. Ensure the tests pass for all Pythons in
   `.python.yml <https://github.com/johnsyweb/python_sparse_list/blob/HEAD/.github/workflows/python.yml>`__
5. Push to the branch (``git push origin my-new-feature``)
6. Create new Pull Request

Thanks
------

If you find this stuff useful, please follow this repository on
`GitHub <https://github.com/johnsyweb/python_sparse_list>`__. If you
have something to say, you can contact
`johnsyweb <http://johnsy.com/about/>`__ on
`Twitter <http://twitter.com/johnsyweb/>`__ and
`GitHub <https://github.com/johnsyweb/>`__.


Many thanks
-----------

I'm grateful for contributions to what was a solo project (hooray for
`GitHub :octocat:) <http://github.com/>`__! If you'd like to thank the
contributors, you can find their details here:

https://github.com/johnsyweb/python_sparse_list/graphs/contributors

.. |Build Status| image:: https://github.com/johnsyweb/python_sparse_list/actions/workflows/python.yml/badge.svg
   :target: https://github.com/johnsyweb/python_sparse_list/actions/workflows/python.yml
