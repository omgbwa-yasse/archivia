from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from .models import (
    Communicability, Activity, Sort, Retention,
    LawType, Law, LawArticle, Organisation, OrganisationActivity, RetentionLawArticle
)
from .forms import (
    CommunicabilityForm, ActivityForm, SortForm,
    RetentionForm, LawTypeForm, LawForm, LawArticleForm, OrganisationForm, OrganisationActivityForm, RetentionLawArticleForm
)

# Communicability Views
class CommunicabilityListView(ListView):
    model = Communicability
    template_name = 'tools/communicability_list.html'
    context_object_name = 'communicability_list'
    paginate_by = 10
    ordering = ['code']

class CommunicabilityDetailView(DetailView):
    model = Communicability
    template_name = 'tools/communicability_detail.html'
    context_object_name = 'communicability'

class CommunicabilityCreateView(LoginRequiredMixin, CreateView):
    model = Communicability
    form_class = CommunicabilityForm
    template_name = 'tools/communicability_form.html'
    success_url = reverse_lazy('tools:communicability_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.updated_by = self.request.user
        messages.success(self.request, 'La communicabilité a été créée avec succès.')
        return super().form_valid(form)

class CommunicabilityUpdateView(LoginRequiredMixin, UpdateView):
    model = Communicability
    form_class = CommunicabilityForm
    template_name = 'tools/communicability_form.html'
    success_url = reverse_lazy('tools:communicability_list')

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        messages.success(self.request, 'La communicabilité a été mise à jour avec succès.')
        return super().form_valid(form)

class CommunicabilityDeleteView(LoginRequiredMixin, DeleteView):
    model = Communicability
    template_name = 'tools/communicability_confirm_delete.html'
    success_url = reverse_lazy('tools:communicability_list')
    context_object_name = 'communicability'

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'La communicabilité a été supprimée avec succès.')
        return super().delete(request, *args, **kwargs)

# Activity Views
class ActivityListView(LoginRequiredMixin, ListView):
    model = Activity
    template_name = 'tools/activity_list.html'
    context_object_name = 'activities'
    paginate_by = 10
    ordering = ['code']

class ActivityDetailView(LoginRequiredMixin, DetailView):
    model = Activity
    template_name = 'tools/activity_detail.html'
    context_object_name = 'activity'

class ActivityCreateView(LoginRequiredMixin, CreateView):
    model = Activity
    form_class = ActivityForm
    template_name = 'tools/activity_form.html'
    success_url = reverse_lazy('tools:activity_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, 'L\'activité a été créée avec succès.')
        return super().form_valid(form)

class ActivityUpdateView(LoginRequiredMixin, UpdateView):
    model = Activity
    form_class = ActivityForm
    template_name = 'tools/activity_form.html'
    success_url = reverse_lazy('tools:activity_list')

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        messages.success(self.request, 'L\'activité a été mise à jour avec succès.')
        return super().form_valid(form)

class ActivityDeleteView(LoginRequiredMixin, DeleteView):
    model = Activity
    template_name = 'tools/activity_confirm_delete.html'
    success_url = reverse_lazy('tools:activity_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'L\'activité a été supprimée avec succès.')
        return super().delete(request, *args, **kwargs)

# Sort Views
class SortListView(LoginRequiredMixin, ListView):
    model = Sort
    template_name = 'tools/sort_list.html'
    context_object_name = 'sorts'
    paginate_by = 10
    ordering = ['code']

class SortDetailView(LoginRequiredMixin, DetailView):
    model = Sort
    template_name = 'tools/sort_detail.html'
    context_object_name = 'sort'

class SortCreateView(LoginRequiredMixin, CreateView):
    model = Sort
    form_class = SortForm
    template_name = 'tools/sort_form.html'
    success_url = reverse_lazy('tools:sort_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, 'Le sort a été créé avec succès.')
        return super().form_valid(form)

class SortUpdateView(LoginRequiredMixin, UpdateView):
    model = Sort
    form_class = SortForm
    template_name = 'tools/sort_form.html'
    success_url = reverse_lazy('tools:sort_list')

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        messages.success(self.request, 'Le sort a été mis à jour avec succès.')
        return super().form_valid(form)

class SortDeleteView(LoginRequiredMixin, DeleteView):
    model = Sort
    template_name = 'tools/sort_confirm_delete.html'
    success_url = reverse_lazy('tools:sort_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Le sort a été supprimé avec succès.')
        return super().delete(request, *args, **kwargs)

# Retention Views
class RetentionListView(LoginRequiredMixin, ListView):
    model = Retention
    template_name = 'tools/retention_list.html'
    context_object_name = 'retentions'
    paginate_by = 10
    ordering = ['code']

class RetentionDetailView(LoginRequiredMixin, DetailView):
    model = Retention
    template_name = 'tools/retention_detail.html'
    context_object_name = 'retention'

class RetentionCreateView(LoginRequiredMixin, CreateView):
    model = Retention
    form_class = RetentionForm
    template_name = 'tools/retention_form.html'
    success_url = reverse_lazy('tools:retention_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, 'La rétention a été créée avec succès.')
        return super().form_valid(form)

class RetentionUpdateView(LoginRequiredMixin, UpdateView):
    model = Retention
    form_class = RetentionForm
    template_name = 'tools/retention_form.html'
    success_url = reverse_lazy('tools:retention_list')

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        messages.success(self.request, 'La rétention a été mise à jour avec succès.')
        return super().form_valid(form)

class RetentionDeleteView(LoginRequiredMixin, DeleteView):
    model = Retention
    template_name = 'tools/retention_confirm_delete.html'
    success_url = reverse_lazy('tools:retention_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'La rétention a été supprimée avec succès.')
        return super().delete(request, *args, **kwargs)

# Law Type Views
class LawTypeListView(LoginRequiredMixin, ListView):
    model = LawType
    template_name = 'tools/law_type_list.html'
    context_object_name = 'law_types'
    paginate_by = 10
    ordering = ['name']

class LawTypeDetailView(LoginRequiredMixin, DetailView):
    model = LawType
    template_name = 'tools/law_type_detail.html'
    context_object_name = 'law_type'

class LawTypeCreateView(LoginRequiredMixin, CreateView):
    model = LawType
    form_class = LawTypeForm
    template_name = 'tools/law_type_form.html'
    success_url = reverse_lazy('tools:law_type_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, 'Le type de loi a été créé avec succès.')
        return super().form_valid(form)

class LawTypeUpdateView(LoginRequiredMixin, UpdateView):
    model = LawType
    form_class = LawTypeForm
    template_name = 'tools/law_type_form.html'
    success_url = reverse_lazy('tools:law_type_list')

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        messages.success(self.request, 'Le type de loi a été mis à jour avec succès.')
        return super().form_valid(form)

class LawTypeDeleteView(LoginRequiredMixin, DeleteView):
    model = LawType
    template_name = 'tools/law_type_confirm_delete.html'
    success_url = reverse_lazy('tools:law_type_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Le type de loi a été supprimé avec succès.')
        return super().delete(request, *args, **kwargs)

# Law Views
class LawListView(LoginRequiredMixin, ListView):
    model = Law
    template_name = 'tools/law_list.html'
    context_object_name = 'laws'
    paginate_by = 10
    ordering = ['code']

class LawDetailView(LoginRequiredMixin, DetailView):
    model = Law
    template_name = 'tools/law_detail.html'
    context_object_name = 'law'

class LawCreateView(LoginRequiredMixin, CreateView):
    model = Law
    form_class = LawForm
    template_name = 'tools/law_form.html'
    success_url = reverse_lazy('tools:law_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, 'La loi a été créée avec succès.')
        return super().form_valid(form)

class LawUpdateView(LoginRequiredMixin, UpdateView):
    model = Law
    form_class = LawForm
    template_name = 'tools/law_form.html'
    success_url = reverse_lazy('tools:law_list')

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        messages.success(self.request, 'La loi a été mise à jour avec succès.')
        return super().form_valid(form)

class LawDeleteView(LoginRequiredMixin, DeleteView):
    model = Law
    template_name = 'tools/law_confirm_delete.html'
    success_url = reverse_lazy('tools:law_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'La loi a été supprimée avec succès.')
        return super().delete(request, *args, **kwargs)

# Law Article Views
class LawArticleListView(LoginRequiredMixin, ListView):
    model = LawArticle
    template_name = 'tools/law_article_list.html'
    context_object_name = 'law_articles'
    paginate_by = 10
    ordering = ['code']

class LawArticleDetailView(LoginRequiredMixin, DetailView):
    model = LawArticle
    template_name = 'tools/law_article_detail.html'
    context_object_name = 'law_article'

class LawArticleCreateView(LoginRequiredMixin, CreateView):
    model = LawArticle
    form_class = LawArticleForm
    template_name = 'tools/law_article_form.html'
    success_url = reverse_lazy('tools:law_article_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, 'L\'article de loi a été créé avec succès.')
        return super().form_valid(form)

class LawArticleUpdateView(LoginRequiredMixin, UpdateView):
    model = LawArticle
    form_class = LawArticleForm
    template_name = 'tools/law_article_form.html'
    success_url = reverse_lazy('tools:law_article_list')

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        messages.success(self.request, 'L\'article de loi a été mis à jour avec succès.')
        return super().form_valid(form)

class LawArticleDeleteView(LoginRequiredMixin, DeleteView):
    model = LawArticle
    template_name = 'tools/law_article_confirm_delete.html'
    success_url = reverse_lazy('tools:law_article_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'L\'article de loi a été supprimé avec succès.')
        return super().delete(request, *args, **kwargs)

# Organisation Views
class OrganisationListView(ListView):
    model = Organisation
    template_name = 'tools/organisation_list.html'
    context_object_name = 'organisations'
    paginate_by = 10
    ordering = ['code']

class OrganisationDetailView(DetailView):
    model = Organisation
    template_name = 'tools/organisation_detail.html'
    context_object_name = 'organisation'

class OrganisationCreateView(CreateView):
    model = Organisation
    form_class = OrganisationForm
    template_name = 'tools/organisation_form.html'
    success_url = reverse_lazy('tools:organisation_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, 'Organisation créée avec succès.')
        return super().form_valid(form)

class OrganisationUpdateView(UpdateView):
    model = Organisation
    form_class = OrganisationForm
    template_name = 'tools/organisation_form.html'
    success_url = reverse_lazy('tools:organisation_list')

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        messages.success(self.request, 'Organisation mise à jour avec succès.')
        return super().form_valid(form)

class OrganisationDeleteView(DeleteView):
    model = Organisation
    template_name = 'tools/organisation_confirm_delete.html'
    success_url = reverse_lazy('tools:organisation_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Organisation supprimée avec succès.')
        return super().delete(request, *args, **kwargs)

# Organisation Activity Views
class OrganisationActivityListView(LoginRequiredMixin, ListView):
    model = OrganisationActivity
    template_name = 'tools/organisation_activity_list.html'
    context_object_name = 'organisation_activities'
    paginate_by = 10
    ordering = ['organisation__code', 'activity__code']

class OrganisationActivityDetailView(LoginRequiredMixin, DetailView):
    model = OrganisationActivity
    template_name = 'tools/organisation_activity_detail.html'
    context_object_name = 'org_activity'

class OrganisationActivityCreateView(LoginRequiredMixin, CreateView):
    model = OrganisationActivity
    form_class = OrganisationActivityForm
    template_name = 'tools/organisation_activity_form.html'
    success_url = reverse_lazy('tools:organisation_activity_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, 'L\'association a été créée avec succès.')
        return super().form_valid(form)

class OrganisationActivityUpdateView(LoginRequiredMixin, UpdateView):
    model = OrganisationActivity
    form_class = OrganisationActivityForm
    template_name = 'tools/organisation_activity_form.html'
    success_url = reverse_lazy('tools:organisation_activity_list')

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        messages.success(self.request, 'L\'association a été mise à jour avec succès.')
        return super().form_valid(form)

class OrganisationActivityDeleteView(LoginRequiredMixin, DeleteView):
    model = OrganisationActivity
    template_name = 'tools/organisation_activity_confirm_delete.html'
    success_url = reverse_lazy('tools:organisation_activity_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'L\'association a été supprimée avec succès.')
        return super().delete(request, *args, **kwargs)

# Retention Law Article Views
class RetentionLawArticleListView(LoginRequiredMixin, ListView):
    model = RetentionLawArticle
    template_name = 'tools/retention_law_article_list.html'
    context_object_name = 'retention_law_articles'
    paginate_by = 10
    ordering = ['retention__code', 'law_article__code']

class RetentionLawArticleDetailView(LoginRequiredMixin, DetailView):
    model = RetentionLawArticle
    template_name = 'tools/retention_law_article_detail.html'
    context_object_name = 'retention_law_article'

class RetentionLawArticleCreateView(LoginRequiredMixin, CreateView):
    model = RetentionLawArticle
    form_class = RetentionLawArticleForm
    template_name = 'tools/retention_law_article_form.html'
    success_url = reverse_lazy('tools:retention_law_article_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, 'L\'association a été créée avec succès.')
        return super().form_valid(form)

class RetentionLawArticleUpdateView(LoginRequiredMixin, UpdateView):
    model = RetentionLawArticle
    form_class = RetentionLawArticleForm
    template_name = 'tools/retention_law_article_form.html'
    success_url = reverse_lazy('tools:retention_law_article_list')

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        messages.success(self.request, 'L\'association a été mise à jour avec succès.')
        return super().form_valid(form)

class RetentionLawArticleDeleteView(LoginRequiredMixin, DeleteView):
    model = RetentionLawArticle
    template_name = 'tools/retention_law_article_confirm_delete.html'
    success_url = reverse_lazy('tools:retention_law_article_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'L\'association a été supprimée avec succès.')
        return super().delete(request, *args, **kwargs) 