from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from users.decorators import permission_required
from .services import list_groups, get_group, create_group, update_group, delete_group
from .forms import GroupForm


@method_decorator(permission_required('view_groups'), name='dispatch')
class GroupListView(LoginRequiredMixin, View):
    def get(self, request):
        groups = list_groups()
        return render(request, 'groups/group_list.html', {'groups': groups})


@method_decorator(permission_required('view_groups'), name='dispatch')
class GroupDetailView(LoginRequiredMixin, View):
    def get(self, request, group_id):
        group = get_group(group_id)
        return render(request, 'groups/group_detail.html', {'group': group})


@method_decorator(permission_required('edit_groups'), name='dispatch')
class GroupCreateView(LoginRequiredMixin, View):
    def get(self, request):
        form = GroupForm()
        return render(request, 'groups/group_form.html', {'form': form})

    def post(self, request):
        group, form = create_group(request.POST)
        if group:
            return redirect('group_list')
        return render(request, 'groups/group_form.html', {'form': form})


@method_decorator(permission_required('edit_groups'), name='dispatch')
class GroupEditView(LoginRequiredMixin, View):
    def get(self, request, group_id):
        group = get_group(group_id)
        form = GroupForm(instance=group)
        return render(request, 'groups/group_form.html', {'form': form})

    def post(self, request, group_id):
        group, form = update_group(group_id, request.POST)
        if group:
            return redirect('group_detail', group_id=group.id)
        return render(request, 'groups/group_form.html', {'form': form})


@method_decorator(permission_required('delete_groups'), name='dispatch')
class GroupDeleteView(LoginRequiredMixin, View):
    def post(self, request, group_id):
        delete_group(group_id)
        return redirect('group_list')
