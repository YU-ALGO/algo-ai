1. Model_Train
1.1. 해당 폴더는 추천시스템 모델 학습하는 용도로 사용된 폴더이다.
1.2. ALGo_Recommendation_Model_Train.ipynb
1.2.1. 해당 ipynb는 추천시스템 모델 학습하는 파일이다.
1.3. User_Item_Rating.csv
1.3.1. 해당 csv는 추천시스템 모델을 학습할때 사용되는 학습데이터이다.

2. ALGo_Recommendation
2.1. 해당 폴더는 추천시스템을 실행시키는 용도로 사용된 폴더이다.
2.2. cmd를 킨 후 해당 폴더로 이동한다. 
2.2.1. ex) cd C:\Users\wodon\OneDrive\Desktop\ALGo_AI\ALGo_Recommendation
2.3. 폴더안에 start.bat를 실행하여 추천시스템 서버를 킨다.
2.4. 서버를 킨 ip로 allergy, favorites, recently_viewed를 파라미터로 넣은 후 get요청을 보내어 추천을 받는다.
2.4.1. ex) http://127.0.0.1:8000/recommend?allergy=11010100000100001000&favorites=[1,2,3,4,5,6]&recently_viewed=[11,22,33,44,55,66]
