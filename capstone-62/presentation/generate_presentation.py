#!/usr/bin/env python3
"""
Presentation Generator for CAPSTONE 62
Generates a professional 5-slide widescreen (.pptx) presentation with
modern design aesthetics, structured card layouts, and complete speaker notes.
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def create_deck(output_path: str) -> None:
    prs = Presentation()
    # 16:9 widescreen dimensions (13.333 x 7.5 inches)
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    # Color Palette: Deep Slate Executive Theme
    BG_COLOR = RGBColor(15, 23, 42)        # Slate 900
    CARD_BG = RGBColor(30, 41, 59)         # Slate 800
    ACCENT_CYAN = RGBColor(56, 189, 248)    # Sky 400
    ACCENT_EMERALD = RGBColor(52, 211, 153) # Emerald 400
    TEXT_LIGHT = RGBColor(248, 250, 252)   # Slate 50
    TEXT_MUTED = RGBColor(148, 163, 184)   # Slate 400
    BORDER_COLOR = RGBColor(51, 65, 85)    # Slate 700

    blank_layout = prs.slide_layouts[6]

    def set_slide_background(slide):
        bg_shape = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), prs.slide_width, prs.slide_height
        )
        bg_shape.fill.solid()
        bg_shape.fill.fore_color.rgb = BG_COLOR
        bg_shape.line.color.rgb = BG_COLOR
        return bg_shape

    def add_header(slide, category: str, title: str):
        # Category Tag
        cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.5), Inches(11.7), Inches(0.4))
        tf_cat = cat_box.text_frame
        tf_cat.word_wrap = True
        p_cat = tf_cat.paragraphs[0]
        p_cat.text = category.upper()
        p_cat.font.size = Pt(11)
        p_cat.font.bold = True
        p_cat.font.color.rgb = ACCENT_CYAN

        # Title
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.85), Inches(11.7), Inches(0.8))
        tf_title = title_box.text_frame
        tf_title.word_wrap = True
        p_title = tf_title.paragraphs[0]
        p_title.text = title
        p_title.font.size = Pt(24)
        p_title.font.bold = True
        p_title.font.color.rgb = TEXT_LIGHT

    def add_card(slide, left, top, width, height, title, body_bullets, accent_color=ACCENT_CYAN):
        # Card Background
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = BORDER_COLOR
        card.line.width = Pt(1.5)

        # Card Title
        tb = slide.shapes.add_textbox(left + Inches(0.25), top + Inches(0.2), width - Inches(0.5), Inches(0.5))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(15)
        p.font.bold = True
        p.font.color.rgb = accent_color

        # Card Body Bullets
        tb_body = slide.shapes.add_textbox(left + Inches(0.25), top + Inches(0.7), width - Inches(0.5), height - Inches(0.85))
        tf_b = tb_body.text_frame
        tf_b.word_wrap = True

        for i, bullet in enumerate(body_bullets):
            p_b = tf_b.paragraphs[0] if i == 0 else tf_b.add_paragraph()
            p_b.text = f"• {bullet}"
            p_b.font.size = Pt(12)
            p_b.font.color.rgb = TEXT_LIGHT
            p_b.space_after = Pt(8)

    # -------------------------------------------------------------------------
    # SLIDE 1: Title, Problem, Target Audience, Objective
    # -------------------------------------------------------------------------
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_background(s1)

    # Large Main Title Hero
    hero_box = slide_hero = s1.shapes.add_textbox(Inches(0.8), Inches(0.7), Inches(11.7), Inches(1.8))
    tf_h = hero_box.text_frame
    tf_h.word_wrap = True
    p1 = tf_h.paragraphs[0]
    p1.text = "CAPSTONE 62"
    p1.font.size = Pt(14)
    p1.font.bold = True
    p1.font.color.rgb = ACCENT_CYAN

    p2 = tf_h.add_paragraph()
    p2.text = "AI-Powered Technical Blog Writing Series for Developers"
    p2.font.size = Pt(28)
    p2.font.bold = True
    p2.font.color.rgb = TEXT_LIGHT

    p3 = tf_h.add_paragraph()
    p3.text = "Research Question: How can AI help a student write clear, original, and accurate technical blog posts?"
    p3.font.size = Pt(13)
    p3.font.color.rgb = ACCENT_EMERALD
    p3.space_before = Pt(6)

    # 3 Column Cards
    col_w = Inches(3.64)
    gap = Inches(0.38)
    y_top = Inches(2.7)
    card_h = Inches(4.2)

    add_card(
        s1, Inches(0.8), y_top, col_w, card_h,
        "1. Problem Statement",
        [
            "CSE students often struggle to translate code projects into readable public blog posts.",
            "Common hurdles: structural disorganization, jargon overload, untested code snippets, and poor clarity.",
            "Unchecked AI usage causes hallucinations, outdated API references, and ethical plagiarism risks.",
            "Students need a rigorous, disciplined framework uniting AI tools with human engineering verification."
        ]
    )

    add_card(
        s1, Inches(0.8) + col_w + gap, y_top, col_w, card_h,
        "2. Target Audience",
        [
            "Primary: Computer Science Engineering (CSE) undergraduate and postgraduate students.",
            "Background: Familiar with programming basics, but beginner technical writers.",
            "Goal: Build an authoritative GitHub portfolio, publish original tech blogs, and improve career communication.",
            "Needs: Reproducible patterns to verify AI suggestions and avoid passive copy-pasting."
        ],
        accent_color=ACCENT_EMERALD
    )

    add_card(
        s1, Inches(0.8) + (col_w + gap) * 2, y_top, col_w, card_h,
        "3. Project Objective",
        [
            "Deliver an end-to-end framework demonstrating AI as a cognitive amplifier, not an unverified ghostwriter.",
            "Produce a validated 3-post Python blog series with 100% executable standard library code.",
            "Implement automated content calendar scheduling with mandatory human verification gates.",
            "Establish ethical guidelines, comprehensive quality checklists, and reproducible verification reports."
        ]
    )

    s1.notes_slide.notes_text_frame.text = (
        "Slide 1 Speaker Notes:\n"
        "Good morning, faculty members and colleagues. Today I am presenting CAPSTONE 62: AI-Powered Technical "
        "Blog Writing Series for Developers. Our guiding question is: How can AI help a student write clear, "
        "original, and accurate technical blog posts? Technical blogging is an essential skill for computer science "
        "students building a public profile. However, unguided AI usage poses serious risks of hallucination, outdated "
        "syntax, and academic dishonesty. This project establishes an end-to-end disciplined engineering workflow "
        "where AI assists with outlining, ideation, and review, while human students remain strictly responsible for "
        "technical accuracy, code execution, and original synthesis."
    )

    # -------------------------------------------------------------------------
    # SLIDE 2: Methodology, Principles, Source Verification, AI Tools
    # -------------------------------------------------------------------------
    s2 = prs.slides.add_slide(blank_layout)
    set_slide_background(s2)
    add_header(s2, "Foundations & Methodology", "Research Methodology, Principles, and AI Tool Ecosystem")

    card_w2 = Inches(5.67)
    card_h2 = Inches(2.6)
    gap_x = Inches(0.38)
    gap_y = Inches(0.3)

    add_card(
        s2, Inches(0.8), Inches(1.8), card_w2, card_h2,
        "Principles of Technical Writing",
        [
            "Audience-Centric: Define explicit learning goals and realistic prerequisites.",
            "Active Voice & Conciseness: Use short paragraphs (<80 words) and direct verbs.",
            "Code Authenticity: Every code example must include real expected terminal output.",
            "Debugging Context: Always explain common errors, causes, and debugging strategies.",
            "Anchor to Authority: Cite official documentation (Google Style Guide, Python.org)."
        ]
    )

    add_card(
        s2, Inches(0.8) + card_w2 + gap_x, Inches(1.8), card_w2, card_h2,
        "Multi-Tool AI Stack (Free Tiers)",
        [
            "Google Gemini / Antigravity: Research synthesis, architecture, and workflow scripts.",
            "ChatGPT (Free Tier): Comparative outlining, brainstorming, and drafting analysis.",
            "Claude: Long-form structural critique and pedagogical flow evaluation.",
            "Grammarly (Free): Readability scoring, passive voice detection, and grammar audits.",
            "GitHub & Notion: Version control, code distribution, and content ops."
        ],
        accent_color=ACCENT_EMERALD
    )

    add_card(
        s2, Inches(0.8), Inches(1.8) + card_h2 + gap_y, card_w2, card_h2,
        "Authoritative Source Verification",
        [
            "Zero Hallucination Policy: All technical claims cross-checked against official documentation.",
            "Primary References: Google Developer Style Guide, Google Tech Writing Courses, Python 3.12 Docs.",
            "Audited Source Table: Documented URLs, verification status, findings, and access dates.",
            "Anti-Plagiarism: Industry blogs consulted solely for structural review, never content copying."
        ]
    )

    add_card(
        s2, Inches(0.8) + card_w2 + gap_x, Inches(1.8) + card_h2 + gap_y, card_w2, card_h2,
        "Comparative AI Experimentation",
        [
            "Side-by-side prompt testing between Gemini and ChatGPT on technical blogging advice.",
            "Gemini excelled at CLI architectural patterns, error typing, and testability advice.",
            "ChatGPT offered strong modular outlining and introductory narrative hooks.",
            "Human Synthesis: Combined Gemini's technical rigour with ChatGPT's pacing for the final posts."
        ],
        accent_color=ACCENT_EMERALD
    )

    s2.notes_slide.notes_text_frame.text = (
        "Slide 2 Speaker Notes:\n"
        "On Slide 2, we present our research methodology and tool stack. We ground our technical writing "
        "in industry standards: the Google Developer Documentation Style Guide, Google Tech Writing courses, "
        "and official Python 3.12 documentation. Our AI ecosystem utilizes four accessible tools: Google Gemini, "
        "ChatGPT, Claude, and Grammarly. Crucially, we conducted comparative prompt experiments between Gemini "
        "and ChatGPT on technical blog architecture. We found that Gemini prioritized defensive programming and unit "
        "testing, while ChatGPT emphasized narrative hook design. We synthesized both perspectives while strictly verifying "
        "all code against official Python standard library documentation."
    )

    # -------------------------------------------------------------------------
    # SLIDE 3: Content Plan & Main Python CLI Project Overview
    # -------------------------------------------------------------------------
    s3 = prs.slides.add_slide(blank_layout)
    set_slide_background(s3)
    add_header(s3, "Curriculum & Engineering", "Three-Post Content Series & Python CLI Architecture")

    add_card(
        s3, Inches(0.8), y_top, col_w, card_h,
        "Post 1 (Main, ~1,000 Words)",
        [
            "Title: 'Build Your First Python CLI Application: A Step-by-Step Guide'.",
            "Core Project: Local Task Manager built strictly with Python Standard Library (`argparse`, `json`, `sys`).",
            "Zero Third-Party Bloat: Works out-of-the-box on vanilla Python 3.10+ installations.",
            "Covers: Persistent JSON storage, subcommands (add/list/complete/delete/clear), and error handling.",
            "Verified Execution: 100% of CLI commands executed and documented with real outputs."
        ]
    )

    add_card(
        s3, Inches(0.8) + col_w + gap, y_top, col_w, card_h,
        "Post 2 (Debugging Guide)",
        [
            "Title: 'Five Common Python Errors and How to Debug Them'.",
            "Covers the 5 most frequent beginner traps: SyntaxError, NameError, TypeError, IndexError, KeyError.",
            "Anatomy of Tracebacks: Teaches students how to read file lines, error types, and exception messages.",
            "Before-and-After Code: Real failing snippets paired with tested defensive corrections.",
            "Tested Module: `error_examples.py` safely reproduces and resolves all 5 exceptions."
        ],
        accent_color=ACCENT_EMERALD
    )

    add_card(
        s3, Inches(0.8) + (col_w + gap) * 2, y_top, col_w, card_h,
        "Post 3 (Functions & Testing)",
        [
            "Title: 'Writing Better Python Code with Functions and Unit Tests'.",
            "Pedagogy: Explains single responsibility, pure functions, and deterministic returns.",
            "Real Utilities: `slugify()`, `calculate_reading_time()`, and `count_words()` for blogging systems.",
            "Automated Testing: Complete `unittest` suite covering typical cases, edge cases, and invalid types.",
            "Reliability Bridge: Demonstrates why unit tests give developers confidence to publish code publicly."
        ]
    )

    s3.notes_slide.notes_text_frame.text = (
        "Slide 3 Speaker Notes:\n"
        "Slide 3 details our 3-post blog series under the theme 'Python Development: From Beginner to Practical Developer'. "
        "Post 1 is our flagship 1,000-word tutorial teaching students to build a full CLI task manager using only standard library "
        "modules—eliminating external dependency friction. Post 2 demystifies Python debugging across 5 universal errors: "
        "SyntaxError, NameError, TypeError, IndexError, and KeyError, teaching students how to diagnose tracebacks. Post 3 "
        "elevates their craft to professional standards by introducing modular pure functions and automated unit testing with "
        "Python's built-in unittest module. All three posts are supported by fully implemented, executed, and passing code files."
    )

    # -------------------------------------------------------------------------
    # SLIDE 4: Before-and-After Editing, Quality Checklist, Verification
    # -------------------------------------------------------------------------
    s4 = prs.slides.add_slide(blank_layout)
    set_slide_background(s4)
    add_header(s4, "Editorial & Technical Rigour", "Before-and-After Editing, Quality Checklist, and Verification")

    add_card(
        s4, Inches(0.8), Inches(1.8), card_w2, card_h2,
        "AI Draft vs. Final Edit Analysis",
        [
            "Raw AI Draft Weaknesses: Used deprecated functions, invented non-existent CLI flags, and used passive fluff.",
            "Hallucination Identified: Raw draft referenced `--json` flag never built in `task_manager.py`.",
            "Clarity Refinement: Replaced wordy explanations with structured step-by-step terminal examples.",
            "Editorial Table: 4-column audit documenting Original Text, Identified Flaw, Revised Text, and Engineering Rationale."
        ]
    )

    add_card(
        s4, Inches(0.8) + card_w2 + gap_x, Inches(1.8), card_w2, card_h2,
        "Quality Checklist (4 Pillars)",
        [
            "1. Content Quality: Clear CSE audience target, logical progression, original prose, and actionable summaries.",
            "2. Technical Accuracy: Code executed in Python 3.12, 17/17 unit tests passing, zero deprecated APIs.",
            "3. Readability: Hemingway grade 8-9 level, active verbs, informative subheadings, code callouts.",
            "4. Ethics: Mandatory AI disclosure, 100% original synthesis, zero fabricated test results, verified URLs."
        ],
        accent_color=ACCENT_EMERALD
    )

    add_card(
        s4, Inches(0.8), Inches(1.8) + card_h2 + gap_y, card_w2, card_h2,
        "Verification Findings & Test Proof",
        [
            "Unit Test Suite: 17/17 tests passing across CLI persistence, edge cases, and string utility logic.",
            "Graceful Failure Testing: Corrupted JSON data files handled cleanly with stderr warnings instead of crashing.",
            "Terminal Proof: Every code block in the blog series was executed in PowerShell/Bash before publishing.",
            "Status Classification: Claims tagged as 'Verified', 'Corrected', or 'Not Tested'—no false claims."
        ]
    )

    add_card(
        s4, Inches(0.8) + card_w2 + gap_x, Inches(1.8) + card_h2 + gap_y, card_w2, card_h2,
        "Prompt Library Engineering",
        [
            "15 Specialized Prompts created spanning topic selection, outlining, drafting, code generation, and audit.",
            "Explicit Anti-Hallucination Constraints: 'Do not invent packages or cite fictional documentation'.",
            "Reproducible Templates: Each prompt includes ID, Purpose, Prompt Text, Expected Output, and Known Limitations.",
            "Verification Mechanism: Mandates that AI output must provide citations directly checkable against Python.org."
        ],
        accent_color=ACCENT_EMERALD
    )

    s4.notes_slide.notes_text_frame.text = (
        "Slide 4 Speaker Notes:\n"
        "Slide 4 demonstrates the editorial and technical rigour that separates our project from superficial AI generation. "
        "We conducted an explicit before-and-after audit on raw AI output. For instance, the unedited AI draft invented a non-existent "
        "'--json' flag and used outdated Python idioms. Our human engineering review identified this hallucination, verified the "
        "code against Python 3.12 documentation, and corrected the tutorial text. Furthermore, our 4-pillar quality checklist and "
        "17 automated unit tests ensure that every single code sample runs reliably on the reader's machine. Our 15-item prompt library "
        "embeds strict anti-fabrication constraints into every query."
    )

    # -------------------------------------------------------------------------
    # SLIDE 5: Automation Workflow, Ethics, Results, Limitations & Conclusion
    # -------------------------------------------------------------------------
    s5 = prs.slides.add_slide(blank_layout)
    set_slide_background(s5)
    add_header(s5, "Automation & Governance", "Content Automation, Responsible AI, Results, and Limitations")

    add_card(
        s5, Inches(0.8), Inches(1.8), card_w2, card_h2,
        "Local Automation Engine",
        [
            "Executable Python Engine (`content_calendar_notifier.py`): Ingests calendar CSV data.",
            "Proactive Scheduling: Automatically detects overdue articles and drafts due within 3 days.",
            "Verification Gate Enforcement: Flags any post entering 'In Review' without technical verification.",
            "Outputs: Produces rich CLI reports, Markdown digests, and persistent JSON audit logs."
        ]
    )

    add_card(
        s5, Inches(0.8) + card_w2 + gap_x, Inches(1.8), card_w2, card_h2,
        "Ethics & Responsible AI Practices",
        [
            "Human-in-the-Loop: AI can outline and suggest, but a human engineer MUST review and approve publication.",
            "Mandatory AI Disclosure: Clear, professional disclosure badge included on every article.",
            "Zero Plagiarism: No scraper bots or unauthorized blog rewriting; all content is student-originated.",
            "Safe Technical Advice: Defensive programming practices taught; security pitfalls explicitly highlighted."
        ],
        accent_color=ACCENT_EMERALD
    )

    add_card(
        s5, Inches(0.8), Inches(1.8) + card_h2 + gap_y, card_w2, card_h2,
        "Project Results & Impact",
        [
            "Complete End-to-End Repository: 15 modular deliverables spanning code, tests, blogs, and reports.",
            "Student Empowerment: Transforms CSE students from passive coders into credible technical communicators.",
            "Portfolio Ready: Provides a reproducible blueprint for building public developer authority on GitHub.",
            "High Academic Utility: Easy for faculty to evaluate via standardized rubrics and verified test logs."
        ]
    )

    add_card(
        s5, Inches(0.8) + card_w2 + gap_x, Inches(1.8) + card_h2 + gap_y, card_w2, card_h2,
        "Limitations & Future Horizons",
        [
            "Current Limitation: Local notifier requires scheduled trigger (cron/Task Scheduler) without webhooks.",
            "Future Scope: Webhook integration with Discord/Slack and automated GitHub Actions CI/CD deployment.",
            "AI Horizon: Static analysis linting integrated directly into prompt verification pipelines.",
            "Conclusion: AI is an unparalleled partner for student developers when governed by strict verification."
        ],
        accent_color=ACCENT_EMERALD
    )

    s5.notes_slide.notes_text_frame.text = (
        "Slide 5 Speaker Notes:\n"
        "To conclude on Slide 5, we look at automation, ethics, and future scope. We implemented a fully working "
        "content calendar automation script that checks deadlines and enforces verification gates before any draft "
        "can be cleared for publishing. Ethical AI is the core foundation of CAPSTONE 62: we mandate transparent AI "
        "disclosures, complete human ownership, and zero fabricated test results. While our current automation operates "
        "locally via CSV and terminal triggers, future iterations can easily hook into GitHub Actions and Slack webhooks. "
        "In conclusion, AI empowers CSE students to communicate their technical ideas clearly and authoritatively, provided "
        "it is matched with rigorous human verification and sound software engineering principles. Thank you, and I look forward "
        "to your questions."
    )

    prs.save(output_path)
    print(f"[Success] 5-Slide Presentation saved to: {output_path}")

if __name__ == "__main__":
    out_file = os.path.join(os.path.dirname(__file__), "five-slide-presentation.pptx")
    create_deck(out_file)
