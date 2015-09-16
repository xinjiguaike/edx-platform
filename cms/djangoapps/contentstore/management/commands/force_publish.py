"""
Script for force publishing a course
"""
from django.core.management.base import BaseCommand, CommandError
from xmodule.modulestore import ModuleStoreEnum
from xmodule.modulestore.django import modulestore
from opaque_keys import InvalidKeyError
from opaque_keys.edx.keys import CourseKey
from .prompt import query_yes_no

# To run from command line: ./manage.py cms force_publish course-v1:org+course+run


class Command(BaseCommand):
    """Force publish a course"""
    help = '''
    Force publish a course. Takes one arguments:
    <course_id>: the course id of the course you want to publish forcefully
    '''

    def handle(self, *args, **options):
        "Execute the command"
        if len(args) != 1:
            raise CommandError("requires 1 argument: <course_id>")

        try:
            course_key = CourseKey.from_string(args[0])
        except InvalidKeyError:
            raise CommandError("Invalid course key.")

        if not modulestore().get_course(course_key):
            raise CommandError("Course with '%s' key not found." % args[0])

        if query_yes_no("Are you sure to publish the {0} course forcefully?".format(course_key), default="no"):
            # for now only support on split mongo
            owning_store = modulestore()._get_modulestore_for_courselike(course_key)
            if hasattr(owning_store, 'force_publish_course'):
                owning_store.force_publish_course(course_key, ModuleStoreEnum.UserID.mgmt_command)
            else:
                raise CommandError("The owning modulestore does not support this command.")

