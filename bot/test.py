import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response

@csrf_exempt
@api_view(['POST'])
def api_ai(request):
    try:
        # ប្រើ .get() ដើម្បីកុំឱ្យ Crash បើ query មិនមាន
        user_query = request.data.get('query')
        
        if not user_query:
            return JsonResponse({"error": "សូមបញ្ចូលសំណួរ"}, status=400)

        api_key = "AIzaSyAtGp0xlrKrfo2HrXgTlm9D4OCabZYwKtI" # ប្រយ័ត្ន Key នេះអាចនឹងងាប់បើអ្នកបង្ហោះជាសាធារណៈ
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"

        payload = {
            "contents": [{"parts": [{"text": user_query}]}]
        }

        response = requests.post(url, json=payload, timeout=30)
        data = response.json()

        if response.status_code != 200:
            return JsonResponse({"error": "Google API Error", "details": data}, status=response.status_code)

        ai_text = data['candidates'][0]['content']['parts'][0]['text']
        return JsonResponse({"answer": ai_text})

    except Exception as e:
        # បោះ Error ចេញមកក្រៅដើម្បីឱ្យយើងដឹងថាវាខុសអ្វី
        print(f"Error detail: {str(e)}") 
        return JsonResponse({"error": str(e)}, status=500)