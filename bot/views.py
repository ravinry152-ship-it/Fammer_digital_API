
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .ai import ask 
@csrf_exempt
#ដោយសា វាជា​API ពីរក្រៅហេីយយេីង អត់ប្រេី serializer  ទេីបប្រេី 
# import json: ប្រើសម្រាប់បំប្លែងទិន្នន័យពី JSON string ទៅជា Python dictionary។  
# async def  បានន័យថា​funtionនេះអាចធ្វើការងារច្រើនក្នុងពេលតែមួយដោយមិនចាំបាច់រង់ចាំគ្នា
# Serializer បំប្លែង JSON String ទៅជា Python Dictionary ព្រោះpython(Django)វាអត់ស្គល់jsonទេ
async def chat(request):  
    if request.method != "POST":
        return JsonResponse({"success": False, "error": "POST only"}, status=405)
    try:
        body = json.loads(request.body)
        question = body.get("question", "").strip()

        if not question:
            return JsonResponse({
                "success": False,
                "error": "សំណួរទទេ!"
            }, status=400)

        result = await ask(question)  
        return JsonResponse(result)

    except Exception as e:
        return JsonResponse({
            "success": False,
            "error": str(e)
        }, status=500)


@csrf_exempt
async def health(request): 
    if request.method != "GET":
        return JsonResponse({"error": "GET only"}, status=405)
    return JsonResponse({
        "status": "ok",
        "message": "Sophy API រួចរាល់!"
    })
#====================================Local machain===============================
# import json
# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# from django.views.decorators.http import require_http_methods
# from .ai import ask

# @csrf_exempt
# @require_http_methods(["POST"])
# def chat(request):
#     try:
#         body = json.loads(request.body)
#         question = body.get("question", "").strip()

#         if not question:
#             return JsonResponse({
#                 "success": False,
#                 "error": "សំណួរទទេ!"
#             }, status=400)

#         result = ask(question)
#         return JsonResponse(result)

#     except Exception as e:
#         return JsonResponse({
#             "success": False,
#             "error": str(e)
#         }, status=500)


# @csrf_exempt
# @require_http_methods(["GET"])
# def health(request):
#     return JsonResponse({
#         "status": "ok",
#         "message": "Sophy API រួចរាល់!"
#     })