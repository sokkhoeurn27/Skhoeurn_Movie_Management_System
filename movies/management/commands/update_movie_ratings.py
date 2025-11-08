from django.core.management.base import BaseCommand
from movies.models import Movie


class Command(BaseCommand):
    help = 'Update all movie ratings based on approved reviews'

    def handle(self, *args, **options):
        movies = Movie.objects.all()
        updated_count = 0
        
        self.stdout.write(self.style.WARNING(f'Updating ratings for {movies.count()} movies...'))
        
        for movie in movies:
            old_rating = movie.rating
            movie.update_rating()
            new_rating = movie.rating
            
            if old_rating != new_rating:
                updated_count += 1
                self.stdout.write(
                    self.style.SUCCESS(
                        f'✓ {movie.title}: {old_rating} → {new_rating} ({movie.get_review_count()} reviews)'
                    )
                )
            else:
                self.stdout.write(
                    f'  {movie.title}: {new_rating} (unchanged, {movie.get_review_count()} reviews)'
                )
        
        self.stdout.write(
            self.style.SUCCESS(f'\n✓ Updated {updated_count} movie ratings successfully!')
        )
