from requests_html import HTML
import requests
import random
import re
import smartypants
import textstat
import time
from readability import Readability
import copy

authors = {
    "hamilton": {
        'buist': {'name': 'steve-buist', 'id': '5c309696-1fb0-43a5-9108-97e776c1c417'},
        'clairmont': {'name': 'susan-clairmont', 'id': 'b3966f66-8d36-42d5-963a-34617a235e11'},
        'dreschel': {'name': 'andrew-dreschel', 'id': 'bfa7bf9e-9f9e-4b10-aa9e-b1d3032af5aa'},
        'fragomeni': {'name': 'carmela-fragomeni', 'id': '4b38e9b6-f805-4301-be2c-e0d4d27b2a32'},
        'frketich': {'name': 'joanna-frketich', 'id': '044a62bb-aab4-4e6c-80bf-fe7aa660c4dd'},
        'grover': {'name': 'rosie-grover', 'id': '6afe52ba-6792-4d53-a3fc-9d6e8badcb41'},
        'hogue': {'name': 'tom-hogue', 'id': 'da04137d-6295-481f-a90a-c59c09907677'},
        'mahoney': {'name': 'jeff-mahoney', 'id': '232dadd6-8e52-4458-af42-5da55bbbdeb0'},
        'mcneil': {'name': 'mark-mcneil', 'id': '0b2707b1-3bf9-4c3c-8c30-5a07ff97d981'},
        'milton': {'name': 'steve-milton', 'id': '346a9bb4-5f2b-4838-b632-4abcc516eeca'},
        'moro': {'name': 'teviah-moro', 'id': 'f66f2aee-9643-4ef3-8691-03117aa544cd'},
        'oreilly': {'name': 'nicole-oreilly', 'id': '8fdadef7-07a0-4911-acb2-71604cb7bbeb'},
        'paddon': {'name': 'natalie-paddon', 'id': '3a3af314-a189-40f4-a6ba-d01a1a67d56f'},
        'pecoskie': {'name': 'teri-pecoskie', 'id': 'ab2cef44-1fd3-4380-a6ee-f695f4e0d4e5'},
        'radley': {'name': 'scott-radley', 'id': '49255a54-3476-496a-8a42-abfd94a67feb'},
        'reilly': {'name': 'emma-reilly', 'id': '8069c27c-8bc8-4f0c-825c-7904ab93cd2b'},
        'rockingham': {'name': 'graham-rockingham', 'id': '2ff0c27b-0289-4232-b726-e66cc72b7897'},
        'vandongen': {'name': 'matthew-van-dongen', 'id': '70c601f0-79a5-4189-b1da-147f61545d27'},
        'wells': {'name': 'jon-wells', 'id': '09cba71e-7888-430d-aae9-a63fc5c07f2e'},
        # photogs
        'coward': {'name': 'cathie-coward', 'id': 'a5d43501-cd8c-48d4-afb6-16ed134d49bf'},
        'gardner': {'name': 'scott-gardner', 'id': '98261032-4787-4562-9985-02c3a8ebff08'},
        'gray': {'name': 'barry-gray', 'id': 'caed145c-9415-4f6f-8570-b4ea24febb64'},
        'rennison': {'name': 'john-rennison', 'id': 'ab2cef44-1fd3-4380-a6ee-f695f4e0d4e5'},
        'yokoyama': {'name': 'gary-yokoyama', 'id': '2f304c58-640e-4d34-ba8e-578fff171e7f'},
        # contributors
        'benedetti': {'name': 'paul-benedetti', 'id': '289d47ff-6088-439c-ae43-0b2eae44c10b'},
        'berton': {'name': 'paul-berton', 'id': '25a2fb14-ae69-41f2-beab-bdda47383f93'},
        'direnfeld': {'name': 'gary-direnfeld', 'id': '24b2643a-dd88-482d-8eaa-c62e0f3aae5f'},
        'haggo': {'name': 'regina-haggo', 'id': '5dc1f3c3-5bc2-4a61-9405-e1065a2129b4'},
        'nadler': {'name': 'sheryl-nadler', 'id': 'fc6bb0f2-b0c3-4d97-8074-e2852ea95dd8'},
        'pike': {'name': 'deirdre-pike', 'id': 'da49041a-00cb-465b-945c-2bad0d8389de'},
        'schramayr': {'name': 'ernie-schramayr', 'id': 'e8f712c3-3ae3-496e-a069-556bb22f89fa'},
        'shkimba': {'name': 'margaret-shkimba', 'id': '7fd5fddd-56a0-4e16-ba29-756d0b193bb4'},
        'smith': {'name': 'gary-smith', 'id': '034e0403-c3f6-41a2-92d3-008f63f43859'},
        'sommerfeld': {'name': 'lorraine-sommerfeld', 'id': 'd13c97bc-5b03-4a04-bb5b-136adeba684b'},
        'tesher': {'name': 'ellie-tesher', 'id': 'b96145c1-3b2a-4ebe-a279-8e763d140430'},
        'turnevicius': {'name': 'leonard-turnevicius', 'id': 'd4ef4754-6b8f-4c97-948f-a41e1f60a35b'},
    },
    "waterlooregion": {
        'booth': {'name': 'laura-booth', 'id': 'e0162a64-2f51-4c10-b215-142cc11f564b'},
        'brown': {'name': 'josh-brown', 'id': '51616995-13d2-42b4-b0b7-34f399aaafe6'},
        'bryson': {'name': 'mark-bryson', 'id': '556bdc79-d03d-4796-9256-a91528eff26f'},
        'damato': {'name': 'luisa-d-amato', 'id': '412d649f-ed04-4044-9960-516c14ea31b7'},
        'davis': {'name': 'brent-davis', 'id': 'b637f89b-935c-446a-bbcc-c7c875a6bfab'},
        'hicks': {'name': 'jeff-hicks', 'id': 'cdbd7ed6-9268-49ba-b447-d49f7d54ad73'},
        'hill': {'name': 'valerie-hill', 'id': '45166471-e4bd-4740-be03-840fb6a77ee0'},
        'jackson': {'name': 'james-jackson', 'id': 'a9430b1e-883a-4e8b-97c0-c495b186c09b'},
        'latif': {'name': 'anam-latif', 'id': '643b1528-bd71-4e8b-ac93-feaaaa3d210d'},
        'mercer': {'name': 'greg-mercer', 'id': '261716c4-b225-40c6-8edb-e898ecd2c751'},
        'monteiro': {'name': 'liz-monteiro', 'id': 'a5427c0a-db30-4dc3-8f41-9f6f2d8f80bc'},
        'outhit': {'name': 'jeff-outhit', 'id': 'cb820047-326c-44d3-9b62-2098cf76324a'},
        'paul': {'name': 'gordon-paul', 'id': '76d40a22-3142-4648-8563-88625eae95ac'},
        'pender': {'name': 'terry-pender', 'id': 'f226a93d-8174-4742-88f1-756aeb58b351'},
        'rubinoff': {'name': 'joel-rubinoff', 'id': '09581a1a-e8b6-4e87-8001-4d355e7853a2'},
        'thompson': {'name': 'catherine-thompson', 'id': '1fb31711-634a-4a8f-8f64-a1da45f1e043'},
        'weidner': {'name': 'johanna-weidner', 'id': '7b167600-a2d2-4618-a225-467d0db4ec9f'},
        # contributors
        'mills': {'name': 'rych-mills', 'id': '21045760-43a8-4503-814a-838d5641dd69'},
        'stevens': {'name': 'geoffrey-stevens', 'id': '290fd071-2aba-4ddd-bcf0-54763f0a3e5c'},
        'taylor': {'name': 'peter-taylor', 'id': 'd1f9fafa-d042-400d-9cf6-b936018057fe'},
    },
    "stcatharines-on": {
        'benner': {'name': 'allan-benner', 'id': 'cb3129c8-afdc-4aa6-93dc-3004460b6522'},
        'clock': {'name': 'cheryl-clock', 'id': '96cab080-b8bd-4414-a95d-76e11da26eb8'},
        'dube': {'name': 'kris-dub-', 'id': 'deb86d65-b2af-4046-beb5-1fd4be08076c'},
        'johnson': {'name': 'nathaniel-johnson', 'id': '5b467606-c31d-4125-bbec-f8bc2d8b6030'},
        'lafleche': {'name': 'grant-lafleche', 'id': 'ae374dcb-0da0-419d-b2ab-444368f94103'},
        'langley': {'name': 'alison-langley', 'id': '68c112be-842c-4960-b40c-829965866f57'},
        'law': {'name': 'john-law', 'id': 'ce6f6b8c-9422-4d59-b05d-8534ddc4aea2'},
        'sawchuck': {'name': 'bill-sawchuk', 'id': '8138da31-f538-43f5-838d-c755299daac5'},
        'spiteri': {'name': 'ray-spiteri', 'id': 'f35d81f3-c34e-4db4-af8c-d6e6270f3434'},
        'tymczyszyn': {'name': 'bob-tymczyszyn', 'id': '2ec916e1-a55c-4a04-853a-10409eb75b89'},
        'walter': {'name': 'karena-walter', 'id': 'a51414df-8a62-4d5c-983c-150ba3470c1c'},
    },
}


def fetch_assets(author, site, count):
    url = f"http://api.zuza.com/search/article/default?guid={author['id']}&pageIndex=1&location={site}&sort=datedesc&pageSize=15&startindex=1&endindex={count}"
    r = fetch_data(url, b_json=True, l_filter=['searchResultView'])
    assets = [x['assetId'] for x in r]
    return assets


def fetch_data(s_url, b_json=True, l_filter=None):
    # DIAGNOSTIC print("+++++++++++++\nNow in fetch_data module ...")
    # string s_url
    # boolean b_json whether to return json or text
    # list of strings that are really keys to drill down the dict
    user_agents = [
        'Mozilla/5.0 (Linux; Android 7.1.2; HTC 2Q4R100 Build/N2G47H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.137 Mobile Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:64.0) Gecko/20100101 Firefox/64.0',
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:63.0) Gecko/20100101 Firefox/63.0',
        'MMozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:63.0) Gecko/20100101 Firefox/63.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/604.4.7 (KHTML, like Gecko) Version/11.0.2 Safari/604.4.7',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1'
    ]
    headers = {'user-agent': random.choice(user_agents)}
    # print(f"Fetch headers: {headers}")
    r = requests.get(s_url, headers=headers)
    if b_json:
        d = r.json()
        if l_filter:
            temp = d
            for item in l_filter:
                # print(item)
                temp = temp[item]
            return temp
        else:
            return d
    else:
        return r.text


def process_html(id, strip_lines=0):
    # striplines should be negative int, ie -1, -2
    # turn article page into article text
    url = f"https://www.thespec.com/news-story/{id}-abc/"
    result = fetch_data(url, b_json=False)
    sel = 'script[type="application/ld+json"]'
    html = HTML(html=result)
    paras = html.find(sel, first=True)
    try:
        found = re.search('articleBody": "(.+?)", "image":', paras.text).group(1)
    except AttributeError:
        found = '#not'  # apply your error handling

    # convert found to new lines using p tags
    found = smartypants.smartypants(found.replace('\\', ''))
    # print("Found ...", found)
    html = HTML(html=found)
    para_list = []
    for item in html.find('p'):
        para_list.append(item.text)
    if strip_lines is not 0:
        para_list = para_list[0:strip_lines]
    return para_list


# pick an author
def get_stats(author, site, count):
    data = {}
    data['author'] = authors[site][author]['name']
    data['articles'] = []
    asset_list = fetch_assets(authors[site][author], site, count)
    for asset in asset_list:
        time.sleep(random.randint(5, 8))
        obj = {}
        obj['assetId'] = asset
        lines = process_html(id=asset, strip_lines=-1)
        article_text = "\n ".join(lines)
        # using textstat library
        obj['wc'] = textstat.lexicon_count(article_text, removepunct=True)
        if int(obj['wc']) > 99:
            # obj['fre'] = textstat.flesch_reading_ease(article_text)
            # obj['fkg'] = textstat.flesch_kincaid_grade(article_text)
            # obj['gfi'] = textstat.gunning_fog(article_text)
            # using py-readibility-metrics
            # https://py-readability-metrics.readthedocs.io/en/latest/
            r = Readability(article_text)
            obj['wc'] = textstat.lexicon_count(article_text, removepunct=True)
            # obj['fre'] = textstat.flesch_reading_ease(article_text)
            fk = r.flesch_kincaid()
            # obj['fk'] = fk.score
            obj['fkg'] = fk.grade_level
            f = r.flesch()
            obj['fre'] = f.grade_levels
        else:
            obj['fkg'] = "0"
            obj['fre'] = "0"
        data['articles'].append(obj)
    return data


site = "stcatharines-on"
count = 8

for name in authors[site]:
    data = get_stats(name, site, count)
    print("\n======================================")
    print(f"Author: {data['author'].replace('-', ' ').title()}")
    score = 0
    wc_total = 0
    divisor = copy.copy(count)
    for item in data['articles']:
        wc_total += int(item['wc'])
        if item['fkg'] is not "0":
            # print(f"Asset ID: {item['assetId']}")
            # print(f"Word count: {item['wc']} | FK Grade: {item['fkg']} | FRE: {item['fre']}")
            score += int(item['fkg'])
        else:
            divisor = divisor - 1

    print(f"Avg. word count: {str(int(wc_total/count))} | Avg. grade: {round( score/divisor, 1)}")
    print("======================================")


#TODO process 10 articles, come up with avg. word count and grade level
#, and showing lowest and highest articles
