from basic import *
from game import *

def season(season_num, dest, driver = None):
    close_driver_at_end = False if driver else False 
    if driver == None:
        driver = driver_init()

    create_dirs = [dest, dest+'/games']
    for d in create_dirs:
        if not os.path.exists(d):
            os.makedirs(d)

    base_url = 'http://www.j-archive.com/showseason.php?season='
    season_soup = get_soup(driver, base_url + str(season_num))

    game_tags = season_soup.tbody('tr', recursive=False)
    game_tags.reverse()
    games = []
    summary_dict = dict()
    
    for g_tag in game_tags:
        link = g_tag.a['href']
        game_id = int(link.split('=')[1])

        exp = re.compile(r'#(\d+), aired ([\d-]+)')
        text = g_tag.a.text.replace(u'\xa0', u' ')
        match = exp.search(text)
        show_id = int(match.group(1))
        date = match.group(2) #datetime.datetime.strptime(match.group(2), '%Y-%m-%d').date()

        cs = g_tag.find_all('td', valign='top')[1].text.strip().split(' vs. ')

        summary_dict[str(game_id)] = {'show_id': show_id, 'date': date, 'Contestant 1': cs[0],
                                      'Contestant 2': cs[1], 'Contestant 3': cs[2]}

        try:
            comment = g_tag.find('td', class_='left_padded').text.strip()

            if comment != '':
                summary_dict[str(game_id)]['comment'] = comment
        except:
            pass
        

    with open(dest+'/summary.json', 'w') as summary_file:
        json.dump(summary_dict, summary_file)

    for game_id in summary_dict:
        print('Getting game ' + game_id)
        game(int(game_id), dest=dest+'/games/' + game_id + '.json', driver=driver)
        sleep(.5)
        
    if close_driver_at_end:
        driver.close()
