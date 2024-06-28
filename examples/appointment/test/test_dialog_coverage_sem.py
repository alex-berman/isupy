import yaml

import pytest
from isupy import semantic_serialization
from isupy.test.dialogtest import run_dialog_test_sem

from examples.appointment.dm import DialogueManager
import examples.appointment.ontology


test_contents = yaml.load(open('examples/appointment/test/dialog_coverage_sem.yml').read(), yaml.Loader)
semantic_serialization.register_module(examples.appointment.ontology)


class TestDialogs(object):
    @pytest.mark.parametrize('name,content', test_contents.items())
    def test_dialog(self, name, content):
        dm = DialogueManager()
        run_dialog_test_sem(dm, content['turns'], examples.appointment.ontology.DialogState())
