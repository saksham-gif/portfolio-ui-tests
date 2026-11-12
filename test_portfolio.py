"""End-to-end UI tests for saksham-gif.github.io.

Covers page load, navigation, the expandable project cards,
contact links and the mobile layout.
"""
import re

from playwright.sync_api import expect


# ---------- Page load ----------

def test_page_loads_with_correct_title(page):
    expect(page).to_have_title(re.compile("Saksham Sharma"))


def test_nav_shows_name_and_section_links(page):
    expect(page.locator(".nav-name")).to_have_text("Saksham Sharma")
    for section in ["Projects", "Skills", "Contact"]:
        expect(page.locator(".nav-links a", has_text=section)).to_be_visible()


# ---------- Navigation ----------

def test_nav_links_point_to_existing_sections(page):
    links = page.locator(".nav-links a")
    for i in range(links.count()):
        target = links.nth(i).get_attribute("href")  # e.g. "#projects"
        assert target.startswith("#"), f"Unexpected nav link: {target}"
        expect(page.locator(target)).to_have_count(1)


def test_clicking_projects_link_scrolls_to_projects(page):
    page.locator(".nav-links a", has_text="Projects").click()
    expect(page).to_have_url(re.compile("#projects$"))
    expect(page.locator("#projects")).to_be_in_viewport()


# ---------- Project cards ----------

def test_project_cards_are_present(page):
    cards = page.locator(".project-card")
    assert cards.count() >= 1, "No project cards found"
    for i in range(cards.count()):
        expect(cards.nth(i).locator(".proj-title")).not_to_be_empty()


def test_card_expands_and_collapses_on_click(page):
    card = page.locator(".project-card").first
    detail = card.locator(".proj-detail")

    expect(detail).to_be_hidden()
    card.click()
    expect(card).to_have_class(re.compile(r"\bactive\b"))
    expect(detail).to_be_visible()
    expect(card.locator(".expand-hint")).to_contain_text("collapse")

    card.click()
    expect(card).not_to_have_class(re.compile(r"\bactive\b"))
    expect(detail).to_be_hidden()
    expect(card.locator(".expand-hint")).to_contain_text("expand")


def test_only_one_card_open_at_a_time(page):
    cards = page.locator(".project-card")
    if cards.count() < 2:
        return  # nothing to compare with a single card
    cards.nth(0).click()
    cards.nth(1).click()
    expect(page.locator(".project-card.active")).to_have_count(1)
    expect(cards.nth(1)).to_have_class(re.compile(r"\bactive\b"))


def test_every_card_has_skill_tags(page):
    cards = page.locator(".project-card")
    for i in range(cards.count()):
        assert cards.nth(i).locator(".proj-tag").count() > 0, f"Card {i} has no tags"


# ---------- Contact ----------

def test_contact_links_are_valid(page):
    contact = page.locator("#contact")
    expect(contact.locator("a[href^='mailto:']")).to_have_count(1)
    linkedin = contact.locator("a", has_text="LinkedIn")
    expect(linkedin).to_have_attribute("href", re.compile(r"linkedin\.com/in/"))


# ---------- Responsive layout ----------

def test_mobile_layout_has_no_horizontal_scroll(mobile_page):
    overflow = mobile_page.evaluate(
        "document.documentElement.scrollWidth - document.documentElement.clientWidth"
    )
    assert overflow <= 1, f"Page scrolls sideways on mobile by {overflow}px"


def test_project_cards_work_on_mobile(mobile_page):
    card = mobile_page.locator(".project-card").first
    card.click()
    expect(card.locator(".proj-detail")).to_be_visible()
