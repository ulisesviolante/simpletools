
#!/usr/bin/env python3

import argparse
import re
import time
from pathlib import Path
from urllib.parse import urljoin, urldefrag, urlparse

import requests
import trafilatura
from bs4 import BeautifulSoup


def sanitize_filename(name):
    name = re.sub(r'[<>:"/\\|?*\x00-\x1f]', '', name)
    name = re.sub(r'\s+', ' ', name).strip(' .')
    return name[:150] or 'untitled'


def fetch_page(session, url):
    response = session.get(url, timeout=30)
    response.raise_for_status()
    return response.text


def get_toc_links(html, base_url, selector=None):
    soup = BeautifulSoup(html, 'html.parser')

    root = soup.select_one(selector) if selector else soup

    if root is None:
        raise ValueError(f'CSS selector not found: {selector}')

    base = urlparse(base_url)
    base_path = base.path.rsplit('/', 2)[0] + '/'

    entries = []
    seen = set()

    for anchor in root.select('a[href]'):
        title = anchor.get_text(' ', strip=True)
        href = anchor.get('href', '').strip()

        if not title or not href:
            continue

        url, _ = urldefrag(urljoin(base_url, href))
        parsed = urlparse(url)

        if parsed.netloc != base.netloc:
            continue

        if not parsed.path.startswith(base_path):
            continue

        if url.rstrip('/') == base_url.rstrip('/'):
            continue

        if url in seen:
            continue

        seen.add(url)
        entries.append((title, url))

    return entries


def extract_content(html, url):
    content = trafilatura.extract(
        html,
        url=url,
        output_format='markdown',
        include_tables=True,
        include_links=True,
        include_images=True,
        include_comments=False,
        favor_recall=True,
    )

    return content.strip() if content else None


def scrape(url, selector=None, delay=1.0):
    output_dir = Path.cwd()

    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (compatible; TOCScraper/1.0)'
    })

    print(f'Index: {url}')
    print(f'Output: {output_dir}')

    index_html = fetch_page(session, url)
    entries = get_toc_links(index_html, url, selector)

    print(f'Found {len(entries)} entries\n')

    used_names = set()
    saved = 0
    total = len(entries)
    digits = max(2, len(str(total)))

    for number, (title, chapter_url) in enumerate(entries, 1):
        print(f'[{number}/{total}] {title}')

        try:
            html = fetch_page(session, chapter_url)
            content = extract_content(html, chapter_url)

            if not content:
                print('  SKIP: No content found')
                continue

            filename = sanitize_filename(title)
            original = filename
            suffix = 2

            while filename.lower() in used_names:
                filename = f'{original}_{suffix}'
                suffix += 1

            used_names.add(filename.lower())

            filepath = output_dir / (
                f'{number:0{digits}d}-{filename}.md'
            )

            text = (
                f'# {title}\n\n'
                f'**Source:** {chapter_url}\n\n'
                f'---\n\n'
                f'{content}\n'
            )

            filepath.write_text(text, encoding='utf-8')

            saved += 1
            print(f'  SAVED: {filepath.name}')

        except (requests.RequestException, OSError) as exc:
            print(f'  ERROR: {exc}')

        if number < total:
            time.sleep(delay)

    print(f'\nCompleted: {saved}/{total} files saved')


def main():
    parser = argparse.ArgumentParser(
        description='Extract TOC entries into individual Markdown files'
    )

    parser.add_argument(
        'url',
        help='Table of contents URL'
    )

    parser.add_argument(
        '--selector',
        help='CSS selector containing the TOC links'
    )

    parser.add_argument(
        '--delay',
        type=float,
        default=1.0,
        help='Delay between requests in seconds'
    )

    args = parser.parse_args()

    scrape(
        args.url,
        args.selector,
        max(0, args.delay)
    )


if __name__ == '__main__':
    main()

