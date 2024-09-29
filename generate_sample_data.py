# generate_sample_data.py

import os
import requests
from bs4 import BeautifulSoup
from typing import List, Dict

sample_contents = [
    {
        'title': 'Lithium-Ion Battery Basics',
        'body': 'Lithium-ion batteries are a type of rechargeable battery that are widely used in consumer electronics, electric vehicles, and energy storage systems. These batteries are known for their high energy density, which allows them to store a large amount of energy in a relatively small and lightweight package. Additionally, they exhibit low self-discharge rates, meaning they retain their charge for longer periods when not in use. The electrochemical performance of lithium-ion batteries is characterized by their Time in Field (TIF) and Total Operating Time (TOT). For instance, a typical lithium-ion battery with a TIF of 365 days and a TOT of 8760 hours demonstrates excellent longevity and reliability. These metrics are crucial for applications where long-term performance and durability are essential. The internal structure of lithium-ion batteries includes a positive electrode (cathode), a negative electrode (anode), a separator, and an electrolyte. The choice of materials for these components, such as lithium cobalt oxide for the cathode and graphite for the anode, significantly impacts the battery\'s overall performance, including its capacity, voltage, and cycle life. Advances in battery engineering continue to focus on improving energy density, enhancing safety features, and extending the operational lifespan of lithium-ion batteries.'
    },
    {
        'title': 'Battery Safety Guidelines',
        'body': 'Proper handling of lithium-ion batteries is essential to prevent safety hazards like overheating or explosion. Recent studies on batteries with a TIF of 180 days and a TOT of 4320 hours have shown that following safety guidelines can significantly reduce risks.'
    },
    {
        'title': 'Charging Techniques for Batteries',
        'body': 'Meeting Minutes: Swollen Battery Issue in Field\n\nDate: 2023-09-15\n\nAttendees:\n- John Doe (Field Engineer)\n- Jane Smith (Battery Specialist)\n- Mark Johnson (Safety Officer)\n\nAgenda:\n1. Overview of the swollen battery issue\n2. Field observations and data collection\n3. Analysis of potential causes\n4. Safety measures and mitigation strategies\n5. Action items and next steps\n\nDiscussion:\nJohn Doe provided an overview of the swollen battery issue observed in several field units. The affected batteries exhibited a noticeable bulge, indicating potential internal pressure buildup. Jane Smith presented data collected from the field, including Time in Field (TIF) of 120 days and Total Operating Time (TOT) of 2880 hours for the affected units. The team discussed possible causes, such as overcharging, exposure to high temperatures, and manufacturing defects. Mark Johnson emphasized the importance of immediate safety measures, including isolating affected units and conducting thorough inspections. The team agreed on a set of action items, including further analysis of the affected batteries, implementation of additional safety protocols, and regular monitoring of field units to prevent recurrence.'
    },
    {
        'title': 'Meeting with Battery Vendor',
        'body': 'Meeting Minutes: Discussion with Battery Vendor\n\nDate: 2023-10-01\n\nAttendees:\n- Alice Brown (Procurement Manager)\n- Bob White (Vendor Representative)\n- Carol Green (Technical Lead)\n\nAgenda:\n1. Introduction and objectives\n2. Vendor presentation on battery specifications\n3. Discussion on pricing and delivery schedules\n4. Technical Q&A session\n5. Next steps and action items\n\nDiscussion:\nAlice Brown opened the meeting by outlining the objectives, which included understanding the vendor\'s battery offerings and evaluating their suitability for our projects. Bob White presented the specifications of their latest lithium-ion batteries, highlighting their high energy density, safety features, and long cycle life. Carol Green led the technical Q&A session, addressing questions about the battery\'s performance metrics, including Time in Field (TIF) of 365 days and Total Operating Time (TOT) of 8760 hours. The team discussed potential integration challenges and mitigation strategies. The meeting concluded with a summary of action items, including a follow-up technical review and a detailed cost analysis.'
    },
    {
        'title': 'Thermal Management in Batteries',
        'body': 'Effective thermal management is crucial for battery performance and safety, especially in high-drain applications. Long-term studies on batteries with a TIF of 545 days and a TOT of 13080 hours highlight the importance of advanced cooling systems in maintaining battery health.'
    }
]

# Add the Apple Support URL
apple_support_url = 'https://support.apple.com/en-us/108055'
sample_contents.append({
    'title': 'About Optimized Battery Charging on your iPhone',
    'body': f'This content is retrieved from {apple_support_url}',
    'url': apple_support_url
})

def generate_html_content(content: Dict[str, str]) -> str:
    """Generate HTML content for a given dictionary of content."""
    title = content['title']
    body = content['body']
    url = content.get('url')

    html_content = f"""
    <html>
    <head>
        <title>{title}</title>
    </head>
    <body>
        <h1>{title}</h1>
        <p>{body}</p>
        {f'<a href="{url}">Read more</a>' if url else ''}
    </body>
    </html>
    """
    return html_content.strip()

def fetch_apple_support_content(url: str) -> str:
    """Fetch content from Apple Support URL."""
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    main_content = soup.find('main', class_='main')
    return str(main_content) if main_content else "Content not found"

def generate_sample_data(sample_contents: List[Dict[str, str]]) -> None:
    """Generate sample HTML files from the given content."""
    os.makedirs('data', exist_ok=True)

    for i, content in enumerate(sample_contents, start=1):
        html_content = generate_html_content(content)
        
        with open(f'data/sample{i}.html', 'w', encoding='utf-8') as f:
            f.write(html_content)

    print("Sample data generated successfully.")

if __name__ == "__main__":
    generate_sample_data(sample_contents)
