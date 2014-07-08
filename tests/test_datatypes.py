import itertools
from datetime import datetime, time
import pandas as pd
from pgcopy import util
from cpgcopy import CopyManager

from . import db

class TypeMixin(db.TemporaryTable):
    null = 'NOT NULL'
    record_count = 3
    def test_type(self):
        bincopy = CopyManager(self.conn, self.table, self.cols)
        bincopy.copy(self.data)
        select_list = ','.join(self.cols)
        self.cur.execute("SELECT %s from %s" % (select_list, self.table))
        for rec in self.data:
            self.checkValues(rec, self.cur.fetchone())

    def checkValues(self, expected, found):
        for a, b in itertools.izip(expected, found):
            assert (a == self.cast(b))

    def cast(self, v): return v

class CTypeMixin(TypeMixin):
    def test_type(self):
        bincopy = CopyManager(self.conn, self.table, self.cols)
        bincopy.copy(self.dataframe())
        select_list = ','.join(self.cols)
        self.cur.execute("SELECT %s from %s" % (select_list, self.table))
        for rec in self.data:
            self.checkValues(rec, self.cur.fetchone())

    def dataframe(self):
        return pd.DataFrame(self.data, columns=self.cols)

class TestCInteger(CTypeMixin):
    datatypes = ['integer']

class TestCBool(CTypeMixin):
    datatypes = ['bool']

class TestCSmallInt(CTypeMixin):
    datatypes = ['smallint']

class TestCBigInt(CTypeMixin):
    datatypes = ['bigint']

class TestCReal(CTypeMixin):
    datatypes = ['real']

class TestCDouble(CTypeMixin):
    datatypes = ['double precision']

class TestCNull(CTypeMixin):
    null = 'NULL'
    datatypes = ['integer']
    data = [(1,), (2,), (None,)]

class TestCVarchar(CTypeMixin):
    datatypes = ['varchar(12)']

class TestCChar(CTypeMixin):
    datatypes = ['char(12)']

    def cast(self, v):
        assert (12 == len(v))
        return v.strip()

class TestCDate(CTypeMixin):
    def dataframe(self):
        t0 = time(0)
        data = [[datetime.combine(d, t0) for d in row] for row in self.data]
        return pd.DataFrame(data, columns=self.cols)

    datatypes = ['date']

class TestCTimestamp(CTypeMixin):
    datatypes = ['timestamp']

class TestCTimestampTZ(CTypeMixin):
    datatypes = ['timestamp with time zone']

    def cast(self, v):
        return util.to_utc(v)
