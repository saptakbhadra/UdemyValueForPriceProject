from flask import Flask,render_template,request
import jsonify
import requests
import pickle
import numpy as np

appu=Flask(__name__)
model=pickle.load(open('udemypickle.pkl','rb'))

@appu.route('/',methods=['GET'])
def home():
    return render_template('index.html')

@appu.route("/predict",methods=['POST'])
def predict():
    if request.method == 'POST':
        title=request.form['title']
        print('title',title)
        CatchyWords=0
        CatchyWordsPresence=0
        for j in title.split():
            print(j)
            if (j == 'Easy' or j == 'easy' or j == 'To' or j == 'to' or j == 'Within' or j == 'within' or j == 'Basics' or j == 'basics' or j == 'Crash' or j == 'crash' or j == 'Become' or j == 'become'):
                CatchyWords = CatchyWords+1
        if CatchyWords > 0:
            CatchyWordsPresence=1
        else:
            CatchyWordsPresence=0
        print('CatchyWordsPresence',CatchyWordsPresence)
        numSubscribers = float(request.form['numSubscribers'])
        print('Number of Subscribers',numSubscribers)
        numReviews = float(request.form['numReviews'])
        print('number of Reviews',numReviews)
        numPublishedLectures=float(request.form['numPublishedLectures'])
        print('number of Lectures',numPublishedLectures)
        instructionalLevel=request.form['instructionalLevel']
        if instructionalLevel== 'All Levels':
            instructionalLevelCat=0
        elif (instructionalLevel == 'Beginner Level'):
            instructionalLevelCat = 1
        elif (instructionalLevel == 'Intermediate Level'):
            instructionalLevelCat = 2
        elif (instructionalLevel == 'Expert Level'):
            instructionalLevelCat = 3

        print('Difficulty Level',instructionalLevelCat)

        Durationtime=float(request.form['Duration'])
        Duration_in_hours=request.form['Duration_in_hours']
        if(Duration_in_hours=='minutes'):
            Durationtime=Durationtime/60
        print('Duration of course',Durationtime)

        websitePrice= float(request.form['websitePrice'])
        print('Website Price',websitePrice)

        array=np.array((numSubscribers,numReviews,numPublishedLectures,instructionalLevelCat,Durationtime,CatchyWordsPresence))
        array=array.reshape(1,-1)
        prediction=model.predict(array)
        output=prediction[0]
        print('prediction price',output)
        if(output<=websitePrice):
            return render_template('index.html', prediction="our Estimated Price:{},Course worth buying".format(output))
        elif (output>websitePrice):
            return render_template('index.html',prediction="Worth Buying")
        else:
            return render_template('index.html',prediction="Not Worth Buying")
    else:
        return render_template('index.html')



if __name__=="__main__":
    appu.run(debug=True)