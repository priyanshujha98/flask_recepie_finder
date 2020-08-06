from  elasticsearch import Elasticsearch
import pandas as pd

def send_data(data,index_name):
    es = Elasticsearch(['localhost:9200'])
    res = es.index(index=index_name,doc_type='devops',body=data)

def get_ingredients():
        es = Elasticsearch(['localhost:9200'])
        result = pd.DataFrame()
          
        r = es.search(index = 'ingredients', size=1000)
        
        test = r['hits']['hits']
       
        for i in test:
            t = pd.DataFrame()
            t = pd.DataFrame([i['_source']]) 
            t['id'] = i['_id']
            try:
                if t.loc[0]['_id'] not in result['_id'].values:
                    result = result.append(t)
            except:
                result = result.append(t)
        
        result.reset_index(drop=True, inplace=True)
       
        return result

def get_recepies(var):
        es = Elasticsearch(['localhost:9200'])
        result = pd.DataFrame()
        
       
        
        r = es.search(index = 'recepie', size=1000)
          
        test = r['hits']['hits']
        
        delete = []
        for i in test:
            temp = ''
            for j in i['_source']['ingredients']:
                temp = temp + j
                temp = temp + ':'

            flag=True
            for k in var:
                if k not in temp:
                    flag = False
                    break
            if flag==False:
                delete.append(i)
        
        for i in delete :
            test.remove(i)
        
        
        
        
        for i in test:
            t = pd.DataFrame()
            t = pd.DataFrame([i['_source']]) 
            t['id'] = i['_id']
            try:
                if t.loc[0]['_id'] not in result['_id'].values:
                    result = result.append(t)
            except:
                result = result.append(t)
        
        result.reset_index(drop=True, inplace=True)
       
        return result



def get_recepie_from_index(index):
     es = Elasticsearch(['localhost:9200'])
     result = pd.DataFrame()
     
     for j in index:
         r = es.search(index = 'recepie', body={'query':{'match':{'_id':j}}})
         
         test = r['hits']['hits']
        
         for i in test:
            t = pd.DataFrame()
            t = pd.DataFrame([i['_source']]) 
            t['id'] = i['_id']
            try:
                if t.loc[0]['_id'] not in result['_id'].values:
                    result = result.append(t)
            except:
                result = result.append(t)
     result.reset_index(drop=True, inplace=True)
     return result
# =============================================================================
# 
# es = Elasticsearch(['localhost:9200'])
# result = pd.DataFrame()
# 
# r = es.search(index = 'recepie', body={'query':{
#     'bool':{
#         'must':[
#             {'match':{'idingredients':'onions'}},
#             {'match':{'idingredients':'garlic'}}
#                 ]
#         }
#     }
#     }, size=1000)
#   
# test = r['hits']['hits']
# =============================================================================
