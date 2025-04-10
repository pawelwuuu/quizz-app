from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from quiz.models import Notification
from django.utils import timezone

class Command(BaseCommand):
    help = 'Wysyła powiadomienia do wszystkich użytkowników'

    def add_arguments(self, parser):
        parser.add_argument(
            'message',
            type=str,
            help='Treść powiadomienia do wysłania'
        )
        parser.add_argument(
            '--test',
            action='store_true',
            help='Tryb testowy - pokaże podgląd bez zapisywania'
        )

    def handle(self, *args, **options):
        User = get_user_model()
        users = User.objects.all()
        message = options['message']
        test_mode = options['test']

        self.stdout.write(self.style.SUCCESS(f'Przygotowano do wysłania {users.count()} powiadomień'))
        
        if test_mode:
            self.stdout.write(self.style.WARNING('\nTRYB TESTOWY - nie zapisuję do bazy\n'))

        for user in users:
            if test_mode:
                self.stdout.write(f'[TEST] Powiadomienie dla {user.email}: {message}')
            else:
                Notification.objects.create(
                    user=user,
                    text=message,
                    created_at=timezone.now()
                )

        if not test_mode:
            self.stdout.write(self.style.SUCCESS(f'\nPomyślnie wysłano {users.count()} powiadomień!'))
        else:
            self.stdout.write(self.style.WARNING('\nZakończono w trybie testowym'))