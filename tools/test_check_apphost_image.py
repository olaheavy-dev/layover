"""Tests for tools/check_apphost_image.py. Run with: python3 -m unittest discover -s tools -p 'test_*.py'."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import check_apphost_image as check  # noqa: E402

DIGEST = "a" * 64
COMPOSE = f"services:\n  db:\n    image: pgvector/pgvector:1.0-pg18@sha256:{DIGEST}\n"
APPHOST = f""".withImage("pgvector/pgvector")
  .withImageTag("1.0-pg18")
  .withImageSHA256("{DIGEST}");"""


class CheckAppHostImage(unittest.TestCase):
    def test_same_image_passes(self) -> None:
        self.assertEqual(check.problems(COMPOSE, APPHOST), [])

    def test_a_different_tag_fails(self) -> None:
        found = check.problems(COMPOSE, APPHOST.replace("1.0-pg18", "1.1-pg18"))
        self.assertEqual(len(found), 1)
        self.assertIn("tag", found[0])

    def test_a_different_digest_fails(self) -> None:
        found = check.problems(COMPOSE, APPHOST.replace(DIGEST, "b" * 64))
        self.assertEqual(len(found), 1)
        self.assertIn("digest", found[0])

    def test_a_missing_digest_fails(self) -> None:
        found = check.problems(COMPOSE, APPHOST.replace(f'\n  .withImageSHA256("{DIGEST}")', ""))
        self.assertTrue(any("digest" in line for line in found))

    def test_a_compose_image_without_digest_fails(self) -> None:
        found = check.problems("    image: pgvector/pgvector:1.0-pg18\n", APPHOST)
        self.assertEqual(len(found), 1)


if __name__ == "__main__":
    unittest.main()
