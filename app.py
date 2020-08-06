from flask import Flask, render_template, request, jsonify, make_response, session, redirect, url_for
import pandas as pd
import json
import database as db
import datetime

app = Flask(__name__)

app.secret_key = 'super secret key'


@app.route('/',methods=['POST','GET'])
def home():
        return render_template('index.html')

@app.route('/recepie/',methods=['POST','GET'])
def recepie():
    print('cooke', request.cookies.get('visited'))
    
    
    
    expire_date = datetime.datetime.now()
    expire_date = expire_date + datetime.timedelta(days=90)
    index =request.args.get('index')
    print('index',index)
    
    d = db.get_recepie_from_index([index])
    resp = make_response(render_template('single.html',img_url = d['images'][0][0] ,name =list( d['name'])[0], 
                                         description = list(d['description'])[0], ingredients =list( d['ingredients'])[0],
                                         directions =list( d['instructions'][0][0]['steps']),
                                         to_time = list(d['total-time'])[0][2:],serving = list(d['yield'])[0],
                                         selected = session['selected']))
    try:
        resp.set_cookie('visited',request.cookies.get('visited')+',' +index ,expires=expire_date)
    except:
        resp.set_cookie('visited',index, expires=expire_date)
    return resp


@app.route('/visited/',methods=['POST','GET'])
def visited():
     
     return render_template('visited.html')


@app.route('/custom_recepie/',methods=['POST','GET'])
def custom_recepie():
        if request.method =='POST':
            try:
                var={}
                for i,j in zip(request.form.keys(),request.form.values()):
                    var[i]=j.lower()
                
                var['ing-list'] = var['ing-list'].split('\r\n')
                var['direction'] = var['direction'].split('\r\n')
                
                
                d = pd.DataFrame({'uuid':[None],'customer-uuid':[None],'name':[var['recipe-name']], 'original-name':[var['recipe-name']],
                                     'description':[var['short-desc']],'original-description':[var['short-desc']],
                                     'images':[[var['img-url']]],'new-images':[var['img-url']], 'new-original-images':[var['img-url']],
                                    'ingredients':[var['ing-list']],'original-ingredients':[var['ing-list']],
                                    'instructions':[[{'steps' : var['direction']}]],
                                    'yield':[var['servings']], 'original-yield':[var['servings']],
                                    'prep-time':[None], 'cook-time':[None], 'total-time':['PT'+ str(var['total_time'])],
                                    'original-total-time':['PT'+ str(var['total_time'])],'url':[None], 'created':[datetime.datetime.now()],
                                     'created-by':[None], 'updated':[None]})
                res = json.loads(d.to_json(orient='records'))[0]
                db.send_data(res, 'recepie')
                
                return redirect(url_for('home'))
            except Exception as e:
                 print('\n Error', e)
                 return render_template('add_recepie.html', message='* Please Enter The Correct Details')
        return render_template('add_recepie.html')

@app.route('/data/',methods = ['POST','GET'])
def data():
        if request.method =='POST':
            var={}
            for i,j in zip(request.form.keys(),request.form.values()):
                var[i]=j.lower()
            print(var)
            d  = db.get_ingredients()
            if var['searchText'] == '':
                d['img_url'] = None
                temp=list(d['idingredients']),list(d['img_url']), list(d['id'])
            else:
                g=[]
                url=[]
                Id=[]
                d['img_url'] = None
                for i,j,k in zip(d['idingredients'],d['img_url'], list(d['id'])):
                    if  var['searchText'] in i:
                        
                        g.append(i)
                        url.append(j)
                        Id.append(k)
                temp = g,url,Id

            
            return jsonify(temp)

@app.route('/maincontent/',methods = ['POST','GET'])
def main_content():
        if request.method =='POST':
            var={}
            for i,j in zip(request.form.keys(),request.form.values()):
                var[i]=j
            var['ingredients'] = var['ingredients'].replace('\n           \n          ','').split('✔')
            
            for i in range(var['ingredients'].count('')):
                var['ingredients'].remove('')
            print(var)
            
            session['selected'] = var['ingredients']
            
            if len(var['ingredients']) ==0 :
                print('In if')
                
                d  = db.get_ingredients()
                
                f = open('top.txt','r')
                f = f.read().split('\n')
                for i in range(len(f)):
                    f[i] = f[i].split('\t')
                    
                d = pd.DataFrame(f)
                
                d = d.rename(columns = {0:'idingredients',1:'img_url'})
                d['id'] = None
                for i in range(len(d['id'])):
                    d['id'][i] = "onclick='add_selected(this.textContent)'"
                    
                temp=list(d['idingredients']),list(d['img_url']), list(d['id'])
            else:
                print('In else')
                d = db.get_recepies(var['ingredients'])
                g=[]
                url=[]
                Id=[]
                
                try:
                    for i in range(len(d['id'])):
                        d['id'][i] = "href = /recepie/?index="+d['id'][i]
                    
                    
                    for i,j,k in zip(d['name'],d['images'], list(d['id'])):
                            g.append(i)
                            url.append(j[0])
                            Id.append(k)
                    temp = g,url,Id,len(g)
                except:
                    temp=None,None,None,0
            return jsonify(temp)


@app.route('/visited_data/',methods = ['POST','GET'])
def visited_data():
        if request.method =='POST':
            print('In post')
            var =  request.cookies.get('visited').split(',')
            
            temp = []
            for i in var:
                if i not in temp:
                    temp.append(i)
            var = temp
            
            print(var)
            
            g=[]
            url=[]
            Id=[]
            d = db.get_recepie_from_index(var)
            try:
                for i in range(len(d['id'])):
                    d['id'][i] = "href = /recepie/?index="+d['id'][i]
                
                
                for i,j,k in zip(d['name'],d['images'], list(d['id'])):
                        g.append(i)
                        url.append(j[0])
                        Id.append(k)
                temp = g,url,Id,len(g)
            except Exception as e:
                print(e)
                temp=None,None,None,0
            return jsonify(temp)

# 

if __name__=='__main__':
    app.run(debug=False)



