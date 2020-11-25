def _init(envs = {}):
    global _global_envs
    _global_envs = envs

def SET(name, value):
    _global_envs[name] = value

def GET(name, defValue=None):
    try:
        return _global_envs[name]
    except KeyError:
        return defValue