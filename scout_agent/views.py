import logging
import os
import base64
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser
from django.shortcuts import get_object_or_404
from openai import OpenAI
from .models import CompanyProfile, PDFAnalysis
from .services.agent_service import LeadScoutAgent
from .services.pdf_service import PDFAnalysisService

# 로깅 설정
logger = logging.getLogger('scout_agent')

# OpenAI 클라이언트 생성
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 리드 스카우트
class LeadScoutView(APIView):
    def post(self, request):
        logger.info("find_potential_leads 호출됨")
        company_id = request.data.get('company_id')

        if not company_id:
            return Response({"error": "company_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        agent = LeadScoutAgent()
        result = agent.find_potential_leads(company_id)

        if result["status"] == "error":
            return Response({"error": result["message"]}, status=status.HTTP_400_BAD_REQUEST)

        return Response(result, status=status.HTTP_200_OK)

# PDF 분석
class PDFAnalysisView(APIView):
    def post(self, request, profile_id=None):
        if profile_id is None:
            profile_id = request.data.get('profile_id')
            if not profile_id:
                return Response({"error": "profile_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        profile = get_object_or_404(CompanyProfile, id=profile_id)
        pdf_service = PDFAnalysisService()
        analysis = pdf_service.analyze_company_pdf(profile)

        if not analysis:
            return Response({"error": "Failed to analyze PDF"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({
            "status": "success",
            "message": "PDF analysis completed successfully",
            "analysis": analysis
        })

    def get(self, request, profile_id):
        analysis = get_object_or_404(PDFAnalysis, profile_id=profile_id)

        return Response({
            "status": "success",
            "analysis": {
                "industry": analysis.industry,
                "sales": analysis.sales,
                "total_funding": analysis.total_funding,
                "homepage": analysis.homepage,
                "key_executive": analysis.key_executive,
                "address": analysis.address,
                "email": analysis.email,
                "phone_number": analysis.phone_number,
                "company_description": analysis.company_description,
                "products_services": analysis.products_services,
                "target_customers": analysis.target_customers,
                "competitors": analysis.competitors,
                "strengths": analysis.strengths,
                "business_model": analysis.business_model,
                "created_at": analysis.created_at,
                "updated_at": analysis.updated_at,
            },
        })

# 음식 이미지 업로드 분석 (OpenAI 최신 방식)
@api_view(["POST"])
@parser_classes([MultiPartParser])
def analyze_food_image(request):
    file_obj = request.FILES.get('file')
    if not file_obj:
        return Response({"error": "No file uploaded"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # base64로 인코딩하여 data URL 생성
        base64_image = base64.b64encode(file_obj.read()).decode('utf-8')
        data_url = f"data:{file_obj.content_type};base64,{base64_image}"

        # OpenAI Vision API 호출
        response = openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": [
                         {
                            "type": "text",
                            "text": (
                                  "다음 음식 사진을 분석하여 탄수화물, 단백질, 지방, 총 칼로리를 추정해줘.\n"
                                "※ 규칙:\n"
                                "- 확신 있는 어조로 작성\n"
                                "- 결과는 숫자만 포함하고, 주의사항 없이 작성\n"
                                "- 대략적이라는 표현 없이 자연스럽게\n"
                                "- 결과 포맷:\n"
                                "탄수화물: xxg\n단백질: xxg\n지방: xxg\n총 칼로리: xxxkcal"
                            )
                        },
                        {"type": "image_url", "image_url": {"url": data_url}},
                    ],
                }
            ],
            max_tokens=400,
            temperature=0.3,
        )
        result_text = response.choices[0].message.content.strip()

        # ✅ 추가 멘트 예쁘게 붙이기
        final_response = (
            "해당 음식의 예상 영양 정보입니다"
            f"{result_text}"
            "일반 성인의 하루 권장 칼로리는 약 2000kcal입니다."
            "참고하여 균형 잡힌 식사를 계획해보세요!"
        )

        logger.info(f"AI 분석 성공: {final_response}")
        return Response({"result": final_response})

    except Exception as e:
        logger.error(f"Error analyzing food image: {str(e)}")
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
