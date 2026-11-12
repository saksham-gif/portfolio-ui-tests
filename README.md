# Portfolio UI Test Automation

![UI Tests](https://github.com/saksham-gif/portfolio-ui-tests/actions/workflows/ui-tests.yml/badge.svg)

Automated end-to-end web UI tests for my portfolio site, **[saksham-gif.github.io](https://saksham-gif.github.io/)**, built with **Python, Playwright and pytest** and run automatically through a **GitHub Actions CI pipeline**.

## Why I built it

My portfolio is a live web app with interactive, expandable project cards. Every time I edit it, something can quietly break: a card stops expanding, a nav link points nowhere, or the layout overflows on a phone. This suite catches those regressions automatically, on every push and every Monday, before a recruiter ever sees a broken page.

## What it tests

| Area | Test | What it checks |
|---|---|---|
| Page load | `test_page_loads_with_correct_title` | Site loads and the title is correct |
| Navigation | `test_nav_shows_name_and_section_links` | Name and Projects / Skills / Contact links are visible |
| Navigation | `test_nav_links_point_to_existing_sections` | Every nav anchor targets a section that exists |
| Navigation | `test_clicking_projects_link_scrolls_to_projects` | Clicking "Projects" updates the URL and scrolls the section into view |
| Project cards | `test_project_cards_are_present` | Cards exist and every card has a title |
| Project cards | `test_card_expands_and_collapses_on_click` | Click opens details and flips the hint text; a second click closes it |
| Project cards | `test_only_one_card_open_at_a_time` | Opening one card closes the others |
| Project cards | `test_every_card_has_skill_tags` | Every card lists its skill tags |
| Contact | `test_contact_links_are_valid` | Email (`mailto:`) and LinkedIn links are present and well-formed |
| Responsive | `test_mobile_layout_has_no_horizontal_scroll` | No sideways scrolling at phone width (390 px) |
| Responsive | `test_project_cards_work_on_mobile` | Cards still expand on a phone-sized viewport |

**11 tests.** I verified they catch real bugs: removing the card-toggle line from the site's JavaScript makes 3 of them fail.

## How it's built

```
portfolio-ui-tests/
├── .github/workflows/ui-tests.yml   # CI pipeline: runs on push, PR, weekly and on demand
├── tests/
│   ├── conftest.py                  # Playwright browser + desktop/mobile page fixtures
│   └── test_portfolio.py            # the 11 UI tests
├── pytest.ini
└── requirements.txt
```

- **Playwright (Python)** drives a real headless Chromium browser and uses auto-waiting `expect` assertions, so there are no fixed sleeps or flaky timing.
- **pytest fixtures** give every test a fresh browser context, at a desktop (1280×800) or a phone (390×844) viewport.
- **`BASE_URL`** is an environment variable, so the same suite can test the live site or a local copy before deploying.
- **GitHub Actions** installs Python and Chromium, runs the suite, and uploads a JUnit XML report as a build artifact.

## Run it locally

```bash
pip install -r requirements.txt
python -m playwright install chromium
pytest                                         # tests the live site
BASE_URL=http://localhost:8000/ pytest         # tests a local copy
```

## Next steps

- Visual regression screenshots with Playwright's `to_have_screenshot`
- A link checker that verifies every external link returns HTTP 200
- Run the suite against each pull request's preview before it merges to the live site

---
Built by **Saksham Sharma**, Mechatronics Engineering, Humber Polytechnic · [LinkedIn](https://www.linkedin.com/in/saksham-sharma-4862092b2)
