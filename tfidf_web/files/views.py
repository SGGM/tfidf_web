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

            preprocessed_lst = preprocessing(res)                              # предобработка текстового файла
            words, array_tf, array_idf = tf_idf_calculation(preprocessed_lst)  # рассчет tf, idf, а также словаря слов в тексте
            res = present_results(words, array_tf, array_idf)                  # вывод результатов в виде списка кортежей

            form = UploadFileForm()

            return render(request, "upload_file.html", {"form": form, "res": res})
    else:
        form = UploadFileForm()
    return render(request, "upload_file.html", {"form": form})
