import os
import json


class ZKNode(object):

    def __init__(self, path=None, data=None, stat=None, acls=None, children=None, json_data=None):
        assert (path or json_data)
        if path is not None:
            self.path = path  # path is full path path for better usage
            self.data = data.decode("utf-8", "ignore") if data else None
            self.stat = stat
            self.acls = acls
            self.children = children or []
        elif json_data is not None:
            self.unjsonify(json_data)

    def add_child(self, c):
        self.children.append(c)

    def jsonify(self):
        data = {
            "path": self.path,
            "data": self.data,
            "children": []
        }
        for c in self.children:
            data["children"].append(c.jsonify())
        return(data)

    def unjsonify(self, data):
        self.path = data["path"]
        self.data = data["data"]
        self.children = []
        for c in data["children"]:
            self.children.append(ZKNode(json_data=c))

    def __unicode__(self):
        version = self.stat.version if self.stat else ""
        data = self.data if self.data else ""
        return("{path}\nVersion: {version}\nACLs: {acls}\nChildren: {children}\nData: {data}".format(
            path=self.path,
            version=version,
            acls=self._prettify_acls(),
            children=len(self.children),
            data=data))

    def __str__(self):
        return(self.__unicode__())

    def _prettify_acls(self):
        acl_strings = []
        if self.acls:
            for acl in self.acls:
                acl_strings.append("%s:%s:%s" % (",".join(acl.acl_list), acl.id.scheme, acl.id.id))
        return(" ".join(acl_strings))
