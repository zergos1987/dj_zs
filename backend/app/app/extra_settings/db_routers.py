# SETTINGS PLUGIN: db_router
class Router(object):

    def db_for_read(self, model, **hints):
        if model._meta.app_label in ['test']:
            return 'test'
        return 'default'

    def db_for_write(self, model, **hints):
        if model._meta.app_label in ['test']:
            return 'test'
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        if obj1._meta.app_label in ['test'] or obj2._meta.app_label in ['test']:
            return True
        elif 'test' not in [obj1._meta.app_label, obj2._meta.app_label]:
            return True
        return False

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label in ['test']:
            return db == 'test'
        return None