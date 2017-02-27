"""
Unit test for populate_created_on_site_user_attribute management command.
"""
import ddt
import mock
from django.test import TestCase
from django.contrib.auth.models import User
from django.core.management import call_command, CommandError

from student.models import Registration, UserAttribute
from student.tests.factories import UserFactory
from openedx.core.djangoapps.site_configuration.tests.mixins import SiteMixin


@ddt.ddt
class TestPopulateUserAttribute(SiteMixin, TestCase):
    """
    Test populate_created_on_site_user_attribute management command.
    """

    def setUp(self):
        super(TestPopulateUserAttribute, self).setUp()

        self._create_sample_data()
        self.users = User.objects.all()
        self.registered_users = Registration.objects.all()
        self.user_ids = ','.join([str(user.id) for user in self.users])
        self.activation_keys = ','.join([registered_user.activation_key for registered_user in self.registered_users])

    def _create_sample_data(self):
        """
        Creates the User objects and register them.
        """
        for __ in range(3):
            Registration().register(UserFactory.create())

    def test_command_by_user_ids(self):
        """
        Test created_on_site attribute's population by user ids.
        """
        call_command(
            "populate_created_on_site_user_attribute",
            "--users", self.user_ids,
            "--site-domain", self.site.domain
        )

        for user in self.users:
            self.assertEqual(UserAttribute.get_user_attribute(user, 'created_on_site'), self.site.domain)

    def test_command_by_activation_keys(self):
        """
        Test created_on_site attribute's population by activation keys.
        """
        call_command(
            "populate_created_on_site_user_attribute",
            "--activation-keys", self.activation_keys,
            "--site-domain", self.site.domain
        )

        for register_user in self.registered_users:
            self.assertEqual(UserAttribute.get_user_attribute(register_user.user, 'created_on_site'), self.site.domain)

    @ddt.data('y', 'n')
    def test_with_invalid_site_domain(self, populate):
        """
        Test management command with invalid site domain.
        """
        fake_site_domain = 'fake-site-domain'
        with mock.patch('__builtin__.raw_input', return_value=populate) as _raw_input:
            call_command(
                "populate_created_on_site_user_attribute",
                "--users", self.user_ids,
                "--site-domain", fake_site_domain
            )

        for user in self.users:
            if populate == 'y':
                self.assertEqual(UserAttribute.get_user_attribute(user, 'created_on_site'), fake_site_domain)
            else:
                self.assertIsNone(UserAttribute.get_user_attribute(user, 'created_on_site'))

    def test_command_without_site_domain(self):
        """
        Test management command raises CommandError without '--site-domain' argument.
        """
        with self.assertRaises(CommandError):
            call_command(
                "populate_created_on_site_user_attribute",
                "--user", self.user_ids,
                "--activation-keys", self.activation_keys
            )

    def test_command_with_invalid_argument(self):
        """
        Test management command raises CommandError without '--users' and '--activation_keys' arguments.
        """
        with self.assertRaises(CommandError):
            call_command(
                "populate_created_on_site_user_attribute",
                "--site-domain", self.site.domain
            )
