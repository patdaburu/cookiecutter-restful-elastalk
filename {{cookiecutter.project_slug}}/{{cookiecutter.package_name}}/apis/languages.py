#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. currentmodule:: restful_api.apis.languages
.. moduleauthor:: my_name <my_email>

This is a sample API for your application.  You can learn from it, but you
probably want to remove it.
"""
import uuid
from elastalk import ElastalkMixin, extract_hits
from elasticsearch import NotFoundError
from flask_restplus import fields, Namespace, Resource
from flask_restplus.model import Model
from ..core.ids import UUID
from ..core.jsend import response, JSendStatus

api = Namespace('languages', description='Popular Programming Languages')

LanguageModel: Model = api.model(
    'Info',
    {
        '_id': UUID(
            attribute='_id',
            readOnly=True,
            description='identifies the record'
        ),
        'name': fields.String(
            description='the language name'
        )
    }
)  #: the language model


@api.route('/')
class LanguageResource(Resource, ElastalkMixin):
    """Manage your list of popular programming languages!"""

    @api.doc('get_languages')
    @api.marshal_with(LanguageModel, envelope='languages')
    def get(self):
        """List all the languages!"""
        try:
            result = self.es.search(
                index='languages',
                body={
                    "query": {"match_all": {}}
                }
            )
            return list(extract_hits(result))
        except NotFoundError:
            return []

    @api.expect(LanguageModel)
    @api.doc('create_language')
    def post(self):
        """Add a language!"""
        # Create an ID for the new record.
        id_ = uuid.uuid4()
        # Create a document (to pass to Elasticsearch).
        doc = api.payload
        # Index the document.
        self.es.index(
            index='languages',
            doc_type='language',
            id=id_,
            body=doc
        )
        # Hooray!
        return response(
            status=JSendStatus.SUCCESS,
            message='The language was added.',
            data={'_id': str(id_)}
        )


@api.route('/<string:id_>')
@api.response(404, 'Not found.')
@api.param('id_', "the language's identifier")
class LanguageIdResource(Resource, ElastalkMixin):
    """Manage individual languages."""

    @api.doc('get_language')
    @api.marshal_with(LanguageModel)
    def get(self, id_):
        """Get a language."""
        result = self.es.search(
            index='languages',
            body={
                "query": {
                    "match": {
                        '_id': id_
                    }
                }
            }
        )
        try:
            for hit in extract_hits(result):
                return hit
        except IndexError:
            return '', 404

    @api.doc('delete_language')
    def delete(self, id_):
        """Delete a language."""
        try:
            self.es.delete(
                index='languages',
                doc_type='language',
                id=id_
            )
        except NotFoundError:
            return '', 404
        return response(
            status=JSendStatus.SUCCESS,
            message='The language was deleted.',
            code=200
        )

    @api.doc('update_language')
    @api.expect(LanguageModel)
    def put(self, id_):
        """Update a language."""
        # Index the document.
        try:
            self.es.update(
                index='languages',
                doc_type='language',
                id=id_,
                body={"doc": api.payload})
        except NotFoundError:
            return '', 404
        # Hooray!
        return response(
            status=JSendStatus.SUCCESS,
            message='The language was updated.',
            code=202
        )
