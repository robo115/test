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
