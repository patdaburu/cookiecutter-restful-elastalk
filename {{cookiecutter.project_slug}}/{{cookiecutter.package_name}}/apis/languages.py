#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. currentmodule:: {{cookiecutter.package_name}}.apis.languages
.. moduleauthor:: {{cookiecutter.author_name}} <{{cookiecutter.author_email}}>

This is a sample API for your application.  You can learn from it, but you
probably want to remove it.
"""
import uuid
from flask_restplus import fields, Namespace, Resource
from flask_restplus.model import Model
from elasticsearch.exceptions import NotFoundError
from ..core.jsend import response, JSendStatus


api = Namespace('languages', description='Popular Programming Languages')

LanguageModel: Model = api.model(
    'Language',
    {
        'id_': fields.String(
            readonly=True,
            description='the API version'
        ),
        'language': fields.String(
            description='the language',
            required=True
        )
    }
)  #: the language model


@api.route('/')
class LanguagesResource(Resource):
    """Manage all the languages!"""

    @api.marshal_with(LanguageModel, envelope='languages')
    @api.doc('get_languages')
    def get(self):
        """Get the list of languages."""
        try:
            # Query and get the response.
            res = self.es.search(
                index="languages",
                body={
                    "query": {"match_all": {}}
                }
            )
            # Get the hits from the response.
            hits = res['hits']['hits']
            # The 'sources' are the records that were returned.
            return [
                {
                    'id_': hit['_id'],
                    **hit['_source']
                }
                for hit in hits
            ]
        except NotFoundError:
            # If the index has not yet been created, return an empty
            # database.
            return []

    @api.expect(LanguageModel)
    @api.doc('create_language')
    def post(self):
        """Add a language."""
        # Create an ID for the new record.
        id_ = uuid.uuid4()
        # Create a document (to pass to Elasticsearch).
        doc = api.payload
        # Index the document.
        self.es.index(
            index='languages',
            doc_type='language',
            id=id_,
            body=doc)
        # Hooray!
        return response(
            status=JSendStatus.SUCCESS,
            message='The language was added.'
        )


@api.route('/<string:id_>')
@api.response(404, 'Not found.')
@api.param('id_', "the language's identifier")
class LanguageResource(Resource):
    """Manage individual languages."""

    @api.doc('get_language')
    @api.marshal_with(LanguageModel)
    def get(self, id_):
        """Get a language."""
        # Query and get the response.
        res = self.es.search(
            index="languages",
            body={
                "query": {
                    "match": {
                        '_id': id_
                    }
                }
            }
        )
        # Get the hits from the response.
        hits = res['hits']['hits']
        # If there were no matches...
        if not hits:
            return '', 404  # ...it's a 404.
        # Get the first hit.
        hit = hits[0]
        # Format it and return it.
        return {
            'id_': hit['_id'],
            **hit['_source']
        }

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
            code=204
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
