from kidney_transplant_llm.postproc import rank_llm
import unittest

class TestTransplantDate(unittest.TestCase):
    def test(self):

        output = rank_llm.count_tf_donor()
        print(output)


