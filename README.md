# Sparse List [![Build Status](https://travis-ci.org/johnsyweb/python_sparse_list.png)](https://travis-ci.org/johnsyweb/python_sparse_list) 

Inspired by http://stackoverflow.com/q/17522753/78845

A "sparse list" is a list where most (say, more than 95% of) values will be None
(or some other default)  and for reasons of memory efficiency you don't wish to
store these (cf. [Sparse array](http://en.wikipedia.org/wiki/Sparse_array)).

This implementation has a similar interface to Python's built-in list but
stores the data in a dictionary to conserve memory.


## Installation

`sparse_list` is available from [PyPI - the Python Package
Index](https://pypi.python.org/pypi) (aka [The
Cheeseshop](https://pypi.python.org/pypi)). Installation is simply:

    $ pip install sparse_list

## Usage

See the [unit-tests](https://github.com/johnsyweb/python_sparse_list/blob/master/t_sparse_list.py)!

## Contributing

1. Fork it
1. Create your feature branch (`git checkout -b my-new-feature`)
1. Commit your changes (`git commit -am 'Add some feature'`)
1. Ensure the tests pass for all Pythons in [`.travis.yml`](https://github.com/johnsyweb/python_sparse_list/blob/master/.travis.yml)
1. Push to the branch (`git push origin my-new-feature`)
1. Create new Pull Request

## Thanks

If you find this stuff useful, please follow this repository on
[GitHub](https://github.com/johnsyweb/python_sparse_list). If you have something to say,
you can contact [johnsyweb](http://johnsy.com/about/) on
[Twitter](http://twitter.com/johnsyweb/) and
[GitHub](https://github.com/johnsyweb/).
