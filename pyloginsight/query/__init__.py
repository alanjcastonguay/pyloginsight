#!/usr/bin/env python
# -*- coding: utf-8 -*-

# VMware vRealize Log Insight SDK
# Copyright (c) 2016 VMware, Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.



# A "Constraint" consists of (field, operator, value).

from . import Operator
from requests.utils import quote
import warnings

class Constraint:
    """"""
    def __init__(self, field="text", operator=Operator.CONTAINS, value=""):
        self.field = field
        self.operator = operator
        self.value = value


    def __str__(self):
        """Url-encode each of the arguments, and return a query fragment like `/field/operator value`."""
        if self.operator in Operator._NUMERIC:
            self.value = str(int(self.value))
        if self.operator in Operator._TIME and self.field != 'timestamp':
            raise(ValueError("Time operator '%s' can only be used with the 'timestamp' field." % self.operator))

        if self.operator in Operator._BOOLEAN: # Boolean operators don't include a value
            warnings.warn("Attempted to use boolean operator with a value")
            return '/' + quote(self.field, safe="") + '/' + quote(self.operator, safe="")
        else:
            return '/' + quote(self.field, safe="") + '/' + quote(self.operator, safe="") + quote(self.value, safe="")

    def __repr__(self):
        """A human-readable representation of the constraint, in constructor form."""
        return 'Constraint("%s", %s, "%s")' % (self.field, self.operator, self.value)

class Parameters(dict):
    def __init__(self, order="DESC", view="DEFAULT", limit=100, timeout=30000, contentpackfields="", *args, **kwargs):
        self.update(*args, **kwargs)
        self.__setitem__("order-by-direction", order)
        self.__setitem__("limit", limit)
        self.__setitem__("timeout", timeout)
        self.__setitem__("content-pack-fields", contentpackfields)

class Query:
    def __init__(self, constraints=None, parameters=None):
        if constraints is None:
            constraints = []

