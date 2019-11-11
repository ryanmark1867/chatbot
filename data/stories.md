
## New Story
* greet
    - utter_what_next
* condition_by_movie{"ranked_col":"movies","cast_name":"Jack Lemmon"}
    - slot{"ranked_col":"movies"}
    - slot{"cast_name":"Jack Lemmon"}
    - action_condition_by_movie


## New Story
* greet
    - utter_what_next
* condition_by_media{"media":"poster","movie":"Harry Meet Sally"}
    - slot{"media":"poster"}
    - slot{"movie":"Harry Meet Sally"}
    - action_condition_by_media



## New Story
* greet
    - utter_what_next
* condition_by_movie_ordered{"ranked_col":"movies","director":"Woody Allen","rank_axis":"popularity"}
    - slot{"ranked_col":"movies"}
    - slot{"director":"Woody Allen"}
	- slot{"rank_axis":"popularity"}
    - action_condition_by_movie_ordered


## New Story
* greet
    - utter_what_next
* condition_by_movie{"ranked_col":"movies","director":"Woody Allen"}
    - slot{"ranked_col":"movies"}
    - slot{"director":"Woody Allen"}
    - action_condition_by_movie

# New Story
* greet
    - utter_what_next
* condition_by_movie{"ranked_col":"characters","cast_name":"Tom Hanks"}
    - slot{"ranked_col":"characters"}
    - slot{"cast_name":"Tom Hanks"}
    - action_condition_by_movie


## New Story

* greet
    - utter_what_next
* condition_by_movie{"ranked_col":"plot","movie":"Taxi Driver"}
    - slot{"movie":"Taxi Driver"}
    - slot{"ranked_col":"plot"}
    - action_condition_by_movie

## New Story

* greet
    - utter_what_next
* condition_by_movie{"ranked_col":"plot","movie":"Toy Story"}
    - slot{"movie":"Toy Story"}
    - slot{"ranked_col":"plot"}
    - action_condition_by_movie

## New Story

* greet
    - utter_what_next
* condition_by_movie{"ranked_col":"plot","movie":"The Exorcist"}
    - slot{"movie":"The Exorcist"}
    - slot{"ranked_col":"plot"}
    - action_condition_by_movie

## New Story

* greet
    - utter_what_next
* condition_by_movie{"ranked_col":"movies","keyword":"midlife crisis"}
    - slot{"ranked_col":"movies"}
    - slot{"keyword":"midlife crisis"}
    - action_condition_by_movie
	
	
## New Story

* greet
    - utter_what_next
* clear_slots
    - action_clear_slots	
