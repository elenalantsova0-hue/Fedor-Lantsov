from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
CONTACT = ROOT / "contact.html"
APP = ROOT / "js" / "app.js"


class InquiryFormTests(unittest.TestCase):
    def test_form_posts_to_formspree_endpoint(self):
        html = CONTACT.read_text(encoding="utf-8")
        self.assertIn('action="https://formspree.io/f/xwlenekv"', html)
        self.assertIn('method="post"', html)

    def test_form_has_submission_metadata_and_honeypot(self):
        html = CONTACT.read_text(encoding="utf-8")
        self.assertIn('name="_subject"', html)
        self.assertIn('name="_gotcha"', html)
        self.assertIn('name="artworkTitle"', html)

    def test_javascript_sends_form_data_and_handles_failures(self):
        script = APP.read_text(encoding="utf-8")
        self.assertIn("fetch(form.action", script)
        self.assertIn("new FormData(form)", script)
        self.assertIn("Accept: 'application/json'", script)
        self.assertIn("if (!response.ok)", script)
        self.assertIn("submitButton.disabled = true", script)
        self.assertNotIn("demo form", script)


if __name__ == "__main__":
    unittest.main()
