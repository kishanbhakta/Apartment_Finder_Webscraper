import urllib3
import certifi

from bs4 import BeautifulSoup
from states import us_state_abbrev

# Get User inputs and store in list
def get_user_inputs():
    get_data = True
    user_inputs = []

    while get_data:
        state_value = input("Enter State: ").title().replace(' ','-')
        city_value = input("Enter City: ").title().replace(' ','-')
        beds_value = input("Are you looking for a studio? (Y/N) ").upper()
        if beds_value[0] == 'Y':
            beds_value = 'Studio'
        else:
            beds_value = int(input("How many beds are you looking for?: "))
            if beds_value == 1:
                beds_value = '1-Bedroom'
            else:
                beds_value = str(beds_value) + '-Bedrooms'
        min_value = int(input("Enter Minimum Amount: "))
        max_value = int(input("Enter Maximum Amount: "))

        user_inputs.append({
            "state": state_value,
            "city": city_value,
            "beds": beds_value,
            "min": min_value,
            "max": max_value
        })

        cont = input("Want to add another? (Y/N): ").upper()
        if cont == "N":
            get_data = False
            break

    return user_inputs

# Concatinate the URL string
def build_url(user_inputs):
    built_urls = []
    for value in user_inputs:
        apartment_url = f"https://www.apartmentfinder.com/{value['state']}/{value['city']}-Apartments/{value['beds']}/q/?nr={value['min']}&xr={value['max']}"
        built_urls.append(apartment_url)
    
    return built_urls

# Grab HTML content from link(s)
def get_html_content(built_urls):
    for url in built_urls:
        http = urllib3.PoolManager(ca_certs=certifi.where())
        response = http.request('GET', url, timeout = 5 )
        content = BeautifulSoup(response.data, 'lxml')
        return content


# Get Apartment info and set in list
def get_apartment_info(content):
    get_content = True
    apartment_info = []
    articles = content.find_all("article")
    while get_content:
        for article in articles:
            if len(articles) > 1:
                address = article.find('address').get_text().lstrip().rstrip()
                rent = article.find('span', class_="altRentDisplay").get_text().lstrip().rstrip()
                phone_number = article.find('span', class_="phone").get_text().lstrip().rstrip()

                print(address + "\t" + rent + "\t" + phone_number)
                
                # apartment_info.append({
                #     "address": address,
                #     "rent": rent,
                #     "phone_number": phone_number
                # })
            else:
                get_content = False
                break

    return apartment_info

if __name__ == '__main__':
    user_inputs = get_user_inputs()
    built_urls = build_url(user_inputs)
    print(built_urls)
    content = get_html_content(built_urls)
    # apartment_info = get_apartment_info(content)
    get_apartment_info(content)
    



