"""The published site: every page must exist, load one data file, and never
render a figure the pipeline did not produce."""
from __future__ import annotations

import json
import pathlib
import re
import shutil
import subprocess
import unittest

from msl import config
from tests.helpers import TmpDirCase, NOW1

PAGES = ["index.html", "library.html", "leaderboard.html", "ideas.html",
         "evidence.html", "sources.html", "irregularities.html", "cycles.html",
         "methodology.html"]


class StaticAssets(unittest.TestCase):
    def test_every_page_exists(self):
        for p in PAGES:
            self.assertTrue((config.ROOT / p).exists(), f"{p} is missing")

    def test_every_page_declares_its_route(self):
        for p in PAGES:
            html = (config.ROOT / p).read_text()
            self.assertIn(f'data-page="{p}"', html, f"{p} does not declare data-page")
            self.assertIn('id="main"', html)
            self.assertIn('data/site.js', html)
            self.assertIn('app.js', html)

    def test_no_page_inlines_data(self):
        """The pages read data/site.js and nothing else, so prose and site cannot drift."""
        for p in PAGES:
            html = (config.ROOT / p).read_text()
            self.assertNotIn("window.MSLDATA =", html)

    def test_every_page_has_a_skip_link_and_a_title(self):
        for p in PAGES:
            html = (config.ROOT / p).read_text()
            self.assertIn('class="skip"', html)
            self.assertRegex(html, r"<title>.+MasterSelfLearn</title>")

    def test_pages_publish_from_the_root_so_no_jekyll_processing(self):
        self.assertTrue((config.ROOT / ".nojekyll").exists())

    def test_app_js_routes_every_page(self):
        js = (config.ROOT / "app.js").read_text()
        for p in PAGES:
            self.assertIn(f'"{p}"', js, f"app.js has no route for {p}")

    def test_app_js_does_not_fetch_anything(self):
        """Zero runtime dependencies: the site must work from file:// too."""
        js = (config.ROOT / "app.js").read_text()
        for banned in ("fetch(", "XMLHttpRequest", "localhost", "127.0.0.1"):
            self.assertNotIn(banned, js, f"app.js uses {banned}")


class GeneratedSiteData(TmpDirCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = pathlib.Path(__file__).resolve().parent
        super().setUpClass()

    def setUp(self):
        super().setUp()
        self.seed_into(self.dir)
        self.cycle(NOW1)
        raw = (self.dir / "site.js").read_text()
        self.data = json.loads(raw.split("window.MSLDATA = ", 1)[1].rstrip().rstrip(";"))

    def test_every_topic_shows_its_verified_claim_count(self):
        for t in self.data["topics"]:
            self.assertIn("verifiedClaims", t)
            self.assertIsInstance(t["verifiedClaims"], int)

    def test_topics_with_no_claims_are_not_hidden(self):
        zero = [t for t in self.data["topics"] if t["verifiedClaims"] == 0]
        self.assertTrue(zero, "a gap that is not displayed is a gap that gets filled with prose")

    def test_every_evidence_row_carries_a_url_and_a_hash(self):
        for c in self.data["evidence"]:
            if c["kind"] == "derived":
                self.assertTrue(c["computedFrom"])
                continue
            self.assertTrue(c["evidenceIds"], f"{c['id']} references no evidence row")
            e = self.data["evidenceRows"][c["evidenceIds"][0]]
            self.assertTrue(e["url"].startswith("http"), f"{c['id']} evidence has no url")
            self.assertTrue(e["sha256"], f"{c['id']} evidence has no hash")

    def test_transcribed_evidence_is_flagged_in_the_data(self):
        """A reading an agent typed in cannot be hash-verified from the wire, and
        the published data must say so rather than look like a direct read."""
        flagged = [e for e in self.data["evidenceRows"].values()
                   if e["wireHashVerifiable"] is False]
        self.assertTrue(flagged, "expected at least one non-wire-verifiable row")
        for e in flagged:
            self.assertTrue(e["url"].startswith("http"))
        claims_on_those = [c for c in self.data["evidence"]
                           if any(i in {f["id"] for f in flagged}
                                  for i in c["evidenceIds"])]
        self.assertTrue(claims_on_those,
                        "flagged rows should still be traceable to the claims they support")

    def test_the_source_registry_includes_the_exclusion_lists(self):
        self.assertTrue(self.data["keyedExcluded"])
        self.assertTrue(self.data["categoriesWithoutSource"])

    def test_the_leaderboard_states_its_qualification_rule(self):
        q = self.data["leaderboard"]["qualification"]
        self.assertEqual(q["minScoredForecasts"], config.MIN_SCORED_FORECASTS_TO_RANK)
        self.assertIn("null", q["rule"])

    def test_the_seed_capture_table_is_published(self):
        self.assertTrue(self.data["seedCaptures"])
        for s in self.data["seedCaptures"]:
            self.assertTrue(s["file"])
            self.assertEqual(len(s["payloadSha256"]), 64)

    def test_no_statement_is_empty(self):
        for c in self.data["evidence"]:
            self.assertTrue(c["statement"].strip(), f"{c['id']} has an empty statement")


class GeneratedDocs(TmpDirCase):
    def setUp(self):
        super().setUp()
        self.seed_into(self.dir)
        self.cycle(NOW1)

    def _readme(self):
        # docs_dir is the temp dir for a test cycle, so the generated documents
        # are read from there, never from the repository root.
        return (self.dir / "README.md").read_text()

    def test_readme_has_the_auto_counts_block(self):
        r = self._readme()
        self.assertIn("<!-- AUTO:COUNTS:BEGIN", r)
        self.assertIn("<!-- AUTO:COUNTS:END -->", r)

    def test_auto_counts_matches_the_ledger(self):
        r = self._readme()
        block = r.split("AUTO:COUNTS:BEGIN", 1)[1].split("AUTO:COUNTS:END", 1)[0]
        claims = [l for l in (self.dir / "claims.jsonl").read_text().splitlines() if l.strip()]
        m = re.search(r"\| Verified claims in the ledger \| \*\*([\d,]+)\*\*", block)
        self.assertIsNotNone(m, "the counts table has no claim total")
        self.assertEqual(int(m.group(1).replace(",", "")), len(claims))

    def test_readme_says_manual_input_is_zero(self):
        self.assertIn("| Manual inputs required | **0** |", self._readme())

    def test_verification_ledger_has_one_row_per_source(self):
        v = (self.dir / "VERIFICATION.md").read_text()
        from msl.sources import REGISTRY
        for s in REGISTRY:
            self.assertIn(f"`{s.id}`", v, f"{s.id} is missing from the audit ledger")

    def test_irregularities_doc_groups_by_severity(self):
        i = (config.ROOT / "IRREGULARITIES.md").read_text()
        self.assertIn("## WARN", i)
        self.assertIn("## INFO", i)

    def test_status_doc_reports_the_cycle(self):
        s = (config.ROOT / "STATUS.md").read_text()
        self.assertIn("# STATUS — cycle 1", s)


if __name__ == "__main__":
    unittest.main()


class RenderCheck(unittest.TestCase):
    """Every page must actually DRAW, not merely parse.

    app.js has twice shipped with a bracket bug that node --check caught but no
    test did, and the result would have been nine blank pages.  This runs the
    headless DOM render over every .html file in the repo and fails if a page is
    blank or throws.
    """

    def test_every_page_renders(self):
        node = shutil.which("node")
        if not node:
            self.skipTest("node is not installed")
        r = subprocess.run([node, str(config.ROOT / "tools" / "render_check.js")],
                           capture_output=True, text=True)
        self.assertEqual(r.returncode, 0,
                         "a page did not render:\n" + r.stdout + r.stderr)
        self.assertIn("RENDER CHECK PASSED", r.stdout)

    def test_the_nine_pages_on_disk_are_the_nine_routes_in_app_js(self):
        js = (config.ROOT / "app.js").read_text(encoding="utf-8")
        on_disk = {p.name for p in config.ROOT.glob("*.html")}
        routed = set(re.findall(r'"([a-z]+\.html)": page', js))
        self.assertEqual(on_disk, routed,
                         "a page exists with no route, or a route with no page")


class Workflows(unittest.TestCase):
    """The cron loop is the product. A workflow that will not parse is a system
    that silently stops thinking, so the failure mode that already happened here
    — a commit message written at column 0 inside a `run: |` block, which ends
    the block scalar and makes the file invalid YAML — gets its own test.
    """

    def test_no_run_block_is_terminated_by_an_underindented_line(self):
        wf = sorted((config.ROOT / ".github" / "workflows").glob("*.yml"))
        self.assertTrue(wf, "no workflow files found")
        for f in wf:
            lines = f.read_text(encoding="utf-8").split("\n")
            block_indent = None
            for i, line in enumerate(lines, 1):
                stripped = line.strip()
                if block_indent is None:
                    if stripped.endswith("|") and stripped.startswith("run:"):
                        block_indent = len(line) - len(line.lstrip())
                    continue
                if not stripped:
                    continue
                indent = len(line) - len(line.lstrip())
                if indent <= block_indent:
                    block_indent = None
                    continue
                self.assertGreater(
                    indent, block_indent,
                    f"{f.name}:{i} is under-indented inside a `run: |` block and "
                    f"would terminate it, making the workflow invalid YAML")
                block_indent = indent if False else block_indent

    def test_every_step_in_the_think_workflow_has_a_name_or_a_uses(self):
        text = (config.ROOT / ".github" / "workflows" / "think.yml").read_text()
        self.assertIn("python3 -m msl.cli selftest", text)
        self.assertIn("python3 -m msl.cli cycle", text)
        self.assertIn("tools/verify_claims.py", text)
        self.assertIn("git push", text)
        self.assertIn("permissions:", text)
        self.assertIn("contents: write", text)
