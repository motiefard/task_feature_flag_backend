from rest_framework import serializers
from .models import FeatureFlag, FlagDependency, AuditLog
from rest_framework.reverse import reverse


class FlagDependencySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = FlagDependency
        fields = ['id', 'flag', 'depends_on']


class FeatureFlagSerializer(serializers.ModelSerializer):
    dependencies = serializers.PrimaryKeyRelatedField(
        queryset=FeatureFlag.objects.all(),
        many=True,
        required=False,
        source='dependencies_set',
        write_only=True
    )
    depends_on = serializers.SerializerMethodField(read_only=True)
    url = serializers.SerializerMethodField()


    def get_url(self, obj):
        request = self.context.get('request')
        return reverse('flag-detail', args=[obj.pk], request=request)

    class Meta:
        model = FeatureFlag
        fields = ['url', 'id', 'name', 'description', 'enabled', 'created_at', 'created_by', 'dependencies', 'depends_on']
        read_only_fields = ['enabled', 'created_at']

    def get_depends_on(self, obj):
        return list(obj.dependencies.values_list('depends_on__id', flat=True))

    def create(self, validated_data):
        dependencies = validated_data.pop('dependencies_set', [])
        flag = FeatureFlag.objects.create(**validated_data)
        for dep in dependencies:
            if self._creates_cycle(flag, dep):
                raise serializers.ValidationError('Circular dependency detected.')
            FlagDependency.objects.create(flag=flag, depends_on=dep)
        return flag

    def _creates_cycle(self, flag, depends_on):
        # DFS to check for cycles
        stack = [depends_on]
        visited = set()
        while stack:
            current = stack.pop()
            if current == flag:
                return True
            visited.add(current)
            next_deps = FeatureFlag.objects.filter(dependents__flag=current)
            for dep in next_deps:
                if dep not in visited:
                    stack.append(dep)
        return False

class AuditLogSerializer(serializers.ModelSerializer):
    flag_name = serializers.CharField(source='flag.name', read_only=True)
    class Meta:
        model = AuditLog
        fields = ['id', 'flag', 'flag_name', 'action', 'actor', 'reason', 'timestamp']
        read_only_fields = fields 