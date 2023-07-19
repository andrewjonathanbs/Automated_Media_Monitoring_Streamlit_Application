import streamlit as st
from datetime import datetime
from requests_html import HTMLSession
from bs4 import BeautifulSoup

def google_searcher(query):
    Query = query
    Limit = int(20)

    s = HTMLSession()
    file = open('Results.txt', 'w')

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}

    params = {
        'q': Query,
        'num': Limit,
        'tbs': 'qdr:d'
    }

    response = s.get('https://www.google.com/search', params=params)

    if 'did not match any documents' in response.text:
        exit('No Results Found')
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
            title_ban = [None, 'untitled','untitle']
            description_ban = ['No information is available for this page']
            url_ban = ['linkedin','jobstreet','loker']
            if 'google' not in link and title.lower() not in title_ban and description.lower() not in description_ban and link.lower() not in url_ban:
                links_list.append(link)
                file.write(link + '\n')
                # Print the title and description of each result
                st.write("Title:", title)
                st.write("Description:", description)
                st.write("URL:", link)
                st.write("\n")

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

# Run the Streamlit app with next and previous buttons to navigate through keywords
if __name__ == "__main__":
    keywords = ['Anugerah Pharmindo Lestari', 'Christopher Piganiol', 'PT APL','APL','APL Healthcare','APL Sustainability','APL Distributor Farmasi','Layanan Kesehatan APL','Ratna Kurniawati','Wishnu Satya','Jesianto Nugroho','Denny Fikri','Ay Lie Widjaja','Bernadina Okti Adiyanti']

    # Initialize session_state
    if 'index' not in st.session_state:
        st.session_state.index = 0

    if st.button("Previous", key="prev"):
        st.session_state.index -= 1

    if st.button("Next", key="next"):
        st.session_state.index += 1

    st.session_state.index = st.session_state.index % len(keywords)  # Handle wrap-around

    display_results(keywords[st.session_state.index])
