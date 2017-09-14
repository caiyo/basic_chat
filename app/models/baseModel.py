import json


class BaseModel(object):

    def __repr__(self):
        return json.dumps(self.__dict__)

    # ignores keys starting with _ denoting it as a private variable
    def reprJSON(self):
        d = {}
        for k, v in self.__dict__.iteritems():
            if k.startswith('_'):
                continue
            if (hasattr(v, "reprJSON")):
                d[k] = v.reprJSON()
            else:
                d[k] = v
        return d
