from django.db import models


class UploadedFile(models.Model):
    file = models.FileField(upload_to="uploads/", verbose_name="Файл")
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата загрузки")

    def __str__(self):
        return f"{self.file}"    
