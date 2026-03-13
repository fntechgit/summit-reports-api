_GRAPHQL_PATH = '/reports'

_GRAPHQL_REQUEST_SCHEMA = {
    'type': 'object',
    'required': ['query'],
    'properties': {
        'query': {
            'type': 'string',
            'description': 'A GraphQL query or mutation string.',
            'example': '{ speakers(summitId: 1) { results { id fullName } } }',
        },
        'variables': {
            'type': ['object', 'null'],
            'description': 'A JSON object of variable values referenced by the query.',
            'additionalProperties': True,
        },
        'operationName': {
            'type': ['string', 'null'],
            'description': 'If the query contains multiple operations, the name of the one to execute.',
        },
    },
}

_GRAPHQL_RESPONSE_SCHEMA = {
    'type': 'object',
    'properties': {
        'data': {
            'type': ['object', 'null'],
            'description': 'The data returned by the GraphQL query.',
            'additionalProperties': True,
        },
        'errors': {
            'type': ['array', 'null'],
            'description': 'A list of errors that occurred during execution.',
            'items': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string'},
                    'locations': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'line': {'type': 'integer'},
                                'column': {'type': 'integer'},
                            },
                        },
                    },
                    'path': {
                        'type': 'array',
                        'items': {'type': 'string'},
                    },
                },
            },
        },
    },
}

_GRAPHQL_PATH_ITEM = {
    'post': {
        'operationId': 'graphql_query',
        'summary': 'Execute a GraphQL query',
        'description': (
            'Single GraphQL endpoint for all summit report queries. '
            'Accepts a GraphQL document in the request body and returns the query result.\n\n'
            'Authentication is required via OAuth2 bearer token. '
            'The GraphiQL interactive explorer is available at this URL when accessed from a browser (GET).'
        ),
        'tags': ['Private'],
        'security': [{'OAuth2': []}],
        'requestBody': {
            'required': True,
            'content': {
                'application/json': {
                    'schema': _GRAPHQL_REQUEST_SCHEMA,
                },
            },
        },
        'responses': {
            '200': {
                'description': (
                    'GraphQL response. Note: errors during query execution are returned '
                    'with HTTP 200 inside the `errors` field.'
                ),
                'content': {
                    'application/json': {
                        'schema': _GRAPHQL_RESPONSE_SCHEMA,
                    },
                },
            },
            '400': {'description': 'Malformed request (e.g. missing or unparseable `query` field).'},
            '401': {'description': 'Missing or invalid OAuth2 bearer token.'},
        },
    },
    'get': {
        'operationId': 'graphql_explorer',
        'summary': 'Open the GraphiQL interactive explorer',
        'description': 'Returns the GraphiQL browser UI for exploring the GraphQL schema interactively.',
        'tags': ['Private'],
        'security': [{'OAuth2': []}],
        'responses': {
            '200': {
                'description': 'GraphiQL HTML interface.',
                'content': {'text/html': {'schema': {'type': 'string'}}},
            },
            '401': {'description': 'Missing or invalid OAuth2 bearer token.'},
        },
    },
}


def custom_postprocessing_hook(result, generator, request, public):
    for path, methods in result.get('paths', {}).items():
        is_public = path.startswith('/api/public/')
        tag = 'Public' if is_public else 'Private'
        for method, operation in methods.items():
            if not isinstance(operation, dict):
                continue
            operation['tags'] = [tag]
            if is_public:
                operation['security'] = []

    paths = result.setdefault('paths', {})
    if _GRAPHQL_PATH not in paths:
        paths[_GRAPHQL_PATH] = _GRAPHQL_PATH_ITEM

    return result
