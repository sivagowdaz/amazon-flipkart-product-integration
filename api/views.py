import json
from bot.run import call_thread
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def product_fun(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        if body:
            search_string = body["search_string"]
            amazon_products, flipkart_products = call_thread(search_string)
            return JsonResponse({'flipkart_products': flipkart_products, 'amazon_products':amazon_products})
        else:
            return JsonResponse({"response":"please provide the search_string in the body"})    
    else:
        return JsonResponse({"response":"only POST requests are allowed"})    
