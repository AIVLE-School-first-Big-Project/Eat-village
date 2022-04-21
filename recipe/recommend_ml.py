
from django.http import HttpResponse
from sklearn.feature_extraction.text import CountVectorizer

import recipe.models as models
from .models import recipe_data, user_ingre

def find_recipe(request ) :
    # 1. DB에 저장된 id 값과 재료를 받는다.
    docs="hello"
    vect = CountVectorizer() # Counter Vectorizer 객체 생성
    # 2. 유저 id와 재료를 받는다.
    # 3. 유저 재료와 DB 재료를 코사인 유사도로 검사하여 정렬한 테이블을 생성 ex) 5개 짜리
    # 4. 테이블의 id값을 바탕으로 그 DB의 내용을 찾아낸다.
    
    return HttpResponse(docs)