import streamlit as st
from datetime import datetime
import time
import requests
from requests_html import HTMLSession
from beautifulsoup4 import BeautifulSoup

def google_searcher(query):
    Query = query
    Limit = int(20)

    s = HTMLSession()

    headers = {
        # Add the same headers as before
    }

    params = {
        'q': Query,
        'num': Limit,
        'tbs': 'qdr:d'
    }

    response = s.get('https://www.google.com/search', params=params)

    if 'did not match any documents' in response.text:
        return []  # Return an empty list when no results are found
    elif 'Our systems have detected unusual traffic from your computer' in response.text:
        exit('Captcha Triggered!\nUse Vpn Or Try After Sometime.')
    else:
        links_list = []
        soup = BeautifulSoup(response.text, 'html.parser')  # Parse the HTML content
        results = soup.select('.tF2Cxc')  # Select the class containing search result items
        for result in results:
            title = result.select_one('.DKV0Md').get_text()  # Extract the title
            try:
                description = result.select_one('.VwiC3b').text  # Extract the description
            except AttributeError:
                description = 'No description available'
            link = result.find('a')['href']  # Extract the link
            if 'google' not in link:
                links_list.append({'title': title, 'description': description, 'url': link})
        return links_list

def display_results(keyword):
    today = datetime.today().date()
    st.subheader('Hey, I am a lazy person who wants to automate my media monitoring task!')
    st.title('Media Monitoring Result on ' + str(today))
    st.write('I wonder if there are any interesting news today?')

    st.write(keyword)
    results = google_searcher(keyword)
    for result in results:
        st.write("Title:", result['title'])
        st.write("Description:", result['description'])
        st.write("URL:", result['url'])
        st.write("\n")

# Set the page config only once at the beginning of the script
st.set_page_config(page_title='Automated Media Monitoring')

# Run the Streamlit app with next and previous buttons to navigate through keywords
if __name__ == "__main__":
    keyword = ['Anugerah Pharmindo Lestari', 'Christopher Piganiol', 'PT APL','APL','APL Healthcare','APL Sustainability','APL Distributor Farmasi','Layanan Kesehatan APL','Ratna Kurniawati','Wishnu Satya','Jesianto Nugroho','Denny Fikri','Ay Lie Widjaja','Bernadina Okti Adiyanti']

    # Initialize session_state
    if 'index' not in st.session_state:
        st.session_state.index = 0

    if st.button("Previous", key="prev"):
        st.session_state.index -= 1

    if st.button("Next", key="next"):
        st.session_state.index += 1

    st.session_state.index = st.session_state.index % len(keywords)  # Handle wrap-around

    display_results(keywords[st.session_state.index])
