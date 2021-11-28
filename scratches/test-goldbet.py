import requests

def run():

    url_list = {
        'serie_A': 'https://www.goldbet.it/getOverviewEvents/0?idDiscipline=0&idTournament=93',
        'champions_league': 'https://www.goldbet.it/getOverviewEvents/0?idDiscipline=0&idTournament=26534',
        'europa_league': 'https://www.goldbet.it/getOverviewEvents/0?idDiscipline=0&idTournament=247944',
        'premier_league': 'https://www.goldbet.it/getOverviewEvents/0?idDiscipline=0&idTournament=26604',
        'la_liga': 'https://www.goldbet.it/getOverviewEvents/0?idDiscipline=0&idTournament=95',
        'bundesliga': 'https://www.goldbet.it/getOverviewEvents/0?idDiscipline=0&idTournament=84',
        'ligue_1': 'https://www.goldbet.it/getOverviewEvents/0?idDiscipline=0&idTournament=86',
        'serie_B': 'https://www.goldbet.it/getOverviewEvents/0?idDiscipline=0&idTournament=1626630'
    }
    response = requests.get(url_list['bundesliga'])
    json_data = response.json()

    matches = json_data['leo']
    for match in matches:
        date = match['ed']
        teams = match['en'].split(' - ')

        quotes_1X2 = match['mmkW']['111;355;4001;0;0']
        string = quotes_1X2['mn']
        quote_values = quotes_1X2['spd']['0.0']['asl']
        list_values = []
        for value in quote_values:
            list_values.append(str(value['ov']))

        quotes_ov = match['mmkW']['111;355;4002;0;0']
        string_ov = quotes_ov['mn']
        ov_values = quotes_ov['spd']['2.5']['asl']
        list2_values = []
        for value in ov_values:
            list2_values.append(str(value['ov']))

        print(date + " " + ' - '.join(teams) + " | " + string + ": " + ' '.join(list_values) + " | " + string_ov +
              "(2.5): " + ' '.join(list2_values))

    # TESTING FINITO