import json
import sys
import tempfile
import unittest
from html.parser import HTMLParser
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from news import load_news, render_news_html
from postprocess_homepage import replace_news_block


class Tags(HTMLParser):
    def __init__(self, html):
        super().__init__()
        self.tags = []
        self.feed(html)

    def handle_starttag(self, tag, attrs):
        self.tags.append((tag, dict(attrs)))


def entry(id="release", date="2026-09-17", **kwargs):
    return dict(id=id, date=date, title="Release", text="Details", **kwargs)


class NewsTests(unittest.TestCase):
    def test_newest_opens_and_matching_dates_keep_source_order(self):
        items = [entry("old", "2026-08-01"), entry("first"), entry("second")]
        tags = Tags(render_news_html(items)).tags
        disclosures = [attrs for tag, attrs in tags if tag == "details"]
        self.assertEqual([d["id"] for d in disclosures], ["news-first", "news-second", "news-old"])
        self.assertEqual(["open" in d for d in disclosures], [True, False, False])
        self.assertEqual({d["name"] for d in disclosures}, {"carwatch-news"})
        self.assertEqual(items[0]["id"], "old")

    def test_plain_text_and_attributes_are_escaped(self):
        item = entry(link={"url": "https://example.org/?a=1&b=2", "label": "<Read>"},
                     image={"src": "/img/test.png", "alt": 'A "sample" & tube'})
        item.update(title='<script>alert("x")</script>', text="A & B < C")
        html = render_news_html([item], base_path="/project")
        tags = Tags(html).tags
        self.assertNotIn("script", [tag for tag, _ in tags])
        self.assertIn("A &amp; B &lt; C", html)
        image = next(attrs for tag, attrs in tags if tag == "img")
        self.assertEqual(image["src"], "/project/img/test.png")
        self.assertEqual(image["alt"], 'A "sample" & tube')
        self.assertEqual(next(attrs["href"] for tag, attrs in tags if tag == "a"), "https://example.org/?a=1&b=2")

    def test_optional_fields_and_empty_section(self):
        tags = Tags(render_news_html([entry()])).tags
        self.assertFalse(any(tag in {"a", "img"} for tag, _ in tags))
        self.assertEqual(render_news_html([]), "")
        html = '<main><section class="text-section"><h2 class="text-section-title">News</h2></section><p>Keep</p></main>'
        self.assertEqual(replace_news_block(html, [], {"title": "News"}), '<main><p>Keep</p></main>')

    def test_invalid_entries_report_actionable_errors(self):
        cases = [
            ({}, "JSON array"),
            ([{}], "entry 1: 'id'"),
            ([dict(entry(), date="2026-02-30")], "YYYY-MM-DD"),
            ([dict(entry(), title=" ")], "'title'"),
            ([entry(), entry()], "duplicate id"),
            ([entry(image={"src": "/image.png"})], "'alt'"),
            ([entry(link={"url": "javascript:alert(1)", "label": "Read"})], "HTTP(S)"),
        ]
        for items, expected in cases:
            with self.subTest(items=items), self.assertRaises(ValueError) as caught:
                render_news_html(items)
            self.assertIn(expected, str(caught.exception))
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "news.json"
            path.write_text(json.dumps([{}]))
            with self.assertRaises(ValueError) as caught:
                load_news(path)
            self.assertIn(str(path), str(caught.exception))

    def test_placeholder_replacement_preserves_position_and_is_repeatable(self):
        html = '<main><p>Before</p><section class="text-section"><h2 class="text-section-title">Updates</h2></section><p>After</p></main>'
        result = replace_news_block(html, [entry()], {"title": "Updates"})
        self.assertLess(result.index("Before"), result.index('id="news"'))
        self.assertLess(result.index('id="news"'), result.index("After"))
        self.assertEqual(result, replace_news_block(result, [entry()], {"title": "Updates"}))
        with self.assertRaisesRegex(ValueError, "placeholder"):
            replace_news_block("<main></main>", [entry()], {"title": "News"})


if __name__ == "__main__":
    unittest.main()
