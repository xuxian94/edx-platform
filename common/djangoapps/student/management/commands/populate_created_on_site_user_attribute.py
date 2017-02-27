"""
Command created to back-populate domain of the site the user account was created on.
"""
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.core.management.base import BaseCommand, CommandError

from student.models import UserAttribute, Registration


class Command(BaseCommand):
    """
    This commands back-populate domain of the site the user account was created on.
    """
    help = """./manage.py lms populate_created_on_site_user_attribute --users <user_id1>,<user_id2>...
           '--activation-keys <key1>,<key2>... --site-domain <site_domain> --settings=devstack"""

    def add_arguments(self, parser):
        """
        Add arguments to the command parser.
        """
        parser.add_argument(
            '--users',
            help='Enter user ids.',
            default='',
            type=str
        )
        parser.add_argument(
            '--activation-keys',
            help='Enter activation keys.',
            default='',
            type=str
        )
        parser.add_argument(
            '--site-domain',
            help='Enter an existing site domain.',
        )

    def handle(self, *args, **options):
        site_domain = options['site_domain']
        user_ids = options['users'].split(',') if options['users'] else []
        activation_keys = options['activation_keys'].split(',') if options['activation_keys'] else []

        if not site_domain:
            raise CommandError('You must provide site-domain argument.')

        if not user_ids and not activation_keys:
            raise CommandError('You must provide user ids or activation keys.')

        try:
            Site.objects.get(domain__exact=site_domain)
        except Site.DoesNotExist:
            question = "The site you specified is not configured as a Site in the system. " \
                       "Are you sure you want to continue? (y/n):"
            if str(raw_input(question)).lower().strip()[0] != 'y':
                return

        for user_id in user_ids:
            try:
                user = User.objects.get(id=user_id)
                if not UserAttribute.get_user_attribute(user, 'created_on_site'):
                    UserAttribute.set_user_attribute(user, 'created_on_site', site_domain)
                else:
                    self.stdout.write("created_site_on attribute already exists for user id: {id}".format(id=user_id))
            except User.DoesNotExist:
                self.stdout.write("This user id [{id}] does not exist in the system.".format(id=user_id))

        for key in activation_keys:
            try:
                user = Registration.objects.get(activation_key=key).user
                if not UserAttribute.get_user_attribute(user, 'created_on_site'):
                    UserAttribute.set_user_attribute(user, 'created_on_site', site_domain)
                else:
                    self.stdout.write("created_site_on attribute already exists for user id: {id}".format(id=user.id))
            except Registration.DoesNotExist:
                self.stdout.write("This activation key [{key}] does not exist in the system.".format(key=key))
