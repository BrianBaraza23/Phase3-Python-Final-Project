from faker import Faker
import random
from database import session
from models import Movie, Actor


if __name__ == "__main__":

    session.query(Movie).delete()
    session.query(Actor).delete()

    fake = Faker()

    all_actors = []

    for i in range(40):
        
        actor = Actor(
            name=fake.name(),
        )

        session.add(actor)
        all_actors.append(actor)

    session.commit()


    movie_categories = [
        "Action",
        "Adventure",
        "Animation",
        "Comedy",
        "Crime",
        "Documentary",
        "Drama",
        "Family",
        "Fantasy",
        "Horror",
        "Mystery",
        "Romance",
        "Science Fiction",
        "Thriller",
        "War",
        "Western",
        "Musical",
        "Historical",
        "Biography",
        "Fantasy",
        "Superhero",
    ]

    suffixes = [
        "Adventure",
        "Journey",
        "Quest",
        "Mystery",
        "Secret",
        "Conspiracy",
        "Dream",
        "Nightmare",
        "Legend",
        "Story",
        "Tale",
        "Chronicles",
        "Legacy",
    ]
    
    all_movies = []

    for actor in all_actors:
        for i in range(random.randint(1, 5)):

            movie = Movie(
                title= f"{fake.word().title()} {random.choice(suffixes)}",
                rating=random.randint(1, 10),
                category=random.choice(movie_categories),
                actor_id=actor.id,
            )

            session.add(movie)
            all_movies.append(movie)

    session.commit()
    session.close()
    print("Database seeded successfully!")