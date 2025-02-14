from typing import Iterable, Type
from sqlalchemy.orm import Session as SessionType, joinedload, noload, selectinload, aliased
from sqlalchemy import func, or_
from models import (
    Base,
    Session,
    User,
    Author,
    Post,
    Tag,
    Product,
    Order,
    ProductOrder
)
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


def create_tags(session: SessionType, names: list[str]):
    tags = []
    for name in names:
        tag = Tag(name=name)
        session.add(tag)
        tags.append(tag)

    session.commit()
    print("created tags", tags)
    return tags


def associate_posts_with_tags(session: SessionType):
    posts = session.query(Post).options(noload(Post.tags)).all()
    tags = session.query(Tag).all()

    tags_dict = {tag.name: tag for tag in tags}

    tag_python = tags_dict["python"]
    tag_sqla = tags_dict["sqlalchemy"]
    tag_news = tags_dict["news"]
    tag_lesson = tags_dict["lesson"]
    tag_postgres = tags_dict["postgres"]
    tag_sql = tags_dict["SQL"]

    for post in posts:
        if "sqlalchemy" in post.title.lower():
            post.tags.append(tag_sqla)
        if "lesson" in post.title.lower():
            post.tags.append(tag_lesson)
        if "news" in post.title.lower():
            post.tags.append(tag_news)
        if "python" in post.title.lower():
            post.tags.append(tag_python)
        if "postgres" in post.title.lower():
            post.tags.append(tag_postgres)
        if "sql" in post.title.lower():
            post.tags.append(tag_sql)

    session.commit()

    return posts


def get_posts_with_tags(session: SessionType):
    posts = session.query(Post).options(selectinload(Post.tags)).all()
    print("found posts", posts)
    for post in posts:
        print("--post", post.id, post.title, "-tags", post.tags)


def get_post_add_tag_and_remove(session: SessionType):
    post = (session.query(Post)
            .filter(Post.title.ilike('python'))
            .options(selectinload(Post.tags))
            .first())

    if not post:
        print("post not found")
        return

    tag = session.query(Tag).filter_by(name="news").one()
    print("post with tags", post, post.tags)

    post.tags.append(tag)
    session.commit()
    print("post tags", post.tags)

    post.tags.remove(tag)
    session.commit()
    print("post tags", post.tags)


def get_posts_by_tag(session: SessionType, tag_name: str):
    posts = (session.query(Post)
             .join(Post.tags)
             .filter(Tag.name == tag_name)
             .options(selectinload(Post.tags))
             .all())
    print("found posts for tag", tag_name)
    for post in posts:
        print("--post -", f"{post.title!r}")
        print("-tag", post.tags)


def get_posts_by_tags(session: SessionType, tag_names: list[str]):
    posts = (
        session.query(Post)
        .join(Post.tags)
        .filter(or_(*(Tag.name == name for name in tag_names)))
        .options(selectinload(Post.tags))
        .all()
    )
    print("found posts for tags", tag_names)
    for post in posts:
        print("--post -", post)
        print("-tag", post.tags)

    return posts


def get_posts_by_all_tags(session: SessionType, *tag_names):
    filters = []
    q_posts = session.query(Post)

    for index, name in enumerate(tag_names, start=1):
        tags_table: Tag = aliased(Tag, name=f"tags_{index}")
        q_posts = q_posts.join(tags_table, Post.tags)
        filters.append(tags_table.name == name)

    posts = (q_posts
             .filter(*filters)
             .options(selectinload(Post.tags))
             .all()
             )
    print("found posts for all tags", tag_names)
    for post in posts:
        print("-- post -", post)
        print("- post tags -", post.tags)

    return posts


def create_product(session: SessionType, name: str, price: int) -> Product:
    product = Product(name=name, price=price)
    session.add(product)
    session.commit()
    print("created product", product)
    return product


def create_order_with_products(session: SessionType, address: str, comment: str, user: User,
                               *products: Product) -> Order:
    order = Order(
        address=address,
        comment=comment,
        user=user
    )
    session.add(order)
    for product in products:
        product_order = ProductOrder()
        product_order.product = product
        product_order.order = order
        product_order.products_count = 2
        product_order.unit_price = product.price
        session.add(product_order)
    session.commit()
    return order


def get_product_by_name(session: SessionType, name: str) -> Product:
    product = session.query(Product).filter_by(name=name).one()
    return product


def get_orders_details(session: SessionType) -> list[Order]:
    orders = (session.query(Order)
              .options(
        joinedload(Order.user),
        joinedload(Order.products).joinedload(ProductOrder.product)
    )
              .all()
              )
    for order in orders:
        print("order for user", order.user)
        print("order to addr", order.address)
        print("order with comment", order.comment)
        print("order.products", order.products)
        for product_order in order.products:  # type ProductOrder
            print("product for", product_order.product)
            print("product count", product_order.products_count)
            print("product for", product_order.unit_price)

    return orders


def main():
    # Base.metadata.drop_all(engine)
    # Base.metadata.create_all(engine)

    session: SessionType = Session()

    # admin = create_user(session, "admin", is_staff=True)
    # john = create_user(session, "John")
    # sam = create_user(session, "Sam")

    # john = get_user_by_username(session, "John")
    sam = get_user_by_username(session, "Sam")

    # author_john = create_author_for_user(session, "John Smith", user=john)
    # author_sam = create_author_for_user(session, "Samuel L.", user=sam)

    # fetch_users_with_authors(session)
    # fetch_authors_with_users(session)

    # author_john = get_author_by_username(session, "John")
    # author_sam = get_author_by_username(session, "Sam")
    # get_author_by_username(session, "nick")
    # get_user_by_author_name_math(session, "smit")

    # create_posts_for_author(
    #     session, author=author_john, posts_titles=("SQL Lesson", "ORM Lesson")
    # )
    # create_posts_for_author(session, author=author_sam, posts_titles=("sql", "news", "python", "postgres"))

    # fetch_authors_with_posts_and_users(session)
    # fetch_users_with_authors_and_posts(session)
    # get_count_items(session, Post)
    # get_grouped_values(session)

    # tags = create_tags(
    #     session,
    #     names=[
    #     "news",
    #     "python",
    #     "lesson",
    #     "sqlalchemy",
    #     "postgres",
    #     "SQL"
    # ]
    # )
    # associate_posts_with_tags(session)
    # get_posts_by_tag(session, "python")
    # get_posts_with_tags(session)
    # get_post_add_tag_and_remove(session)
    # get_posts_by_tags(session, ["python", "lesson"])
    # get_posts_by_all_tags(session, "python", "lesson")

    # laptop = create_product(session, "Laptop", 1999)
    # desktop = create_product(session, "Desktop", 2500)

    # laptop = get_product_by_name(session, "Laptop")
    # desktop = get_product_by_name(session, "Desktop")

    # create_order_with_products(
    #     session,
    #     "GG Lane 2",
    #     "",
    #     sam,
    #     laptop,
    #     desktop )

    # get_orders_details(session)

    session.close()


if __name__ == "__main__":
    main()
