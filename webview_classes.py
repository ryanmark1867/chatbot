# classes defined to share information with the code responsible for generating the dynamic web content

class movie_info:
    '''define the characteristics that need to be carried for movies'''
    def __init__(self,poster_url, title, year, rating,run_time,genre_list,director_list,actor_list,crew_dict,plot):
        self.poster_url = poster_url
        self.title = title
        self.year = year
        self.rating = rating
        self.run_time = run_time
        self.genre_list = genre_list
        self.director_list = director_list
        self.actor_list = actor_list
        self.crew_dict = crew_dict
        self.plot = plot
        