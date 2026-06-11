from sqlalchemy.orm import DeclarativeBase, declared_attr

class Base(DeclarativeBase):
    @declared_attr.directive
    def __tablename__(cls) -> str:
        # Your snake_case logic is great
        name = cls.__name__
        snake = []
        for idx, char in enumerate(name):
            if char.isupper() and idx != 0:
                snake.append("_")
            snake.append(char.lower())
        return "".join(snake)