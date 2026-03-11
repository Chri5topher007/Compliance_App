from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Creates a default admin user if none exists'

    def handle(self, *args, **options):
        if User.objects.filter(is_superuser=True).exists():
            self.stdout.write(self.style.WARNING('Admin account already exists.'))
            return

        default_username = 'admin'
        default_password = 'Admin@12345'
        
        try:
            user = User.objects.create_superuser(
                username=default_username,
                email='admin@company.com',
                password=default_password,
                role='ADMIN'
            )
            self.stdout.write(self.style.success('========================================'))
            self.stdout.write(self.style.SUCCESS(f'DEFAULT ADMIN CREATED'))
            self.stdout.write(self.style.SUCCESS(f'Username: {default_username}'))
            self.stdout.write(self.style.SUCCESS(f'Password: {default_password}'))
            self.stdout.write(self.style.SUCCESS('========================================'))
        except Exception as e:
            self.stderr.write(self.style.ERROR(str(e)))