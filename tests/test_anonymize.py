import os
import unittest
from unittest.mock import patch

import pandas as pd

from src.ingestion.anonymize import anonymize_dataframe


class AnonymizeTests(unittest.TestCase):
    def test_direct_fields_removed_and_identifier_pseudonymized(self):
        source = pd.DataFrame({"cpf": ["00000000000"], "nome": ["Pessoa Fictícia"], "categoria": ["exemplo"]})
        with patch.dict(os.environ, {"BRONZE_HASH_SALT": "synthetic-test-salt"}):
            result = anonymize_dataframe(source, ["cpf"], ["nome"])
        self.assertNotIn("nome", result.columns)
        self.assertNotEqual("00000000000", result.loc[0, "cpf"])
        self.assertEqual(64, len(result.loc[0, "cpf"]))
        self.assertEqual("exemplo", result.loc[0, "categoria"])

    def test_missing_salt_fails_closed(self):
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(RuntimeError):
                anonymize_dataframe(pd.DataFrame({"cpf": ["00000000000"]}), ["cpf"], [])
