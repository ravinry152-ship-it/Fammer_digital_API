
import json
import traceback
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from asgiref.sync import async_to_sync
from .ai import ask

@csrf_exempt
def chat(request):
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

        # ✅ run async function ក្នុង sync view
        result = async_to_sync(ask)(question)
        return JsonResponse(result)

    except Exception as e:
        traceback.print_exc()  # បង្ហាញ error ពេញក្នុង Logs
        return JsonResponse({
            "success": False,
            "error": str(e)
        }, status=500)


@csrf_exempt
def health(request):
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