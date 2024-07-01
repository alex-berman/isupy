import pytest

from isupy.ontology import *
from isupy.semantic_serialization import deserialize



instances = [
    ('Greet()', Greet()),
]


class TestSemanticSerialization:
    @pytest.mark.parametrize('string,object', instances)
    def test_deserialize(self, string, object):
        actual = deserialize(string)
        assert actual == object
