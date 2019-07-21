from __future__ import print_function

import sys
import services.database.model

class ModelClassFactory:
    _name=""

    def __init__(self, name):
        self._name=name
        pass

    def create(self):
        return getattr(sys.modules["services.database.model"], self._name)


'''
Get a list of models by a raw sql stement.
where, order,pagesize or sql
'''
def get_modellist_by_raw(*args, **kwargs):
    from peewee import Ordering
    from operator import attrgetter
    from peewee import RawQuery

    table=args[0]
    mod_cls=ModelClassFactory(table).create()
    table=mod_cls._meta.table_name
    
    if not 'sql' in kwargs:
        order=""
        limit=""
        where=""
        pagesize=0

        if 'pagesize' in kwargs:
            pagesize=int(kwargs['pagesize'])

        if 'order' in kwargs:
            order = kwargs["order"]

        if 'where' in kwargs:
            where = kwargs["where"]

        if order!="":
            order=" ORDER BY %s" % order

        if int(pagesize)>0:
            limit=" LIMIT %s" % str(pagesize)

        if where!="":
            where = " WHERE %s" % where

        sql='/* Build by  get_modellist_by_raw*/ Select * from %s %s %s %s;' % (table, where, order, limit)
    else:
        sql=kwargs['sql']

    print(sql)
    query=mod_cls.raw(sql)
    return list(query.dicts())
