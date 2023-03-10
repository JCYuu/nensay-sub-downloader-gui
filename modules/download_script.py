
from bs4 import BeautifulSoup
prev_anime = prev_chapter = next_anime = next_chapter = False



class Chapter:
    """
    A basic chapter consisting of its title and its accesible download link
    """
    def __init__(self, title, link):
        self.title = title
        self.link = link


class CustomException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


def login(session):
    """
    Logs in https://nensaysubs.net bypassing the number check

    :param session: A python requests session
    :return:
    """
    print('Login in...')
    response = session.get("http://nensaysubs.net/")
    #print(response.text)
    soup = BeautifulSoup(response.text, 'html.parser')
    captcha = eval(soup.find(name='h1', attrs={'class': 'text4'}).text)
    #time.sleep(1)
    with session.post("http://nensaysubs.net/ingreso/index.php/", data={'valor': captcha}) as response:
        print(response)
        print(response.headers)


def reload_filter(soup):
    """
    Walks through html tags and returns a list containing each found anime's title

    :param soup: A BeautifulSoup object for traversing html
    :return: query_list: A list cointaining found anime titles
    """
    query_list = []
    global prev_anime, next_anime
    children = soup.find_all(name='td', attrs={'valign': 'top'})
    filtering = [x.findChildren('a', recursive=True) for x in children]
    for i, element in enumerate(filtering):
        title = element[0].text
        query_list.append(title)
    previous = soup.find(name='a', text='Anterior')
    nxt = soup.find(name='a', text='Siguiente')
    prev_anime = True if previous is not None else False
    next_anime = True if nxt is not None else False
    print(query_list)
    print(prev_anime)
    print(next_anime)
    return query_list


def reload_chapters(soup):
    """
    Walks through an anime page html tags and returns a list containing its chapters

    :param soup:
    :return: ch_list: a Chapter(title, link) list
    """
    ch_list = []
    title = ''
    dl = ''
    global prev_chapter, next_chapter
    for tag in soup.find_all(['span', 'input']):
        if tag.get('id') == 'bloqueados':
            child = tag.find('a', attrs={'id': 'caramelo'})
            start_pos = child.get('href').find('senos')
            dl = child.get('href')[start_pos:]
        if tag.get('value') == 'Bajar': dl = tag.get('onclick')[13:-3]
        if tag.get('id') == 'animetitu': title = tag.text
        if title != '' and dl != '':
            ch_list.append(Chapter(title, dl))
            title = dl = ''
    previous = soup.find(name='a', text='Anterior')
    nxt = soup.find(name='a', text='Siguiente')
    prev_chapter = True if previous is not None else False
    next_chapter = True if nxt is not None else False
    print(prev_chapter)
    print(next_chapter)
    return ch_list




def search(session, query):
    """
    Searchs for anime results using the input query and returns a list with its results

    :param session: python requests session
    :param query: name to search
    :return: query_list: list with anime names found as a result
    """
    if not query:
        raise CustomException("Don't leave search field blank")
    with session.post(f"http://nensaysubs.net/buscador/?query={query.replace(' ', '+')}") as response:
        #print(response.text)
        soup = BeautifulSoup(response.text, 'html.parser')
        query_list = reload_filter(soup)
        print(query_list)
        if not query_list:
            raise CustomException("No results found for your query")
        return query_list
        # await download(session, chosen)


def get_chapters(session, chosen):
    """
    Gets all the current page chapters for a specific anime

    :param session: python requests session
    :param chosen: anime name to retrieve chapters
    :return: ch_list: list containing anime chapters in Chapter(title, link) format
    """
    ch_list = []
    with session.post(f"http://nensaysubs.net/sub/{chosen.replace(' ', '_')}") as response:
        soup = BeautifulSoup(response.text, 'html.parser')
        ch_list = reload_chapters(soup)
        return ch_list



