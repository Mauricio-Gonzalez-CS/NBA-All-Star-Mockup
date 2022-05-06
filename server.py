from calendar import c
from flask import Flask
from flask import render_template
from flask import Response, request, jsonify, redirect, url_for
from pymysql import NULL
from sympy import Q, re
app = Flask(__name__)

current_id = 14
data = [
    {
        "id": 1,
        "name": "michael scott"
    },
    {
        "id": 2,
        "name": "jim halpert"
    },
]

players = {
    "1": {
        "id": '1',
        "name": "Jarrett Allen",
        "image": "https://www.si.com/.image/ar_1:1%2Cc_fill%2Ccs_srgb%2Cfl_progressive%2Cq_auto:good%2Cw_1200/MTg2NjIyMzU4NjA4NDIyNTc0/jarrett-allen-cavs.jpg",
        "summary": "Ranks third in the league with 528 points in the restricted area. His 77.6 percent shooting in the restricted area ranks fourth among 55 players with at least 200 attempts. Opponents have shot 51.3 percent at the rim when he's been there to protect it. That's the third-best rim protection mark among 21 players who've defended at least 250 shots at the rim.",
        "team": "Cleveland Cavaliers",
        "position": "Center",
        "height": "6' 10",
        "age": "23",
        "year": "1998",
        "parents": ["Leonard Allen", "Cheryl Allen"]
    },
    "2": {
        "id": '2',
        "name": "Giannis Antetokounmpo",
        "image": "https://cdn.vox-cdn.com/thumbor/DfKHHAfrvYygOvTNSwJrnoKVtDs=/0x0:4323x3254/1200x800/filters:focal(1835x894:2525x1584)/cdn.vox-cdn.com/uploads/chorus_image/image/69938435/usa_today_16842344.0.jpg",
        "summary": "Leads the league in scoring at 29.4 points per game. Also leads the league in points scored per 36 minutes (32.5). Has drawn 8.6 fouls per game, which would be the highest average in the last six seasons. Has accounted for 65.9% of the Bucks' free throw attempts while he's been on the floor, the highest rate among 334 players who've played at least 500 minutes.",
        "team": "Milwaukee Bucks",
        "position": "Forward",
        "height": "6' 7",
        "age": "27",
        "year": "1994",
        "parents": ["Charles Antetokounmpo", "Veronica Antetokounmpo"]
    },
    "3": {
        "id": '3',
        "name": "LaMelo Ball",
        "image": "https://cdn.nba.com/manage/2022/01/20201001-lamelo-ball-celebrates-3-vs-bucks-cropped-1568x882.jpg",
        "summary": "One of four players (all All-Stars) averaging at least 20 points, seven rebounds, and seven assists per game. Has averaged 7.1 “pass-ahead” passes per game, second-most in the league, according to Second Spectrum tracking. The Hornets have averaged 103.6 possessions per 48 minutes with him on the floor. That's the highest on-court mark for pace among 224 players who've averaged at least 20 minutes per game.",
        "team": "Charlotte Hornets",
        "position": "Guard",
        "height": "6' 7",
        "age": "20",
        "year": "2001",
        "parents": ["LaVar Ball", "Tina Ball"]
    },
    "4": {
        "id": '4',
        "name": "Devin Booker",
        "image": "https://cdn.vox-cdn.com/thumbor/3T1NsyolyYSvYx7UFaALCSJWsxI=/1400x1400/filters:format(jpeg)/cdn.vox-cdn.com/uploads/chorus_asset/file/22305545/usa_today_15576738.jpg",
        "summary": "One of three players - Antetokounmpo and LeBron James are the others - who've averaged at least 25 points per game in each of the last four seasons.  Has scored 0.461 points per touch, the third-highest rate among 286 players with at least 1,000 total touches. Has shot 22-for-35 (62.9%) on clutch shots, the third-best mark among 95 players who've attempted at least 20.",
        "team": "Phoenix Suns",
        "position": "Guard",
        "height": "6' 5",
        "age": "25",
        "year": "1996",
        "parents": ["Melvin Booker", "Veronica Gutierrez"]
    },
    "5": {
        "id": '5',
        "name": "Jimmy Butler",
        "image": "https://media.gq.com/photos/5f57b3f8b356afdae15b0ea3/1:1/w_2656,h_2656,c_limit/GQ-JimmyButler-090820.jpg",
        "summary": "Has a free throw rate of 54.4 attempts per 100 shots from the field, the fourth-highest rate among 280 players (highest among non-bigs) with at least 200 field goal attempts. Has an effective field goal percentage of 35.4% on shots from outside the paint, the third-worst mark among 257 players with at least 100 field goal attempts from the outside. One of eight players (Dejounte Murray is another) who've played at least 500 minutes and have more steals (69) than personal fouls (57). Has done so in each of his last six (and eight of his last nine) seasons.",
        "team": "Miami Heat",
        "position": "Forward",
        "height": "6' 7",
        "age": "32",
        "year": "1989",
        "parents": ["Londa Butler", "unknown"]
    },
    "6": {
        "id": '6',
        "name": "Stephen Curry",
        "image": "https://phantom-marca.unidadeditorial.es/ca882e26a8156d56d3a2f4edc40e3094/resize/1320/f/jpg/assets/multimedia/imagenes/2022/02/18/16452051299726.jpg",
        "summary": "Leads the league (by wide margins) in 3-point makes (251) and 3-point attempts (663). Has made a 3-pointer in a record 179 straight games. His 37.9% from 3-point range is the lowest mark of his career (not including the season in which he played only five games), and he's seen a slightly bigger drop from last season in catch-and-shoot 3-point percentage (from 43.7% to 38.5%) than he has in pull-up 3-point percentage (40.9% to 37.5%). He's shot worse from 3-point range (37.2%) and has been assisted on a far lower percentage of his 3s (50.4%) with Draymond Green off the floor than he has with Green on the floor (38.8%, 66.1%), though that 38.8% with Green on the floor would still be a career-low mark. Curry's field goal percentage in the paint (53.8%) is also his lowest mark in the last eight seasons.",
        "team": "Golden State Warriors",
        "position": "Guard",
        "ppg": "25.6",
        "apg": "6.4",
        "rpg": "5.2",
        "number": "#30",
        "height": "6' 2",
        "age": "33",
        "year": "1988",
        "parents": ["Dell Curry", "Sonya Curry"],
        "logo": "https://images.ctfassets.net/a4rx79jcl3n1/139uoz1HBz6PsWh8pEqOCK/eced155325ccb92acf76962ca5d688e5/gsw-logo-1920.png"
    },
    "7": {
        "id": '7',
        "name": "DeMar DeRozan",
        "image": "https://www.nba.com/bulls/sites/bulls/files/derozan_swap_16x9_11.jpg",
        "summary": "Has scored 1.13 points per possession on isolations, the best mark among 35 players with at least 100 isolation possessions, according to Synergy tracking. Has also scored 1.26 points per possession on post-ups, the best mark among 38 players with at least 75 post-up possessions. His 516 mid-range field goal attempts are 172 more than any other player has attempted this season and already more than any player attempted in either of the previous two seasons. His 50.2% shooting from mid-range ranks eighth among 62 players with at least 100 attempts.",
        "team": "Chicago Bulls",
        "position": "Forward",
        "height": "6' 6",
        "age": "32",
        "year": "1989",
        "parents": ["Frank DeRozan", "Diane DeRozan"]
    },
    "8": {
        "id": '8',
        "name": "Luka Doncic",
        "image": "https://e0.365dm.com/21/10/2048x1152/skysports-nba-luka-doncic-dallas-mavericks_5554205.jpg",
        "summary": "Averaging 27.0 points, 9.0 rebounds and 9.0 assists per game. Would be just the third different player in NBA history to put up those numbers, joining Oscar Robertson (five seasons) and Russell Westbrook (2016-17). Ranks second in drives per game for the third straight season. His 21.6 drives per game are a career-high mark and his 55.1% shooting on drives ranks sixth among 48 players with at least 200 field goal attempts on drives. Has been assisted on just 15.1% of his buckets, the lowest rate among 264 players with at least 100 total field goals (though up from just 13.6% last season).",
        "team": "Dallas Mavericks",
        "position": "Guard",
        "height": "6' 7",
        "age": "22",
        "year": "1999",
        "parents": ["Sasa Doncic", "Mirjam Poterbin"]
    },
    "9": {
        "id": '9',
        "name": "Kevin Durant",
        "image": "https://as01.epimg.net/en/imagenes/2022/02/21/nba/1645401208_166087_1645403812_noticia_normal_recorte1.jpg",
        "summary": "True shooting percentage of 62.6 percent ranks fifth among 108 players with at least 500 field goal attempts, but is his lowest mark in the last 10 seasons. Has taken only 13% of his shots, the lowest rate of his career, in the restricted area. His 50.5% on non-restricted-area shots in the paint ranks 15th among 93 players who've attempted at least 100, and his 55.1% from mid-range ranks second among 62 players with at least 100 mid-range attempts.",
        "team": "Brooklyn Nets",
        "position": "Forward",
        "ppg": "29.1",
        "apg": "5.8",
        "rpg": "7.2",
        "number": '#7',
        "height": "6' 10",
        "age": "33",
        "year": "1988",
        "parents": ["Wanda Durant", "Wayne Pratt"],
        "logo": "https://toppng.com/uploads/preview/brooklyn-nets-football-logo-png-11536017106v1capepmnr.png"
    },
    "10": {
        "id": '10',
        "name": "Joel Embiid",
        "image": "https://dynaimage.cdn.cnn.com/cnn/c_fill,g_auto,w_1200,h_675,ar_16:9/https%3A%2F%2Fcdn.cnn.com%2Fcnnnext%2Fdam%2Fassets%2F211128185623-joel-embiid-1127-restricted.jpg",
        "summary": "Leads the league in usage rate at 37.6%, the fourth-highest mark in the 26 seasons for which we have play-by-play data. His 3.4 minutes per game of possession ranks just 69th but is the highest average of his career (and up from 2.9 minutes last season). Leads the league (for the third straight season) with 10.2 post-ups per game, according to Second Spectrum tracking. His 1.09 points per possession on post-ups rank fifth among 38 players with at least 75 post-up possessions, according to Synergy tracking.",
        "team": "Philadelphia 76ers",
        "position": "Center",
        "ppg": '29.7',
        "apg": '4.3',
        "rpg": '11.3',
        "number": '#21',
        "height": "7' 0",
        "age": "27",
        "year": "1994",
        "parents": ["Thomas Embiid", "Muriel Embiid"],
        "logo": "https://upload.wikimedia.org/wikipedia/en/thumb/0/0e/Philadelphia_76ers_logo.svg/1200px-Philadelphia_76ers_logo.svg.png"
    },
    "11": {
        "id": '11',
        "name": "Lebron James",
        "image": "https://a.espncdn.com/photo/2022/0210/r972475_1296x729_16-9.jpg",
        "summary": "Ranks third in scoring at 29.1 points per game. His 28.4 points per 36 minutes is the highest mark of his career. Has taken 37.2% of his shots, the highest rate of his career, from 3-point range, having seen a jump in each of the last six seasons. His 35.3% shooting from 3-point range is down from 36.5% last season and ranks 69th among 123 players with at least 200 attempts. Leads the league with 4.8 fast break points per game. His 76.8% shooting in the restricted area ranks seventh among 55 players with at least 200 restricted-area attempts and is his best mark in the last eight seasons.",
        "team": "Los Angeles Lakers",
        "position": "Forward",
        "ppg": '29.4',
        "apg": '6.2',
        "rpg": '8.1',
        "number": '#6',
        "height": "6' 9",
        "age": "37",
        "year": "1984",
        "parents": ["Anthony McClelland", "Gloria Marie James"],
        "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3c/Los_Angeles_Lakers_logo.svg/1200px-Los_Angeles_Lakers_logo.svg.png"
    },
    "12": {
        "id": '12',
        "name": "Ja Morant",
        "image": "https://www.gannett-cdn.com/presto/2021/12/30/PMCA/2d9d5407-129f-4874-a6f5-92b9e01c7de5-Los_3.jpg",
        "summary": "Leads the league with 16.4 points in the paint per game, the highest mark for a guard in the 26 seasons for which points in the paint have been tracked. The only players to have averaged more are Shaquille O’Neal (eight times), Giannis Antetokounmpo (three times) and Zion Williamson (20.3 last season). Leads the league with five field goals (on seven attempts) to tie or take the lead in the final minute of the fourth quarter or overtime. Has averaged 29.1 points per 36 minutes, up from 21.1 last season. That’s the biggest jump among 284 players who’ve played at least 500 minutes in each of the last two seasons. He’s also seen the ninth biggest jump in rebounds per 36 minutes (from 4.4 to 6.3) among that same group.",
        "team": "Memphis Grizzlies",
        "position": "Guard",
        "ppg": '27.5',
        "apg": '6.7',
        "rpg": '5.8',
        "number": '#12',
        "height": "6' 3",
        "age": "22",
        "year": "1999",
        "parents": ["Tee Morant", "Jamie Morant"],
        "logo": "https://upload.wikimedia.org/wikipedia/en/thumb/f/f1/Memphis_Grizzlies.svg/1200px-Memphis_Grizzlies.svg.png"
    },
    "13": {
        "id": '13',
        "name": "Jayson Tatum",
        "image": "https://cdn.vox-cdn.com/thumbor/094pRwuVlGHfFpeb-CzuvEDSMfw=/1400x1400/filters:format(jpeg)/cdn.vox-cdn.com/uploads/chorus_asset/file/23293507/1238984107.jpg",
        "summary": "Ranks fourth in cumulative plus-minus, with the Celtics having outscored their opponents by 394 points with him on the floor. They’ve been 12.7 points per 100 possessions better with him on the floor (+9.6) than they’ve been with him off the floor (-3.1). That’s the 10th biggest on-off differential among 330 players that have played at least 500 minutes for a single team. Has seen a jump in usage rate every season he’s been in the league, from 19.2% as a rookie to 31.1% this (his fifth) season. His true shooting percentage of 55.3% is the second lowest mark of his career and ranks 25th among 49 players with a usage rate of 24% or higher. Has shot 32-for-33 (97.0%) on clutch free throws, the second best mark among 24 players with at least 20 attempts. Has shot just 2-for-23 on clutch 3-pointers, the worst mark among 16 players with at least 20 attempts.",
        "team": "Boston Celtics",
        "position": "Guard",
        "ppg": '26.5',
        "apg": '4.2',
        "rpg": '8.2',
        "number": '#0',
        "height": "6' 6",
        "age": "24",
        "year": "1998",
        "parents": ["Brandy Cole", "Justin Tatum"],
        "logo": "https://upload.wikimedia.org/wikipedia/en/thumb/8/8f/Boston_Celtics.svg/1200px-Boston_Celtics.svg.png"
    },
    "14": {
        "id": '14',
        "name": "Rudy Gobert",
        "image": "https://www.gannett-cdn.com/presto/2020/03/12/USAT/5746e69e-ed6a-4f4c-b175-f9c9b1d99e63-USP_NBA__Boston_Celtics_at_Utah_Jazz.JPG",
        "summary": "Leads the league in both total dunks (155) and dunks per game (3.5). Opponents have shot just 50.0% at the rim when he’s been there to protect it. That’s the best rim protection mark among 41 players who’ve defended at least 200 shots at the rim. Has grabbed 21.9% of available rebounds while he’s been on the floor, the highest rate among 224 players who’ve averaged at least 20 minutes per game. Has six games of 20 or more rebounds, most in the league. Leads the league with 4.4 second chance points per game.",
        "team": "Utah Jazz",
        "position": "Center",
        "ppg": '15.6',
        "apg": '1.1',
        "rpg": '14.8',
        "number": '#27',
        "height": "7' 1",
        "age": "29",
        "year": "1992",
        "parents": ["Rudy Bourgarel", "Corinne Gobert"],
        "logo": "https://www.nba.com/.element/img/1.0/teamsites/logos/teamlogos_500x500/uta.png"
    }
}
popular = [players['9'], players['11'], players['10'],
           players['6']]

# ROUTES
app.add_url_rule("/search_for", endpoint='/')


@app.route('/')
def hello_world():
    return render_template('home.html', popular=popular)


@app.route('/add', methods=["GET", "POST"])
def add():
    global players
    global current_id

    s_id = str(current_id)

    if request.method == 'POST':
        current_id += 1
        entry = request.form.to_dict()
        entry['id'] = s_id
        players[s_id] = entry
        print(players[s_id])
        success = "You successfully made an entry!"
        print(success)
        return render_template('add.html', data=s_id, success=success)
    return render_template('add.html', data=s_id, success='')


@app.route('/view/<id>', methods=["GET"])
def view(id):
    global players
    layout = []
    if request.method == 'GET':
        for i in players.keys():
            for j in players[i].keys():
                if j == 'id':
                    if players[i][j] == id:
                        print(players[i])
                        if isinstance(players[i]['parents'], list):
                            layout.append(players[i])
                        else:
                            players[i]['parents'] = players[i]['parents'].split(
                                ",")
                            layout.append(players[i])
                        return render_template("view.html", layout=layout, id=id)


@app.route('/edit/<id>', methods=['GET', 'POST'])
def edit(id):
    print(id)
    global players
    results = []
    s_id = str(id)
    if request.method == 'GET':
        for i in players.keys():
            for j in players[i].keys():
                if j == 'id':
                    if players[i][j] == id:
                        print(players[i])
                        results.append(players[i])
                        print(results)
                        return render_template('edit.html', results=results, id=id)

    if request.method == 'POST':
        entry = request.form.to_dict()
        print(entry)
        entry['id'] = id
        players[s_id] = entry
        print(players[s_id])
        return redirect(f"/view/{s_id}")


@app.route("/search_for", methods=["POST"])
def search_for():
    global players
    player = request.form.get("result")
    sorry = 'No results found'
    resultsN = []
    resultsT = []
    resultsP = []
    countN = 0
    countT = 0
    countP = 0
    count = 0
    for i in players.keys():
        for j in players[i].keys():
            if j == 'name':
                if player in players[i][j].lower():
                    resultsN.append(players[i])
                    count += 1
                    countN += 1
            if j == 'team':
                if player in players[i][j].lower():
                    resultsT.append(players[i])
                    count += 1
                    countT += 1
            if j == 'parents':
                for k in players[i][j]:
                    if player in k.lower():
                        resultsP.append(k)
                        count += 1
                        countP += 1

    if (len(resultsN) > 0) | (len(resultsT) > 0) | (len(resultsP) > 0):
        return render_template('results.html', player=resultsN, search=player, count=count, team=resultsT, parents=resultsP, countN=countN, countT=countT, countP=countP)
    return render_template('results.html', sorry=sorry, search=player, count=count, countN=countN, countT=countT, countP=countP)


if __name__ == '__main__':
    app.run(debug=True)
