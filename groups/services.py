from django.shortcuts import get_object_or_404
from .models import Group
from .forms import GroupForm


def list_groups():
    return Group.objects.all()


def get_group(group_id):
    return get_object_or_404(Group, id=group_id)


def create_group(form_data):
    form = GroupForm(form_data)
    if form.is_valid():
        return form.save(), None
    return None, form


def update_group(group_id, form_data):
    group = get_group(group_id)
    form = GroupForm(form_data, instance=group)
    if form.is_valid():
        return form.save(), None
    return None, form


def delete_group(group_id):
    group = get_object_or_404(Group, id=group_id)
    group.delete()
