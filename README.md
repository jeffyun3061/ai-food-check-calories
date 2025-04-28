🥗 AI Food Calorie Check
음식 사진을 업로드하면
탄수화물, 단백질, 지방, 총 칼로리를 AI가 자동 분석해주는 서비스입니다.

🚀 기능
음식 사진 업로드 (jpg, png)

AI를 통한 탄단지 + 총 칼로리 분석

결과를 심플하고 직관적으로 제공

📦 주요 기술
Python 3.11

Django 4.2

OpenAI GPT-4o Vision

Rest Framework (DRF)

🛠️ 설치 방법
bash
복사
편집
git clone https://github.com/jeffyun3061/ai-food-check-calories.git
cd ai-food-check-calories
python -m venv venv
source venv/bin/activate (or .\venv\Scripts\activate)
pip install -r requirements.txt
python manage.py runserver
📄 환경변수 (.env 예시)
bash
복사
편집
SECRET_KEY=your-django-secret-key
OPENAI_API_KEY=your-openai-api-key
DB_USER=root
DB_PASSWORD=your-db-password
DB_HOST=127.0.0.1
DB_PORT=3306
DB_NAME=lead_scout_db
✨ 사용법
Postman이나 웹에서 /api/food/analyze/ 엔드포인트로 이미지 파일 업로드




추후 목표 : LLM 모델이나 LangChain을 연동하면,

음식 분석 결과에 따른 개인별 맞춤 식단 추천,

사진 속 음식 재료 추출 → 영양소 계산,

사용자 데이터(CSV) 기반으로 개인 맞춤형 리포트 생성,
같은 식으로 훨씬 똑똑하게 발전시킬 수 있다고 생각

결과로 탄수화물(g), 단백질(g), 지방(g), 총 칼로리(kcal)를 응답받습니다.

✅ 프로젝트 목표
"실제 사진을 기반으로 자연스럽고 정확한 칼로리 예측 서비스를 구축하는 것!"
