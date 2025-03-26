from django.db import models
from django.conf import settings
from tools.models import Activity, Organisation

class CorrespondencePriority(models.Model):
    name = models.CharField(max_length=50)
    duration = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class CorrespondenceTypology(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class CorrespondenceAction(models.Model):
    name = models.CharField(max_length=100)
    duration = models.IntegerField()
    to_return = models.BooleanField(default=False)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Correspondence(models.Model):
    DOCUMENT_TYPE_CHOICES = [
        ('original', 'Original'),
        ('duplicate', 'Duplicate'),
        ('copy', 'Copy'),
    ]
    
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('in_progress', 'In Progress'),
        ('transmitted', 'Transmitted'),
        ('reject', 'Rejected'),
    ]

    code = models.CharField(max_length=25)
    name = models.CharField(max_length=150)
    date = models.DateTimeField()
    description = models.TextField(null=True, blank=True)
    document_type = models.CharField(max_length=10, choices=DOCUMENT_TYPE_CHOICES, default='original')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    priority = models.ForeignKey(CorrespondencePriority, on_delete=models.CASCADE)
    typology = models.ForeignKey(CorrespondenceTypology, on_delete=models.CASCADE)
    action = models.ForeignKey(CorrespondenceAction, on_delete=models.CASCADE)
    sender_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_correspondences')
    sender_organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE, related_name='sent_correspondences')
    recipient_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='received_correspondences')
    recipient_organisation = models.ForeignKey(Organisation, on_delete=models.SET_NULL, null=True, related_name='received_correspondences')
    is_archived = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.code} - {self.name}"

class CorrespondenceAttachment(models.Model):
    correspondence = models.ForeignKey(Correspondence, on_delete=models.CASCADE, related_name='attachments')
    name = models.CharField(max_length=255)
    hash = models.CharField(max_length=255)
    extension = models.CharField(max_length=50)
    original_name = models.CharField(max_length=255)
    added_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.original_name} ({self.correspondence.code})"

class CorrespondenceRelated(models.Model):
    correspondence = models.ForeignKey(Correspondence, on_delete=models.CASCADE, related_name='related_correspondences')
    related_correspondence = models.ForeignKey(Correspondence, on_delete=models.CASCADE, related_name='related_to_correspondences')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('correspondence', 'related_correspondence')

    def __str__(self):
        return f"{self.correspondence.code} related to {self.related_correspondence.code}"

class Batch(models.Model):
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=250)
    organisation_holder = models.ForeignKey(Organisation, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.code} - {self.name}"

class BatchCorrespondence(models.Model):
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, related_name='correspondences')
    correspondence = models.ForeignKey(Correspondence, on_delete=models.CASCADE)
    insert_date = models.DateTimeField(null=True)
    remove_date = models.DateTimeField(null=True)
    insert_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='batch_inserts')
    insert_by_organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE, related_name='batch_inserts')
    remove_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='batch_removes')
    remove_by_organisation = models.ForeignKey(Organisation, on_delete=models.SET_NULL, null=True, related_name='batch_removes')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.batch.code} - {self.correspondence.code}"

class BatchTransaction(models.Model):
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    send_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_batch_transactions')
    send_by_organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE, related_name='sent_batch_transactions')
    send_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_batch_transactions')
    send_to_organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE, related_name='received_batch_transactions')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Batch {self.batch.code} transaction from {self.send_by_organisation.name} to {self.send_to_organisation.name}" 