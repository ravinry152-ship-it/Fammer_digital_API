""""
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

BOT_TOKEN = "8455978510:AAFSHfpz_gEWuWfbVbc8KXpz7xJGubbScHk"
CHAT_IDS = [" 7831405898", " 7831405898"]

@csrf_exempt  # អនុញ្ញាតឱ្យ Post ទិន្នន័យពីខាងក្រៅបាន
def send_order(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            
            # រៀបចំសារ
            message = f"🛒 New Order (Django)!\n\n"
            message += f"Customer: {data['customer_name']}\n"
            message += f"Phone: {data['customer_phone']}\n"
            message += f"Address: {data['customer_address']}\n\nItems:\n"
            
            for item in data["items"]:
                message += f"- {item['name']} x {item['quantity']} (${item['price']})\n"

            message += f"\nTotal: ${data['total']:.2f}"

            # ផ្ញើទៅ Telegram
            for chat_id in CHAT_IDS:
                url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
                requests.post(url, data={"chat_id": chat_id, "text": message})

            return JsonResponse({"status": "success"}, status=200)
        
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)
    
    return JsonResponse({"status": "only POST allowed"}, status=405)
"""