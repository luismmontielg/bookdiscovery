from django.contrib import admin
from .models import Recommendation, Book, Author, UserProfile, Category, BookRelation


class RecommendationAdmin(admin.ModelAdmin):
    model = Recommendation


class BookAdmin(admin.ModelAdmin):
    model = Book
    prepopulated_fields = {"slug": ("title",)}


class AuthorAdmin(admin.ModelAdmin):
    model = Author


class UserProfileAdmin(admin.ModelAdmin):
    model = UserProfile


class CategoryAdmin(admin.ModelAdmin):
    model = Category


admin.site.register(Recommendation, RecommendationAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(BookRelation)

