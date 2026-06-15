"""
Convert nu-reading-list.json → Obsidian notes.

Usage:
  python3 "Novel Tracker/import-nu.py" nu-reading-list.json

Generates one .md file per novel in the current directory.
"""

import json, re, sys, pathlib

STATUS_MAP = {
    'Reading': 'Reading',
    'Completed': 'Completed',
    'On Hold': 'On-Hold',
    'Plan to Read': 'Plan-to-Read',
    'Dropped': 'Dropped',
}


def slugify(title):
    s = re.sub(r'[^a-zA-Z0-9 ]', '', title)
    s = s.replace(' ', '_').replace('__', '_').strip('_')
    return s


def yaml_str(s):
    if not s or not s.strip():
        return ''
    return "'" + s.replace("'", "''") + "'"


def parse_chapter(raw):
    """Try to extract a number from chapter strings like 'c230', 'v1c1', 'prologue'."""
    if not raw:
        return None
    raw = raw.strip().lower()
    # Try direct number
    if raw.isdigit():
        return int(raw)
    # Try patterns: c123, chapter 123, v1c123, etc.
    m = re.search(r'(\d+)', raw)
    if m:
        return int(m.group(1))
    return None


def update_novel_if_exists(out_path, status, cc, tc, rating, url, title):
    try:
        content = out_path.read_text()
    except Exception as e:
        print(f"  Error reading {out_path.name}: {e}")
        return False

    m = re.match(r'^---\n(.*?)\n---\n(.*)', content, re.DOTALL)
    if not m:
        return False

    fm_text = m.group(1)
    rest_text = m.group(2)

    fm_lines = fm_text.splitlines()
    fm_dict = {}
    for line in fm_lines:
        if ':' in line and not line.strip().startswith('-'):
            k, v = line.split(':', 1)
            fm_dict[k.strip()] = v.strip()

    try:
        curr_cc = int(fm_dict.get('current-chapter', '0').strip().strip("'").strip('"') or 0)
    except ValueError:
        curr_cc = 0
    try:
        curr_tc = int(fm_dict.get('total-chapters', '0').strip().strip("'").strip('"') or 0)
    except ValueError:
        curr_tc = 0

    new_cc = max(cc, curr_cc)
    new_tc = max(tc, curr_tc)

    # Let's prepare updates
    updates = {
        'status': status,
        'current-chapter': str(new_cc),
        'total-chapters': str(new_tc),
    }
    if rating:
        updates['rating'] = rating
    if url:
        updates['source-url'] = yaml_str(url)

    # Reconstruct frontmatter lines
    updated_lines = []
    seen = set()
    for line in fm_lines:
        if ':' in line and not line.strip().startswith('-'):
            k, v = line.split(':', 1)
            k_strip = k.strip()
            if k_strip in updates:
                updated_lines.append(f"{k_strip}: {updates[k_strip]}")
                seen.add(k_strip)
                continue
        updated_lines.append(line)

    for k, v in updates.items():
        if k not in seen:
            updated_lines.append(f"{k}: {v}")

    new_fm_text = '\n'.join(updated_lines)
    try:
        out_path.write_text(f"---\n{new_fm_text}\n---\n{rest_text}")
        return True
    except Exception as e:
        print(f"  Error writing {out_path.name}: {e}")
        return False


def generate_novel(n, status='Reading'):
    title = n.get('title', 'Untitled').strip()
    if not title:
        return None
    slug = slugify(title)
    url = n.get('url', '')
    raw_my = (n.get('myChapter') or '').strip()
    raw_latest = (n.get('latestChapter') or '').strip()
    rating = (n.get('rating') or '').strip()
    genre_ids = (n.get('genreIds') or '').strip()

    my_ch = parse_chapter(raw_my)
    latest = parse_chapter(raw_latest)

    cc = my_ch if my_ch is not None else 0
    if latest is not None:
        tc = max(latest, cc)
    else:
        tc = cc

    unread = ''
    if cc < tc:
        start = cc + 1
        if start == tc:
            unread = f"\n\n### Unread\n- [ ] Chapter {tc}"
        else:
            unread = f"\n\n### Unread\n- [ ] Chapters {start}-{tc}"

    # NU chapter info as comment
    nu_info = ''
    if raw_my or raw_latest:
        nu_info = f"\n\n_NU: my chapter `{raw_my}`, latest `{raw_latest}`_"

    content = f"""---
fileClass: novel
cssclasses:
  - novel-page
tags:
  - novel
aliases:
  - {yaml_str(title)}
status: {status}
author: ''
source-url: {yaml_str(url)}
total-chapters: {tc}
current-chapter: {cc}
rating: {rating}
description: ''
---

# {title}

![[covers/{slug}.webp|100|left]]

> [Read Here]({url})

| | |
| --- | --- |
| **Status** | `INPUT[inlineSelect(option(Reading), option(Plan-to-Read), option(Completed), option(Dropped), option(On-Hold)):status]` |
| **Rating** | `INPUT[inlineSelect(option(1, ⭐), option(2, ⭐⭐), option(3, ⭐⭐⭐), option(4, ⭐⭐⭐⭐), option(5, ⭐⭐⭐⭐⭐)):rating]` |
| **Progress** | `INPUT[number:current-chapter]` / `INPUT[number:total-chapters]` ch |
| **Genres** | `=this.file.tags` |
{nu_info}

---

## Chapter Log

### Read
- [x] Chapters 1-{cc if cc > 0 else '?'}{unread}
"""

    return slug, content, cc, tc, rating, url, title


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python3 "Novel Tracker/import-nu.py" nu-reading-list.json [status]')
        sys.exit(1)

    path = pathlib.Path(sys.argv[1])
    data = json.loads(path.read_text())

    if not data:
        print('No novels found in JSON. Make sure the browser script found entries.')
        sys.exit(1)

    # Determine default status
    default_status = 'Reading'
    if len(sys.argv) >= 3:
        status_arg = sys.argv[2]
        default_status = STATUS_MAP.get(status_arg, status_arg)
    else:
        # Guess from filename
        fn = path.name.lower()
        if 'deseos' in fn:
            default_status = 'Plan-to-Read'
        elif 'dropped' in fn:
            default_status = 'Dropped'
        elif 'finish' in fn:
            default_status = 'Completed'
        elif 'reading' in fn:
            default_status = 'Reading'

    print(f"Importing {path.name} with default status: {default_status}")

    count_created = 0
    count_updated = 0
    for n in data:
        result = generate_novel(n, default_status)
        if result is None:
            continue
        slug, content, cc, tc, rating, url, title = result
        out = pathlib.Path(f'{slug}.md')
        if out.exists():
            if update_novel_if_exists(out, default_status, cc, tc, rating, url, title):
                count_updated += 1
            continue
        out.write_text(content)
        print(f'  Created {out.name}')
        count_created += 1

    print(f'\nDone: {count_created} notes created, {count_updated} notes updated')

