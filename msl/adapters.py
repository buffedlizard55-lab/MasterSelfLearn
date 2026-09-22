"""Adapters: turn a real payload into ``Fact`` rows.

Every extractor is defensive by design.  A payload whose shape has changed yields
zero facts plus a recorded shape problem — it never yields a partially-guessed
fact.  Nothing here computes anything: extraction is projection only.  Arithmetic
lives in :mod:`msl.reason` where it can be rechecked.
"""
from __future__ import annotations

import re
import xml.etree.ElementTree as ET
import dataclasses
from dataclasses import dataclass

from typing import Any, Callable, Dict, List, Optional

ATOM = "{http://www.w3.org/2005/Atom}"


@dataclass
class Fact:
    """A projected observation, before the evidence gate turns it into a Claim."""

    topic: str
    field: str
    value: Any
    unit: str = ""
    statement: str = ""
    kind: str = "captured"
    path: str = ""
    tags: List[str] = dataclasses.field(default_factory=list)
    #: topic slugs this fact is evidence FOR.  Without it, claims attach only to
    #: the family topic and every discovered entity stays at zero verified claims.
    entities: List[str] = dataclasses.field(default_factory=list)


@dataclass
class ExtractResult:
    facts: List[Fact] = dataclasses.field(default_factory=list)
    #: (entity_slug, title, weight, url) — seeds the discovery stage
    entities: List[tuple] = dataclasses.field(default_factory=list)
    problems: List[str] = dataclasses.field(default_factory=list)

    def add(self, *a: Any, **kw: Any) -> None:
        self.facts.append(Fact(*a, **kw))

    def ent(self, slug: str, title: str, weight: float, url: str) -> None:
        self.entities.append((slug, title, weight, url))


def _num(v: Any) -> Optional[float]:
    if v is None or isinstance(v, bool):
        return None
    if isinstance(v, (int, float)):
        return float(v)
    try:
        return float(str(v).replace(",", ""))
    except (TypeError, ValueError):
        return None


def _str(v: Any, limit: int = 200) -> str:
    return ("" if v is None else str(v))[:limit]


# --------------------------------------------------------------------------- #
# GitHub
# --------------------------------------------------------------------------- #
def gh_search(payload: Any, ctx: Dict[str, Any]) -> ExtractResult:
    r = ExtractResult()
    if not isinstance(payload, dict):
        r.problems.append("github_search: payload is not a JSON object")
        return r
    total = _num(payload.get("total_count"))
    # The query is the subject of the count.  Without it the field name is empty —
    # 106 rows in the ledger read ``github.total_count[]`` and were published as
    # "GitHub Search reports 3,667,127 repositories matching ." (87 by cycle 14; the
    # unattended workflow kept writing them until this fix was merged) — and, worse, every
    # query that lacked a context collapsed into that one field, so unrelated
    # searches shared a series.  A total that cannot be attributed to a query is not
    # recorded at all.
    qlabel = _str(ctx.get("query"), 120)
    if total is None:
        r.problems.append("github_search: total_count missing")
    elif not qlabel:
        r.problems.append("github_search: the read reported total_count="
                          f"{int(total):,} but neither the task nor the URL names the "
                          f"query, so the count cannot be attributed; no fact was "
                          f"recorded rather than a field named after nothing")
    else:
        label = _str(ctx.get("query_label"), 160) or f"the query “{qlabel}”"
        r.add(ctx["topic"], f"github.total_count[{qlabel}]", int(total), "repositories",
              f"GitHub Search reports {int(total):,} repositories matching {label}.",
              path="total_count", tags=["github", "search", qlabel])
    items = payload.get("items")
    if not isinstance(items, list):
        r.problems.append("github_search: items is not a list")
        return r
    if payload.get("incomplete_results") is True:
        r.problems.append("github_search: incomplete_results=true — the index was still computing")
    for i, it in enumerate(items[:25]):
        if not isinstance(it, dict):
            continue
        full = _str(it.get("full_name"), 120)
        if not full:
            continue
        raw_stars = _num(it.get("stargazers_count"))
        raw_forks = _num(it.get("forks_count"))
        stars = raw_stars if raw_stars is not None else 0.0
        forks = raw_forks if raw_forks is not None else 0.0
        if raw_stars is None or raw_forks is None:
            # Do NOT silently default to 0.  That is exactly what published every
            # repository as having "0 stars" once, when a seed projection used
            # shortened keys the adapter could not find.  Report the shape and
            # withhold the affected figure entirely.
            r.problems.append(
                f"github_search: items[{i}] ({full}) is missing "
                f"{'stargazers_count' if raw_stars is None else ''}"
                f"{'/' if raw_stars is None and raw_forks is None else ''}"
                f"{'forks_count' if raw_forks is None else ''}; "
                f"no star/fork figure was recorded for it rather than a 0")
            continue
        slug = "repo:" + full.lower()
        ents = [slug] + ["tag:" + _str(t, 40).lower() for t in (it.get("topics") or [])[:6]]
        # key the field by repository name, NOT by position in the result list:
        # index-based names collided across queries and put five different
        # repositories' star counts under one field name.
        key = full.lower()
        for fname, val, unit, txt, path in [
            ("stars", int(stars), "stars", f"{full} has {int(stars):,} stars.",
             f"items[{i}].stargazers_count"),
            ("forks", int(forks), "forks", f"{full} has {int(forks):,} forks.",
             f"items[{i}].forks_count"),
            ("created", _str(it.get("created_at"), 40), "iso8601",
             f"{full} was created {it.get('created_at')}.", f"items[{i}].created_at"),
        ]:
            r.add(ctx["topic"], f"github.repo[{key}].{fname}", val, unit, txt, path=path,
                  tags=["github", "repo", full], entities=ents)
        r.ent(slug, full, float(stars), it.get("html_url") or f"https://github.com/{full}")
        for tg in (it.get("topics") or [])[:6]:
            r.ent("tag:" + _str(tg, 40).lower(), _str(tg, 40), float(stars) / 4.0,
                  f"https://github.com/topics/{_str(tg, 40)}")
    return r


def gh_repos(payload: Any, ctx: Dict[str, Any]) -> ExtractResult:
    r = ExtractResult()
    if not isinstance(payload, list):
        r.problems.append("github_repos: payload is not a JSON array")
        return r
    r.add(ctx["topic"], "owner.public_repos", len(payload), "repositories",
          f"The account {ctx.get('owner','buffedlizard55-lab')} publishes {len(payload)} "
          f"public repositories.", path="len(payload)", tags=["owner", "corpus"])
    pages = sum(1 for x in payload if isinstance(x, dict) and x.get("has_pages"))
    r.add(ctx["topic"], "owner.pages_repos", pages, "repositories",
          f"{pages} of those repositories publish a GitHub Pages site.",
          path="count(has_pages)", tags=["owner", "corpus"])
    kb = sum(_num(x.get("size")) or 0 for x in payload if isinstance(x, dict))
    r.add(ctx["topic"], "owner.total_kb", int(kb), "KiB",
          f"Combined repository size is {int(kb):,} KiB.", path="sum(size)",
          tags=["owner", "corpus"])
    return r


def gh_repo_detail(payload: Any, ctx: Dict[str, Any]) -> ExtractResult:
    """``GET /repos/{owner}/{repo}`` — one repository, the fields search omits.

    Counts are keyed by the repository name the payload reports (``full_name``),
    never by position, and a missing field is a shape problem rather than a 0: the
    failure that once published "0 stars" for every repository is always one shape
    change away.  A field that is genuinely present and genuinely 0 is recorded as
    the 0 it is — a real repository can have no stars.
    """
    r = ExtractResult()
    if not isinstance(payload, dict):
        r.problems.append("github_repo: payload is not a JSON object")
        return r
    full = _str(payload.get("full_name"), 120)
    if not full:
        r.problems.append("github_repo: payload has no full_name, so the counts "
                          "cannot be attributed to a repository; nothing was recorded")
        return r
    declared = _str(ctx.get("repo"), 120)
    if declared and declared.lower() != full.lower():
        # The payload names the subject; the task names what it meant to read.  If
        # they disagree, one of them is wrong and publishing either reading would be
        # a claim about a repository that was not the one asked for.  This is the
        # same class of defect as the retracted lowercased-Wikipedia-title claims.
        r.problems.append(f"github_repo: the task asked for {declared} but the payload "
                          f"describes {full}; the two disagree, so no claim was "
                          f"recorded from this read")
        return r
    key = full.lower()
    ents = ["repo:" + key]
    tags = ["github", "repo", full]
    # Discovery weight only; nothing in the sentence reads it.  An unknown star
    # count leaves the weight at 1.0 rather than at an invented 0.
    stars_value: Optional[float] = None
    # The endpoint is in the sentence on purpose: this read and the Search API
    # publish the same stars fields, and a reader comparing them should be able to
    # see which endpoint said which.
    api = "per the GitHub Repositories API"
    numeric = [
        ("stars", "stargazers_count", "stars", f"{full} has {{v:,}} stars, {api}."),
        ("forks", "forks_count", "forks", f"{full} has {{v:,}} forks, {api}."),
        ("open_issues", "open_issues_count", "open issues",
         f"{full} has {{v:,}} open issues, {api}."),
        ("watchers", "subscribers_count", "watching users",
         f"{full} has {{v:,}} watching users, {api}."),
        ("size_kb", "size", "KiB", f"The repository {full} is {{v:,}} KiB, {api}."),
    ]
    for fname, path, unit, template in numeric:
        if path not in payload:
            r.problems.append(f"github_repo: payload for {full} has no {path}; no "
                              f"figure was recorded for it rather than a 0")
            continue
        v = _num(payload.get(path))
        if v is None:
            r.problems.append(f"github_repo: {path} for {full} is not numeric "
                              f"({payload.get(path)!r}); no figure was recorded")
            continue
        if fname == "stars":
            stars_value = float(v)
        r.add(ctx["topic"], f"github.repo[{key}].{fname}", int(v), unit,
              template.format(v=int(v)), path=path, tags=tags, entities=ents)
    lang = payload.get("language")
    if lang in (None, ""):
        # Observed absence, reported as absence.  GitHub is the authority on how it
        # classifies a repository, so "no primary language" is a fact about the repo
        # and not a hole in our reading.
        r.add(ctx["topic"], f"github.repo[{key}].language", "", "language",
              f"GitHub reports no primary language for {full}.", path="language",
              tags=tags, entities=ents)
    else:
        r.add(ctx["topic"], f"github.repo[{key}].language", _str(lang, 60), "language",
              f"GitHub classifies {full} primarily as {_str(lang, 60)}.",
              path="language", tags=tags, entities=ents)
    pushed = _str(payload.get("pushed_at"), 40)
    if pushed:
        r.add(ctx["topic"], f"github.repo[{key}].pushed", pushed, "iso8601",
              f"The most recent push to {full} was at {pushed}, per the GitHub "
              f"Repositories API.", path="pushed_at", tags=tags, entities=ents)
    if "archived" in payload:
        # Not a boolean field: "active" and "archived" are the two states a
        # repository can be in, and that is a categorical series the competition can
        # ask a knowable question about ("will the state differ next cycle?").
        state = "archived" if payload.get("archived") else "active"
        r.add(ctx["topic"], f"github.repo[{key}].state", state, "state",
              f"The GitHub Repositories API reports {full} as {state}.",
              path="archived", tags=tags, entities=ents)
    r.ent("repo:" + key, full, 1.0 if stars_value is None else stars_value,
          _str(payload.get("html_url"), 200) or f"https://github.com/{full}")
    return r


def repo_from_html_url(html_url: str) -> str:
    """``https://github.com/owner/name/...`` → ``owner/name``, else ``""``."""
    s = _str(html_url, 200)
    if not s.startswith("https://") and not s.startswith("http://"):
        return ""
    parts = [p for p in s.split("/") if p]
    # ["https:", "github.com", "owner", "name", ...]
    return f"{parts[2]}/{parts[3]}" if len(parts) >= 4 else ""


def gh_releases(payload: Any, ctx: Dict[str, Any]) -> ExtractResult:
    """``GET /repos/{owner}/{repo}/releases?per_page=1`` — the newest release.

    GitHub returns releases newest-first, so element 0 is the one that answers
    "when did this project last ship, and what was it called?".  An empty list is
    not an error and not an absence of data: it is proof that the repository
    publishes no release, which is recorded as a ``negative`` claim carrying the
    same field name as a real tag.  That keeps one continuous series per repository
    — "" until the first release, then the tag — so a first release is visible as a
    change rather than as the series appearing from nowhere.
    """
    r = ExtractResult()
    if not isinstance(payload, list):
        r.problems.append("github_releases: payload is not a JSON array")
        return r
    declared = _str(ctx.get("repo"), 120)
    first = payload[0] if payload and isinstance(payload[0], dict) else {}
    stated = (repo_from_html_url(_str(first.get("html_url"), 200))
              or repo_from_html_url(_str(first.get("url"), 200)))
    if payload and not first:
        r.problems.append("github_releases: the first record in the array is not an "
                          "object, so no release could be read from this payload")
        return r
    if stated and declared and stated.lower() != declared.lower():
        r.problems.append(f"github_releases: the task asked for {declared} but the "
                          f"payload describes {stated}; the two disagree, so no claim "
                          f"was recorded from this read")
        return r
    full = stated or declared
    if not full:
        r.problems.append("github_releases: the task did not record which repository "
                          "was asked about and the payload does not name it; the "
                          "release cannot be attributed, so nothing was recorded")
        return r
    slug = "repo:" + full.lower()
    field = f"github.release[{full.lower()}].tag"
    if not payload:
        r.add(ctx["topic"], field, "", "tag",
              f"The GitHub Releases API lists no release for {full}.",
              kind="negative", path="[]", tags=["github", "releases", full], entities=[slug])
        return r
    tag = _str(first.get("tag_name"), 80)
    if not tag:
        r.problems.append(f"github_releases: the newest record for {full} has no "
                          f"tag_name; no release fact was recorded")
        return r
    published = _str(first.get("published_at"), 30)
    flags = ", ".join(x for x in ("prerelease" if first.get("prerelease") else "",
                                  "draft" if first.get("draft") else "") if x)
    r.add(ctx["topic"], field, tag, "tag",
          f"The newest release of {full} is tagged {tag}"
          + (f", published {published}" if published else "")
          + (f" ({flags})." if flags else "."),
          path="[0].tag_name", tags=["github", "releases", full], entities=[slug])
    if published:
        r.add(ctx["topic"], f"github.release[{full.lower()}].published", published,
              "iso8601",
              f"The GitHub Releases API dates release {tag} of {full} at {published}.",
              path="[0].published_at", tags=["github", "releases", full], entities=[slug])
    r.ent(slug, full, 1.0, _str(first.get("html_url"), 200) or f"https://github.com/{full}")
    return r


def pypi_json(payload: Any, ctx: Dict[str, Any]) -> ExtractResult:
    r = ExtractResult()
    info = (payload or {}).get("info") if isinstance(payload, dict) else None
    if not isinstance(info, dict):
        r.problems.append("pypi_json: info object missing")
        return r
    pkg = _str(info.get("name"), 80)
    ver = _str(info.get("version"), 40)
    rel = (payload or {}).get("releases") or {}
    r.add(ctx["topic"], f"pypi[{pkg}].version", ver, "version",
          f"PyPI reports {pkg} at version {ver}.", path="info.version",
          tags=["pypi", pkg])
    r.add(ctx["topic"], f"pypi[{pkg}].releases", len(rel), "releases",
          f"{pkg} has {len(rel)} published releases on PyPI.", path="len(releases)",
          tags=["pypi", pkg])
    r.ent("pkg:" + pkg.lower(), f"{pkg} (PyPI)", 1.0, f"https://pypi.org/project/{pkg}/")
    return r


def npm_latest(payload: Any, ctx: Dict[str, Any]) -> ExtractResult:
    r = ExtractResult()
    if not isinstance(payload, dict):
        r.problems.append("npm_latest: payload is not a JSON object")
        return r
    pkg = _str(payload.get("name"), 80)
    ver = _str(payload.get("version"), 40)
    if not pkg or not ver:
        r.problems.append("npm_latest: name or version missing")
        return r
    r.add(ctx["topic"], f"npm[{pkg}].version", ver, "version",
          f"The npm registry reports {pkg} at version {ver}.", path="version",
          tags=["npm", pkg])
    r.ent("pkg:" + pkg.lower(), f"{pkg} (npm)", 1.0, f"https://www.npmjs.com/package/{pkg}")
    return r


# --------------------------------------------------------------------------- #
# Attention
# --------------------------------------------------------------------------- #
def wiki_pageviews(payload: Any, ctx: Dict[str, Any]) -> ExtractResult:
    r = ExtractResult()
    items = (payload or {}).get("items") if isinstance(payload, dict) else None
    if not isinstance(items, list) or not items:
        r.problems.append("wikimedia_pageviews: items missing or empty")
        return r
    art = _str(items[0].get("article"), 120)
    for it in items:
        ts = _str(it.get("timestamp"), 20)
        day = f"{ts[0:4]}-{ts[4:6]}-{ts[6:8]}" if len(ts) >= 8 else ts
        v = _num(it.get("views"))
        if v is None:
            continue
        r.add(ctx["topic"], f"wiki[{art}].views.{day}", int(v), "views/day",
              f"Wikipedia article “{art}” received {int(v):,} views from users on {day}.",
              path=f"items[{day}].views", tags=["wikipedia", "attention", art],
              entities=["wiki:" + art.lower()])
    r.ent("wiki:" + art.lower(), art, float(len(items)),
          f"https://en.wikipedia.org/wiki/{art}")
    return r


def hn_top(payload: Any, ctx: Dict[str, Any]) -> ExtractResult:
    r = ExtractResult()
    if not isinstance(payload, list):
        r.problems.append("hn_firebase: payload is not a JSON array")
        return r
    r.add(ctx["topic"], "hn.topstories.length", len(payload), "stories",
          f"The Hacker News topstories list currently holds {len(payload)} story ids.",
          path="len(payload)", tags=["hn", "attention"])
    for i, sid in enumerate(payload[:10]):
        n = _num(sid)
        if n is None:
            continue
        r.add(ctx["topic"], f"hn.top[{i}].id", int(n), "story id",
              f"Story id {int(n)} is at rank {i + 1} on Hacker News.",
              path=f"[{i}]", tags=["hn", "attention"])
    return r


# --------------------------------------------------------------------------- #
# Regulatory / civic
# --------------------------------------------------------------------------- #
def federal_register(payload: Any, ctx: Dict[str, Any]) -> ExtractResult:
    r = ExtractResult()
    if not isinstance(payload, dict):
        r.problems.append("federal_register: payload is not a JSON object")
        return r
    count = _num(payload.get("count"))
    # The API's own ``description`` for a term query is the phrase
    # "Documents matching 'artificial intelligence'".  An earlier template
    # interpolated that phrase after the word "matching" and published
    # "holds 1,573 documents matching Documents matching 'artificial intelligence'."
    # 102 rows in the ledger carry that sentence (80 by cycle 14).  The sentence is now built from
    # the term this project actually asked for, so it cannot double a word, and the
    # API's own phrasing is recorded in the field's tags instead of being spliced
    # into a sentence it was not written for.
    term = _str(ctx.get("term"), 160)
    key = term or "newest"
    if count is None:
        r.problems.append("federal_register: count missing")
    else:
        # ``description`` is the API's own phrasing for the query it answered.  It is
        # recorded as a tag (where a reader can compare it with what was asked for)
        # and never spliced into the sentence — that splice is what published
        # "holds 1,573 documents matching Documents matching 'artificial
        # intelligence'" in 102 rows.
        described = _str(payload.get("description"), 160)
        if term:
            sentence = (f"The U.S. Federal Register holds {int(count):,} documents "
                        f"matching “{term}”.")
        else:
            # An unfiltered count: say what the number covers, and let the API's own
            # description of the query stand next to it rather than inside it.
            sentence = f"The U.S. Federal Register holds {int(count):,} documents in total."
            if described:
                sentence += f" The API describes this query as “{described}”."
        r.add(ctx["topic"], f"fedreg.documents[{key}]", int(count), "documents",
              sentence, path="count",
              tags=["federal-register", "regulatory"] + ([term] if term else []))
    res = payload.get("results")
    if not isinstance(res, list):
        r.problems.append("federal_register: results is not a list")
        return r
    for i, d in enumerate(res[:10]):
        if not isinstance(d, dict):
            continue
        num = _str(d.get("document_number"), 30)
        pub = _str(d.get("publication_date"), 20)
        title = _str(d.get("title"), 220)
        if not num:
            continue
        agencies = [_str(a.get("name"), 90) for a in (d.get("agencies") or []) if isinstance(a, dict)]
        agency_slugs = ["agency:" + re.sub(r"[^a-z0-9]+", "-", a.lower()).strip("-")
                        for a in agencies if a]
        doc_slug = "frdoc:" + num
        ents = [doc_slug] + agency_slugs
        r.add(ctx["topic"], f"fedreg.doc[{i}].published", pub, "date",
              f"Federal Register document {num} (“{title}”) was published {pub}.",
              path=f"results[{i}].publication_date",
              tags=["federal-register", "regulatory", num], entities=ents)
        r.add(ctx["topic"], f"fedreg.doc[{i}].agency", agencies[0] if agencies else "",
              "agency",
              f"Document {num} was issued by {agencies[0] if agencies else 'an unnamed agency'}.",
              path=f"results[{i}].agencies[0].name",
              tags=["federal-register", "regulatory", num], entities=ents)
        r.ent(doc_slug, title, 2.0,
              d.get("html_url") or f"https://www.federalregister.gov/documents/search?term={num}")
        for a, slug in zip(agencies, agency_slugs):
            r.ent(slug, a, 1.0, "https://www.federalregister.gov/agencies")
    return r


def _window_id(ctx: Dict[str, Any]) -> str:
    """The window a count covers, as a field-key component.

    The rolling weekly count and the probe's open-ended count are different
    measurements, so they must not share a field name: mixing them would put a
    7-day count and a count-from-a-fixed-date-until-now into one series and make
    every comparison between them meaningless.
    """
    window = _str(ctx.get("window"), 40)
    if window:
        return window
    start = _str(ctx.get("starttime"), 20)
    end = _str(ctx.get("endtime"), 20)
    if start and end:
        return f"{start}..{end}"
    if start:
        return f"from-{start}"
    return "unspecified"


def _window_phrase(ctx: Dict[str, Any]) -> str:
    """Describe the window a count was taken over, from the query that took it.

    The window used to be a hand-written label in the task ("the configured
    window") that named nothing, while the URL carried the real dates.  A count is
    only meaningful with the window it covers, so the phrase is built from the
    parameters of the read itself.
    """
    start = _str(ctx.get("starttime"), 20)
    end = _str(ctx.get("endtime"), 20)
    mag = ctx.get("minmagnitude")
    if start and end:
        where = f"between {start} and {end}"
    elif start:
        where = f"from {start} to the time of this read"
    elif end:
        where = f"up to {end}"
    else:
        # No dates in the query at all.  Fall back to the plan's own window label if
        # the task carried one, and otherwise say plainly that the window is not
        # pinned down rather than inventing one.
        label = _str(ctx.get("window_label"), 80)
        where = f"in the window {label}" if label else "over the window this query leaves open"
    if mag is not None:
        where += f", at magnitude {mag} and above"
    return where


def usgs_count(payload: Any, ctx: Dict[str, Any]) -> ExtractResult:
    r = ExtractResult()
    if not isinstance(payload, dict) or "count" not in payload:
        r.problems.append("usgs_fdsn: count field missing")
        return r
    c = _num(payload.get("count"))
    mx = _num(payload.get("maxAllowed"))
    if c is None:
        r.problems.append("usgs_fdsn: count is not numeric")
        return r
    r.add(ctx["topic"], f"usgs.events[{_window_id(ctx)}]", int(c), "events",
          f"USGS counts {int(c)} earthquakes {_window_phrase(ctx)}.", path="count",
          tags=["usgs", "geohazard", _window_id(ctx)])
    if mx is not None:
        r.add(ctx["topic"], "usgs.maxAllowed", int(mx), "events",
              f"The USGS count endpoint caps its reply at {int(mx)} events.",
              path="maxAllowed", tags=["usgs", "geohazard"])
        if c >= mx:
            r.problems.append(f"usgs_fdsn: count {int(c)} hit the maxAllowed cap {int(mx)}; the true number is higher")
    return r


# --------------------------------------------------------------------------- #
# Scholarly
# --------------------------------------------------------------------------- #
def arxiv_atom(payload: Any, ctx: Dict[str, Any]) -> ExtractResult:
    r = ExtractResult()
    if not isinstance(payload, (bytes, str)):
        r.problems.append("arxiv: payload was not parsed as text")
        return r
    try:
        root = ET.fromstring(payload if isinstance(payload, bytes) else payload.encode())
    except ET.ParseError as e:
        r.problems.append(f"arxiv: Atom parse error: {e}")
        return r
    entries = root.findall(f"{ATOM}entry")
    total_el = root.find("{http://a9.com/-/spec/opensearch/1.1/}totalResults")
    if total_el is not None and total_el.text:
        n = _num(total_el.text)
        if n is not None:
            r.add(ctx["topic"], "arxiv.totalResults", int(n), "papers",
                  f"arXiv reports {int(n):,} results for {ctx.get('query_label','the query')}.",
                  path="opensearch:totalResults", tags=["arxiv", "research"])
    if not entries:
        r.problems.append("arxiv: feed contained no entries")
    for i, e in enumerate(entries[:10]):
        title = _str((e.findtext(f"{ATOM}title") or "").strip(), 220)
        pub = _str(e.findtext(f"{ATOM}published"), 30)
        aid = _str(e.findtext(f"{ATOM}id"), 160)
        if not title:
            continue
        r.add(ctx["topic"], f"arxiv.entry[{i}].published", pub, "iso8601",
              f"arXiv lists “{title}” published {pub}.",
              path=f"entry[{i}].published", tags=["arxiv", "research"])
        slug = "paper:" + re.sub(r"[^a-z0-9]+", "-", title.lower())[:70].strip("-")
        r.ent(slug, title, 1.5, aid or "https://arxiv.org/")
    return r


def pubmed_esearch(payload: Any, ctx: Dict[str, Any]) -> ExtractResult:
    r = ExtractResult()
    res = (payload or {}).get("esearchresult") if isinstance(payload, dict) else None
    if not isinstance(res, dict):
        r.problems.append("pubmed: esearchresult missing")
        return r
    c = _num(res.get("count"))
    term = _str(res.get("querytranslation"), 200)
    if c is None:
        r.problems.append("pubmed: count missing")
        return r
    r.add(ctx["topic"], f"pubmed.hits[{ctx.get('term','*')}]", int(c), "records",
          f"PubMed holds {int(c):,} records for {term or 'the query'}.",
          path="esearchresult.count", tags=["pubmed", "clinical"])
    return r


def clinicaltrials(payload: Any, ctx: Dict[str, Any]) -> ExtractResult:
    r = ExtractResult()
    if not isinstance(payload, dict):
        r.problems.append("clinicaltrials: payload is not a JSON object")
        return r
    total = _num(payload.get("totalCount"))
    if total is not None:
        r.add(ctx["topic"], "clinicaltrials.totalCount", int(total), "studies",
              f"ClinicalTrials.gov returns {int(total):,} studies for the configured query.",
              path="totalCount", tags=["clinicaltrials", "clinical"])
    studies = payload.get("studies")
    if not isinstance(studies, list):
        r.problems.append("clinicaltrials: studies is not a list")
        return r
    for i, s in enumerate(studies[:10]):
        proto = (s or {}).get("protocolSection") or {}
        ident = proto.get("identificationModule") or {}
        nct = _str(ident.get("nctId"), 20)
        title = _str(ident.get("briefTitle"), 200)
        if not nct:
            continue
        status = _str(((proto.get("statusModule") or {}).get("overallStatus")), 60)
        r.add(ctx["topic"], f"clinicaltrials.study[{i}].status", status, "status",
              f"ClinicalTrials.gov study {nct} (“{title}”) is {status or 'of unreported status'}.",
              path=f"studies[{i}].protocolSection.statusModule.overallStatus",
              tags=["clinicaltrials", "clinical"])
        r.ent("trial:" + nct.lower(), title or nct, 1.5, f"https://clinicaltrials.gov/study/{nct}")
    return r


def openalex(payload: Any, ctx: Dict[str, Any]) -> ExtractResult:
    r = ExtractResult()
    meta = (payload or {}).get("meta") if isinstance(payload, dict) else None
    if not isinstance(meta, dict):
        r.problems.append("openalex: meta missing")
        return r
    c = _num(meta.get("count"))
    if c is not None:
        r.add(ctx["topic"], "openalex.count", int(c), "works",
              f"OpenAlex indexes {int(c):,} works matching {ctx.get('query_label','the query')}.",
              path="meta.count", tags=["openalex", "research"])
    for i, w in enumerate((payload or {}).get("results") or []):
        title = _str((w or {}).get("title"), 200)
        date = _str((w or {}).get("publication_date"), 20)
        if not title:
            continue
        r.add(ctx["topic"], f"openalex.work[{i}].date", date, "date",
              f"OpenAlex lists “{title}” with publication date {date}.",
              path=f"results[{i}].publication_date", tags=["openalex", "research"])
        r.ent("work:" + re.sub(r"[^a-z0-9]+", "-", title.lower())[:70].strip("-"),
              title, 1.2, _str((w or {}).get("id"), 200) or "https://openalex.org/")
    return r


def crossref(payload: Any, ctx: Dict[str, Any]) -> ExtractResult:
    r = ExtractResult()
    msg = (payload or {}).get("message") if isinstance(payload, dict) else None
    if not isinstance(msg, dict):
        r.problems.append("crossref: message missing")
        return r
    t = _num(msg.get("total-results"))
    if t is not None:
        r.add(ctx["topic"], "crossref.totalResults", int(t), "works",
              f"Crossref reports {int(t):,} registered works for the configured query.",
              path="message.total-results", tags=["crossref", "research"])
    return r


def europepmc(payload: Any, ctx: Dict[str, Any]) -> ExtractResult:
    r = ExtractResult()
    c = _num((payload or {}).get("hitCount")) if isinstance(payload, dict) else None
    if c is None:
        r.problems.append("europepmc: hitCount missing")
        return r
    r.add(ctx["topic"], "europepmc.hitCount", int(c), "records",
          f"Europe PMC returns {int(c):,} records for the configured query.",
          path="hitCount", tags=["europepmc", "clinical"])
    return r


def stackexchange(payload: Any, ctx: Dict[str, Any]) -> ExtractResult:
    r = ExtractResult()
    if not isinstance(payload, dict):
        r.problems.append("stackexchange: payload is not a JSON object")
        return r
    items = payload.get("items")
    quota = _num(payload.get("quota_remaining"))
    if quota is not None:
        r.add(ctx["topic"], "stackexchange.quota_remaining", int(quota), "requests",
              f"Stack Exchange reports {int(quota)} requests remaining on this IP's quota.",
              path="quota_remaining", tags=["stackexchange"])
        if quota < 50:
            r.problems.append(f"stackexchange: quota_remaining={int(quota)} is low")
    if not isinstance(items, list):
        r.problems.append("stackexchange: items is not a list")
        return r
    for i, q in enumerate(items[:10]):
        title = _str((q or {}).get("title"), 200)
        score = _num((q or {}).get("score"))
        if not title:
            continue
        r.add(ctx["topic"], f"stackexchange.q[{i}].score", int(score or 0), "score",
              f"Stack Overflow question “{title}” scores {int(score or 0)}.",
              path=f"items[{i}].score", tags=["stackexchange"])
    return r


def huggingface(payload: Any, ctx: Dict[str, Any]) -> ExtractResult:
    r = ExtractResult()
    if not isinstance(payload, list):
        r.problems.append("huggingface: payload is not a JSON array")
        return r
    r.add(ctx["topic"], "huggingface.models_returned", len(payload), "models",
          f"The Hub API returned {len(payload)} trending model records.",
          path="len(payload)", tags=["huggingface", "research"])
    for i, m in enumerate(payload[:15]):
        mid = _str((m or {}).get("modelId") or (m or {}).get("id"), 120)
        dl = _num((m or {}).get("downloads"))
        if not mid:
            continue
        if dl is not None:
            r.add(ctx["topic"], f"huggingface.model[{i}].downloads", int(dl), "downloads/30d",
                  f"Hub model {mid} records {int(dl):,} downloads in the last 30 days.",
                  path=f"[{i}].downloads", tags=["huggingface", "research"])
        r.ent("model:" + mid.lower(), mid, float(dl or 1) / 1000.0, f"https://huggingface.co/{mid}")
    return r


# --------------------------------------------------------------------------- #
# Macro / geo / local
# --------------------------------------------------------------------------- #
def nws_alerts(payload: Any, ctx: Dict[str, Any]) -> ExtractResult:
    r = ExtractResult()
    feats = (payload or {}).get("features") if isinstance(payload, dict) else None
    if not isinstance(feats, list):
        r.problems.append("nws_alerts: features is not a list")
        return r
    r.add(ctx["topic"], f"nws.alerts[{ctx.get('area','US')}]", len(feats), "active alerts",
          f"The National Weather Service lists {len(feats)} active alerts for "
          f"{ctx.get('area','the configured area')}.", path="len(features)",
          tags=["nws", "sf-local"])
    for i, f in enumerate(feats[:10]):
        props = (f or {}).get("properties") or {}
        ev = _str(props.get("event"), 90)
        sev = _str(props.get("severity"), 40)
        if not ev:
            continue
        r.add(ctx["topic"], f"nws.alert[{i}].event", ev, "event",
              f"Active NWS alert #{i + 1}: {ev} (severity {sev or 'unreported'}).",
              path=f"features[{i}].properties.event", tags=["nws", "sf-local"])
    return r


def worldbank(payload: Any, ctx: Dict[str, Any]) -> ExtractResult:
    r = ExtractResult()
    if not isinstance(payload, list) or len(payload) < 2 or not isinstance(payload[1], list):
        r.problems.append("worldbank: expected [meta, rows] JSON array")
        return r
    rows = [x for x in payload[1] if isinstance(x, dict) and x.get("value") is not None]
    if not rows:
        r.problems.append("worldbank: no non-null observations in the page")
        return r
    latest = max(rows, key=lambda x: _str(x.get("date"), 10))
    v = _num(latest.get("value"))
    if v is None:
        r.problems.append("worldbank: latest value is not numeric")
        return r
    ind_obj = latest.get("indicator") if isinstance(latest.get("indicator"), dict) else {}
    ind = _str(ind_obj.get("value"), 120)
    # The indicator id builds the field name.  It used to come from the task
    # context only, so a read whose context did not carry it published the field
    # ``worldbank[?].latest`` and the sentence "The World Bank reports GDP ... "
    # under a placeholder.  9 rows in the ledger carry that (7 by cycle 14).  The payload names the
    # indicator itself; use it, and refuse the fact if neither source names it.
    code = _str(ind_obj.get("id"), 60) or _str(ctx.get("indicator"), 60)
    if not code:
        r.problems.append("worldbank: neither the payload's indicator.id nor the task "
                          "context names the indicator; no fact was recorded rather "
                          "than a field named after a placeholder")
        return r
    r.add(ctx["topic"], f"worldbank[{code}].latest", v, "units",
          f"The World Bank reports {ind or code} at {v:,.0f} for {latest.get('date')}.",
          path="1[latest].value", tags=["worldbank", "macro", code])
    return r


def ecb_sdmx(payload: Any, ctx: Dict[str, Any]) -> ExtractResult:
    r = ExtractResult()
    try:
        ds = payload["data"]["dataSets"][0]
        series = ds.get("series") or {}
        obs = {}
        for s in series.values():
            obs.update(s.get("observations") or {})
        if not obs:
            obs = ds.get("observations") or {}
        if not obs:
            r.problems.append("ecb_sdmx: no observations in dataSets[0]")
            return r
        key = sorted(obs.keys())[-1]
        vals = obs[key]
        v = _num(vals[0]) if isinstance(vals, list) and vals else None
        if v is None:
            r.problems.append("ecb_sdmx: observation value is not numeric")
            return r
        r.add(ctx["topic"], f"ecb[{ctx.get('flow','EXR')}].latest", v, "rate",
              f"The ECB publishes {ctx.get('label','the configured exchange-rate series')} at {v}.",
              path=f"data.dataSets[0].observations[{key}][0]", tags=["ecb", "macro"])
    except (KeyError, IndexError, TypeError) as e:
        r.problems.append(f"ecb_sdmx: unexpected jsondata shape ({type(e).__name__}: {e})")
    return r


def frankfurter(payload: Any, ctx: Dict[str, Any]) -> ExtractResult:
    r = ExtractResult()
    rates = (payload or {}).get("rates") if isinstance(payload, dict) else None
    date = _str((payload or {}).get("date"), 20)
    if not isinstance(rates, dict) or not rates:
        r.problems.append("frankfurter: rates missing")
        return r
    for cur, val in list(rates.items())[:12]:
        v = _num(val)
        if v is None:
            continue
        r.add(ctx["topic"], f"fx[{cur}].vsUSD", v, f"{cur} per USD",
              f"Frankfurter (a third-party mirror of ECB reference rates) reports "
              f"{v} {cur} per USD for {date}.  Not an official ECB endpoint.",
              path=f"rates.{cur}", tags=["fx", "macro", "third-party"])
    return r


def census_acs(payload: Any, ctx: Dict[str, Any]) -> ExtractResult:
    r = ExtractResult()
    if not isinstance(payload, list) or len(payload) < 2:
        r.problems.append("census_acs: expected [header, ...rows] JSON array")
        return r
    header = payload[0] if isinstance(payload[0], list) else []
    for i, row in enumerate(payload[1:6]):
        if not isinstance(row, list) or len(row) < 2:
            continue
        v = _num(row[1])
        if v is None:
            continue
        r.add(ctx["topic"], f"census.row[{i}].value", int(v), "count",
              f"U.S. Census ACS reports {header[1] if len(header) > 1 else 'the variable'} "
              f"= {int(v):,} for {row[0]}.", path=f"[{i+1}][1]", tags=["census", "sf-local"])
    return r


def bls(payload: Any, ctx: Dict[str, Any]) -> ExtractResult:
    r = ExtractResult()
    if not isinstance(payload, dict) or payload.get("status") != "REQUEST_SUCCEEDED":
        r.problems.append(f"bls: status={_str((payload or {}).get('status'),40)!r} "
                          f"{_str((payload or {}).get('message'),200)!r}")
        return r
    res = payload.get("Results") or {}
    series = (res.get("series") or [{}])[0]
    data = series.get("data") or []
    if not data:
        r.problems.append("bls: no data rows returned")
        return r
    d0 = data[0] if isinstance(data[0], dict) else {}
    v = _num(d0.get("value"))
    if v is None:
        r.problems.append("bls: latest value is not numeric")
        return r
    # The payload names the series (seriesID); the task context also does.  The
    # field key and the sentence used the context alone, so a read without it
    # published ``bls[?].latest`` and the sentence "BLS reports series ? at ..."
    # — a literal placeholder in a published claim.  9 rows in the ledger carry it.
    sid = _str(series.get("seriesID"), 40) or _str(ctx.get("series"), 40)
    if not sid:
        r.problems.append("bls: neither the payload's seriesID nor the task context "
                          "names the series; no fact was recorded rather than a field "
                          "named after a placeholder")
        return r
    # A missing period is described in words, never with a "?": the same class of
    # defect as the placeholder field name, one field further along the sentence.
    period = " ".join(x for x in (_str(d0.get("periodName"), 20),
                                  _str(d0.get("year"), 8)) if x)
    when = f"for {period}" if period else "for an unstated period"
    r.add(ctx["topic"], f"bls[{sid}].latest", v, "index",
          f"BLS reports series {sid} at {v} {when}.",
          path="Results.series[0].data[0].value", tags=["bls", "macro", sid])
    if not period:
        r.problems.append("bls: the returned observation carries no periodName/year, "
                          "so the figure is published without a period rather than "
                          "with a placeholder")
    return r


def sec_submissions(payload: Any, ctx: Dict[str, Any]) -> ExtractResult:
    r = ExtractResult()
    if not isinstance(payload, dict) or "cik" not in payload:
        r.problems.append("sec_edgar: submissions document missing cik")
        return r
    name = _str(payload.get("name"), 160)
    cik = _str(payload.get("cik"), 20)
    recent = payload.get("filings", {}).get("recent") or {}
    forms = recent.get("form") or []
    r.add(ctx["topic"], f"sec[{cik}].name", name, "registrant",
          f"SEC EDGAR registrant CIK {cik} is {name}.", path="name",
          tags=["sec", "filings"])
    r.add(ctx["topic"], f"sec[{cik}].recent_filings", len(forms), "filings",
          f"EDGAR's most recent filings page for {name} lists {len(forms)} filings.",
          path="len(filings.recent.form)", tags=["sec", "filings"])
    r.ent("registrant:" + re.sub(r"[^a-z0-9]+", "-", name.lower())[:60],
          name, 1.0, f"https://www.sec.gov/cgi-bin/browse-edgar?CIK={cik}")
    return r


def nominatim(payload: Any, ctx: Dict[str, Any]) -> ExtractResult:
    r = ExtractResult()
    if not isinstance(payload, list):
        r.problems.append("nominatim: payload is not a JSON array")
        return r
    # The place name is the whole content of the answer: three results for "Seoul"
    # is a different fact from three results for "Paris".  It used to be read from
    # the task context only, with a fallback sentence for when it was missing, so
    # 9 rows in the ledger say "Nominatim returns 1 place result(s) for the query."
    # with the field ``nominatim.results[?]``.  A read that cannot be attributed to
    # a place is refused rather than published under a placeholder.
    q = _str(ctx.get("query"), 120)
    if not q:
        r.problems.append("nominatim: the task did not record which place was asked "
                          "for, so the result cannot be attributed; no fact was "
                          "recorded")
        return r
    r.add(ctx["topic"], f"nominatim.results[{q}]", len(payload), "results",
          f"Nominatim returns {len(payload)} place result(s) for “{q}”.",
          path="len(payload)", tags=["osm", "travel", q])
    for i, p in enumerate(payload[:3]):
        r.add(ctx["topic"], f"nominatim[{i}].display", _str((p or {}).get("display_name"), 200),
              "place", f"Nominatim resolves “{q}” to “{_str((p or {}).get('display_name'),200)}”.",
              path=f"[{i}].display_name", tags=["osm", "travel", q])
    return r


# --------------------------------------------------------------------------- #
# Sports / markets
# --------------------------------------------------------------------------- #
def kalshi_markets(payload: Any, ctx: Dict[str, Any]) -> ExtractResult:
    r = ExtractResult()
    mkts = (payload or {}).get("markets") if isinstance(payload, dict) else None
    if not isinstance(mkts, list):
        r.problems.append("kalshi_public: markets is not a list")
        return r
    r.add(ctx["topic"], "kalshi.markets_returned", len(mkts), "markets",
          f"The Kalshi public API returned {len(mkts)} market record(s) for this page.",
          path="len(markets)", tags=["kalshi", "markets"])
    for i, m in enumerate(mkts[:10]):
        tid = _str((m or {}).get("ticker"), 80)
        yes = _num((m or {}).get("yes_bid"))
        if not tid:
            continue
        if yes is not None:
            r.add(ctx["topic"], f"kalshi[{tid}].yes_bid", yes, "cents",
                  f"Kalshi market {tid} shows a YES bid of {yes} cents.",
                  path=f"markets[{i}].yes_bid", tags=["kalshi", "markets"])
    return r


# The three league feeds below are undocumented public endpoints (IRR-009): no
# operator contract, no versioning promise, no status page.  Every fact they produce
# carries the tag ``undocumented`` so the claim itself says what it rests on, rather
# than the site promising a marker that the claims do not have.
def mlb_schedule(payload: Any, ctx: Dict[str, Any]) -> ExtractResult:
    r = ExtractResult()
    dates = (payload or {}).get("dates") if isinstance(payload, dict) else None
    if not isinstance(dates, list):
        r.problems.append("mlb_statsapi: dates is not a list")
        return r
    for i, d in enumerate(dates[:3]):
        games = (d or {}).get("games") or []
        day = _str((d or {}).get("date"), 20)
        r.add(ctx["topic"], f"mlb.games[{day}]", len(games), "games",
              f"MLB's StatsAPI lists {len(games)} game(s) on {day}.",
              path=f"dates[{i}].games.length", tags=["mlb", "sports", "undocumented"])
    return r


def nhl_scoreboard(payload: Any, ctx: Dict[str, Any]) -> ExtractResult:
    r = ExtractResult()
    games = (payload or {}).get("games") if isinstance(payload, dict) else None
    if not isinstance(games, list):
        r.problems.append("nhl_web: games is not a list")
        return r
    r.add(ctx["topic"], "nhl.games_today", len(games), "games",
          f"The NHL public scoreboard lists {len(games)} game(s) for the current date.",
          path="len(games)", tags=["nhl", "sports", "undocumented"])
    return r


def nba_scoreboard(payload: Any, ctx: Dict[str, Any]) -> ExtractResult:
    r = ExtractResult()
    games = ((payload or {}).get("scoreboard") or {}).get("games") if isinstance(payload, dict) else None
    if not isinstance(games, list):
        r.problems.append("nba_cdn: scoreboard.games is not a list")
        return r
    r.add(ctx["topic"], "nba.games_today", len(games), "games",
          f"The NBA CDN scoreboard lists {len(games)} game(s) for the current date.",
          path="scoreboard.games.length", tags=["nba", "sports", "undocumented"])
    return r


ADAPTERS: Dict[str, Callable[[Any, Dict[str, Any]], ExtractResult]] = {
    "github_search": gh_search,
    "github_repos": gh_repos,
    "github_repo": gh_repo_detail,
    "github_releases": gh_releases,
    "pypi_json": pypi_json,
    "npm_registry": npm_latest,
    "wikimedia_pageviews": wiki_pageviews,
    "hn_firebase": hn_top,
    "federal_register": federal_register,
    "usgs_fdsn": usgs_count,
    "arxiv": arxiv_atom,
    "pubmed": pubmed_esearch,
    "clinicaltrials": clinicaltrials,
    "openalex": openalex,
    "crossref": crossref,
    "europepmc": europepmc,
    "stackexchange": stackexchange,
    "huggingface": huggingface,
    "nws_alerts": nws_alerts,
    "worldbank": worldbank,
    "ecb_sdmx": ecb_sdmx,
    "frankfurter": frankfurter,
    "census_acs": census_acs,
    "bls": bls,
    "sec_edgar": sec_submissions,
    "nominatim": nominatim,
    "kalshi_public": kalshi_markets,
    "mlb_statsapi": mlb_schedule,
    "nhl_web": nhl_scoreboard,
    "nba_cdn": nba_scoreboard,
}


def adapter_for(source_id: str) -> Optional[Callable[[Any, Dict[str, Any]], ExtractResult]]:
    return ADAPTERS.get(source_id)
