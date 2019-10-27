## intent:affirm
- yes
- indeed
- of course
- that sounds good
- correct

## intent:condition_by_cast
- list [movies](ranked_col) with [Marilyn Monroe](cast_name)
- list [movies](ranked_col) with [Jack Lemmon](cast_name)
- list [movies](ranked_col) with [Pacino](cast_name) and [De Niro](cast_name)
- [movies](ranked_col) with [Pacino](cast_name) and [De Niro](cast_name)
- list [movies](ranked_col) with [Marilyn Monroe](cast_name) and [Jack Lemmon](cast_name)
- [movies](ranked_col) with [Marilyn Monroe](cast_name) and [Jack Lemmon](cast_name)
- [characters](ranked_col) played by [Tom Hanks](cast_name)
- what are the [characters](ranked_col) played by [Tom Hanks](cast_name)

## intent:condition_by_keyword
- list [movies](ranked_col) about [midlife crisis](keyword)
- list [movies](ranked_col) about [vampires](keyword)
- list [midlife crisis](keyword) [movies](ranked_col)
- list [movies](ranked_col) about [usa president](keyword]
- list [funny](genre) [vampire](keyword) [movies](ranked_col)
- [funny](genre) [movies](ranked_col) about [vampires](keyword)
- [funny](genre) [vampire](keyword) [movies](ranked_col)

## intent:condition_by_movie
- what is the [plot](ranked_col) for [Taxi Driver](movie)
- what is the [plot](ranked_col) for [Toy Story](movie)
- show me the [plot](ranked_col) for [The Exorcist](movie)
- what's the [plot](ranked_col) of [Braveheart](movie)
- show me the [plot](ranked_col) for [Taxi Driver](movie)
- show me the [plot](ranked_col) for [Toy Story](movie)
- what's the [plot](ranked_col) for [The Exorcist](movie)
- what's the [year](ranked_col) for [The Exorcist](movie)
- what's the [year](ranked_col)
- what [year](ranked_col) did [The Exorcist](movie) come out
- what [year](ranked_col) did [Toy Story](movie) come out
- what [year](ranked_col) did [Taxi Driver](movie) come out
- what [year](ranked_col) did [Braveheart](movie) come out
- what was the [budget](ranked_col) for [Goldfinger](movie)
- what was the [budget](ranked_col) for [Taxi Driver](movie)
- what was the [budget](ranked_col) for [Jaws](movie)
- what was the [budget](ranked_col) for [The Exorcist](movie)
- what was the [budget](ranked_col) for [Toy Story](movie)

## intent:condition_by_year
- show me the [top](top_bottom) [movies](ranked_col) from [2004](year)
- show me the [top](top_bottom) [movies](ranked_col) from [1948](year)
- show me the [top](top_bottom) [movies](ranked_col) from [1995](year)
- show me the [bottom](top_bottom) [movies](ranked_col) from [2004](year)
- show me the [bottom](top_bottom) [movies](ranked_col) from [1948](year)
- show me the [bottom](top_bottom) [movies](ranked_col) from [1995](year)
- show me the [top](top_bottom) [movies](ranked_col) from [1949](year)
- show me the [top](top_bottom) [movies](ranked_col) from [1950](year)
- show me the [top](top_bottom) [movies](ranked_col) from [1992](year)
- show me the [bottom](top_bottom) [movies](ranked_col) from [1949](year)
- show me the [bottom](top_bottom) [movies](ranked_col) from [1950](year)
- show me the [bottom](top_bottom) [movies](ranked_col) from [1992](year)
- show me the [top](top_bottom) [movies](ranked_col) from [1990](year)
- show me the [top](top_bottom) [movies](ranked_col) from [1991](year)
- show me the [top](top_bottom) [movies](ranked_col) from [1993](year)
- show me the [bottom](top_bottom) [movies](ranked_col) from [1990](year)
- show me the [bottom](top_bottom) [movies](ranked_col) from [1991](year)
- show me the [bottom](top_bottom) [movies](ranked_col) from [1993](year)
- show me the [top](top_bottom) [2](row_number) [movies](ranked_col) from [2004](year)
- show me the [top](top_bottom) [3](row_number) [movies](ranked_col) from [1948](year)
- show me the [top](top_bottom) [4](row_number) [movies](ranked_col) from [1995](year)
- show me the [bottom](top_bottom) [5](row_number) [movies](ranked_col) from [2004](year)
- show me the [bottom](top_bottom) [6](row_number) [movies](ranked_col) from [1948](year)
- show me the [bottom](top_bottom) [7](row_number) [movies](ranked_col) from [1995](year)
- show me the [top](top_bottom) [8](row_number) [movies](ranked_col) from [1949](year)
- show me the [top](top_bottom) [9](row_number) [movies](ranked_col) from [1950](year)
- show me the [top](top_bottom) [10](row_number) [movies](ranked_col) from [1992](year)
- show me the [bottom](top_bottom) [11](row_number) [movies](ranked_col) from [1949](year)
- show me the [bottom](top_bottom) [12](row_number) [movies](ranked_col) from [1950](year)
- show me the [bottom](top_bottom) [13](row_number) [movies](ranked_col) from [1992](year)
- show me the [top](top_bottom) [14](row_number) [movies](ranked_col) from [1990](year)
- show me the [top](top_bottom) [15](row_number) [movies](ranked_col) from [1991](year)
- show me the [top](top_bottom) [16](row_number) [movies](ranked_col) from [1993](year)
- show me the [bottom](top_bottom) [17](row_number) [movies](ranked_col) from [1990](year)
- show me the [bottom](top_bottom) [18](row_number) [movies](ranked_col) from [1991](year)
- show me the [bottom](top_bottom) [19](row_number) [movies](ranked_col) from [1993](year)

## intent:deny
- no
- never
- I don't think so
- don't like that
- no way
- not really

## intent:get_file_columns
- can i get details for [c:\personal\chatbot_july_2019\datasets\links.csv](file_name)
- can i get details for [c:\personal\chatbot_july_2019\datasets\credits.csv](file_name)
- can i get details for [c:\personal\chatbot_july_2019\datasets\keywords.csv](file_name)
- can i get details for [c:\personal\chatbot_july_2019\datasets\links_small.csv](file_name)
- can i get details for [c:\personal\chatbot_july_2019\datasets\movies_metadata.csv](file_name)
- can i get details for [c:\personal\chatbot_july_2019\datasets\ratings.csv](file_name)
- can i get details for [c:\personal\chatbot_july_2019\datasets\ratings_small.csv](file_name)
- details for [c:\personal\chatbot_july_2019\datasets\links.csv](file_name)
- details for [c:\personal\chatbot_july_2019\datasets\credits.csv](file_name)
- details for [c:\personal\chatbot_july_2019\datasets\keywords.csv](file_name)
- details for [c:\personal\chatbot_july_2019\datasets\links_small.csv](file_name)
- details for [c:\personal\chatbot_july_2019\datasets\movies_metadata.csv](file_name)
- details for [c:\personal\chatbot_july_2019\datasets\ratings.csv](file_name)
- details for [c:\personal\chatbot_july_2019\datasets\ratings_small.csv](file_name)
- details for [https://gist.githubusercontent.com/curran/a08a1080b88344b0c8a7/raw/d546eaee765268bf2f487608c537c05e22e4b221/iris.csv](file_name)
- can I get details for [https://gist.githubusercontent.com/curran/a08a1080b88344b0c8a7/raw/d546eaee765268bf2f487608c537c05e22e4b221/iris.csv](file_name)
- details\nfor [c:\personal\chatbot_july_2019\datasets\ratings.csv](file_name:c: personal chatbot_july_2019\datasets ratings.csv)
- details please for [c:\personal\chatbot_july_2019\datasets\ratings.csv](file_name:c: personal chatbot_july_2019\datasets ratings.csv)
- details\nfor [https://raw.githubusercontent.com/ryanmark1867/manning/master/CSV_XLS/Streetcar%20Jan%202014.csv](file_name)
- details\nfor [https://raw.githubusercontent.com/ryanmark1867/manning/master/CSV_XLS/Streetcar%20Jan%202014.csv](file_name)
- details\nfor [https://raw.githubusercontent.com/ryanmark1867/manning/master/CSV_XLS/Streetcar%20Jan%202014.csv](file_name)

## intent:get_file_row
- row [4](row_number)
- row [0](row_number)
- row [1](row_number)
- row [2](row_number)
- row [3](row_number)
- row [9](row_number)
- row [5](row_number)
- row [6](row_number)
- row [7](row_number)
- row [8](row_number)
- row [4](row_number) please
- row [0](row_number) please
- row [1](row_number) please
- row [2](row_number) please
- row [3](row_number) please
- row [9](row_number) please
- row [5](row_number) please
- row [6](row_number) please
- row [7](row_number) please
- row [8](row_number) please
- 2
- [3](row_number)
- [5](row_number)
- [6](row_number)
- [7](row_number)
- [8](row_number)

## intent:get_first_n_rows
- first [3](row_range) rows please

## intent:get_last_n_rows
- show me that last [2](row_range) rows
- show me that last [3](row_range) rows
- show me that last [4](row_range) rows
- show me that last [5](row_range) rows
- show me that last [6](row_range) rows
- show me that last [7](row_range) rows
- show me that last [8](row_range) rows
- show me that last [9](row_range) rows
- show me that last [10](row_range) rows
- please show me that last [2](row_range) rows
- please show me that last [3](row_range) rows
- please show me that last [4](row_range) rows
- please show me that last [5](row_range) rows
- please show me that last [6](row_range) rows
- please show me that last [7](row_range) rows
- please show me that last [8](row_range) rows
- please show me that last [9](row_range) rows
- please show me that last [10](row_range) rows
- show me the last [4](row_range) rows

## intent:goodbye
- bye
- goodbye
- see you around
- see you later

## intent:greet
- hey
- hello
- hi
- good morning
- good evening
- hey there
- good day
- Hi

## intent:mood_great
- perfect
- very good
- great
- amazing
- wonderful
- I am feeling very good
- I am great
- I'm good

## intent:mood_unhappy
- sad
- very sad
- unhappy
- bad
- very bad
- awful
- terrible
- not very good
- extremely sad
- so sad

## synonym:c: personal chatbot_july_2019\datasets ratings.csv
- c:\personal\chatbot_july_2019\datasets\ratings.csv
