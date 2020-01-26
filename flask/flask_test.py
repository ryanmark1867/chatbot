# tester app to exercised Flask

from flask import Flask, render_template
from string import Template

# poster URLs copied from main file
image_path = 'https://image.tmdb.org/t/p/w500'
image_path_dict = {}
image_path_dict["small"] = 'https://image.tmdb.org/t/p/w92'
image_path_dict["medium"] = 'https://image.tmdb.org/t/p/w342'
image_path_dict["big"] = 'https://image.tmdb.org/t/p/w500'

'''
Toy Story
Jumanji
Grumpier Old Men
Waiting to Exhale
Father of the Bride Part II
'''


# poster filenames:
poster_file = {}
poster_file['toy_story'] = 'rhIRbceoE9lR4veEXuwCC2wARtG.jpg'
poster_file['jumanji'] = 'vzmL6fP7aPKNKPRTFnZmiUfciyV.jpg'
poster_file['grumpier_old_men'] ='6ksm1sjKMFLbO7UY2i6G1ju9SML.jpg'
poster_file['waiting_to_exhale'] ='16XOMpEaLWkrcPqSQqhTmeJuqQl.jpg'
poster_file['father_of_the_bride'] ='e64sOI48hQXyru7naBFyssKFxVd.jpg'


app = Flask(__name__)

HTML_TEMPLATE = Template("""
<h1>Hello ${file_name}!</h1>

<img src="https://image.tmdb.org/t/p/w342/${file_name}" alt="poster for ${file_name}">

""")

@app.route('/')
def homepage():
    return """<h1>Test of dynamic poster display</h1>"""

@app.route('/<some_file>')
def some_place_page(some_file):
    return(HTML_TEMPLATE.substitute(file_name=some_file))

'''
@app.route('/')
def index():
    return render_template('summary_template.html')
#    return 'Hello world'
'''

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
