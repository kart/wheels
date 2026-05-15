#!/usr/bin/env python3

import argparse
import html
import re
import sys
from pathlib import Path

try:
    import markdown
except ImportError:
    print("Missing dependency: markdown")
    print("Install it with: pip install markdown")
    sys.exit(1)


ROOT = Path.cwd()


def topic_dir(topic: str) -> Path:
    return ROOT / "topics" / topic


def wiki_dir(topic: str) -> Path:
    return topic_dir(topic) / "wiki"


def preview_dir(topic: str) -> Path:
    return topic_dir(topic) / "wiki_preview"


def title_from_markdown(path: Path, text: str) -> str:
    for line in text.splitlines():
        match = re.match(r"^#\s+(.+?)\s*$", line)
        if match:
            return match.group(1).strip()

    return path.stem.replace("_", " ").replace("-", " ").title()


def slugify(value: str) -> str:
    value = value.lower()
    value = re.sub(r"<[^>]+>", "", value)
    value = re.sub(r"[^\w\s-]", "", value)
    value = re.sub(r"[-\s]+", "-", value).strip("-")
    return value or "section"


def unique_slug(base: str, used: set[str]) -> str:
    slug = base
    index = 2

    while slug in used:
        slug = "{}-{}".format(base, index)
        index += 1

    used.add(slug)
    return slug


def flatten_toc_tokens(tokens: list[dict], article_id: str) -> list[dict]:
    headings = []

    for token in tokens:
        prefixed_id = "{}--{}".format(article_id, token["id"])
        headings.append(
            {
                "level": token["level"],
                "text": token["name"],
                "id": prefixed_id,
            }
        )
        headings.extend(flatten_toc_tokens(token.get("children", []), article_id))

    return headings


def prefix_heading_ids(rendered_html: str, article_id: str, headings: list[dict]) -> str:
    for heading in headings:
        original_id = heading["id"].removeprefix("{}--".format(article_id))
        rendered_html = rendered_html.replace(
            'id="{}"'.format(html.escape(original_id, quote=True)),
            'id="{}"'.format(html.escape(heading["id"], quote=True)),
            1,
        )

    return rendered_html


def render_markdown(text: str, article_id: str) -> tuple[str, list[dict]]:
    renderer = markdown.Markdown(
        extensions=[
            "markdown.extensions.extra",
            "markdown.extensions.fenced_code",
            "markdown.extensions.tables",
            "markdown.extensions.toc",
            "markdown.extensions.sane_lists",
        ],
        output_format="html5",
    )
    rendered = renderer.convert(text)
    headings = flatten_toc_tokens(renderer.toc_tokens, article_id)
    rendered = prefix_heading_ids(rendered, article_id, headings)

    return rendered, headings


def collect_pages(base_dir: Path) -> list[dict]:
    paths = sorted(base_dir.rglob("*.md"), key=lambda path: path.relative_to(base_dir).as_posix())
    pages = []
    used_article_ids = set()

    for path in paths:
        text = path.read_text(encoding="utf-8")
        relative_path = path.relative_to(base_dir).as_posix()
        title = title_from_markdown(path, text)
        article_id = unique_slug(slugify(relative_path.removesuffix(".md")), used_article_ids)
        rendered, headings = render_markdown(text, article_id)

        pages.append(
            {
                "path": path,
                "relative_path": relative_path,
                "title": title,
                "article_id": article_id,
                "headings": headings,
                "html": rendered,
            }
        )

    return pages


def sidebar_html(pages: list[dict]) -> str:
    items = []

    for page in pages:
        page_title = html.escape(page["title"])
        page_path = html.escape(page["relative_path"])
        article_id = html.escape(page["article_id"])
        heading_links = []

        for heading in page["headings"]:
            if heading["level"] > 3:
                continue

            heading_text = html.escape(heading["text"])
            heading_id = html.escape(heading["id"])
            class_name = "toc-h{}".format(heading["level"])
            heading_links.append(
                '<li class="{}"><a href="#{}">{}</a></li>'.format(
                    class_name,
                    heading_id,
                    heading_text,
                )
            )

        headings_markup = ""
        if heading_links:
            headings_markup = '<ol class="page-toc">{}</ol>'.format("".join(heading_links))

        items.append(
            """
            <li class="nav-page">
              <a class="nav-title" href="#{article_id}">{title}</a>
              <div class="nav-path">{path}</div>
              {headings}
            </li>
            """.format(
                article_id=article_id,
                title=page_title,
                path=page_path,
                headings=headings_markup,
            )
        )

    return '<ol class="nav-list">{}</ol>'.format("".join(items))


def article_html(page: dict) -> str:
    title = html.escape(page["title"])
    article_id = html.escape(page["article_id"])
    relative_path = html.escape(page["relative_path"])

    return """
    <article id="{article_id}" class="wiki-article">
      <header class="article-header">
        <p class="article-path">{relative_path}</p>
        <h1>{title}</h1>
      </header>
      <div class="article-body">
        {body}
      </div>
    </article>
    """.format(
        article_id=article_id,
        title=title,
        relative_path=relative_path,
        body=page["html"],
    )


def build_html(topic: str, pages: list[dict]) -> str:
    title = "Wheels Wiki: {}".format(topic)
    escaped_title = html.escape(title)
    articles = "\n".join(article_html(page) for page in pages)
    sidebar = sidebar_html(pages)

    return """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <style>
    :root {{
      --bg: #f8f9fa;
      --panel: #ffffff;
      --ink: #202122;
      --muted: #54595d;
      --line: #a2a9b1;
      --line-soft: #eaecf0;
      --link: #0645ad;
      --link-visited: #0b0080;
      --code-bg: #f5f5f5;
      --sidebar-width: 19rem;
    }}

    * {{
      box-sizing: border-box;
    }}

    html {{
      scroll-behavior: smooth;
    }}

    body {{
      margin: 0;
      background: var(--bg);
      color: var(--ink);
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      font-size: 16px;
      line-height: 1.58;
    }}

    a {{
      color: var(--link);
      text-decoration: none;
    }}

    a:visited {{
      color: var(--link-visited);
    }}

    a:hover {{
      text-decoration: underline;
    }}

    .layout {{
      display: grid;
      grid-template-columns: var(--sidebar-width) minmax(0, 1fr);
      min-height: 100vh;
    }}

    .sidebar {{
      position: sticky;
      top: 0;
      height: 100vh;
      overflow: auto;
      border-right: 1px solid var(--line);
      background: #ffffff;
      padding: 1.1rem 1rem 2rem;
    }}

    .brand {{
      margin-bottom: 1.25rem;
      padding-bottom: 1rem;
      border-bottom: 1px solid var(--line-soft);
    }}

    .brand-title {{
      margin: 0;
      font-family: Georgia, "Times New Roman", serif;
      font-size: 1.45rem;
      line-height: 1.2;
    }}

    .brand-subtitle {{
      margin: 0.35rem 0 0;
      color: var(--muted);
      font-size: 0.88rem;
    }}

    .nav-list,
    .page-toc {{
      list-style: none;
      margin: 0;
      padding: 0;
    }}

    .nav-page {{
      margin: 0 0 1rem;
      padding-bottom: 1rem;
      border-bottom: 1px solid var(--line-soft);
    }}

    .nav-title {{
      display: block;
      font-weight: 650;
      line-height: 1.25;
    }}

    .nav-path {{
      margin-top: 0.18rem;
      color: var(--muted);
      font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
      font-size: 0.72rem;
      overflow-wrap: anywhere;
    }}

    .page-toc {{
      margin-top: 0.5rem;
      font-size: 0.84rem;
    }}

    .page-toc li {{
      margin: 0.18rem 0;
    }}

    .toc-h2 {{
      padding-left: 0.65rem;
    }}

    .toc-h3 {{
      padding-left: 1.25rem;
    }}

    .content {{
      max-width: 72rem;
      padding: 2rem clamp(1rem, 4vw, 4rem) 4rem;
    }}

    .wiki-article {{
      background: var(--panel);
      border: 1px solid var(--line);
      margin: 0 0 2rem;
      padding: clamp(1.1rem, 3vw, 2.25rem);
    }}

    .article-header {{
      border-bottom: 1px solid var(--line);
      margin-bottom: 1.5rem;
      padding-bottom: 0.8rem;
    }}

    .article-path {{
      color: var(--muted);
      font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
      font-size: 0.78rem;
      margin: 0 0 0.35rem;
    }}

    h1,
    h2,
    h3,
    h4,
    h5,
    h6 {{
      color: var(--ink);
      font-family: Georgia, "Times New Roman", serif;
      font-weight: 500;
      line-height: 1.28;
    }}

    h1 {{
      margin: 0;
      font-size: clamp(1.8rem, 4vw, 2.55rem);
    }}

    .article-body h1 {{
      margin-top: 0;
      font-size: 1.9rem;
    }}

    .article-body h2 {{
      border-bottom: 1px solid var(--line-soft);
      margin-top: 2rem;
      padding-bottom: 0.25rem;
      font-size: 1.55rem;
    }}

    .article-body h3 {{
      margin-top: 1.55rem;
      font-size: 1.25rem;
    }}

    p,
    ul,
    ol,
    table,
    pre,
    blockquote {{
      margin-top: 0;
      margin-bottom: 1rem;
    }}

    ul,
    ol {{
      padding-left: 1.45rem;
    }}

    li + li {{
      margin-top: 0.25rem;
    }}

    code {{
      background: var(--code-bg);
      border: 1px solid var(--line-soft);
      border-radius: 3px;
      font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
      font-size: 0.92em;
      padding: 0.1rem 0.22rem;
    }}

    pre {{
      background: var(--code-bg);
      border: 1px solid var(--line-soft);
      overflow: auto;
      padding: 0.9rem 1rem;
    }}

    pre code {{
      background: transparent;
      border: 0;
      padding: 0;
    }}

    table {{
      border-collapse: collapse;
      display: block;
      max-width: 100%;
      overflow-x: auto;
      width: max-content;
    }}

    th,
    td {{
      border: 1px solid var(--line);
      padding: 0.45rem 0.62rem;
      vertical-align: top;
    }}

    th {{
      background: #eaecf0;
      font-weight: 650;
    }}

    blockquote {{
      border-left: 4px solid var(--line);
      color: var(--muted);
      padding-left: 1rem;
    }}

    hr {{
      border: 0;
      border-top: 1px solid var(--line);
      margin: 2rem 0;
    }}

    @media (max-width: 860px) {{
      .layout {{
        display: block;
      }}

      .sidebar {{
        position: relative;
        height: auto;
        border-right: 0;
        border-bottom: 1px solid var(--line);
      }}

      .content {{
        padding: 1rem;
      }}

      .wiki-article {{
        border-left: 0;
        border-right: 0;
        margin-left: -1rem;
        margin-right: -1rem;
      }}
    }}
  </style>
</head>
<body>
  <div class="layout">
    <aside class="sidebar">
      <div class="brand">
        <h1 class="brand-title">Wheels Wiki</h1>
        <p class="brand-subtitle">{topic}</p>
      </div>
      {sidebar}
    </aside>
    <main class="content">
      {articles}
    </main>
  </div>
</body>
</html>
""".format(
        title=escaped_title,
        topic=html.escape(topic),
        sidebar=sidebar,
        articles=articles,
    )


def build_preview(topic: str) -> Path:
    source_dir = wiki_dir(topic)

    if not topic_dir(topic).exists():
        print("ERROR: Missing topic directory: {}".format(topic_dir(topic)))
        sys.exit(1)

    if not source_dir.exists():
        print("ERROR: Missing wiki directory: {}".format(source_dir))
        sys.exit(1)

    pages = collect_pages(source_dir)

    if not pages:
        print("ERROR: No Markdown files found under {}".format(source_dir))
        sys.exit(1)

    output_dir = preview_dir(topic)
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "index.html"
    output_path.write_text(build_html(topic, pages), encoding="utf-8")

    return output_path


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Build a local HTML preview for a Wheels topic wiki."
    )
    parser.add_argument(
        "--topic",
        required=True,
        help="Topic id, for example: word2vec",
    )
    args = parser.parse_args()

    output_path = build_preview(args.topic)
    print("Built wiki preview: {}".format(output_path))


if __name__ == "__main__":
    main()
