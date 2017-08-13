from flask import request

def cache_key():
    return request.url

@main.route("/test/", methods=['GET'])
@cache.cached(timeout=10, key_prefix=cache_key)
def do_somthing():
    return "hello %s" % str(request.args)