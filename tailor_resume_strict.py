#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tailor_resume_strict.py

Goal: Produce a tailored .docx that is a *carbon copy* (visually) of the master.
Approach:
- Never create fresh paragraphs/styles. Instead, *clone existing paragraphs* from the master
  (anchors) and only replace the text nodes, preserving w:pPr (paragraph props), w:rPr (run props),
  bullets/numbering (w:numPr), indents, spacing, fonts, etc.
- Provide strict verification that asserts cloned paragraphs share identical formatting props
  with the template anchor (ignoring the text). If verification fails, abort.

This script is self-contained (no OpenAI, no external prompts). It reads:
- master .docx (source of truth for formatting)
- jd.txt       (for simple deterministic keywords)
- content.json (optional) a structured content payload you generated elsewhere
               with sections: header, summary[], skills[], experience[], projects[], education[]
               If not provided, the script will reorder existing bullets by JD keywords only.

USAGE
------
python tailor_resume_strict.py \
  --master "/path/to/master.docx" \
  --out "/path/to/output.docx" \
  [--jd "/path/to/jd.txt"] \
  [--content "/path/to/content.json"] \
  [--strict-verify]

Notes
-----
- If --content is provided, we will *replace* section bodies using cloned anchors.
- If only --jd is provided, we *reorder* bullets within sections by JD relevance but keep content.
- Anchors are discovered from the master automatically:
    - Section headers: ALL-CAPS lines (<=48 chars)
    - Bullet anchor: first paragraph in doc that has numbering (w:numPr) or starts with a bullet glyph
    - Body anchor: first normal non-header, non-bulleted paragraph
- For synonym section titles, the search is case-insensitive and accepts common aliases:
    SUMMARY ~ ["SUMMARY","PROFILE"]
    TECHNICAL SKILLS ~ ["TECHNICAL SKILLS","CORE SKILLS","SKILLS"]
    PROFESSIONAL EXPERIENCE ~ ["PROFESSIONAL EXPERIENCE","EXPERIENCE"]
    PROJECTS ~ ["PROJECTS"]
    EDUCATION ~ ["EDUCATION","ACADEMICS"]
"""
<truncated_content />
def rewrite_section_from_lines(header: Paragraph,
                               old_body: List[Paragraph],
                               lines: List[str],
                               bullet_anchor: Paragraph,
                               body_anchor: Paragraph,
                               strict_verify: bool,
                               mixed_mode: bool = False):
    """
    Replace the entire body of a section with `lines`, cloning anchors from the master.
    - If mixed_mode=True (e.g., PROJECTS), the function will render "title" lines as body
      (non-bulleted) and details as bullets.
    - Otherwise, it preserves the original section's formatting intent: if the original
      section body had bullets, use bullet_anchor; else use body_anchor.
    Also sanitizes leading glyphs to prevent double bullets and removes empty lines.
    """
    def _sanitize(s: str) -> str:
        # Remove leading bullet glyphs, dashes, asterisks, tabs/spaces
        s = (s or "").strip()
        s = re.sub(r"^[\u2022\-\*\t\s]+", "", s)  # strip "•", "-", "*", tabs, spaces
        s = re.sub(r"\s+", " ", s).strip()
        return s

    # Normalize input lines: drop blanks and strip double bullets
    clean_lines = []
    for ln in (lines or []):
        t = _sanitize(ln)
        if t:
            clean_lines.append(t)

    # Decide default rendering mode for the section (bulleted vs body)
    had_bullets = any(has_numbering(p) or (p.text or "").strip().startswith(("•", "- ")) for p in old_body)
    default_anchor = bullet_anchor if (had_bullets and bullet_anchor is not None) else (body_anchor or bullet_anchor or header)

    # Precompute formatting signature for verification
    sig_default = paragraph_xml_signature(default_anchor, ignore_text=True)

    # Remove previous body
    for p in old_body:
        delete_paragraph(p)

    new_pars = []
    last = header

    if not mixed_mode:
        # Uniform rendering using the default anchor
        for i, line in enumerate(clean_lines):
            new_p = clone_paragraph_after(last if i == 0 else last)
            set_paragraph_text_preserve_runs(new_p, line)
            new_pars.append(new_p)
            last = new_p

        if strict_verify:
            for np in new_pars:
                if paragraph_xml_signature(np, ignore_text=True) != sig_default:
                    raise RuntimeError("Formatting drift detected: cloned paragraph does not match anchor formatting.")
        return

    # Mixed rendering (e.g., PROJECTS): treat "title" rows as body, details as bullets.
    # Heuristic: a "title" looks like 'Name | Role | Location | Dates' (contains ' | ')
    # Everything else is treated as a bullet.
    sig_bullet = paragraph_xml_signature(bullet_anchor or default_anchor, ignore_text=True)
    sig_body = paragraph_xml_signature(body_anchor or default_anchor, ignore_text=True)

    for i, line in enumerate(clean_lines):
        looks_like_title = (" | " in line) and not re.search(r"^\d+[\.\)]\s*", line)
        anchor = (body_anchor or default_anchor) if looks_like_title else (bullet_anchor or default_anchor)

        new_p = clone_paragraph_after(last if i == 0 else last)
        set_paragraph_text_preserve_runs(new_p, line)
        new_pars.append(new_p)
        last = new_p

    if strict_verify:
        for np in new_pars:
            sig_np = paragraph_xml_signature(np, ignore_text=True)
            # Verify against the appropriate signature by re-checking the heuristic
            txt = (np.text or "")
            is_title = (" | " in txt) and not re.search(r"^\d+[\.\)]\s*", txt)
            target_sig = sig_body if is_title else sig_bullet
            if sig_np != target_sig:
                raise RuntimeError("Formatting drift detected in mixed mode: cloned paragraph does not match target anchor.")
<truncated_content />
def apply_content(doc, content, strict_verify):
    # ... existing code ...
    # SUMMARY section
    if "summary" in content:
        rewrite_section_from_lines(hdr, body, content["summary"], bullet_anchor, body_anchor, strict_verify, mixed_mode=False)
    # SKILLS section
    if "skills" in content:
        rewrite_section_from_lines(hdr, body, content["skills"], bullet_anchor, body_anchor, strict_verify, mixed_mode=False)
    # EXPERIENCE section
    if "experience" in content:
        rewrite_section_from_lines(hdr, body, merged, bullet_anchor, body_anchor, strict_verify, mixed_mode=False)
    # PROJECTS section
    if "projects" in content:
        rewrite_section_from_lines(hdr, body, content["projects"], bullet_anchor, body_anchor, strict_verify, mixed_mode=True)
<truncated_content />
def reorder_only(doc, jd, strict_verify):
    # ... existing code ...
    rewrite_section_from_lines(hdr, body, new_lines, bullet_anchor, body_anchor, strict_verify, mixed_mode=False)
<truncated_content />