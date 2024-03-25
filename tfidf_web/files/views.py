import os

from django.conf import settings
from django.shortcuts import render

from .forms import UploadFileForm
from .vectorization import tf_idf_calculation, preprocessing, present_results


def upload_file(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save()
            
            with open(os.path.join(settings.BASE_DIR, f"media/{obj.file}"), encoding="utf-8") as f:
                res = " ".join([line.strip() for line in f])

            preprocessed_lst = preprocessing(res)
            a, b, c = tf_idf_calculation(preprocessed_lst)
            res = present_results(a, b, c)

            form = UploadFileForm()

            return render(request, "upload_file.html", {"form": form, "res": res})
    else:
        form = UploadFileForm()
    return render(request, "upload_file.html", {"form": form})
