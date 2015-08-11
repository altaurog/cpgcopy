cpgcopy
=================

cpgcopy is a Cython implementation of pgcopy_, a
small system for very fast bulk insertion of data into a
PostgreSQL database table using `binary copy`_.

cpgcopy is somewhat faster than pgcopy.  In reality, network bandwith and
other system limitations are much more likely to be your rate-limiting
factor.  In retrospect, I learned a nice bit about cython with this
project, but ultimately found it a misplaced optimization effort.

Requirements
-------------
Cython_ and numpy_ must be installed to build the package.
(Help distributing sources without Cython dependency would
be greatly appreciated.)
Additional run-time dependencies are:

* pytz_
* psycopg2_
* pandas_
* pgcopy_

cpgcopy can be built on recent linux
systems (glibc version 2.9 or higher).
No information is available regarding
its use on other platforms.

nose_ is required to run the tests.

Basic use
---------

cpgcopy provides facility for copying data from a pandas ``DataFrame`` to a
table in a postgresql database using a ``CopyManager``, which must be
instantiated with a psycopg2 db connection, the table name, and an iterable
indicating the names of the columns to be inserted.  cpgcopy inspects the
database to determine the datatypes of the columns.

For example::

    import numpy as np
    import pandas as pd
    import psycopg2
    from cpgcopy import CopyManager
    cols = ('a', 'b', 'c')
    df = pd.DataFrame(np.random.randn(500, 3), columns=cols)
    conn = psycopg2.connect(database='weather_db')
    mgr = CopyManager(conn, 'measurements_table', cols)
    mgr.copy(df)

Supported datatypes
-------------------

Currently the following PostgreSQL datatypes are supported:

* bool
* smallint
* integer
* bigint
* real
* double precision
* char
* varchar
* date
* timestamp
* timestamp with time zone


Benchmarks
-----------

Below are simple benchmark results for 100000 records.
This gives a general idea of the kind of speedup 
available with cpgcopy::

    $ nosetests -c tests/benchmark.cfg 
                         Benchmark:   0.35s
              ExecuteManyBenchmark:   7.86s
    ----------------------------------------------------------------------
    Ran 2 tests in 9.085s


.. _binary copy: http://www.postgresql.org/docs/9.3/static/sql-copy.html
.. _psycopg2: https://pypi.python.org/pypi/psycopg2/
.. _pytz: https://pypi.python.org/pypi/pytz/
.. _nose: https://pypi.python.org/pypi/nose/
.. _pgcopy: https://github.com/altaurog/pgcopy
.. _Cython: https://pypi.python.org/pypi/Cython
.. _numpy: https://pypi.python.org/pypi/numpy
.. _pandas: https://pypi.python.org/pypi/pandas
