#!/usr/bin/env python3
from database import Base, engine, session
from models import Movie, Actor
import click

@click.group()
def cli():
    pass

def valid_rating(ctx, param, value):
    if not isinstance(value, (int, float)):
        raise click.BadParameter("Rating must be a number")
    else:
        return value


@click.command()
@click.option('--title', prompt='Title', help="Movie title")
@click.option('--actor', prompt='Actor', help='Movie main actor')
@click.option('--category', prompt='Category', help='Movie category')
@click.option('--rating', prompt='Rating', help='Movie rating')
def add_movie(title, rating, category, actor):
    """Add a new movie to the database."""

    existing_actor = session.query(Actor).filter(Actor.name == actor).first()
    if existing_actor:
        new_movie = Movie(title=title, rating=rating, category=category, actor_id=existing_actor.id)
        session.add(new_movie)
        session.commit()

        click.echo(f"\nAdded movie with ID: {new_movie.id}\n")

    else:
        click.echo(f"\n{actor} not found. Make sure the actor exists before adding a movie.\n")


@click.command()
@click.option('--id', prompt='ID', help="Id of movie to delete")
def delete_movie(id):
    """Delete a movie from the database."""

    exists = session.query(Movie).filter(Movie.id == id).first()
    if exists:
        session.delete(exists)
        session.commit()
        click.echo("\nMovie deleted successfully! \n")

    else:
        click.echo("\nMovie not found! \n")


@click.command()
@click.option("--title", prompt="Movie Title", help="title of the movie you want to find")
def find_by_title(title):
    "Find movie by title"
    existing_movie = session.query(Movie).filter(Movie.title == title).first()
    starring = session.query(Actor.name).filter(Actor.id == existing_movie.actor_id).first()
    actor_name = starring[0] if starring else ""

    if existing_movie:
        click.echo(f"\nMovie Details\n"
                   f"-------------\n"
                   f'Id: {existing_movie.id}\n'
                    f'Title: {existing_movie.title}\n'
                    f"Category: {existing_movie.category}\n"
                    f"Starring: {actor_name}\n")
    else:
        click.echo(f"{title} doesn't exist in the database.")


@click.command()
@click.option("--category", prompt="Movie Category", help="category of the movie you want to find")
def find_by_category(category):
    "Find movies by category"

    category_exists = session.query(Movie).filter(Movie.category == category).first()

    if category_exists:
        all_movies = session.query(Movie).filter(Movie.category == category).all()

        cli_title = f"\nAll {category} movies\n"
        click.echo(
            f"{'-' * (len(cli_title)-2)}"
            f"{cli_title}"
            f"{'-' * (len(cli_title)-2)}\n"
            )
        
        for movie in all_movies:
            starring = session.query(Actor.name).filter(Actor.id == movie.actor_id).first()
            actor_name = starring[0] if starring else ""

            cli_result = f"Id: {movie.id}, Title: {movie.title.title()}, Category: {movie.category}, Starring: {actor_name}\n"
            click.echo(
                f"{cli_result}"
                f"{'-' * (len(cli_result)-1)}"
                )
    else:
        click.echo(f"\"{category}\" category doesn't exist in the database.")


@click.command()
@click.option("--actor", prompt="Actor", help="Name of the actor")
def find_by_actor(actor):
    """Find movies by actor"""
    actor_exists = session.query(Actor).filter(Actor.name == actor).first()

    if actor_exists:
        movies = session.query(Movie).filter(Movie.actor_id == actor_exists.id).all()

        cli_title = f"\nAll movies by {actor}\n"
        click.echo(
            f"{'-' * (len(cli_title)-2)}"
            f"{cli_title}"
            f"{'-' * (len(cli_title)-2)}\n"
            )
        
        for movie in movies:
            cli_result = f"Id: {movie.id}, Title: {movie.title}, Category: {movie.category}\n"
            click.echo(
                f"{cli_result}"
                f"{'-' * (len(cli_result)-1)}"
                )        
    else:
        click.echo(f"\"{actor}\" doesn't exist in the database.")


cli.add_command(add_movie)
cli.add_command(delete_movie)
cli.add_command(find_by_title)
cli.add_command(find_by_category)
cli.add_command(find_by_actor)



if __name__ == "__main__":
    Base.metadata.create_all(engine)
    cli()