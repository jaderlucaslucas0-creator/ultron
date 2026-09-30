from app.plugins.registry import Plugin,register_plugin

def diagnostics(payload):
    return {'ok':True,'received':payload}

register_plugin(Plugin(name='system',description='Diagnóstico interno do ULTRON.',capabilities=['diagnostics'],handler=diagnostics))
