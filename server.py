import json
import asyncio
import functools

from aiohttp import web

from en_dict import Dictionary


@asyncio.coroutine
def recommend(request):
    """Return a json response for recommending while typing.
    Test by:
    $ curl -H "Content-Type: application/json" \
        -X POST -d '{"word": "ab"}' http://localhost:8000/recommend
    """
    content = yield from request.json()

    if content.get('word') is None:
        error = dict(word="can't be blank")
        body = json.dumps(dict(error=error)).encode('utf-8')
        raise web.HTTPBadRequest(body=body,
                                 content_type='application/json')

    items = request.app['en_dict'].prefix_recommend(content['word'])
    words = [item.word for item in items]
    if words:
        return web.json_response(data=dict(prefix_exist=True,
                                           words=words),
                                 dumps=request.app['unicode_dumps'])
    else:
        return web.json_response(data=dict(prefix_exist=False),
                                 dumps=request.app['unicode_dumps'])


@asyncio.coroutine
def find(request):
    """Return a json response for finding a word.
    Test by:
    $ curl -H "Content-Type: application/json" \
        -d '{"word": "dad"}' http://localhost:8000/find
    """
    content = yield from request.json()

    if content.get('word') is None:
        error = dict(word="can't be blank")
        body = json.dumps(dict(error=error)).encode('utf-8')
        raise web.HTTPBadRequest(body=body,
                                 content_type='application/json')

    item = request.app['en_dict'].find(content['word'])
    if item:
        return web.json_response(data=dict(success=True, item=item.to_dict()),
                                 dumps=request.app['unicode_dumps'])
    else:
        return web.json_response(data=dict(success=False),
                                 dumps=request.app['unicode_dumps'])


@asyncio.coroutine
def modify(request):
    """Receive a word to add or modify the existed word."""
    pass


@asyncio.coroutine
def add(request):
    """Add a word to dictionary"""
    content = yield from request.json()

    request.app['en_dict'].insert(content['word'],
                                  [(m['part_of_speech'], m['explanation'])
                                   for m in content['meanings']],
                                  [(e['sentence'], e['translation'])
                                   for e in content['examples']]
                                  )
    return web.json_response(data=dict(success=True),
                             dumps=request.app['unicode_dumps'])


def create_app(loop=None):
    """Application factory function."""
    app = web.Application(loop=loop)

    app['en_dict'] = Dictionary('data/items_comp.json')
    app['unicode_dumps'] = functools.partial(json.dumps, ensure_ascii=False)

    app.router.add_route('POST', '/api/recommend', recommend)
    app.router.add_route('POST', '/api/find', find)
    app.router.add_route('POST', '/api/add', add)

    return app


@asyncio.coroutine
def init(loop):
    app = create_app(loop=loop)

    host, port = '0.0.0.0', '8000'
    handler = app.make_handler()
    server = yield from loop.create_server(handler, host, port)
    print('Server started at http://{}:{}'.format(host, port))
    return server

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(init(loop))
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
