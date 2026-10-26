# /// script
# requires-python = ">=3.10"
# ///
"""Merge the slides of several PPTX decks into one deck, at the package (XML) level.

Usage: uv run scripts/merge_pptx.py OUT.pptx DECK1.pptx DECK2.pptx ...

The first deck is the base: its master, layouts and theme are kept. Slides of the
other decks are appended in order. Their layouts are matched by name to the base.
Charts, embedded workbooks and images are copied as they are; the template builders
already prefix those parts with the tool name, so a clash means a bug and stops the run.
All decks must share the slide size.
"""

import posixpath
import re
import sys
import xml.etree.ElementTree as ET
import zipfile

REL_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
PKG_REL_NS = "http://schemas.openxmlformats.org/package/2006/relationships"
SLIDE_CT = "application/vnd.openxmlformats-officedocument.presentationml.slide+xml"
CHART_CT = "application/vnd.openxmlformats-officedocument.drawingml.chart+xml"
XLSX_CT = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
COPIED = ("chart", "image", "package", "oleObject")


def rels_of(part):
    return posixpath.join(posixpath.dirname(part), "_rels", posixpath.basename(part) + ".rels")


def read_rels(files, part):
    path = rels_of(part)
    if path not in files:
        return []
    xml = files[path].decode("utf-8")
    return [(m.group(1), m.group(2), m.group(3)) for m in re.finditer(
        r'<Relationship\s+[^>]*?Id="([^"]+)"[^>]*?Type="([^"]+)"[^>]*?Target="([^"]+)"[^>]*?/?>', xml)]


def write_rels(rels):
    items = "".join(f'<Relationship Id="{i}" Type="{t}" Target="{g}"/>' for i, t, g in rels)
    return ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
            f'<Relationships xmlns="{PKG_REL_NS}">{items}</Relationships>').encode("utf-8")


def load(path):
    with zipfile.ZipFile(path) as z:
        return {n: z.read(n) for n in z.namelist()}


def slide_parts(files):
    pres = files["ppt/presentation.xml"].decode("utf-8")
    rels = {i: g for i, _, g in read_rels(files, "ppt/presentation.xml")}
    ids = re.findall(r'<p:sldId\s[^>]*r:id="([^"]+)"', pres)
    return [posixpath.normpath(posixpath.join("ppt", rels[r])) for r in ids]


def layouts_by_name(files):
    out = {}
    for n in files:
        if re.match(r"ppt/slideLayouts/slideLayout\d+\.xml$", n):
            m = re.search(r'<p:cSld[^>]*\bname="([^"]*)"', files[n].decode("utf-8"))
            out.setdefault(m.group(1) if m else "", n)
    return out


def slide_size(files):
    return re.search(r"<p:sldSz[^>]*/>", files["ppt/presentation.xml"].decode("utf-8")).group(0)


def merge(out_path, sources):
    base = load(sources[0])
    base_layouts = layouts_by_name(base)
    sizes = {slide_size(base)}
    ct = base["[Content_Types].xml"].decode("utf-8")
    pres = base["ppt/presentation.xml"].decode("utf-8")
    pres_rels = read_rels(base, "ppt/presentation.xml")
    next_rid = max(int(re.sub(r"\D", "", i) or 0) for i, _, _ in pres_rels) + 1
    next_id = max([int(x) for x in re.findall(r'<p:sldId\s[^>]*\bid="(\d+)"', pres)] + [255]) + 1
    next_slide = len(slide_parts(base)) + 1
    added = 0

    for path in sources[1:]:
        src = load(path)
        sizes.add(slide_size(src))
        src_layouts = {n: re.search(r'<p:cSld[^>]*\bname="([^"]*)"', src[n].decode("utf-8")) for n in src
                       if re.match(r"ppt/slideLayouts/slideLayout\d+\.xml$", n)}
        for part in slide_parts(src):
            new_slide = f"ppt/slides/slide{next_slide}.xml"
            next_slide += 1
            new_rels = []
            for rid, rtype, target in read_rels(src, part):
                resolved = posixpath.normpath(posixpath.join(posixpath.dirname(part), target))
                if rtype.endswith("/slideLayout"):
                    m = src_layouts.get(resolved)
                    name = m.group(1) if m else ""
                    if name not in base_layouts:
                        raise SystemExit(f"{path}: layout '{name}' is not in the base deck")
                    new_rels.append((rid, rtype, posixpath.relpath(base_layouts[name], "ppt/slides")))
                elif rtype.endswith(tuple("/" + c for c in COPIED)):
                    new_name = resolved
                    if new_name in base:
                        raise SystemExit(f"{path}: part {new_name} already exists; builders must prefix parts")
                    base[new_name] = src[resolved]
                    if resolved.startswith("ppt/charts/"):
                        crels = read_rels(src, resolved)
                        for crid, ctype, ctarget in crels:
                            emb = posixpath.normpath(posixpath.join("ppt/charts", ctarget))
                            if emb in base:
                                raise SystemExit(f"{path}: part {emb} already exists")
                            base[emb] = src[emb]
                        base[rels_of(resolved)] = write_rels(crels)
                        if f'PartName="/{resolved}"' not in ct:
                            ct = ct.replace("</Types>", f'<Override PartName="/{resolved}" ContentType="{CHART_CT}"/></Types>')
                    if resolved.endswith(".xlsx") and 'Extension="xlsx"' not in ct:
                        ct = ct.replace("</Types>", f'<Default Extension="xlsx" ContentType="{XLSX_CT}"/></Types>')
                    new_rels.append((rid, rtype, posixpath.relpath(resolved, "ppt/slides")))
                else:
                    raise SystemExit(f"{path}: unsupported relationship {rtype.rsplit('/', 1)[-1]} on {part}")
            base[new_slide] = src[part]
            base[rels_of(new_slide)] = write_rels(new_rels)
            ct = ct.replace("</Types>", f'<Override PartName="/{new_slide}" ContentType="{SLIDE_CT}"/></Types>')
            rid = f"rIdM{next_rid}"
            next_rid += 1
            pres_rels.append((rid, f"{REL_NS}/slide", posixpath.relpath(new_slide, "ppt")))
            pres = pres.replace("</p:sldIdLst>", f'<p:sldId id="{next_id}" r:id="{rid}"/></p:sldIdLst>')
            next_id += 1
            added += 1

    if len(sizes) > 1:
        raise SystemExit(f"slide sizes differ: {sizes}")
    for name in base:
        if name.endswith(".xlsx") and 'Extension="xlsx"' not in ct and f'PartName="/{name}"' not in ct:
            ct = ct.replace("</Types>", f'<Default Extension="xlsx" ContentType="{XLSX_CT}"/></Types>')
    base["[Content_Types].xml"] = ct.encode("utf-8")
    base["ppt/presentation.xml"] = pres.encode("utf-8")
    base["ppt/_rels/presentation.xml.rels"] = write_rels(pres_rels)
    content_types = base.pop("[Content_Types].xml")
    with zipfile.ZipFile(out_path, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("[Content_Types].xml", content_types)
        for name, data in base.items():
            zf.writestr(name, data)
    problems = check(out_path)
    if problems:
        raise SystemExit(f"{out_path} is broken:\n  " + "\n  ".join(problems))
    print(f"{out_path}: {added} slides added, {len(slide_parts(base))} in total, self-check passed")


def check(path):
    """Structural self-check of a package: zip CRC, content types, relationship targets."""
    problems = []
    with zipfile.ZipFile(path) as z:
        bad = z.testzip()
        if bad:
            problems.append(f"corrupt zip entry {bad}")
        files = {n: z.read(n) for n in z.namelist()}
    ct_root = ET.fromstring(files["[Content_Types].xml"])
    defaults = {e.get("Extension").lower() for e in ct_root if e.tag.endswith("}Default")}
    overrides = {e.get("PartName") for e in ct_root if e.tag.endswith("}Override")}
    for name in files:
        if name == "[Content_Types].xml" or name.endswith("/"):
            continue
        ext = name.rsplit(".", 1)[-1].lower()
        if f"/{name}" not in overrides and ext not in defaults:
            problems.append(f"no content type for {name}")
    for name in files:
        if not name.endswith(".rels"):
            continue
        owner = posixpath.normpath(posixpath.join(posixpath.dirname(name), "..", posixpath.basename(name)[:-5]))
        base_dir = posixpath.dirname(owner)
        for rel in ET.fromstring(files[name]):
            if rel.get("TargetMode") == "External":
                continue
            target = posixpath.normpath(posixpath.join(base_dir, rel.get("Target")))
            if target.startswith("/"):
                target = target[1:]
            if target not in files:
                problems.append(f"{name}: {rel.get('Id')} points to missing {target}")
    slides = [n for n in files if re.match(r"ppt/slides/slide\d+\.xml$", n)]
    if not slides:
        problems.append("no slides in the package")
    return problems


if __name__ == "__main__":
    if len(sys.argv) < 3:
        raise SystemExit(__doc__)
    merge(sys.argv[1], sys.argv[2:])
