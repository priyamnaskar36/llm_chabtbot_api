import requests
from bs4 import BeautifulSoup
import json
import os

# Create data directory if it doesn't exist
os.makedirs("../data", exist_ok=True)

def scrape_page(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        text = soup.get_text(separator=' ', strip=True)
        return text
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return None

# Starter URLs (safe, simple pages)
urls = [
    "https://www.changiairport.com/en/airport-guide.html",
    "https://www.jewelchangiairport.com/en/attractions.html",
"https://www.changiairport.com/en/maps.html",
    "https://www.changiairport.com/en/dining.html",
    "https://www.changiairport.com/en/attractions/jewel.html",
    "https://www.changiairport.com/in/en/search.html?searchTerm=dine",
    "https://www.changiairport.com/in/en/fly/flight-information.html",
    "https://www.changiairport.com/in/en/fly/arrival-guide.html",
    "https://www.changiairport.com/in/en/fly/flight-information/arrivals.html",
    "https://www.changiairport.com/in/en/fly/flight-information/departures.html",
    "https://www.changiairport.com/in/en/fly/flight-information/freighter/arrivals.html",
    "https://www.ica.gov.sg/enter-transit-depart/entering-singapore",
    "https://www.changiairport.com/in/en/fly/arrival-guide/immigration.html",
    "https://www.changiairport.com/in/en/fly/dutiable-and-prohibited-items.html",
    "https://www.changiairport.com/in/en/fly/arrival-guide/baggage-services.html",
    "https://www.changiairport.com/in/en/at-changi/facilities-and-services-directory/changi-airport-lost-and-found-services-retrieve-your-lost-items.html",
    "https://www.changiairport.com/in/en/at-changi/facilities-and-services-directory/passenger-meeting-services.html",
    "https://www.changiairport.com/in/en/at-changi/transport-and-directions/leaving-the-airport.html",
    "https://www.changiairport.com/in/en/fly/getting-started-in-singapore.html",
    "https://www.changiairport.com/in/en/fly/departure-guide.html",
    "https://www.changiairport.com/in/en/fly/departure-guide/pre-flight-check.html",
    "https://www.changiairport.com/in/en/at-changi/transport-and-directions/getting-to-changi-airport.html",
    "https://www.changiairport.com/in/en/fly/departure-guide/early-check-in-services.html",
    "https://www.changiairport.com/in/en/fly/departure-guide/fast-check-in.html",
    "https://www.changiairport.com/in/en/fly/departure-guide/immigration.html",
    "https://www.changiairport.com/in/en/experience/tours/free-singapore-tour.html",
    "https://www.changiairport.com/in/en/at-changi/facilities-and-services-directory/transit-hotels.html",
    "https://www.changiairport.com/in/en/fly/lounges.html",
    "https://www.changiairport.com/in/en/at-changi/facilities-and-services-directory/explore-changi-airport-lounges-airline-lounges-information.html",
    "https://www.changiairport.com/in/en/at-changi/facilities-and-services-directory/pay-per-use-lounges.html",
    "https://www.changiairport.com/in/en/at-changi/facilities-and-services-directory/free-snooze-lounges-changi-airport-rest-areas.html",
    "https://www.changiairport.com/in/en/at-changi/facilities-and-services-directory/shower-and-spa-services.html",
    "https://www.changiairport.com/in/en/fly/airline-information.html",
    "https://www.changiairport.com/in/en/fly/airline-information/passenger.html",
    "https://www.changiairport.com/in/en/fly/airline-information/freighter.html",
    "https://www.changiairport.com/in/en/at-changi/terminal-guides.html",
    "https://www.changiairport.com/in/en/at-changi/terminal-guides/terminal-1.html",
    "https://www.changiairport.com/in/en/at-changi/terminal-guides/terminal-2.html",
    "https://www.changiairport.com/in/en/at-changi/terminal-guides/terminal-3.html",
    "https://www.changiairport.com/in/en/at-changi/terminal-guides/terminal-4.html",
    "https://www.changiairport.com/in/en/at-changi/transport-and-directions.html",
    "https://www.changiairport.com/in/en/at-changi/transport-and-directions/transferring-between-terminals-jewel.html",
    "https://www.changiairport.com/in/en/at-changi/transport-and-directions/getting-to-changi-airport.html",
    "https://www.changiairport.com/in/en/at-changi/transport-and-directions/leaving-the-airport.html",
    "https://www.changiairport.com/in/en/at-changi/transport-and-directions/coach-to-johor-bahru.html",
    "https://www.changiairport.com/in/en/at-changi/facilities-and-services-directory/airport-parking.html",
    "https://www.changiairport.com/in/en/at-changi/special-assistance.html",
    "https://www.changiairport.com/in/en/at-changi/special-assistance.html?linkedListSection=children",
    "https://www.changiairport.com/in/en/at-changi/special-assistance.html?linkedListSection=reduced-mobility",
    "https://www.changiairport.com/in/en/at-changi/special-assistance.html?linkedListSection=invisible-disability",
    "https://www.changiairport.com/in/en/at-changi/special-assistance.html?linkedListSection=other",
    "https://www.changiairport.com/in/en/at-changi/facilities-and-services-directory.html",
    "https://www.changiairport.com/in/en/at-changi/facilities-and-services-directory.html?category=amenities",
    "https://www.changiairport.com/in/en/at-changi/facilities-and-services-directory.html?category=assistance",
    "https://www.changiairport.com/in/en/at-changi/facilities-and-services-directory.html?category=baggage",
    "https://www.changiairport.com/in/en/at-changi/facilities-and-services-directory.html?category=digital-travel-services",
    "https://www.changiairport.com/in/en/at-changi/facilities-and-services-directory.html?category=facilities",
    "https://www.changiairport.com/in/en/at-changi/facilities-and-services-directory.html?category=health-wellness",
    "https://www.changiairport.com/in/en/at-changi/facilities-and-services-directory.html?category=hotels",
    "https://www.changiairport.com/in/en/at-changi/facilities-and-services-directory.html?category=lounges",
    "https://www.changiairport.com/in/en/at-changi/facilities-and-services-directory.html?category=other-services",
    "https://www.changiairport.com/in/en/at-changi/facilities-and-services-directory.html?category=transportation",
    "https://www.changiairport.com/in/en/at-changi/facilities-and-services-directory.html?category=hotels",
    "https://www.changiairport.com/in/en/at-changi/facilities-and-services-directory/transit-hotels.html",
    "https://www.changiairport.com/in/en/at-changi/facilities-and-services-directory/yotelair-singapore-changi-airport.html",
    "https://www.jewelchangiairport.com/en.html",
    "https://www.jewelchangiairport.com/en/travellers-information.html",
    "https://www.jewelchangiairport.com/en/attractions.html",
    "https://www.jewelchangiairport.com/en/shop.html",
    "https://www.jewelchangiairport.com/en/dine.html",
    "https://www.jewelchangiairport.com/en/stay-yotel.html"
    "https://www.changiairport.com/in/en/at-changi/plan-your-events.html",
    "https://www.changiairport.com/in/en/at-changi/plan-your-events/corporate-events-.html",
    "https://www.changiairport.com/in/en/at-changi/plan-your-events/weddings-at-changi-airport.html",
    "https://www.changiairport.com/in/en/at-changi/plan-your-events/birthday-parties.html",
    "https://www.changiairport.com/in/en/dine-and-shop/dining-directory.html",
    "https://www.changiairport.com/in/en/dine-and-shop/dining-directory.html?dietaryPreferences=&advancedFilter=cafe",
    "https://www.changiairport.com/in/en/dine-and-shop/dining-directory.html?dietaryPreferences=&advancedFilter=fast-food",
    "https://www.changiairport.com/in/en/dine-and-shop/dining-directory.html?dietaryPreferences=&advancedFilter=fine-dining",
    "https://www.changiairport.com/in/en/dine-and-shop/dining-directory.html?dietaryPreferences=&advancedFilter=food-court",
    "https://www.changiairport.com/in/en/dine-and-shop/dining-directory.html?dietaryPreferences=&advancedFilter=homegrown",
    "https://www.changiairport.com/in/en/dine-and-shop/dining-directory.html?dietaryPreferences=&advancedFilter=pubs-%26-bars",
    "https://www.changiairport.com/in/en/dine-and-shop/dining-directory.html?dietaryPreferences=&advancedFilter=restaurant",
    "https://www.changiairport.com/in/en/dine-and-shop/shop-directory.html",
    "https://www.changiairport.com/in/en/dine-and-shop/shop-directory.html?category=beauty",
    "https://www.changiairport.com/in/en/dine-and-shop/shop-directory.html?category=children-%26-maternity",
    "https://www.changiairport.com/in/en/dine-and-shop/shop-directory.html?category=deli-%26-confectionary",
    "https://www.changiairport.com/in/en/dine-and-shop/shop-directory.html?category=electronics",
    "https://www.changiairport.com/in/en/dine-and-shop/shop-directory.html?category=entertainment",
    "https://www.changiairport.com/in/en/dine-and-shop/shop-directory.html?category=fashion-%26-accessories",
    "https://www.changiairport.com/in/en/dine-and-shop/shop-directory.html?category=health-%26-wellness",
    "https://www.changiairport.com/in/en/dine-and-shop/shop-directory.html?category=home-%26-living",
    "https://www.changiairport.com/in/en/dine-and-shop/shop-directory.html?category=homegrown",
    "https://www.changiairport.com/in/en/dine-and-shop/shop-directory.html?category=lifestyle",
    "https://www.changiairport.com/in/en/dine-and-shop/shop-directory.html?category=luxury",
    "https://www.changiairport.com/in/en/dine-and-shop/shop-directory.html?category=optical",
    "https://www.changiairport.com/in/en/help/changi-app/changi-pay.html",
    "https://www.changiairport.com/in/en/rewards.html",
    "https://www.changiairport.com/in/en/dine-and-shop/shopping-concierge.html",
    "https://www.changiairport.com/in/en/experience/attractions-directory.html",
    "https://www.changiairport.com/in/en/experience/attractions-directory.html?category=art",
    "https://www.changiairport.com/in/en/experience/attractions-directory.html?category=gardens",
    "https://www.changiairport.com/in/en/experience/attractions-directory.html?category=play",
    "https://www.changiairport.com/in/en/experience/kids.html",
    "https://www.changiairport.com/in/en/experience/attractions-directory.html?category=play",
    "https://nowboarding.changiairport.com/discover-changi/free-things-to-do-at-changi-airport.html",
    "https://www.changiairport.com/en/corporate/about-us/learning-journeys.html",
    "https://www.changiairport.com/in/en/experience/tours.html",
    "https://www.changiairport.com/in/en/experience/tours/free-singapore-tour.html",
    "https://www.changiairport.com/in/en/experience/tours/changi-airport-tours.html",
    "https://www.jewelchangiairport.com/en/JewelGuidedTours.html",
    "https://www.changiairport.com/in/en/happenings/events-directory.html",
    "https://www.changiairport.com/in/en/happenings/events-directory/changi-first.html",
    "https://www.changiairport.com/in/en/happenings/promotions.html",
    "https://www.changiairport.com/in/en/rewards/members-special.html",
    "https://www.changiairport.com/in/en/rewards/benefits-and-privileges.html",
    "https://www.changiairport.com/in/en/rewards/benefits-and-privileges.html",
    "https://www.changiairport.com/in/en/rewards/members-special/parking-benefits.html",
    "https://www.changiairport.com/in/en/rewards/catalogue.html",
    "https://www.changiairport.com/in/en/rewards/members-special.html",
    "https://www.changiairport.com/in/en/rewards/members-events.html",
    "https://www.changiairport.com/in/en/rewards/monarch.html",
    "https://www.changiairport.com/in/en/rewards/monarch.html?linkedListSection=about",
    "https://www.changiairport.com/in/en/rewards/monarch.html?linkedListSection=benefits",
    "https://www.changiairport.com/in/en/rewards/monarch.html?linkedListSection=specials",
    "https://www.changiairport.com/in/en/rewards/monarch.html?linkedListSection=concierge",
    "https://www.changiairport.com/in/en/rewards/monarch.html?linkedListSection=parking",
    "https://www.changiairport.com/in/en/rewards/monarch.html?linkedListSection=faq",
    "https://www.changiairport.com/in/en/rewards/faq.html",
    "https://www.changiairport.com/in/en/rewards/changi-rewards-terms-and-conditions.html",
    "https://www.changiairport.com/in/en/rewards/feedback.html",
    "https://www.changiairport.com/in/en/help/assistance.html",
    "https://www.changiairport.com/in/en/at-changi/facilities-and-services-directory/changi-airport-lost-and-found-services-retrieve-your-lost-items.html",
    "https://www.changiairport.com/in/en/at-changi/special-assistance.html",
    "https://www.changiairport.com/in/en/help/assistance/faq.html",
    "https://www.changiairport.com/in/en/help/changi-app.html",
    "https://www.changiairport.com/in/en/help/changi-app/key-travel-features.html",
    "https://www.changiairport.com/in/en/help/changi-app/baggage-tracker.html",
    "https://www.changiairport.com/in/en/help/changi-app/book-redeem-play.html",
    "https://www.changiairport.com/in/en/help/changi-app/dine.html",
    "https://www.changiairport.com/in/en/help/changi-app/changi-pay.html",
    "https://www.changiairport.com/in/en/help/changi-app/faq.html",
    "https://www.changiairport.com/in/en/help/changi-app/download-qr.html",
    "https://www.changiairport.com/in/en/happenings/events-directory/miffy-celebration-quest.html"
]

results = []

for url in urls:
    print(f"🔍 Scraping: {url}")
    text = scrape_page(url)
    if text:
        results.append({
            "url": url,
            "content": text[:5000]  # limit to 5000 chars for simplicity
        })


output_path = "../data/changi_cleaned_chunks.json"
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print(f"Scraping complete. Data saved to {output_path}")
