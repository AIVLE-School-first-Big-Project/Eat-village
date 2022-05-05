import re
from numpy import rec
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
# from recipe.models import user_ingre
from users.models import *
# import recipe.models as models
# from .models import recipe_data, user_ingre

def recommend_recipe(user_model, recipe_model):
    # 매개변수를 통한 데이터 모델.
    # user_data = user_model.objects.all()
    re_data = recipe_model.objects.all()
    
    # 당근,사과,오이,양파
    # 1. 유저 id와 재료를 받는다.
    # user_ids = list(user.id for user in user_data)
    # user_ingres = list(user.ingre for user in user_data)
    
    user_ingres = user_model
    
    # 2. 레시피 id 값과 재료를 받는다.
    recipe_ids = list(recipe.recipe_id - 1 for recipe in re_data) # id -1 이 index
    recipe_names = list(recipe.title for recipe in re_data)
    recipe_igds = list(recipe.ingre for recipe in re_data)
    
    # 3. 유저 재료와 레시피 재료를 코사인 유사도 검사 후 정렬 테이블 생성
    # 유저의 재료 데이터를 레시피 리스트 마지막에 추가
    result = ','.join(s for s in user_ingres)
    
    recipe_igds.insert(len(recipe_igds),result)
    
    tfidf_vect_simple = TfidfVectorizer()
    feature_vect_simple = tfidf_vect_simple.fit_transform(recipe_igds)
    
    similarity_simple_pair = cosine_similarity(feature_vect_simple[len(recipe_igds)-1] , feature_vect_simple)
    # 딕셔너리로 만들어서 관리 / 매트릭스 만들어서 유사도 비교
    title_to_index = dict(zip(recipe_ids,recipe_names))
    
    
    idx = len(recipe_igds)-1# 유저의 재료를 가리키는 인덱스 
    cosine_sim = cosine_similarity(feature_vect_simple, feature_vect_simple)
    # 유저 재료와 모든 레시피의 재료와의 유사도를 가져온다.
    sim_scores = list(enumerate(cosine_sim[idx]))
    # 유사도에 따라 레시피들을 정렬한다.
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    # 가장 유사한 3개의 영화를 받아온다.
    sim_scores = sim_scores[1:5]
    
    # 가장 유사한 3개의 레시피의 인덱스를 얻는다.
    recipe_idx = [idx[0] for idx in sim_scores]
    # 가장 유사한 10개의 영화의 제목을 리턴한다.
    # title_to_index[recipe_idx]
    recommend_recipe_name = []
    
    for i in recipe_idx: # [1,0,2]
        recommend_recipe_name.append(title_to_index[i])

    # recommend_recipe_name.append(title_to_index[1])
    # return(feature_vect_simple.shape,similarity_simple_pair) : 코사인유사도 매트릭스 shape와 각 매트릭스 별 유사도

    return (recommend_recipe_name)
    
    
    
    # return render(request, 'recipe/show.html',{'data' : re_data, 'user' : user_data})
    # docs="hello"
    # vect = CountVectorizer() # Counter Vectorizer 객체 생성
    # 4. 테이블의 id값을 바탕으로 그 DB의 내용을 찾아낸다.
    
    # return HttpResponse(docs)