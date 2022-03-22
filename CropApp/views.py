from django.shortcuts import render
from CropApp.models import CreateUser
import pickle
from utility.namedutils import fertilizer_dic
from utility import croprecommend
from utility.scraper import heading_list, final_content, image_urls, schemes_content, final_image
# from utility.sentiment import getlabel, getscore
import pandas as pd
import numpy as np

# spacy for ner

import spacy
from spacy import displacy
nlp = spacy.load('en_core_web_md')

# Loading the Crop Recommendation Model

file = open('CropApp/Crop_recommendation_model_svc.pkl', 'rb')
svm = pickle.load(file)
file.close()


file1 = open('CropApp/crop_yeildprediction_model_dtree.pkl', 'rb')
dtree = pickle.load(file1)
file1.close()

# loading the croprecommendation file

crop_recomend = pd.read_csv('./utility/Crop_recommendation.csv')
recommendation_map = croprecommend.runcode(crop_recomend)

# User Login


def login(request, methods=['GET', 'POST']):
    final_dict = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        count = 1
        for user in CreateUser.objects.all():
            final_dict[count] = user.__dict__
            count += 1

        final_users = []
        final_passwords = []
        for key, value in final_dict.items():
            for key1, value1 in value.items():
                if key1 == 'username':
                    final_users.append(value1)
                if key1 == 'password':
                    final_passwords.append(value1)

        # print(f'Final Passwords: {final_passwords}')
        # print(f'Final Users : {final_users}')
        user_map = {}
        for key, value in final_dict.items():
            for key1, value1 in value.items():
                if key1 == 'username':
                    user_map[value[key1]] = value['password']

        # print(f' Final dict is : {user_map}')

        if username == '':
            context = {'createvalue': True, 'username': True}
            return render(request, 'createerror.html', context=context)

        elif password == '':
            context = {'createvalue': True, 'password': True}
            return render(request, 'createerror.html', context=context)

        elif username in user_map.keys():
            if password == user_map[username]:
                return render(request, 'home.html')

            else:
                context = {'setuser': True}
                return render(request, 'login.html', context)
        else:
            context = {'createvalue': True, 'usernotfound': True}
            return render(request, 'login.html', context)

    return render(request, 'login.html')


# User Registration

def createaccount(request, methods=['GET', 'POST']):

    all_users = {}
    count = 1
    for user in CreateUser.objects.all():
        all_users[count] = user.__dict__
        count += 1
    fullnames = []
    usernames = []
    passwords = []
    for key, value in all_users.items():
        for key1, val1 in value.items():
            if key1 == 'fullname':
                fullnames.append(val1)
            if key1 == 'username':
                usernames.append(val1)
            if key1 == 'password':
                passwords.append(val1)

    # print(f' AllFullnamess are : {fullnames}')
    # print(f' All Usernames are : {usernames}')
    # print(f' Password is : {passwords}')

    if request.method == 'POST':
        fullname = request.POST.get('name')
        username = request.POST.get('username')
        password = request.POST.get('password')

        if fullname == '':
            context = {'value': True, 'fullname': True}
            return render(request, 'createerror.html', context=context)

        elif username == '':
            context = {'value': True, 'username': True}
            return render(request, 'createerror.html', context=context)

        elif password == '':
            context = {'value': True, 'password': True}
            return render(request, 'createerror.html', context=context)

        elif fullname in fullnames or username in usernames or password in passwords:
            context = {'value': True, 'userexists': True}
            return render(request, 'createerror.html', context=context)

        else:
            instance = CreateUser(
                fullname=fullname, username=username, password=password)
            instance.save()
            context = {'value': True}
            return render(request, 'login.html', context=context)

    return render(request, 'createaccount.html')


def homepage(request, methods=['GET', 'POST']):
    return render(request, 'home.html')


# recommendation page

def recommend(request, methods=['GET', 'POST']):

    mapper = {1: 'rice', 2: 'maize', 3: 'chickpea', 4: 'kidneybeans', 5: 'pigeonpeas', 6: 'mothbeans', 7: 'mungbean',
              8: 'blackgram', 9: 'lentil', 10: 'pomegranate', 11: 'banana', 12: 'mango', 13: 'grapes',
              14: 'watermelon', 15: 'muskmelon', 16: 'apple', 17: 'orange', 18: 'papaya', 19: 'coconut', 20: 'cotton', 21: 'jute', 22: 'coffee'}
    if request.method == 'POST':

        nitrogen = request.POST.get('nitrogen')
        phosphorus = request.POST.get('phosphorus')
        potassium = request.POST.get('potassium')
        temperature = request.POST.get('temperature')
        humidity = request.POST.get('humidity')
        ph = request.POST.get('ph')
        rainfall = request.POST.get('rainfall')

        if nitrogen == '' or phosphorus == '' or potassium == '' or temperature == '' or humidity == '' or ph == '' or rainfall == '':

            context = {'error2': True}
            return render(request, 'recommendation.html', context=context)

        elif int(nitrogen) <= 0 or int(phosphorus) <= 0 or int(potassium) <= 0 or int(temperature) <= 0 or int(humidity) <= 0 or int(ph) <= 0 or int(rainfall) <= 0:

            context = {'error1': True}
            return render(request, 'recommendation.html', context=context)

        elif (int(nitrogen) < 1 or int(nitrogen) > 140) or (int(phosphorus) < 1 or int(phosphorus) > 145) or (int(potassium) < 1 or int(potassium) > 205) or (int(temperature) < 1 or int(temperature) > 45) or (int(humidity) < 1 or int(humidity) > 100) or (int(ph) < 1 or int(ph) > 10):

            context = {'error3': True}
            return render(request, 'recommendation.html', context=context)

        input_features = [nitrogen, phosphorus, potassium,
                          temperature, humidity, ph, rainfall]

        inf = svm.predict([input_features])
        inf = inf[0]
        value = mapper[inf]
        print(value)

        value_params = list(
            crop_recomend[crop_recomend['label'] == value].iloc[1])[:-1]

        print()

        recommendations = list(recommendation_map[value].keys())
        recomendedparams = []
        for crop in recommendations:
            recomendedparams.append(
                list(crop_recomend[crop_recomend['label'] == crop].iloc[1])[:-1])

        print(recomendedparams)
        print()
        recommendations = [i.capitalize() for i in recommendations]

        df = pd.read_csv('./utility/fertilizer.csv')
        # print(df.head())

        nitro = df[df['Crop'] == value]['N'].iloc[0]
        phos = df[df['Crop'] == value]['P'].iloc[0]
        pota = df[df['Crop'] == value]['K'].iloc[0]
        # print(f' Nitrogen is : {nitro},phos is : {phos},potassium is : {pota}')
        # print(nitrogen)

        print(int(nitro)-int(nitrogen))

        n = int(nitro)-int(nitrogen)
        p = int(phos)-int(phosphorus)
        k = int(pota)-int(potassium)

        temp = {abs(n): "N", abs(p): "P", abs(k): "K"}
        max_val = temp[max(temp.keys())]
        print(f' Max val is : {max_val}')

        if max_val == 'N':
            if n < 0:
                key = 'NHigh'

            else:
                key = 'Nlow'

        elif max_val == 'P':
            if p < 0:
                key = 'PHigh'
            else:
                key = 'Plow'

        else:
            if k < 0:
                key = 'KHigh'
            else:
                key = 'Klow'

        response = str(fertilizer_dic[key])

        value = value

        context = {'inf': response, 'value': value,
                   'recommend': recommendations,
                   'recommended_params': recomendedparams}
        return render(request, 'recommendationresult.html', context=context)

    return render(request, 'recommendation.html')


# yeild prediction

def yeild(request, methods=['GET', 'POST']):

    if request.method == 'POST':

        season = request.POST.get('season')
        cropharvested = request.POST.get('crop')
        area = request.POST.get('cultivation')

        if season == '' or cropharvested == '' or area == '':
            context = {'error2': True}
            return render(request, 'yeild.html', context=context)

        elif int(season) <= 0 or int(cropharvested) <= 0 or int(area) <= 0:

            context = {'error1': True}
            return render(request, 'yeild.html', context=context)

        area = np.log(float(area))+1
        input_features = [int(season), int(cropharvested), area]
        print(input_features)

        inf = dtree.predict([input_features])
        result = round(np.exp(inf)[0])

        context = {'value': result}
        return render(request, 'yeildresult.html', context=context)

    return render(request, 'yeild.html')


# dashboard

def dashboard(request, methods=['GET', 'POST']):

    # preprocess the string

    results = str(request.get_full_path).split('?')
    suggestedcrop = str(results[1]).split('=')[1].lower()
    actualcrop = str(results[2]).split('=')[1].split("'")[0]
    print(suggestedcrop.lower(), actualcrop)

    suggesteddata = list(
        crop_recomend[crop_recomend['label'] == suggestedcrop].iloc[1])[:-1]
    actualdata = list(
        crop_recomend[crop_recomend['label'] == actualcrop].iloc[1])[:-1]

    n_values = [suggesteddata[0], actualdata[1]]
    p_values = [suggesteddata[1], actualdata[1]]
    k_values = [suggesteddata[2], actualdata[2]]
    temp_values = [suggesteddata[3], actualdata[3]]
    humidity_values = [suggesteddata[4], actualdata[4]]
    ph_values = [suggesteddata[5], actualdata[5]]

    context = {'suggestedcrop': suggestedcrop.capitalize(),
               'actualcrop': actualcrop.capitalize(),
               'n_values': n_values,
               'p_values': p_values,
               'k_values': k_values,
               'temp_values': temp_values,
               'humidity_values': humidity_values,
               'ph_values': ph_values,
               }

    # make the dataset

    return render(request, 'dashboard.html', context=context)


# blog

def blog(request, methods=['GET', 'POST']):

    # print(heading_list)
    mylist = zip(heading_list, final_content, image_urls)
    context = {
        'mylist': mylist,
    }
    return render(request, 'blog.html', context=context)


# spacy-ner helper function

def showents(doc):

    label_map = {}
    if doc.ents:
        for ent in doc.ents:

            if ent.label_ in label_map:
                label_map[ent.label_] += 1
            else:
                label_map[ent.label_] = 1

    else:
        pass

    return label_map


# blog content

def blogcontent(request, methods=['GET', 'POST']):

    HTML_WRAPPER = """<div style="overflow-x: auto; border: 1px solid #e6e9ef; border-radius: 0.25rem; padding: 1rem">{}</div>"""

    results = str(request.get_full_path).split(
        '?')[1].split('=')[1].split("'")[0]
    finalcontent = final_content[int(results)]

    doc = nlp(finalcontent)
    label_map = showents(doc)
    html = displacy.render(doc, style="ent")
    html = html.replace("\n\n", "\n")
    result = HTML_WRAPPER.format(html)
    print(label_map)
    context = {'result': result,
               'keys': list(label_map.keys()),
               'values': list(label_map.values())
               }

    # label = getlabel(doc)
    # score = getscore(doc)
    # print(label, score)

    return render(request, 'blogcontent.html', context=context)


# schemes page

def schemes(request, methods=['GET', 'POST']):

    # print(heading_list)
    heading_list_new = []
    for key, val in schemes_content.items():
        heading_list_new.append(val[0])

    final_content_new = list(schemes_content.values())
    print(image_urls)
    mylist = zip(heading_list_new, final_content_new, image_urls)
    context = {
        'mylist': mylist,
    }
    return render(request, 'blog.html', context=context)


# schemes content

def schemescontent(request, methods=['GET', 'POST']):

    HTML_WRAPPER = """<div style="overflow-x: auto; border: 1px solid #e6e9ef; border-radius: 0.25rem; padding: 1rem">{}</div>"""

    results = str(request.get_full_path).split(
        '?')[1].split('=')[1].split("'")[0]

    finalcontent = schemes_content[int(results)]

    doc = nlp(finalcontent)
    label_map = showents(doc)
    html = displacy.render(doc, style="ent")
    html = html.replace("\n\n", "\n")
    result = HTML_WRAPPER.format(html)
    print(label_map)
    context = {'result': result,
               'keys': list(label_map.keys()),
               'values': list(label_map.values())
               }

    # label = getlabel(doc)
    # score = getscore(doc)
    # print(label, score)

    return render(request, 'blogcontent.html', context=context)
