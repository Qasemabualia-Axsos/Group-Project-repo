from django.db import models

class CategoryManager(models.Manager):
    def category_validator(self, postData):
        errors = {}

        # Validate name
        if not postData.get('name', '').strip():
            errors['name_empty'] = 'Category name is required.'
        else:
            if len(postData['name'].strip()) < 3:
                errors['name_short'] = 'Category name must be at least 3 characters long.'
            elif Category.objects.filter(name__iexact=postData['name'].strip()).exists():
                errors['name_exists'] = 'Category name already exists.'

        # Validate description
        if not postData.get('description', '').strip():
            errors['description_empty'] = 'Description is required.'
        elif len(postData['description'].strip()) < 5:
            errors['description_short'] = 'Description must be at least 5 characters long.'

        return errors


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = CategoryManager()

    def __str__(self):
        return self.name
