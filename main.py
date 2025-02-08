from typing import Iterable, Type
from sqlalchemy.orm import Session as SessionType, joinedload
from sqlalchemy import func
from models import Base, Session, User, Author, Post
from models.base import engine


def create_user(session: SessionType, username: str, is_staff: bool = False) -> User:
    user = User(username=username, is_staff=is_staff)
    print("Creating user", user)
    session.add(user)
    session.commit()
    print("Created user", user)
    return user


def get_user_by_username(session: SessionType, username: str) -> User:
    user = session.query(User).filter_by(username=username).one()
    return user


def create_author_for_user(
    session: SessionType,
    author_name: str,
    user: User,
) -> Author:
    # author = Author(name=author_name, user_id=user.id)
    author = Author(name=author_name, user=user)
    print("Creating author", author)
    session.add(author)
    session.commit()
    print("Created author", author)
    return author


def fetch_users_with_authors(session: SessionType) -> list[User]:
    users = session.query(User).options(joinedload(User.author)).order_by(User.id).all()

    for user in users:
        print("user", user, "author", user.author)
    return users


def fetch_authors_with_users(session: SessionType) -> list[Author]:
    authors = (
        session.query(Author).options(joinedload(Author.user)).order_by(Author.id).all()
    )

    for author in authors:
        print("author", author, "user", author.user)

    return authors


def get_author_by_username(session: SessionType, username: str) -> Author | None:
    author = (
        session.query(Author)
        .join(Author.user)
        .filter(User.username == username)
        .one_or_none()
    )

    print("Getting author", author)
    return author


def get_user_by_author_name_math(
    session: SessionType, author_name_part: str
) -> list[User]:
    users = (
        session.query(User)
        .join(User.author)
        .filter(Author.name.ilike(f"%{author_name_part}%"))
        .all()
    )

    print("found users", users)

    return users


def create_posts_for_author(
    session: SessionType, author: Author, posts_titles: Iterable[str]
) -> list[Post]:
    posts = []
    for title in posts_titles:
        post = Post(title=title, author=author)
        session.add(post)
        posts.append(post)

    print("Creating posts", posts)
    session.commit()
    print("Created posts", posts)
    return posts


def fetch_authors_with_posts_and_users(session: SessionType) -> list[Author]:
    authors = (
        session.query(Author)
        .options(joinedload(Author.posts))
        .order_by(Author.id)
        .all()
    )

    print("found authors", authors)

    for author in authors:
        print("author", author.name, "posts", author.posts, "user", author.user)

    return authors


def fetch_users_with_authors_and_posts(session: SessionType) -> list[User]:
    users = (
        session.query(User)
        .options(joinedload(User.author).joinedload(Author.posts))
        .order_by(User.id)
        .all()
    )
    print("found users", users)

    for user in users:
        print("---- user", user)
        if not user.author:
            print("---- no author for user")
            continue
        print("---- user author", user.author)
        print("---- posts", user.author.posts)

    return users


def get_average_rating(session: SessionType) -> None:
    result = session.query(func.avg(Post.rating)).scalar()
    print("average rating", result)


def get_count_items(session: SessionType, Model: Type[Base]) -> None:
    result = session.query(Model).count()
    print("model", Model, "items count", result)


def get_grouped_values(session: SessionType) -> None:
    result = session.query(func.sum(Post.rating)).scalar()
    print("rating sum result", result)

    result = (
        session.query(
            # Post.author_id,
            Author.name,
            func.sum(Post.rating),
        )
        .join(Post.author)
        .group_by(Author.name)
        .all()
    )

    print("sum by authors", result)

    result = (
        session.query(
            Author.name.label("author_name"),
            func.avg(Post.rating).label("avg_rating"),
            func.min(Post.rating).label("min_rating"),
            func.max(Post.rating).label("max_rating"),
        )
        .join(Post.author)
        .group_by(Author.name)
        .all()
    )

    print("result:", result)

    for res in result:
        print("Results for author", res.author_name)
        print("--- max rating", res.max_rating)
        print("--- min rating", res.min_rating)
        print("--- avg rating", res.avg_rating)


def main():
    # Base.metadata.drop_all(engine)
    # Base.metadata.create_all(engine)

    session: SessionType = Session()

    # admin = create_user(session, "admin", is_staff=True)
    # john = create_user(session, "John")
    # sam = create_user(session, "Sam")

    # john = get_user_by_username(session, "John")
    # sam = get_user_by_username(session, "Sam")
    #
    # author_john = create_author_for_user(session, "John Smith", user=john)
    # author_sam = create_author_for_user(session, "Samuel L.", user=sam)

    # fetch_users_with_authors(session)
    # fetch_authors_with_users(session)

    # author_john = get_author_by_username(session, "John")
    # author_sam = get_author_by_username(session, "Sam")
    # get_author_by_username(session, "nick")
    # get_user_by_author_name_math(session, "smit")
    #
    # create_posts_for_author(
    #     session, author=author_john, posts_titles=("SQL Lesson", "ORM Lesson")
    # )

    # create_posts_for_author(session, author=author_sam, posts_titles=("LOL", "ORM "))
    # fetch_authors_with_posts_and_users(session)
    # fetch_users_with_authors_and_posts(session)
    # get_count_items(session, Post)
    # get_grouped_values(session)
    session.close()


if __name__ == "__main__":
    main()
