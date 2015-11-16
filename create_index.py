#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
from elasticsearch import Elasticsearch

if __name__ == '__main__':
    es = Elasticsearch()
    es.indices.delete(index="joe")
    es.indices.create(
        index="joe",
        body={
            'mappings': {
                "comments": {
                    'properties': {
                        'link': {'type': 'string', 'index': 'not_analyzed'},
                        'website': {'type': 'string', 'index': 'not_analyzed'},
                        'content': {'type': 'string', 'analyzer': 'english'},
                        'thread_name': {'type': 'string', 'analyzer': 'english'}
                    }
                }
            }
        }
    )
