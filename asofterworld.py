#! python3
# asofterworld.py - Downloads every single asofterworld comic.

import requests, os, bs4

url = str('http://asofterworld.com') # starting url
os.makedirs('asofterworld', exist_ok=True) # store comics in ./asofterworld
while not url.endswith('id=0'):
    # Download the page.
    print('Downloading page %s...' % url)
    res = requests.get(url)
    res.raise_for_status()

    soup = bs4.BeautifulSoup(res.text)

    # Find the URL of the comic image.
    comicElem = soup.select('#comicimg img')
    if comicElem == []:
        print('Could not find comic image.')
    else:
        comicUrl = comicElem[0].get('src')
        # Download the image.
        print('Downloading image %s...' % (comicUrl))
        res = requests.get(comicUrl)
        res.raise_for_status()

        # Save the image to ./asofterworld
        imageFile = open(os.path.join('asofterworld', os.path.basename(comicUrl)), 'wb')
        for chunk in res.iter_content(100000):
            imageFile.write(chunk)
        imageFile.close()

    # Get the Prev button's url.
    prevurl = soup.select('#previous a')[0]
    url = prevurl.get('href')


print('Done.')
