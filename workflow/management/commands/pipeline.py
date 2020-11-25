from django.core.management.base import BaseCommand, CommandError
from kratos.apps.pipeline.models import Pipeline
from kratos.apps.pipeline.serializers import PipelineSerializer
from workflow import executor

class Command(BaseCommand):
    help = 'run pipeline'

    def add_arguments(self, parser):
        parser.add_argument('pipeline_ids', nargs='+', type=int)

    def handle(self, *args, **options):
        pipelines = Pipeline.objects.filter(pk__in=options['pipeline_ids'])
        pipelines = PipelineSerializer(pipelines, many=True).data

        for pipeline in pipelines:
            executor.run(pipeline)
