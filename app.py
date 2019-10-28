# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import datetime
import json
import re
import pandas as pd
from bs4 import BeautifulSoup
from urllib.request import urlopen
from pandas import DataFrame
import numpy as np
import numpy as nd
import numpy.ma as ma
import plotly.plotly as py
from plotly.graph_objs import *
import  plotly.graph_objs as go
from datetime import datetime as dt
import itertools
from datetime import timedelta

external_stylesheets = ['/assets/code.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
    <head>
    <meta charset="utf-8">

    <title>Hyper-Astrology</title>
        {%favicon%}
        {%css%}

    </head>
    <body>
        {%app_entry%}
    <footer>
        {%config%}
        {%scripts%}
    </footer>
    </body>
</html>
'''

app.config['suppress_callback_exceptions'] = True
app.css.config.serve_locally = True
app.scripts.config.serve_locally = True

server = app.server

starsigns = ['capricorn', 'aquarius', 'pisces', 'aries', 'taurus', 'gemini', 'cancer', 'leo', 'virgo', 'libra', 'scorpio', 'sagittarius']
months=['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']

aspect12={1:'Trines: Trines are among the most beneficial of all aspects. When a planet is trined with your native starsign, you will experience all the benefits of that planet’s graces. Communication with others is generally better with others during times like these and you will be able to move forward with your plans with the assurance that whatever you put your hand to will be better off because of it.\n \r Trine aspects also feature return (or Conjunction) aspects, when a planet returns to the same position in the sky, as it was in when you were born. During this period, the planet’s unique energy shines on your sign, nourishing you and giving you a well needed break. But beware, it can also be a very intense experience.\n \r  ',

2:'Squares: The Square symbolises obstacles in our lives, whether this is to do with relationships, career goals or everything in between. When a planet squares your native sign, you can expect hardship in the area, which the planet rules. But it is not all bad, because the Square Aspect also brings with it much opportunity for growth and expansion. Seize the day and go for it!\n\r   Along with the results of Squares are those of the Conjunctions and Oppositions. This is because a square aspect is 90 degrees to your native sign and two 90 degrees equals 180. When a planet is in opposition to your native sign, you can expect the most resistance to your goals (as far as the attributes of said planet is concerned). But there is also bountiful opportunities to expand your love life, career goals and dreams. On the flipside, when a planet is at the Return or Conjunction phase, you can find an entire world of new beginnings open up. But, there are still reasons to be cautious, as Returns can feel stifling, due to the lack of dynamic energy. Be warned…\n  \r ',

3: 'Hyper-Quintile: The Hyper-Quintile borrows its name from the ordinary quintile, which represents a planetary aspect 72 degrees from your native sign. Much like quintiles, you can expect a greater proficiency in all things technical during this period and an increased creative streak in your life, but as with all hyper-dimensional aspects, these feelings will be more potent than usual. This is a great time to develop some unique talents and abilities and to make plans for the future. All the Best.\n  \r',

4:'Hyper-Septile: The hyper-septile is a very auspicious planetary aspect. Ruled by the planet Jupiter (or Jove), you can expect a pleasant, or jovial, tint to proceedings, enriched by that planet’s deep spiritual side. This is a great time to go on a spiritual quest, meditate or read up on the deeper, more meaningful aspects of life. It is also a great time to spend with friends and family, or just laughing and joking around. Don’t be so serious all the time, although with a Hyper-Septile in your life, being serious might not really be much of an option for you, anyway.\n  \r',

5: 'Hyper-Squares: As with all hyper-dimensional aspects, the attributes of the ordinary aspects are heightened. During, the ordinary Square Aspect you can expect obstacles to your dreams and relationships, but also a great opportunity for growth and development. A Hyper-Square is just this on steroids. During this period, you may find that things are much more difficult for you, in certain areas, then they otherwise should be. But this is also a prime time to break out of your old habits and encounter the new you head on, free of all the old cobwebs of the past. Great adventures of the spiritual kind, await. Don’t delay.\n\r  Commensurate with the results of Hyper-squares are those of the Hyper-conjunctions and Hyper—oppositions. Ordinary oppositions, can leave you feel torn between two choices, to go or to stay, to marry or to break up. During a Hyper-Opposition, these feelings can be intensified, leaving with with no clue, which avenue to choose. In the case of a Hyper-Return (or Conjunction), you may find things a bit more stable. But, watch-out, Hyper-Returns can be challenging in their own right, as the lack of dynamism and creative impulses can leave you searching for a way out.\n  \r ',

6: 'Hyper-Trines: Hyper-Trines are without a doubt, the best configuration there is in all of astrology. When a planet is in hyper-trine with your native starsign, it will lend it’s specific energy to your life, making you much more successful, then you would be otherwise. During hyper-trines you can expect better relationship prospects, better health, more energy, or deeper insights in the spiritual or material aspects of the world. It all depends which planet is in the mix.\n  \r ',

7: 'The common semi-sextile is, as its name suggests, half the angle of a full sextile. Sextiles are usually beneficials signs, although not as beneficial as trines and semi-sextiles are even less beneficial again. There is great opportunity there, but you have to work for it. It doesn’t just drop into your lap. But, the good news is that with Hyper-Semisextiles, you might not have to work quite so much. Consider it a rest day. You’ve earned it.\n \r '}


planeta={'moon': 'Moon: The Moon rules the human soul and its unconsciousness depths, along with the realm of the emotions, and dreams. When the moon shines in your positive aspects, your instincts are heightened, your moods improve and you might experience a greater potential for interesting and valuable dreams. However, expect a resurgence of old memories when the Moon squares the native star-sign. Don’t give in to past regrets, you are more than the some of your own experiences Your intuition may suffer during this period, so be careful not to place any outlandish bets. You will lose! You may also find that you are moodier than usual. Try not to blow up at that person, when they spill the coffee on your lap. Breathe.\n \r',

'merc':'Mercury: Mercury is the God of communication, reason, language and intellect. He moves swiftly on his heels, gathering information from all corners, before tying it altogether neatly with a strap from one of his sandals. With this planet trined to your native sign, you can expect to communicate your feelings, thoughts and desires more effectively to others. Your energy for all things creative and technical are also greatly increased. When Mercury is Squared with your native sign, you might find it more difficult to say what you really mean and when you do it tends to come out all wrong. Take care not to offend anyone with careless words. If you can get through this little speed bump smoothly, your relationships will go from strength to strength.\n \r',

'ven':'Venus: This Goddess rules the attributes of Love, Attraction, Relationships, Beauty and Art. She is also the bearer of much harmony, in our lives, but she can be deceitful and tempestuous, which are some of her more negative aspects.\n \r',

'mars': 'Mars: Mars rules the aspects of Science, Creation, Forthrightness, Temperance, Courage,  and Passion. His darker side rules the aspects of Aggression, War and Violence.\n \r',

'jupiter': 'Jupiter: Jupiter is a positive planet who rules the area of Luck, Growth, Spiritual Evolution, Goodwill, Cornucopia, and a heightened understanding of ourselves, each other and our place in the universe. Of his less flattering attributes, he can be vain, hedonistic, immoral and spoilt.\n \r',

'saturn': 'Saturn: Saturn is a stern companion. His attributes include the necessity of structure, law, discipline, and responsibility in our daily lives. If we have these and are mindful of the future, Saturn will shine favourably upon us. However, if we have scrimped on our obligations, or failed to live up to our obligations, we will feel the full weight of this planet pressed down on our shoulders.\n \r'}

about = '''Astrological aspects are the names given to the various angles that the planets can make in the sky in relation to star signs and to one another. Anyone who is familiar with these aspects will have heard of Trines (120 degrees), Squares (90 degrees), Sextiles (60 degrees), and Semi-Sextiles (30 degrees). However, fewer of you will have heard of quintiles (75 degrees), septiles(51°26’ ), noniles(40 degrees) or noviles, as they are sometimes called. Each of these aspects partitions the circle into smaller and smaller subsections, but I thought; “Wouldn’t it be wonderful, if we could create new aspects that were larger than the circle round and, in effect, modular (or hyper-dimensional).”

 With that goal in mind, I set about making the Hyper Astrology app, which is supposed to calculate these new aspects for you!

 Hyper-dimensional aspects extend around the circle and often take several years to complete. They aren’t like ordinary aspects, which have a direct relation to the position of the ascendant star sign, or the other celestial bodies, as the angles generated are abstract or, even, metaphorical. However, I believe that these new aspects do have a bearing on the nature of Mankind, by way of twisting space around the Earth (or the Sun, if you prefer).

 Now, I know the concept of warped or twisted space is outlandish, but what isn’t at all outlandish is the idea that the planets above our heads and their motions have a marked effect on our daily lives. And now, for the first time, we can figure out what they are.

 You might be wondering what the little button in the corner; marked ‘Do not filter my results” is. That’s a very good question. The button is disabled by default. However, if you select any hyper-dimensional aspect, it will give you the option to switch off the filter. This option is recommended, as the filter is still in beta mode and can produce unexpected results.

 With the filter off, you will have to proceed manually (See note at bottom of page), which is the best course of action, because then you will be able to see results for the retrograde motion of the planets, which the filter currently isn’t calibrated to deal with.'''

seit= '''How to Manually Filter Results:

  With the filter off, the app will return results for every starsign in consequitive order, including results which are - for our purposes - undesired. So for example, if the slider was set to Square and the native sign was 'scorpio', then we would get a list that might look like this; 'scorpio', 'aquarius', 'taurus', 'leo', scorpio', 'aquarius', 'taurus', 'leo'. However, if the slider is set to Hyper-Square, then the list will look exactly the same; ('scorpio'), 'aquarius', 'taurus', ('leo'), scorpio', 'aquarius', ('taurus'), 'leo', scorpio', ('aquarius'). The signs with the brackets are the ones you are after, in this case. You can use the above radar chart to help you, but a quick rule of thumb is to skip 5 signs for a hyper-quintile, 7 for a hyper-sextile, 8 for a hyper-trine, 9 for a hyper-square and 11 for a hyper-sextile.
  '''

def dropdlist():
    if slider in range(3, 8):
        sd = False
    sd = True
    return(sd)

colors = {
    'background': '#2b2b2c',
}

app.layout = html.Div(children=[
    html.Div([
        html.Br(),
        html.H1('Hyper Astrology', style={ 'font-size': 100,  'margin-top': 15}, 
      className = "nine columns"),
        html.Img(src='/assets/crs-logo-hype.jpg', className = 'three columns', style={'width': '15%', 'float': 'right', 'margin-right': 5, 'z-index': 1, 'margin-top': -15}),
        html.Hr(style={'width':'49%', 'margin-top': -35},
        className='eight columns'),
        html.H5('The Hyper-dimensional Aspects of the Stars', style={'margin-top': -30, 'margin-bottom': 30},
        className='eight columns'),
    ], className = "row"),
    html.Hr(style={'margin-bottom': -20}),
    html.Div(id="inter-sign", style={'display': 'none'}),
    html.Div(id="inter-aspect", style={'display': 'none'}),
    html.Div(id="intermediate-value3", style={'display': 'none'}),
    html.Div(id="intermediate-value4", style={'display': 'none'}),
    html.Div(style={'backgroundColor': colors['background']}, children=[
        html.Br(),
        html.P('Input your Birthdate: Month DD YYYY', style={'color':'#abe2fb', 'font-family': 'arial', 'size': 14, 'margin-left':30}),
        html.Div([
             html.Label('Month', className="two columns", style={'margin-left':30, 'color':'#2ff72c'}),
             html.Label('Day', className="two columns", style={'margin-left':15, 'color':'#2ff72c'}),
             html.Label('Year', className="two columns", style={'margin-left':25, 'color':'#2ff72c'}),
             html.Label('Select a Planet',  style={'color':'#2ff72c'}, className="six columns"),
        ], style={ 'margin-bottom':0}, className = "row"),
        html.Div([
            dcc.Dropdown(
                id='my-dropdown',
                options=[{'label': 'january', 'value': 'january'},
                    {'label': 'february', 'value': 'february'},
                    {'label': 'march', 'value': 'march'},
                    {'label': 'april', 'value': 'april'},
                    {'label': 'may', 'value': 'may'},
                    {'label': 'june', 'value': 'june'},
                    {'label': 'july', 'value': 'july'},
                    {'label': 'august', 'value': 'august'},
                    {'label': 'september', 'value': 'september'},
                    {'label': 'october', 'value': 'october'},
                    {'label': 'november', 'value': 'november'},
                    {'label': 'december', 'value': 'december'},
                ],
                value='january', className="two columns", style={'margin-left':15}),
            dcc.Input(id='days',
                type='text',
                value=13,
            className="two columns", style={'margin-left':30}),
            dcc.Input(id='years',
                type='text',
                value=2015,
            className="two columns", style={'margin-left':30}),
            dcc.RadioItems(id='radio',
                options=[
                    {'label': 'Sun', 'value': 'sun'},
                    {'label': 'Moon', 'value': 'moon'},
                    {'label': 'Mercury', 'value': 'merc'},
                    {'label': 'Venus', 'value': 'ven'},
                    {'label': 'Mars', 'value': 'mars'},
                    {'label': 'Jupiter', 'value': 'jupiter'},
                    {'label': 'Saturn', 'value': 'saturn'},
                ],
                value='ven', labelStyle={'display': 'inline-block', 'color':'#2ff72c'}, className="six columns", style={'margin-left':35}),
        ], className = "row"),
        html.Br(),
        html.Div([
             html.Label('Pick a date range', className="four columns"),
             html.Label('Astrological Aspect'),
        ], style={ 'margin-bottom':0, 'color':'#2ff72c', 'margin-left':30}, className = "row"),
        html.Div([
            html.Div(id='container'),
            html.Div(
                dcc.Slider(
                    min=1,
                    max=7,
                    id='slider',
                    marks={
                        1: {'label': 'Trine',  'style':{'color':'#2ff72c'}},
                        2: {'label': 'Square',  'style':{'color':'#2ff72c'}},
                        3: {'label': 'Hyper-Quintile',  'style':{'color':'#2ff72c'}},
                        4: {'label': 'Hyper-Septile',  'style':{'color':'#2ff72c'}},
                        5: {'label': 'Hyper-Square',  'style':{'color':'#2ff72c'}},
                        6: {'label': 'Hyper-Trine',  'style':{'color':'#2ff72c'}},
                        7: {'label': 'Hyper-Semi-sextile',  'style':{'color':'#2ff72c'}},
                    },
                    value=2,
                className = 'seven columns'),
            style={'margin-top':20, 'margin-bottom':0, 'margin-left':30}),
        ], className='row', style={'margin-left':30, 'margin-bottom':40}),
        html.Br(),
    ]),
    html.Hr(style={'margin-top': 0}),
    html.H3('Hyper Astrological Aspects'),
    html.Div([
        dcc.Graph(id='plot', style={'height': '90vh','margin-left':40},  className="six columns"),
        html.Textarea(id='text_box', readOnly = 'True', style={'width': '40%',  'height': '75vh',  'padding-top': 20, 'padding-bottom': 40, 'background-color': '#ffffff', 'border-radius': 1,  'resize': 'none', 'font-family': 'arial', 'size': 14, 'border-color': 'black', 'margin-top': 40, 'margin-right': 0}, className="five columns"),
    ], className = "row"),
    html.Hr(style={'margin-top': 0}),
    html.Div([
        html.H3('Hyper-dimensional Astrological Aspect Results', style={'margin-top':-5}, className = 'five columns'),
        html.Div(id='drop-filter', className="three columns offset-by-two"),
        html.Button('Calculate', id='button', style={'background-color': '#2ff72c'}, className = 'two columns'),
    ], className = "row"),
    html.Div([
        html.Div(id='data_base', style={'margin-top': 40, 'margin-bottom':0}),
        html.P(seit, style={'width': '90%', 'padding-top': 20, 'padding-bottom': 40, 'font-family': 'arial', 'size': 10, 'margin-top': 40, 'margin-left': 40},),
    ], className = "row"),
        html.Hr(),
    html.Div(style={'backgroundColor': colors['background'], 'margin-top':-60, 'margin-bottom':0}, children=[
        html.Br(),
        html.Br(),
        html.Footer(
            html.Center(
            dcc.Markdown('''[Cataphysical Research Society - 2019](https://cataphysical-research-society.herokuapp.com)''')),
        ),
        html.Br(),
        html.Br(),
    ], className = "row"),
])


@app.callback(Output('drop-filter', 'children'),
                        [Input('slider', 'value')])
def filters(slider):
    if slider in range(3, 8):
        sd = False
    else:
        sd = True
    return dcc.Dropdown(
            id='my-dropdown2',
            options=[{'label': 'Filter my search results (Beta)', 'value': 'filter'},
                    {'label': "Don't filter my results (recommended)", 'value': 'no-filter'},
            ],
            value='filter', disabled=sd),


@app.callback(Output('inter-sign', 'children'),
                        [Input('days', 'value'),
                        Input('my-dropdown', 'value'),
                        Input('years', 'value')])
def stars(days, mydropdown, years):
    # Get the user's starsign
    month = mydropdown
    if days != None and years != None:
        days = int(days)
        if month == 'january':
            astro_sign = 'capricorn' if (days < 20) else 'aquarius'
        elif month == 'february':
            astro_sign = 'aquarius' if (days < 19) else 'pisces'
        elif month == 'march':
            astro_sign = 'pisces' if (days < 21) else 'aries'
        elif month == 'april':
            astro_sign = 'aries' if (days < 20) else 'taurus'
        elif month == 'may':
            astro_sign = 'taurus' if (days < 21) else 'gemini'
        elif month == 'june':
            astro_sign = 'gemini' if (days < 21) else 'cancer'
        elif month == 'july':
            astro_sign = 'cancer' if (days < 23) else 'leo'
        elif month == 'august':
            astro_sign = 'leo' if (days < 23) else 'virgo'
        elif month == 'september':
            astro_sign = 'virgo' if (days < 23) else 'libra'
        elif month == 'october':
            astro_sign = 'libra' if (days < 23) else 'scorpio'
        elif month == 'november':
            astro_sign = 'scorpio' if (days < 22) else 'sagitarius'
        elif month == 'december':
            astro_sign = 'sagittarius' if (days < 22) else 'capricorn'
        return(astro_sign)

@app.callback(Output('container', 'children'),
                        [Input('days', 'value'),
                        Input('my-dropdown', 'value'),
                        Input('years', 'value')])
def stars(days, mydropdown, years):
    f = months.index(mydropdown)
    dates = f+1
    d = datetime.datetime.now()
    year = d.year
    year2 = year+1
    days=int(days)
    return dcc.DatePickerRange(
        id='date-range',
        end_date=dt(year2, 1, 14),
        start_date=dt(year, dates, days),
        min_date_allowed=dt(1800, 1, 1),
        max_date_allowed=dt(2099, 12, 31),
        initial_visible_month=dt(year2, 1, 14),
    className="four columns"),

@app.callback(Output('inter-aspect', 'children'),
                        [Input('inter-sign', 'children'),
                        Input('button', 'n_clicks')],
                        state = [State('days', 'value'),
                        State('my-dropdown', 'value'),
                        State('years', 'value'),
                        State('slider', 'value')])
def aspect(intersign, n_clicks, days, mydropdown, years, slider):
    # Find the position of the sun with respect to user's birthdate
    if days != None and years != None:
        url = 'https://horoscopes.astro-seek.com/astrology-ephemeris-' + str(mydropdown) + '-' + str(years)
        html = urlopen(url)

        soup = BeautifulSoup(html, 'lxml')

        table = soup.findAll('table')
        df = pd.read_html(str(table))
        df= (df[0].to_json(orient='split'))
        df = pd.read_json(df, orient='split')

        df1 = df.loc[df[0] == str(days)].values.tolist()
        df2=df1[0]
        df3 = (df2[3])
        df4 = re.split('[°\'"]+', df3)
        df5 = df4[1]
        df6 = df5[:-1]
        df4.pop()
        df4.append(df6)
        df7=[]
        for i in df4:
            gf = int(i)
            df7.append(gf)
        # Find the degree of the planet in terms of its corresponding hyper-geometric aspect
        if slider == 1:
            degs = [0, 120, 240, 360]
        elif slider == 2:
            degs = [0, 90, 180, 270, 360]
        elif slider == 3:
            degs = [0, 150, 300, 90, 240, 30, 180, 330, 120, 270, 60, 210, 360]
        elif slider == 4:
            degs = [0, 210, 60, 270, 120, 330, 180, 30, 240, 90, 300, 150, 360]
        elif slider == 5:
            degs = [0, 270, 180, 90, 360]
        elif slider == 6:
            degs = [0, 240, 120]
        elif slider == 7:
            degs = [0, 330, 300, 270, 240, 210, 180, 150, 120, 90, 60, 30, 360]
        signlist=[]
        signlist.append(df7[1])
        for i in degs:
            v = df7[0] + i
            house = v//30
            mod = v % 30
            loc = starsigns.index(intersign)
            modum=house%12
            g = (loc+modum)%12
            sign=starsigns[g]
            signlist.append(sign)
        signlist.append(df7[0])
        return(signlist)

@app.callback(Output('intermediate-value3', 'children'),
                        [Input('radio', 'value'),
                        Input('days', 'value'),
                        Input('my-dropdown', 'value'),
                        Input('years', 'value'),
                        Input('inter-aspect', 'children'),
                        Input('date-range', 'start_date'),
                        Input('date-range', 'end_date')])
def update_graph(radio, days, mydropdown, years, interaspect, start_date, end_date):
    #Create Url list for use in search
    try:
        end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")
    except:
        end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d %H:%M:%S")
    try:
        start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
    except:
        start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d %H:%M:%S")
    j = mydropdown
    delta = int(end_date.year - start_date.year)+1
    months2 = months * delta
    lenmo=(len(months2))

    list1=[]
    while len(list1) < lenmo:
        list1.append(start_date.year)

    list2=[]
    for idx, val in enumerate(list1):
        idx2 = idx // 12
        val2 = val + idx2
        list2.append(str(val2))


    totalists = list(zip(months2, list2))

    urls=[]
    for idx, val in enumerate(totalists):
        totalist2=totalists[idx]
        url =  'https://horoscopes.astro-seek.com/astrology-ephemeris-' + totalist2[0] + '-' + totalist2[1]
        urls.append(url)


    if delta == 1:
        s = months2.index(j)
        st = urls[s:end_date.month]
    elif delta == 2:
        s = months2.index(j)
        ydelta = 12+end_date.month
        st = urls[s:ydelta]
    else:
        s = months2.index(j)
        ydelta = delta - 1
        t = (ydelta * 12) +end_date.month
        st = urls[s:t]

    listo = []
    for url in st:
        # Get a list of starsigns and positions
        html = urlopen(url)

        soup = BeautifulSoup(html, 'lxml')

        type5 = soup.findAll(attrs={'class':'udaj_planeta'})
        type5.append(0)
        type6 = np.array(type5)
        type7 = np.roll(type6,1).tolist()
        if radio == "sun":
            type8 = type7[1::13]
        elif radio == "moon":
            type8 = type7[2::13]
        elif radio == "merc":
            type8 = type7[3::13]
        elif radio == "ven":
            type8 = type7[4::13]
        elif radio == "mars":
            type8 = type7[5::13]
        elif radio == "jupiter":
            type8 = type7[6::13]
        elif radio == "saturn":
            type8 = type7[7::13]
        lex = len(type8)
        ranlex = list(range(0, lex))
        for c in ranlex:
            zim = type8[c]
            zim = str(zim)
            clean = zim.replace('<td class="udaj_planeta"><img alt="" src="https://www.astro-seek.com/seek-images/seek-icons/horoskop-p-', '')
            clean = clean.replace('.png" style="margin: 0 1px -3px 2px;"/>', ' ')
            clean = clean.replace('<span style="font-weight: normal; font-size: 1.1em;">0','')
            clean = clean.replace('<span style="font-weight: normal; font-size: 1.1em;">','')
            clean = clean.replace('<span style="font-size: 0.85em; margin: -4px 0 4px 0;">',' ')
            clean = clean.replace('</span></td>', '')
            clean = clean.replace('</span>', '')
            clean = clean.replace('</td>', '')
            clean = clean.replace("°", "")
            if radio == "moon" or radio == "merc" or radio == "sun":
                type5 = clean[:-1]
            else:
                type5 = clean
            listo.append(type5)
            c+=1
    # make starsign list
    signs = []
    for i in listo:
        x = ''.join(filter(str.isalpha, i))
        signs.append(x)
    # make position list
    pos = []
    for i in listo:
        x = ''.join(filter(str.isdigit, i))
        if radio == "moon" or radio == "merc" or radio == "sun":
            try:
                if x[0] == '0':
                    x = x[1:]
                    pos.append(x)
                else:
                    pos.append(x)
            except IndexError:
                pos.append('0')
        else:
            pos.append(x)
    info=[]
    del signs[:start_date.day-1]
    del pos[:start_date.day-1]

    # make position list useable
    if radio == 'moon' or radio == 'merc' or radio=='sun':
        pos2=[int(x) for x in pos]
    else:
        pos2=[]
        for x in pos:
            c = int(x)
            b = c*100
            pos2.append(b)

    # find ranges of starsigns traversed by planets
    # find indices for splicing
    signs1 = np.array(signs)
    gen3=[]
    siop=[]
    e12=[]
    for f in interaspect[1:-1]:
        e8 = [signs1 != f]
        e9 = np.ma.masked_array(signs1,e8)
        e10 = e9.tolist()
        e11=[x for x in e10 if x is not None]
        e12.append(e11)
        f9 = np.ma.masked_array(pos2,e8)
        f10 = f9.tolist()
        f11=[x for x in f10 if x is not None]
        gen3.append(f11)
        for idx, val in enumerate(e8[0]):
            if val == False:
                siop.append(idx)
    siop2=np.array(siop)
    siop3=np.roll(siop2, 1)
    siop4=siop2-siop3
    siop5 = siop4.tolist()
    siop6=[]
    for idx, val in enumerate(siop5):
        if val != 1:
            siop6.append(idx)

    e13 = [val for sublist in e12 for val in sublist]
    gen4 = [val for sublist in gen3 for val in sublist]

    # splice indices

    lensi=len(siop6)
    jj=0
    kk=1
    zaa=[]
    zax0=[]
    pos9=[]
    while kk <= lensi:
        if kk >= lensi:
            des = gen4[siop6[jj]:]
            res = e13[siop6[jj]:]
            ind= siop[siop6[jj]:]
        else:
            des = gen4[siop6[jj]:siop6[kk]]
            res = e13[siop6[jj]:siop6[kk]]
            ind= siop[siop6[jj]:siop6[kk]]
        pos3=des
        star3=res
        muv=ind
        pos9.append(pos3)
        zaa.append(star3)
        zax0.append(muv)
        jj+=1
        kk+=1

    # starsigns ranges

    e13=[]
    for i in zaa:
        e13.append(i[0])

    pos10=np.array(pos9)
    zax=np.array(zax0)

    # fix ranges and make lists equivalent lengths

    pos8=[]
    zax2=[]
    for zg in range(len(pos10)-1):
        zk = pos10[zg]
        if zk[0] == 0:
            pos8.append(zk)
            zax3 = zax[zg]
            zax2.append(zax3)
        elif zk[0] == 3000:
            pos8.append(zk)
            zax3 = zax[zg]
            zax2.append(zax3)
        else:
            if  zk[0] >1500:
                pos4= np.array([3000])
                pos5 = np.concatenate((pos4, zk), axis=None).tolist()
                pos8.append(pos5)
                zax3 = zax[zg]
                zax4= np.array([zax3[0]])
                zax5 = np.concatenate((zax4, zax3), axis=None).tolist()
                zax2.append(zax5)
            elif zk[0] < 1500:
                pos4= [0]
                pos5 = np.concatenate((pos4, zk), axis=None).tolist()
                pos8.append(pos5)
                zax3 = zax[zg]
                zax4= np.array([zax3[0]])
                zax5 = np.concatenate((zax4, zax3), axis=None).tolist()
                zax2.append(zax5)
    pos7=[]
    zax6=[]
    for gz in range(len(pos8)-1):
        kz = pos8[gz]
        zax3 = zax2[gz]
        if kz[-1] ==3000:
            pos7.append(kz)
            zax6.append(zax3)
        elif kz[-1] == 0:
            pos7.append(kz)
            zax6.append(zax3)
        else:
            if  kz[-1] >1500:
                kz.append(3000)
                pos7.append(kz)
                zax3.append(zax3[-1])
                zax6.append(zax3)
            elif kz[0] < 1500:
                kz.append(0)
                pos7.append(kz)
                zax3.append(zax3[-1])
                zax6.append(zax3)

    zax9 = [val for sublist in zax6 for val in sublist]
    pos12 = [val for sublist in pos7 for val in sublist]

    zax6=[]
    zax7=[]
    for i in range(len(pos12)-1):
        if pos12[i] == 0:
            zax6.append(i)
        elif pos12[i]==3000:
            zax7.append(i)
    zax8=zip(zax6, zax7)
    tren=(list(zax8))

    # evaluate if the users position is in range
    gen2=[]
    for i in tren:
        pos22=pos12[i[0]:i[1]]
        lex4 = len(pos22)
        pos33 = []
        pos33.append(interaspect[-1])
        pos33.append(interaspect[0])
        s = [str(n) for n in pos33]
        m = ("".join(s))
        m = int(m)
        c = 0
        k = 1
        start=True
        while start and k <= lex4-1:
            if pos22[k] - pos22[c] == 3000:
                c+=1
                k+=1
            elif pos22[k] - pos22[c] == -3000:
                c+=1
                k+=1
            else:
                if m in range(pos22[c], pos22[k]):
                    gen2.append(k+i[0])
                    c+=1
                    k+=1
                    start=False
                else:
                    c+=1
                    k+=1
    scorp=[]
    for i in gen2:
        tem = zax9[i]
        scorp.append(tem)
    dates=[]
    for i in scorp:
        d = start_date+timedelta(days=(i))
        dates.append(d)
    z = len(dates)
    four=[]
    four.append(z)
    for i in dates:
        timestampStr = i.strftime("%Y-%m-%d")
        four.append(timestampStr)
    for i in e13:
        four.append(i)
    return (four)

@app.callback(Output('plot', 'figure'),
                        [Input('slider', 'value'),
                        Input('inter-sign', 'children')])
def update_graph3(slider, intersign):
    starsigns1=starsigns[::-1]
    ssigns=starsigns1*2
    gsign=ssigns.index(intersign)
    signs=ssigns[gsign-3:gsign+10]
    theta = signs[:]

    def rabout():
        colorway=['#32a332', '#d72e2f', '#9467bd', '#3282ba', '#ff7f0e']
        if slider in range(4, 7):
            colorway=colorway[::-1]
            return(colorway)
        else:
            return(colorway)

    if slider == 1:
        data = [go.Scatterpolar(
          r =  [29, 25, 29, 50, 29],
          theta = theta[:5],
          marker= dict(size= 2, colorscale='Rainbow'),
        ),
        go.Scatterpolar(
          r =  [29, 25, 29, 50, 29],
          theta = theta[4:9],
          marker= dict(size= 2, colorscale='Rainbow'),
        ),
        go.Scatterpolar(
          r =  [29, 25, 29, 50, 29],
          theta = theta[8:],
          marker= dict(size= 2, colorscale='Rainbow'),
        )
        ]
    elif slider == 2:
        data = [go.Scatterpolar(
          r = [50, 37, 37, 50],
          theta = theta[:4],
          marker= dict(size= 2, colorscale='Rainbow'),
        ),
        go.Scatterpolar(
          r = [50, 37, 37, 50],
          theta = theta[3:7],
          marker= dict(size= 2, colorscale='Rainbow'),
        ),
        go.Scatterpolar(
          r = [50, 37, 37, 50],
          theta = theta[6:10],
          marker= dict(size= 2, colorscale='Rainbow'),
        ),
        go.Scatterpolar(
          r = [50, 37, 37, 50],
          theta = theta[9:],
          marker= dict(size= 2, colorscale='Rainbow'),
        )
        ]
    elif slider == 3:
        data = [go.Scatterpolar(
          r = [50, 18, 13.25, 13.25, 18, 50, 18, 13.25, 13.25, 18, 50, 18, 13.25],
          theta = theta,
          marker= dict(size= 2, colorscale='Rainbow'),
        ),
        go.Scatterpolar(
          r = [13.25, 13.25, 18, 50, 18, 13.25, 13.25, 18, 50, 18, 13.25, 13.25, 18],
          theta = theta,
          marker= dict(size= 2, colorscale='Rainbow'),
        ),
        go.Scatterpolar(
          r = [18, 50, 18, 13.25, 13.25, 18, 50, 18, 13.25, 13.25, 18, 50, 18],
          theta = theta,
          marker= dict(size= 2, colorscale='Rainbow'),
        ),
        go.Scatterpolar(
          r = [18, 13.25, 13.25, 18, 50, 18, 13.25, 13.25, 18, 50, 18, 13.25, 13.25],
          theta = theta,
          marker= dict(size= 2, colorscale='Rainbow'),
        ),
        go.Scatterpolar(
          r = [13.25, 18, 50, 18, 13.25, 13.25, 18, 50, 18, 13.25, 13.25, 18, 50],
          theta = theta,
          marker= dict(size= 2, colorscale='Rainbow'),
        )
        ]
    elif slider == 4:
        data = [go.Scatterpolar(
          r = [50, 18, 13.25, 13.25, 18, 50, 18, 13.25, 13.25, 18, 50, 18, 13.25],
          theta = theta,
          marker= dict(size= 2, colorscale='Rainbow', reversescale=True),
        ),
        go.Scatterpolar(
          r = [13.25, 13.25, 18, 50, 18, 13.25, 13.25, 18, 50, 18, 13.25, 13.25, 18],
          theta = theta,
          marker= dict(size= 2, colorscale='Rainbow', reversescale=True),
        ),
        go.Scatterpolar(
          r = [18, 50, 18, 13.25, 13.25, 18, 50, 18, 13.25, 13.25, 18, 50, 18],
          theta = theta,
          marker= dict(size= 2, colorscale='Rainbow', reversescale=True),
        ),
        go.Scatterpolar(
          r = [18, 13.25, 13.25, 18, 50, 18, 13.25, 13.25, 18, 50, 18, 13.25, 13.25],
          theta = theta,
          marker= dict(size= 2, colorscale='Rainbow', reversescale=True),
        ),
        go.Scatterpolar(
          r = [13.25, 18, 50, 18, 13.25, 13.25, 18, 50, 18, 13.25, 13.25, 18, 50],
          theta = theta,
          marker= dict(size= 2, colorscale='Rainbow', reversescale=True),
        )
        ]
    elif slider == 5:
        data = [go.Scatterpolar(
          r = [50, 37, 37, 50],
          theta = theta[:4],
          marker= dict(size= 2, colorscale='Rainbow', reversescale=True),
        ),
        go.Scatterpolar(
          r = [50, 37, 37, 50],
          theta = theta[3:7],
          marker= dict(size= 2, colorscale='Rainbow', reversescale=True),
        ),
        go.Scatterpolar(
          r = [50, 37, 37, 50],
          theta = theta[6:10],
          marker= dict(size= 2, colorscale='Rainbow', reversescale=True),
        ),
        go.Scatterpolar(
          r = [50, 37, 37, 50],
          theta = theta[9:],
          marker= dict(size= 2, colorscale='Rainbow', reversescale=True),
        )
        ]
    elif slider == 6:
        data = [go.Scatterpolar(
          r =  [29, 25, 29, 50, 29],
          theta = theta[:5],
          marker= dict(size= 2, colorscale='Rainbow', reversescale=True),
        ),
        go.Scatterpolar(
          r =  [29, 25, 29, 50, 29],
          theta = theta[4:9],
          marker= dict(size= 2, colorscale='Rainbow', reversescale=True),
        ),
        go.Scatterpolar(
          r =  [29, 25, 29, 50, 29],
          theta = theta[8:],
          marker= dict(size= 2, colorscale='Rainbow', reversescale=True),
        )
        ]
    elif slider == 7:
        data = [go.Scatterpolar(
          r =  [50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50],
          theta = theta,
          marker= dict(size= 2, colorscale='Rainbow'),
        )
        ]
    layout = go.Layout(
      polar = dict(
        radialaxis = dict(
          visible = False,
          range = [0, 50]
        )
      ),
      colorway=rabout(),
      margin= {
        "b": 49,
        "r": 72,
        "t": 20,
        "pad": 0
      },
      showlegend = False,
    )

    fig = go.Figure(data=data, layout=layout)
    return(fig)

@app.callback(dash.dependencies.Output('text_box', 'value'),
              [dash.dependencies.Input('slider', 'value'),
               dash.dependencies.Input('radio', 'value')])
def func(slider, radio):
    planetary=['sun', 'moon', 'merc', 'ven', 'mars', 'jupiter', 'saturn']
    title1='ASPECT:\n \r'
    title2='PLANET:\n \r'
    title3='ABOUT THIS APP:\n \r'
    for i in range(1, 8):
        for c in planetary:
            if slider == i and radio == c:
                return('{}{}{}{}{}{}'.format(title1, aspect12[i], title2, planeta[c], title3, about))

@app.callback(Output('data_base', 'children'),
                        [Input('intermediate-value3', 'children'),
                        Input('radio', 'value'),
                        Input('slider', 'value'),
                        Input('inter-aspect', 'children'),
                        Input('my-dropdown2', 'value')])
def update_data(intermediatevalue3, radio, slider, interaspect, mydropdown2):
    g = intermediatevalue3[0]
    y1 = interaspect[1:-1]
    y1=y1[:-1]
    dates=intermediatevalue3[1:g+1]
    signs=intermediatevalue3[g+1:]
    base=intermediatevalue3[-1]
    planet = radio
    det=zip(dates, signs)
    df = pd.DataFrame(det, columns=['Dates', 'Signs'])
    df1 = df.sort_values(by=['Dates'])
    df4 = df1.drop_duplicates()
    df1 = df4.reset_index(drop=True)
    kel = g*2+1
    dax = range(1, 3)
    if slider in dax:
        return html.Table(
            # Header
            [html.Tr([html.Th(col) for col in df1.columns])] +

            # Body
            [html.Tr([
                html.Td(df1.iloc[i][col]) for col in df1.columns
            ]) for i in range(min(len(df1), kel))],
        )
    else:
        if mydropdown2 == 'filter':
            df2 = df1.to_dict()
            light=[]
            sim=[]
            #Create dictionary from dataframe
            for i in df2['Signs']:
                light.append(df2['Signs'][i])
                sim.append(df2['Dates'][i])

            top = (len(sim))
            if slider == 5:
                loe = 3
            elif slider == 6:
                loe = 2
            elif slider == 7:
                loe = 11
            elif slider == 3:
                loe = 5
            elif slider == 4:
                loe = 7
            #Create modular field of results to search through (like a V. Cipher table)
            steel = []
            glass = []
            for idx, val in enumerate(light):
                card = light[idx::loe]
                steel.append(card)
                card2 = sim[idx::loe]
                glass.append(card2)


            chi = len(steel)//2

            if len(y1) != len(steel[0]):
                if len(y1) < len(steel[0]):
                    zen = len(steel[0])//len(y1)
                else:
                    zen = len(y1)//len(steel[0])
                if zen >= 1:
                    y2 = y1*zen
                    y3 = y2[:len(steel[0])]
                else:
                    y3 = y1[:len(steel[0])]
            else:
                y3=y1

            y4 = np.array(y3)
            steel = np.array(steel)

            cop = list(range(1, chi))
            cos = [i*-1 for i in cop]
            com = [ [cop[i], cos[i]] for i in range(len(cop)) ]
            com2 = [k for z in com for k in z]

            torz=[]
            torz2=[]
            go=0
            mm=0
            steel2=steel[0]
            while go <= len(y4)-1:
                if steel2[go] != y4[go]:
                    while mm <= len(com2)-1:
                        gel=com2[mm]
                        gunit=steel[gel]
                        gun2=glass[gel]
                        try:
                            if gunit[go] == y4[go]:
                                torz.append(gunit[go])
                                torz2.append(gun2[go])
                                go+=1
                            mm+=1
                        except:
                            try:
                                mm+=1
                            except:
                                go+=1
                else:
                    torz.append(y4[go])
                    torz2.append(sim[go])
                go+=1
            det2=zip(torz2, torz)
            df = pd.DataFrame(det2, columns=['Dates', 'Signs'])
            kel=(len(torz))
            return html.Table(
                # Header
                [html.Tr([html.Th(col) for col in df.columns])] +

                # Body
                [html.Tr([
                    html.Td(df.iloc[i][col]) for col in df.columns
                ]) for i in range(min(len(df), kel))],
            )
        else:
            return html.Table(
                # Header
                [html.Tr([html.Th(col) for col in df1.columns])] +

                # Body
                [html.Tr([
                    html.Td(df1.iloc[i][col]) for col in df1.columns
                ]) for i in range(min(len(df1), kel))],
            )


if __name__ == '__main__':
    app.run_server(debug=True)
