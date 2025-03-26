from rest_framework import serializers
from .models import (
    Folder, Document, MetadataDefinition,
    DocumentMetadata, FolderMetadata, ReferenceList,
    ReferenceValue
)

class ReferenceValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReferenceValue
        fields = ['id', 'value', 'description', 'active', 'created_by', 'created_at', 'updated_by', 'updated_at']
        read_only_fields = ['created_by', 'created_at', 'updated_by', 'updated_at']

class ReferenceListSerializer(serializers.ModelSerializer):
    values = ReferenceValueSerializer(many=True, read_only=True)

    class Meta:
        model = ReferenceList
        fields = ['id', 'name', 'description', 'values', 'created_by', 'created_at', 'updated_by', 'updated_at']
        read_only_fields = ['created_by', 'created_at', 'updated_by', 'updated_at']

class MetadataDefinitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MetadataDefinition
        fields = ['id', 'name', 'description', 'data_type', 'mandatory', 'created_by', 'created_at', 'updated_by', 'updated_at']
        read_only_fields = ['created_by', 'created_at', 'updated_by', 'updated_at']

class DocumentMetadataSerializer(serializers.ModelSerializer):
    definition = MetadataDefinitionSerializer(read_only=True)

    class Meta:
        model = DocumentMetadata
        fields = ['id', 'document', 'definition', 'value', 'created_by', 'created_at', 'updated_by', 'updated_at']
        read_only_fields = ['created_by', 'created_at', 'updated_by', 'updated_at']

class FolderMetadataSerializer(serializers.ModelSerializer):
    definition = MetadataDefinitionSerializer(read_only=True)

    class Meta:
        model = FolderMetadata
        fields = ['id', 'folder', 'definition', 'value', 'created_by', 'created_at', 'updated_by', 'updated_at']
        read_only_fields = ['created_by', 'created_at', 'updated_by', 'updated_at']

class DocumentSerializer(serializers.ModelSerializer):
    metadata = DocumentMetadataSerializer(many=True, read_only=True)

    class Meta:
        model = Document
        fields = ['id', 'name', 'description', 'file', 'folder', 'metadata', 'created_by', 'created_at', 'updated_at']
        read_only_fields = ['created_by', 'created_at', 'updated_at']

class FolderSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()
    metadata = FolderMetadataSerializer(many=True, read_only=True)

    class Meta:
        model = Folder
        fields = ['id', 'name', 'description', 'parent', 'children', 'metadata', 'created_by', 'created_at', 'updated_by', 'updated_at', 'deleted_by', 'deleted_at', 'version', 'activity']
        read_only_fields = ['created_by', 'created_at', 'updated_by', 'updated_at', 'deleted_by', 'deleted_at']

    def get_children(self, obj):
        children = Folder.objects.filter(parent=obj)
        return FolderSerializer(children, many=True).data

class FolderDetailSerializer(FolderSerializer):
    documents = DocumentSerializer(many=True, read_only=True) 