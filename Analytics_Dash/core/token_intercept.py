def TokenMiddleware(get_response):
    def middleware(request):
        if  request.__dict__['path_info'] == '/accounts/google/login/' and request.method == 'POST':
            print(request.user)
        return get_response(request)
    return middleware