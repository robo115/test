from django.shortcuts import render
from .models import *
import datetime


def sorting(request, product_name):
    product = Product.objects.get(name=product_name)
    users = User.objects.filter(product__name=product_name)
    groups = Group.objects.filter(product__name=product_name)
    group_index = 0
    now = datetime.datetime.now(tz=datetime.timezone.utc)
    if now >= product.start_date:
        return False
    else:
        for user in users:
            group = groups[group_index]
            user.group.add(group)
            if User.objects.filter(group=group).count() < product.max_in_group:
                if group_index == groups.count() - 1:
                    group_index = 0
                else:
                    group_index += 1
            elif (group_index < len(groups) - 1) and User.objects.filter(
                group=groups[group_index + 1]
            ).count() < product.max_in_group:
                group_index += 1
            else:
                break


def product_list(request):
    products = Product.objects.all()
    available_products = []
    for product in products:
        all_users = User.objects.all().count()
        groups = Group.objects.filter(product=product).count()
        users = User.objects.filter(product=product).count()
        lessons = Lesson.objects.filter(product=product).count()
        fullness = users / (product.max_in_group * groups) * 100
        popularity = (all_users / users) * 100
        if users / groups < product.max_in_group:
            product_api = {
                "name": product.name,
                "author": product.autor,
                "start_date": product.start_date,
                "price": product.price,
                "lessons": lessons,
                "users_in_product": users,
                "fullness": fullness,
                "popularity": popularity
            }
            available_products.append(product_api)
        else:
            continue
    context = {
        "available_products": available_products
    }
    return context  # need return template with context but i dont have template
