from catalog.dao.game_dao import GameDao


class GameService:
    """ Provider of common services and operations for a Game entity. """

    def __init__(self):
        self.dao = GameDao()

    def new(self, game):
        try:
            self.dao.merge(game)
            return True
        except Exception as e:
            print "Error persisting game: %s" % e.message
            return False

    def find_by(self, gid, join_category=False):
        return self.dao.find_by_id(gid, join_category)

    def find_by_category(self, c, limit=0):
        return self.dao.find_by_category(c, limit)

    def all(self):
        return self.dao.find_all()

    def delete(self, game):
        self.dao.delete(game)

    def find_by_platform(self, plat):
        plat_name = GameService.mapped_platforms(plat)

        if not plat_name:
            return {'platform': None, 'games': None}

        games = self.dao.find_by_platform(plat)

        return {'platform': plat_name + ' Games', 'games': games}

    def latest(self, batch_num):
        """ Returns the most recent N inserted games. """
        return self.dao.latest(batch_num)

    def increment(self, gid):
        """ Add 1 to game view count. """
        self.dao.increment(gid)

    def top10(self):
        return self.dao.top10()

    @staticmethod
    def mapped_platforms(plat):
        """ Maps categories acronym for user readable format. """
        if plat == 'pc':
            return 'PC'
        elif plat == 'xo':
            return 'Xbox One'
        elif plat == 'ps':
            return 'PS4'
