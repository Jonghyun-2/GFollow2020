def handle_uploaded_file(f):
    with open('test/test.txt', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)