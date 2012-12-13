#!/usr/bin/python
import urlparse
import re

class Link(object):
    def __init__(self, json_object, relative_to_url):
        self.href = json_object['href']

        if 'name' in json_object:
            self.name = json_object['name']

        if 'label' in json_object:
            self.label = json_object['label']

        self.arguments = re.findall(r'{([^}]+)}', self.href)

        if relative_to_url is None:
            self.template = self.href
        else:
            self.template = urlparse.urljoin(relative_to_url, self.href)

    def url(self, **kwargs):
        result = self.template

        for arg in self.arguments:
            result = result.replace("{%s}" % arg, kwargs.get(arg, ''))

        return result

    @classmethod
    def from_object(cls, o, relative_to_url):
        if isinstance(o, list):
            return map(lambda x: cls.from_object(x, relative_to_url), o)

        return cls(o, relative_to_url)

