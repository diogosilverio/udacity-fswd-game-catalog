from sqlalchemy import Column, String, Integer, Text
from catalog.infra.db_factory import Base


class Category(Base):
    """ An entity that aggregates games with common features and aspects. """
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True)
    description = Column(Text, nullable=False)

    def top_games(self, top):
        return self.games[0:top]

    def to_json(self, load_game=True):

        me_as_json = {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'link': "/category/%d" % self.id
        }

        if load_game:
            me_as_json['games'] = len(self.games)

        return me_as_json

    def to_short_json(self, load_games=True):
        j = self.to_json(load_games)
        j.pop('description', None)

        return j
