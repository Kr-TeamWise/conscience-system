from django.db import models


class BaseModel(models.Model):
    """Common Model Definition"""

    created_at = models.DateTimeField(auto_now_add=True, help_text="생성일")
    updated_at = models.DateTimeField(auto_now=True, help_text="수정일")

    class Meta:
        abstract = True
