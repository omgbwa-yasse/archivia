from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from decimal import Decimal

class Project(models.Model):
    STATUS_CHOICES = [
        ('PLANNING', 'En planification'),
        ('ACTIVE', 'En cours'),
        ('ON_HOLD', 'En attente'),
        ('COMPLETED', 'Terminé'),
        ('CANCELLED', 'Annulé'),
    ]

    name = models.CharField(max_length=100, verbose_name="Nom")
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='owned_projects', verbose_name="Propriétaire")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PLANNING', verbose_name="Statut")
    start_date = models.DateTimeField(verbose_name="Date de début")
    end_date = models.DateTimeField(null=True, blank=True, verbose_name="Date de fin")
    version = models.IntegerField(default=1, verbose_name="Version")
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='created_projects', verbose_name="Créé par")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Créé le")
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='updated_projects', verbose_name="Mis à jour par")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Mis à jour le")
    deleted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='deleted_projects', verbose_name="Supprimé par")
    deleted_at = models.DateTimeField(null=True, blank=True, verbose_name="Supprimé le")

    class Meta:
        verbose_name = "Projet"
        verbose_name_plural = "Projets"
        ordering = ['-created_at']

    def __str__(self):
        return self.name

class ProjectMember(models.Model):
    ROLE_CHOICES = [
        ('MANAGER', 'Chef de projet'),
        ('MEMBER', 'Membre'),
        ('VIEWER', 'Observateur'),
    ]

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='members', verbose_name="Projet")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='project_memberships', verbose_name="Utilisateur")
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, verbose_name="Rôle")
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='created_project_memberships', verbose_name="Créé par")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Créé le")
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='updated_project_memberships', verbose_name="Mis à jour par")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Mis à jour le")

    class Meta:
        verbose_name = "Membre du projet"
        verbose_name_plural = "Membres du projet"
        unique_together = ['project', 'user']

    def __str__(self):
        return f"{self.user} - {self.project} ({self.get_role_display()})"

class ProjectTask(models.Model):
    STATUS_CHOICES = [
        ('TO_DO', 'À faire'),
        ('IN_PROGRESS', 'En cours'),
        ('BLOCKED', 'Bloqué'),
        ('REVIEW', 'En revue'),
        ('DONE', 'Terminé'),
    ]

    PRIORITY_CHOICES = [
        ('LOW', 'Basse'),
        ('MEDIUM', 'Moyenne'),
        ('HIGH', 'Haute'),
        ('URGENT', 'Urgente'),
    ]

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks', verbose_name="Projet")
    parent_task = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='subtasks', verbose_name="Tâche parente")
    title = models.CharField(max_length=190, verbose_name="Titre")
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='TO_DO', verbose_name="Statut")
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='MEDIUM', verbose_name="Priorité")
    estimated_hours = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, validators=[MinValueValidator(Decimal('0.01'))], verbose_name="Heures estimées")
    start_date = models.DateTimeField(null=True, blank=True, verbose_name="Date de début")
    due_date = models.DateTimeField(null=True, blank=True, verbose_name="Date d'échéance")
    completed_at = models.DateTimeField(null=True, blank=True, verbose_name="Date de complétion")
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_tasks', verbose_name="Assigné à")
    version = models.IntegerField(default=1, verbose_name="Version")
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='created_tasks', verbose_name="Créé par")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Créé le")
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='updated_tasks', verbose_name="Mis à jour par")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Mis à jour le")
    deleted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='deleted_tasks', verbose_name="Supprimé par")
    deleted_at = models.DateTimeField(null=True, blank=True, verbose_name="Supprimé le")

    class Meta:
        verbose_name = "Tâche"
        verbose_name_plural = "Tâches"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.project}"

class ProjectResource(models.Model):
    RESOURCE_TYPES = [
        ('HUMAN', 'Humain'),
        ('MATERIAL', 'Matériel'),
        ('FINANCIAL', 'Financier'),
    ]

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='resources', verbose_name="Projet")
    resource_type = models.CharField(max_length=20, choices=RESOURCE_TYPES, verbose_name="Type de ressource")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='project_resources', verbose_name="Utilisateur")
    name = models.CharField(max_length=190, verbose_name="Nom")
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    quantity = models.IntegerField(null=True, blank=True, verbose_name="Quantité")
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, validators=[MinValueValidator(Decimal('0.01'))], verbose_name="Coût unitaire")
    start_date = models.DateTimeField(null=True, blank=True, verbose_name="Date de début")
    end_date = models.DateTimeField(null=True, blank=True, verbose_name="Date de fin")
    version = models.IntegerField(default=1, verbose_name="Version")
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='created_resources', verbose_name="Créé par")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Créé le")
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='updated_resources', verbose_name="Mis à jour par")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Mis à jour le")
    deleted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='deleted_resources', verbose_name="Supprimé par")
    deleted_at = models.DateTimeField(null=True, blank=True, verbose_name="Supprimé le")

    class Meta:
        verbose_name = "Ressource"
        verbose_name_plural = "Ressources"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.project}"

class TaskDependency(models.Model):
    DEPENDENCY_TYPES = [
        ('FINISH_TO_START', 'Fin à début'),
        ('START_TO_START', 'Début à début'),
        ('FINISH_TO_FINISH', 'Fin à fin'),
        ('START_TO_FINISH', 'Début à fin'),
    ]

    task = models.ForeignKey(ProjectTask, on_delete=models.CASCADE, related_name='dependencies', verbose_name="Tâche")
    depends_on_task = models.ForeignKey(ProjectTask, on_delete=models.CASCADE, related_name='dependent_tasks', verbose_name="Dépend de la tâche")
    dependency_type = models.CharField(max_length=20, choices=DEPENDENCY_TYPES, verbose_name="Type de dépendance")
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='created_dependencies', verbose_name="Créé par")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Créé le")

    class Meta:
        verbose_name = "Dépendance de tâche"
        verbose_name_plural = "Dépendances de tâches"
        unique_together = ['task', 'depends_on_task']

    def __str__(self):
        return f"{self.task} dépend de {self.depends_on_task} ({self.get_dependency_type_display()})"

class TaskComment(models.Model):
    task = models.ForeignKey(ProjectTask, on_delete=models.CASCADE, related_name='comments', verbose_name="Tâche")
    comment = models.TextField(verbose_name="Commentaire")
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='created_comments', verbose_name="Créé par")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Créé le")
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='updated_comments', verbose_name="Mis à jour par")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Mis à jour le")
    deleted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='deleted_comments', verbose_name="Supprimé par")
    deleted_at = models.DateTimeField(null=True, blank=True, verbose_name="Supprimé le")

    class Meta:
        verbose_name = "Commentaire"
        verbose_name_plural = "Commentaires"
        ordering = ['-created_at']

    def __str__(self):
        return f"Commentaire sur {self.task} par {self.created_by}"

class TimeEntry(models.Model):
    task = models.ForeignKey(ProjectTask, on_delete=models.CASCADE, related_name='time_entries', verbose_name="Tâche")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='time_entries', verbose_name="Utilisateur")
    hours_spent = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))], verbose_name="Heures passées")
    work_date = models.DateField(verbose_name="Date de travail")
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='created_time_entries', verbose_name="Créé par")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Créé le")
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='updated_time_entries', verbose_name="Mis à jour par")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Mis à jour le")

    class Meta:
        verbose_name = "Entrée de temps"
        verbose_name_plural = "Entrées de temps"
        ordering = ['-work_date']

    def __str__(self):
        return f"{self.user} - {self.task} - {self.hours_spent}h - {self.work_date}" 