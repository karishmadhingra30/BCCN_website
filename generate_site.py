#!/usr/bin/env python3
"""
Generate BCCN static site structure based on the new Information Architecture
"""

import os
import json
from pathlib import Path

BASE_URL = "/BCCN_website"

# Page tagging system for category filters
PAGE_TAGS = {
    # Home page
    '/': ['students', 'faculty-and-staff', 'off-campus-partners', 'media', 'funders-and-investors'],

    # About section
    '/about/': ['students', 'faculty-and-staff', 'off-campus-partners', 'media', 'funders-and-investors'],

    # Students section
    '/students/': ['students'],
    '/students/climate-classes/': ['students', 'faculty-and-staff'],
    '/students/internships-and-jobs/': ['students', 'off-campus-partners'],
    '/students/clubs-and-organizations/': ['students'],
    '/students/hot-topics/': ['students', 'media'],

    # Faculty & Staff section
    '/faculty-and-staff/': ['faculty-and-staff'],
    '/faculty-and-staff/people-projects-and-programs/': ['faculty-and-staff', 'off-campus-partners', 'funders-and-investors'],
    '/faculty-and-staff/financial-support/': ['faculty-and-staff', 'funders-and-investors'],
    '/faculty-and-staff/hot-topics/': ['faculty-and-staff', 'media'],
    '/faculty-and-staff/find-help/': ['faculty-and-staff', 'students', 'off-campus-partners'],

    # BCCN Resources
    '/bccn-resources/': ['students', 'faculty-and-staff', 'off-campus-partners'],
    '/bccn-resources/bccn-campus-climate-news/': ['students', 'faculty-and-staff', 'media'],
    '/bccn-resources/podcasts-and-videos/': ['students', 'faculty-and-staff', 'media', 'off-campus-partners'],
    '/bccn-resources/hot-topics/': ['students', 'faculty-and-staff', 'media'],

    # Off-Campus Partners
    '/off-campus-partners/': ['off-campus-partners', 'faculty-and-staff'],

    # Media
    '/media/media-inquiries/': ['media', 'faculty-and-staff'],

    # Funders & Investors
    '/funders-and-investors/': ['funders-and-investors', 'off-campus-partners'],

    # Sponsors (referenced in user's mapping)
    '/resources-and-tools/give-and-sponsor/': ['off-campus-partners', 'funders-and-investors', 'media'],
}

# Filter category metadata
FILTER_CATEGORIES = {
    'students': {
        'title': 'Students',
        'slug': 'students',
    },
    'faculty-and-staff': {
        'title': 'Faculty & Staff',
        'slug': 'faculty-and-staff',
    },
    'off-campus-partners': {
        'title': 'Off-Campus Partners',
        'slug': 'off-campus-partners',
    },
    'media': {
        'title': 'Media',
        'slug': 'media',
    },
    'funders-and-investors': {
        'title': 'Funders/Investors',
        'slug': 'funders-and-investors',
    },
}

# Page template
def create_page_template(title, breadcrumb, content, show_audience_filter=False, is_placeholder=False):
    """Create an HTML page from template"""

    placeholder_badge = '<span class="placeholder-badge">PLACEHOLDER</span>' if is_placeholder else ''
    audience_script = ""

    if not show_audience_filter:
        audience_script = """
    <script>
      // Hide audience filter on pages that don't need it
      window.addEventListener('DOMContentLoaded', function() {
        var filter = document.getElementById('audience-filter');
        if (filter) filter.style.display = 'none';
      });
    </script>"""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} - Berkeley Climate Change Network</title>
  <link rel="icon" href="https://bccn.berkeley.edu/sites/default/files/favicon.ico" type="image/x-icon">
</head>
<body>
  <div id="global-nav"></div>

  <main>
    {breadcrumb}
    <h1>{title}{placeholder_badge}</h1>
    {content}
  </main>

  <footer>
    <div class="container">
      <div class="card-grid">
        <div>
          <h3 style="color: #FDB515;">Quick Links</h3>
          <p><a href="{BASE_URL}/about/contact-and-help/">Get Help</a></p>
          <p><a href="{BASE_URL}/about/">About BCCN</a></p>
          <p><a href="https://www.berkeley.edu/">UC Berkeley</a></p>
        </div>
        <div>
          <h3 style="color: #FDB515;">Resources</h3>
          <p><a href="{BASE_URL}/resources-and-tools/">Resources & Tools</a></p>
          <p><a href="{BASE_URL}/programs-and-opportunities/">Programs</a></p>
        </div>
        <div>
          <h3 style="color: #FDB515;">Connect</h3>
          <p><a href="{BASE_URL}/news-events-community/">News & Events</a></p>
          <p><a href="{BASE_URL}/media/media-inquiries/">Media Inquiries</a></p>
        </div>
      </div>
      <p style="margin-top: 30px; text-align: center; color: #FDB515;">&copy; 2024 Berkeley Climate Change Network. All rights reserved.</p>
    </div>
  </footer>

  <script>
    fetch('{BASE_URL}/nav.html')
      .then(r => r.text())
      .then(html => {{
        document.getElementById('global-nav').innerHTML = html;
      }});
  </script>
  {audience_script}
</body>
</html>"""

def create_breadcrumb(crumbs):
    """Create breadcrumb navigation"""
    if not crumbs:
        return ""

    parts = ['<nav class="breadcrumb">']
    for i, (name, url) in enumerate(crumbs):
        if i > 0:
            parts.append(' &gt; ')
        if url:
            parts.append(f'<a href="{url}">{name}</a>')
        else:
            parts.append(name)
    parts.append('</nav>')
    return ''.join(parts)

def lorem_ipsum():
    """Return lorem ipsum placeholder text"""
    return """
    <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
    Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.</p>

    <p>Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.
    Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.</p>"""

def create_card_links(links):
    """Create a grid of card links"""
    cards = ['<div class="card-grid">']
    for title, url, is_placeholder in links:
        badge = '<span class="placeholder-badge">PLACEHOLDER</span>' if is_placeholder else ''
        cards.append(f"""
        <div class="card">
          <h3><a href="{url}">{title}</a>{badge}</h3>
          <p>Learn more about {title.lower()}.</p>
        </div>""")
    cards.append('</div>')
    return ''.join(cards)

def ensure_dir(path):
    """Ensure directory exists"""
    Path(path).mkdir(parents=True, exist_ok=True)

def write_page(path, content):
    """Write page content to file"""
    ensure_dir(os.path.dirname(path))
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Created: {path}")

# Define all pages to generate
pages = []

# HOME PAGE
pages.append({
    'path': 'index.html',
    'title': 'Home',
    'breadcrumb': [],
    'show_audience_filter': False,
    'content': f"""
    <div style="background: linear-gradient(135deg, #003262 0%, #3B7EA1 100%); color: white; padding: 60px 40px; margin: -40px -20px 40px -20px; text-align: center; border-radius: 8px;">
      <h2 style="color: #FDB515; font-size: 42px; margin-bottom: 20px;">Welcome to the Berkeley Climate Change Network</h2>
      <p style="font-size: 20px; max-width: 800px; margin: 0 auto;">Connecting the UC Berkeley community in climate research, education, and action.</p>
    </div>

    <h2>Explore BCCN</h2>
    {create_card_links([
        ('About BCCN', f'{BASE_URL}/about/', False),
        ('Programs & Opportunities', f'{BASE_URL}/programs-and-opportunities/', False),
        ('People & Partners', f'{BASE_URL}/people-and-partners/', False),
        ('Resources & Tools', f'{BASE_URL}/resources-and-tools/', False),
        ('News, Events & Community', f'{BASE_URL}/news-events-community/', False),
    ])}

    <h2 style="margin-top: 50px;">Quick Access</h2>
    {create_card_links([
        ('For Faculty & Staff', f'{BASE_URL}/faculty-and-staff/', False),
        ('For Students', f'{BASE_URL}/students/', False),
        ('For Partners', f'{BASE_URL}/off-campus-partners/', False),
        ('Get Help', f'{BASE_URL}/about/contact-and-help/', False),
    ])}
    """
})

# ABOUT SECTION
pages.append({
    'path': 'about/index.html',
    'title': 'About BCCN',
    'breadcrumb': [('Home', f'{BASE_URL}/'), ('About BCCN', None)],
    'show_audience_filter': False,
    'content': f"""
    {lorem_ipsum()}

    <h2>Learn More</h2>
    {create_card_links([
        ('Contact & Get Help', f'{BASE_URL}/about/contact-and-help/', False),
        ('Our Network & Governance', f'{BASE_URL}/about/our-network-governance/', True),
    ])}
    """
})

pages.append({
    'path': 'about/contact-and-help/index.html',
    'title': 'Contact and Help',
    'breadcrumb': [('Home', f'{BASE_URL}/'), ('About', f'{BASE_URL}/about/'), ('Contact and Help', None)],
    'show_audience_filter': False,
    'content': f"""
    <h2>Find HELP!</h2>
    {lorem_ipsum()}

    <h2>Contact Information</h2>
    <p>For general inquiries about BCCN, please reach out to our team.</p>
    {lorem_ipsum()}
    """
})

pages.append({
    'path': 'about/our-network-governance/index.html',
    'title': 'Our Network Governance',
    'breadcrumb': [('Home', f'{BASE_URL}/'), ('About', f'{BASE_URL}/about/'), ('Network Governance', None)],
    'show_audience_filter': False,
    'is_placeholder': True,
    'content': lorem_ipsum()
})

# PROGRAMS & OPPORTUNITIES SECTION
pages.append({
    'path': 'programs-and-opportunities/index.html',
    'title': 'Programs & Opportunities',
    'breadcrumb': [('Home', f'{BASE_URL}/'), ('Programs & Opportunities', None)],
    'show_audience_filter': True,
    'content': f"""
    {lorem_ipsum()}

    <h2>Explore Opportunities</h2>
    {create_card_links([
        ('Climate Classes', f'{BASE_URL}/programs-and-opportunities/climate-classes/', False),
        ('Internships & Jobs', f'{BASE_URL}/programs-and-opportunities/internships-and-jobs/', False),
        ('Clubs & Organizations', f'{BASE_URL}/programs-and-opportunities/clubs-and-organizations/', False),
        ('Research & Mentoring Programs', f'{BASE_URL}/programs-and-opportunities/research-and-mentoring/', False),
        ('Funding & Grants', f'{BASE_URL}/programs-and-opportunities/funding-and-grants/', False),
        ('Partner Programs', f'{BASE_URL}/programs-and-opportunities/partner-programs/', False),
    ])}
    """
})

# Programs sub-pages
program_pages = [
    ('climate-classes', 'Climate Classes'),
    ('internships-and-jobs', 'Internships and Jobs'),
    ('clubs-and-organizations', 'Clubs and Organizations'),
    ('research-and-mentoring', 'Research and Mentoring Programs'),
    ('funding-and-grants', 'Funding and Grants'),
    ('partner-programs', 'Partner Programs'),
]

for slug, title in program_pages:
    pages.append({
        'path': f'programs-and-opportunities/{slug}/index.html',
        'title': title,
        'breadcrumb': [('Home', f'{BASE_URL}/'), ('Programs & Opportunities', f'{BASE_URL}/programs-and-opportunities/'), (title, None)],
        'show_audience_filter': True,
        'content': lorem_ipsum()
    })

# PEOPLE & PARTNERS SECTION
pages.append({
    'path': 'people-and-partners/index.html',
    'title': 'People & Partners',
    'breadcrumb': [('Home', f'{BASE_URL}/'), ('People & Partners', None)],
    'show_audience_filter': True,
    'content': f"""
    {lorem_ipsum()}

    <h2>Connect With Our Community</h2>
    {create_card_links([
        ('Faculty & Staff', f'{BASE_URL}/faculty-and-staff/', False),
        ('Student Leaders', f'{BASE_URL}/students/', False),
        ('Off-Campus Partners', f'{BASE_URL}/off-campus-partners/', False),
        ('Funders & Investors', f'{BASE_URL}/funders-and-investors/', False),
        ('Media Contacts', f'{BASE_URL}/media/', False),
        ('People Directory', f'{BASE_URL}/people-and-partners/people-directory/', True),
    ])}
    """
})

pages.append({
    'path': 'people-and-partners/people-directory/index.html',
    'title': 'People Directory',
    'breadcrumb': [('Home', f'{BASE_URL}/'), ('People & Partners', f'{BASE_URL}/people-and-partners/'), ('People Directory', None)],
    'show_audience_filter': True,
    'is_placeholder': True,
    'content': lorem_ipsum()
})

# RESOURCES & TOOLS SECTION
pages.append({
    'path': 'resources-and-tools/index.html',
    'title': 'Resources & Tools',
    'breadcrumb': [('Home', f'{BASE_URL}/'), ('Resources & Tools', None)],
    'show_audience_filter': True,
    'content': f"""
    {lorem_ipsum()}

    <h2>Available Resources</h2>
    {create_card_links([
        ('BCCN Resource Hub', f'{BASE_URL}/bccn-resources/', False),
        ('Student Financial Support', f'{BASE_URL}/resources-and-tools/financial-support/', False),
        ('Give & Sponsor BCCN', f'{BASE_URL}/resources-and-tools/give-and-sponsor/', False),
        ('Institutes and Centers Map', f'{BASE_URL}/resources-and-tools/institutes-and-centers-map/', False),
        ('Climate Maps & Data', f'{BASE_URL}/resources-and-tools/climate-maps-data/', True),
    ])}
    """
})

resource_pages = [
    ('financial-support', 'Financial Support', False),
    ('give-and-sponsor', 'Give and Sponsor BCCN', False),
    ('institutes-and-centers-map', 'Berkeley Institute/Center Map', False),
    ('climate-maps-data', 'Climate Maps & Data', True),
]

for slug, title, is_placeholder in resource_pages:
    pages.append({
        'path': f'resources-and-tools/{slug}/index.html',
        'title': title,
        'breadcrumb': [('Home', f'{BASE_URL}/'), ('Resources & Tools', f'{BASE_URL}/resources-and-tools/'), (title, None)],
        'show_audience_filter': True,
        'is_placeholder': is_placeholder,
        'content': lorem_ipsum()
    })

# NEWS, EVENTS & COMMUNITY SECTION
pages.append({
    'path': 'news-events-community/index.html',
    'title': 'News, Events & Community',
    'breadcrumb': [('Home', f'{BASE_URL}/'), ('News, Events & Community', None)],
    'show_audience_filter': True,
    'content': f"""
    {lorem_ipsum()}

    <h2>Stay Connected</h2>
    {create_card_links([
        ('News & Updates', f'{BASE_URL}/news-events-community/news-and-updates/', False),
        ('Events & Community', f'{BASE_URL}/news-events-community/events-and-community/', False),
        ('Hot Topics', f'{BASE_URL}/news-events-community/hot-topics/', False),
        ('Newsletter & Mailing Lists', f'{BASE_URL}/news-events-community/newsletter/', False),
    ])}
    """
})

news_pages = [
    ('news-and-updates', 'News and Updates'),
    ('events-and-community', 'Events and Community'),
    ('hot-topics', 'Hot Topics'),
    ('newsletter', 'Newsletter and Mailing Lists'),
    ('bccn-campus-climate-news', 'BCCN Campus Climate News'),
]

for slug, title in news_pages:
    pages.append({
        'path': f'news-events-community/{slug}/index.html',
        'title': title,
        'breadcrumb': [('Home', f'{BASE_URL}/'), ('News, Events & Community', f'{BASE_URL}/news-events-community/'), (title, None)],
        'show_audience_filter': True,
        'content': lorem_ipsum()
    })

# FACULTY & STAFF SECTION
pages.append({
    'path': 'faculty-and-staff/index.html',
    'title': 'Faculty and Staff',
    'breadcrumb': [('Home', f'{BASE_URL}/'), ('Faculty and Staff', None)],
    'show_audience_filter': True,
    'content': f"""
    {lorem_ipsum()}

    <h2>Faculty & Staff Resources</h2>
    {create_card_links([
        ('People, Projects and Programs', f'{BASE_URL}/faculty-and-staff/people-projects-and-programs/', False),
        ('Financial Support', f'{BASE_URL}/faculty-and-staff/financial-support/', False),
        ('Find HELP!', f'{BASE_URL}/faculty-and-staff/find-help/', False),
        ('Media Coverage', f'{BASE_URL}/faculty-and-staff/media-coverage/', False),
        ('Hot Topics', f'{BASE_URL}/faculty-and-staff/hot-topics/', False),
    ])}
    """
})

faculty_pages = [
    ('people-projects-and-programs', 'People, Projects and Programs'),
    ('financial-support', 'Financial Support'),
    ('find-help', 'Find HELP!'),
    ('media-coverage', 'Media Coverage'),
    ('hot-topics', 'Hot Topics'),
]

for slug, title in faculty_pages:
    pages.append({
        'path': f'faculty-and-staff/{slug}/index.html',
        'title': title,
        'breadcrumb': [('Home', f'{BASE_URL}/'), ('Faculty and Staff', f'{BASE_URL}/faculty-and-staff/'), (title, None)],
        'show_audience_filter': True,
        'content': lorem_ipsum()
    })

# STUDENTS SECTION
pages.append({
    'path': 'students/index.html',
    'title': 'Students',
    'breadcrumb': [('Home', f'{BASE_URL}/'), ('Students', None)],
    'show_audience_filter': True,
    'content': f"""
    {lorem_ipsum()}

    <h2>Student Resources</h2>
    {create_card_links([
        ('Climate Classes', f'{BASE_URL}/students/climate-classes/', False),
        ('Internships and Jobs', f'{BASE_URL}/students/internships-and-jobs/', False),
        ('Clubs and Organizations', f'{BASE_URL}/students/clubs-and-organizations/', False),
        ('Researchers, Mentors and Projects', f'{BASE_URL}/students/researchers-mentors-and-projects/', False),
        ('Hot Topics', f'{BASE_URL}/students/hot-topics/', False),
    ])}
    """
})

student_pages = [
    ('climate-classes', 'Climate Classes'),
    ('internships-and-jobs', 'Internships and Jobs'),
    ('clubs-and-organizations', 'Clubs and Organizations'),
    ('researchers-mentors-and-projects', 'Researchers, Mentors and Projects'),
    ('hot-topics', 'Hot Topics'),
]

for slug, title in student_pages:
    pages.append({
        'path': f'students/{slug}/index.html',
        'title': title,
        'breadcrumb': [('Home', f'{BASE_URL}/'), ('Students', f'{BASE_URL}/students/'), (title, None)],
        'show_audience_filter': True,
        'content': lorem_ipsum()
    })

# BCCN RESOURCES (Cool BCCN Resources)
pages.append({
    'path': 'bccn-resources/index.html',
    'title': 'BCCN Resource Hub',
    'breadcrumb': [('Home', f'{BASE_URL}/'), ('BCCN Resource Hub', None)],
    'show_audience_filter': True,
    'content': f"""
    {lorem_ipsum()}

    <h2>Cool BCCN Resources</h2>
    {create_card_links([
        ('Podcasts and Videos', f'{BASE_URL}/bccn-resources/podcasts-and-videos/', False),
        ('In-Person Events and Webinars', f'{BASE_URL}/bccn-resources/events-and-webinars/', False),
        ('Hot Topics', f'{BASE_URL}/bccn-resources/hot-topics/', False),
        ('Campus Climate News', f'{BASE_URL}/bccn-resources/bccn-campus-climate-news/', False),
        ('Berkeley Climate Calendar', f'{BASE_URL}/bccn-resources/berkeley-climate-calendar/', False),
        ('Climate 101', f'{BASE_URL}/bccn-resources/climate-101/', False),
    ])}
    """
})

bccn_resource_pages = [
    ('podcasts-and-videos', 'Podcasts and Videos'),
    ('events-and-webinars', 'In-Person Events and Webinars'),
    ('hot-topics', 'BCCN Global Hot Topics'),
    ('bccn-campus-climate-news', 'BCCN Campus Climate News'),
    ('berkeley-climate-calendar', 'Berkeley Climate Calendar'),
    ('climate-101', 'Climate 101'),
]

for slug, title in bccn_resource_pages:
    pages.append({
        'path': f'bccn-resources/{slug}/index.html',
        'title': title,
        'breadcrumb': [('Home', f'{BASE_URL}/'), ('BCCN Resource Hub', f'{BASE_URL}/bccn-resources/'), (title, None)],
        'show_audience_filter': True,
        'content': lorem_ipsum()
    })

# OFF-CAMPUS PARTNERS
pages.append({
    'path': 'off-campus-partners/index.html',
    'title': 'Off-campus Partners',
    'breadcrumb': [('Home', f'{BASE_URL}/'), ('People & Partners', f'{BASE_URL}/people-and-partners/'), ('Off-campus Partners', None)],
    'show_audience_filter': True,
    'content': lorem_ipsum()
})

# FUNDERS & INVESTORS
pages.append({
    'path': 'funders-and-investors/index.html',
    'title': 'Funders and Investors',
    'breadcrumb': [('Home', f'{BASE_URL}/'), ('People & Partners', f'{BASE_URL}/people-and-partners/'), ('Funders and Investors', None)],
    'show_audience_filter': True,
    'content': lorem_ipsum()
})

# MEDIA
pages.append({
    'path': 'media/index.html',
    'title': 'Media',
    'breadcrumb': [('Home', f'{BASE_URL}/'), ('People & Partners', f'{BASE_URL}/people-and-partners/'), ('Media', None)],
    'show_audience_filter': True,
    'content': f"""
    {lorem_ipsum()}

    <h2>Media Resources</h2>
    {create_card_links([
        ('Media Inquiries', f'{BASE_URL}/media/media-inquiries/', False),
        ('Press Kit', f'{BASE_URL}/media/press-kit/', False),
    ])}
    """
})

pages.append({
    'path': 'media/media-inquiries/index.html',
    'title': 'Media Inquiries',
    'breadcrumb': [('Home', f'{BASE_URL}/'), ('Media', f'{BASE_URL}/media/'), ('Media Inquiries', None)],
    'show_audience_filter': False,
    'content': lorem_ipsum()
})

pages.append({
    'path': 'media/press-kit/index.html',
    'title': 'Press Kit',
    'breadcrumb': [('Home', f'{BASE_URL}/'), ('Media', f'{BASE_URL}/media/'), ('Press Kit', None)],
    'show_audience_filter': False,
    'content': lorem_ipsum()
})

def create_filter_landing_page(category_slug):
    """Create a filter landing page for a specific category"""
    category = FILTER_CATEGORIES[category_slug]
    title = category['title']

    # Find all pages tagged with this category
    tagged_pages = []
    for page_url, tags in PAGE_TAGS.items():
        if category_slug in tags:
            # Determine page title from URL
            if page_url == '/':
                page_title = 'Home'
            else:
                # Try to extract title from the URL path
                path_parts = page_url.strip('/').split('/')
                page_title = path_parts[-1].replace('-', ' ').title()

                # Special case handling for known pages
                if page_url == '/about/':
                    page_title = 'About BCCN'
                elif page_url == '/students/':
                    page_title = 'Students'
                elif page_url == '/students/climate-classes/':
                    page_title = 'Climate Classes'
                elif page_url == '/students/internships-and-jobs/':
                    page_title = 'Internships and Jobs'
                elif page_url == '/students/clubs-and-organizations/':
                    page_title = 'Clubs and Organizations'
                elif page_url == '/students/hot-topics/':
                    page_title = 'Hot Topics Global – Students'
                elif page_url == '/faculty-and-staff/':
                    page_title = 'Faculty and Staff'
                elif page_url == '/faculty-and-staff/people-projects-and-programs/':
                    page_title = 'People, Projects and Programs'
                elif page_url == '/faculty-and-staff/financial-support/':
                    page_title = 'Financial Support'
                elif page_url == '/faculty-and-staff/hot-topics/':
                    page_title = 'Global Hot Topics – Faculty & Staff'
                elif page_url == '/faculty-and-staff/find-help/':
                    page_title = 'Find HELP!'
                elif page_url == '/bccn-resources/':
                    page_title = 'Cool BCCN Resources'
                elif page_url == '/bccn-resources/bccn-campus-climate-news/':
                    page_title = 'BCCN Campus Climate News'
                elif page_url == '/bccn-resources/podcasts-and-videos/':
                    page_title = 'Podcasts and Videos'
                elif page_url == '/bccn-resources/hot-topics/':
                    page_title = 'BCCN Global Hot Topics – central'
                elif page_url == '/off-campus-partners/':
                    page_title = 'Off Campus Partners'
                elif page_url == '/media/media-inquiries/':
                    page_title = 'Media Inquiries'
                elif page_url == '/funders-and-investors/':
                    page_title = 'Funders/Investors'
                elif page_url == '/resources-and-tools/give-and-sponsor/':
                    page_title = 'Sponsors'

            tagged_pages.append({
                'title': page_title,
                'url': f"{BASE_URL}{page_url}" if page_url != '/' else f"{BASE_URL}/"
            })

    # Sort pages alphabetically by title
    tagged_pages.sort(key=lambda x: x['title'])

    # Build the page content
    content = f"""
    <div style="background: #f9f9f9; padding: 20px; border-left: 4px solid #FDB515; margin-bottom: 30px;">
      <p style="font-style: italic; color: #666; margin: 0;">
        <strong>Note:</strong> This filter landing page is a draft. UX enhancements to follow.
      </p>
    </div>

    <p>Below are all pages relevant to <strong>{title}</strong>:</p>

    <div class="card-grid">
    """

    for page in tagged_pages:
        content += f"""
        <div class="card">
          <h3><a href="{page['url']}">{page['title']}</a></h3>
          <p>View this page</p>
        </div>
        """

    content += """
    </div>
    """

    return {
        'path': f'filter/{category_slug}/index.html',
        'title': title,
        'breadcrumb': [('Home', f'{BASE_URL}/'), (f'{title} Filter', None)],
        'show_audience_filter': True,
        'content': content
    }

# Generate all pages
def main():
    """Generate all pages"""
    base_path = '/home/user/BCCN_website'

    for page in pages:
        breadcrumb = create_breadcrumb(page['breadcrumb'])
        is_placeholder = page.get('is_placeholder', False)

        html = create_page_template(
            title=page['title'],
            breadcrumb=breadcrumb,
            content=page['content'],
            show_audience_filter=page.get('show_audience_filter', False),
            is_placeholder=is_placeholder
        )

        file_path = os.path.join(base_path, page['path'])
        write_page(file_path, html)

    # Generate filter landing pages
    filter_pages_count = 0
    for category_slug in FILTER_CATEGORIES.keys():
        filter_page = create_filter_landing_page(category_slug)
        breadcrumb = create_breadcrumb(filter_page['breadcrumb'])

        html = create_page_template(
            title=filter_page['title'],
            breadcrumb=breadcrumb,
            content=filter_page['content'],
            show_audience_filter=filter_page['show_audience_filter'],
            is_placeholder=False
        )

        file_path = os.path.join(base_path, filter_page['path'])
        write_page(file_path, html)
        filter_pages_count += 1

    print(f"\n✓ Successfully generated {len(pages)} pages!")
    print(f"✓ Successfully generated {filter_pages_count} filter landing pages!")
    print(f"✓ Site ready at: https://karishmadhingra30.github.io/BCCN_website/")

if __name__ == '__main__':
    main()
