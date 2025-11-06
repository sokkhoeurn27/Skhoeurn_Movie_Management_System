from django.core.management.base import BaseCommand
from accounts.models import Account


class Command(BaseCommand):
    help = 'Creates a default admin account if it does not exist'

    def handle(self, *args, **options):
        # Default admin credentials
        username = 'admin'
        email = 'admin@moviemanagement.com'
        password = 'admin123'
        
        # Check if admin already exists
        if Account.objects.filter(username=username).exists():
            self.stdout.write(
                self.style.WARNING(f'Admin account "{username}" already exists!')
            )
            return
        
        # Create default admin account
        admin_user = Account.objects.create_user(
            username=username,
            email=email,
            password=password,
            role='admin',
            is_staff=True,
            is_superuser=True
        )
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully created default admin account!')
        )
        self.stdout.write(
            self.style.SUCCESS(f'Username: {username}')
        )
        self.stdout.write(
            self.style.SUCCESS(f'Password: {password}')
        )
        self.stdout.write(
            self.style.WARNING('Please change the password after first login!')
        )
