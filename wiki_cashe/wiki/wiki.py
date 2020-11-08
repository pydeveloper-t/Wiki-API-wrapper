import logging; logger = logging.getLogger('Wiki')
import json
import aiowiki
from fuzzywuzzy import fuzz
from polyglot.text import Text as T
from wiki_cashe.transport.request import get
from wiki_cashe.models.wiki_models import Wiki

WIKILANG = 'en'

async def wiki_entity(search_term, levenstein_threshold=80, wiki_summary_sentences=5):
    ''' str ->> str/None
    Finds entity in wikipedia, tkaes the first occurrence of topics found in wikipedia,
    computes Levenshtein distance between entity and wikipedia topic. If topic is found
    for this entity in wikipedia, and the Levenshtein distance is smaller than threshold,
    returns this topic. Otherwise returns None.
    Args:
        search_term (str): any entity as a string to be looked up in wikipedia
    Returns:
        bool: is wiki search successful?
        str: The best-matched verified topic page name from wikipedia that corresponds to the entity
    '''
    global WIKILANG
    wiki = aiowiki.Wiki.wikipedia(WIKILANG)
    wiki_obj  = Wiki()
    try:
        wiki_topics = await wiki.opensearch(search_term)
        matches = [(wt.title, fuzz.ratio(search_term, wt.title)) for wt in wiki_topics]
        sorted_matches = sorted(matches, key=lambda x: x[1], reverse=True)
        best_match = sorted_matches[0]
        if best_match[1] >= levenstein_threshold:
            page = wiki.get_page(best_match[0])
            _urls = await page.urls()
            url = _urls[0]
            summary = await page.summary()
            # _images = await page.media()
            title= page.title
            page_slug = url[url.rfind("/")+1:]
            wiki_image_url = f'https://{WIKILANG}.wikipedia.org/w/api.php?action=query&prop=pageimages&format=json&piprop=original&titles={page_slug}'
            res_txt = await get(wiki_image_url)
            res_json = json.loads(res_txt['content'])['query']['pages']
            image = res_json[list(res_json.keys())[0]]['original']['source']
            page_text = ' '.join([str(sent) for sent in T(summary).sentences][:wiki_summary_sentences])
            wiki_obj = Wiki(success=True, wiki_article=best_match[0], wiki_text=page_text, wiki_title=title,
                            wiki_image=image, wiki_url=url)
    except Exception as exc:
        logger.warning(f'wiki entity exception: {exc} search_term = {search_term}, levenstein_threshold = {levenstein_threshold} , wiki_summary_sentences = {wiki_summary_sentences}')
    return wiki_obj