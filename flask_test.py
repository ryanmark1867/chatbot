# tester app to exercised Flask

from flask import Flask, render_template
from string import Template
from OpenSSL import SSL
# import classes for exchanging data with dynamic web serving code
from webview_classes import movie_info
from webview_classes import payload_item
import pickle
#from actions import wv_payload
# import ssl
# context = SSL.Context(SSL.PROTOCOL_TLS)
# client_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
#
#context = SSL.Context(SSL.PROTOCOL_TLSv1_2)
#context = SSL.Context(SSL.TLSv1_METHOD)
# context = ssl.Context(ssl.PROTOCOL_TLS)
#context.use_privatekey_file('C:\personal\chatbot_july_2019\ssl_experiment\server.key')
#context.use_certificate_file('C:\personal\chatbot_july_2019\ssl_experiment\server.crt')

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
# wv_payload = {}


app = Flask(__name__)

HTML_TEMPLATE = Template("""
<h1>Hello ${file_name}!</h1>

<img src="https://image.tmdb.org/t/p/w342/${file_name}" alt="poster for ${file_name}">

""")

@app.route('/')
def homepage():
    #global wv_payload
    # TODO REPLACE THIS HACKY WAY TO GET PAYLOAD
    print("about to try to show page")
    wv_payload_path = 'wv_payload.pkl'
    with open(wv_payload_path, 'rb') as handle:
        wv_payload = pickle.load(handle)
    for wv_payload_index in wv_payload:
        print("here is item "+str(wv_payload_index))
        print("display content is "+str(wv_payload[wv_payload_index].display_content))
        print("display type is "+str(wv_payload[wv_payload_index].display_type))
        print("return type is "+str(wv_payload[wv_payload_index].return_type))
        print("return payload is "+str(wv_payload[wv_payload_index].return_payload))
    title_display = wv_payload['original_title'].display_content[0]
    print("title_display is "+str(title_display))
    title = {'titlename':str(title_display)}
    year = {'yearname':str(wv_payload['year'].display_content[0])}
    plot = {'plotname':str(wv_payload['overview'].display_content[0])}
    return render_template('home.html',title=title,year = year,plot=plot)
    #return """<h1>Test of dynamic poster display here Feb 1 afternoon</h1>"""
    
@app.route('/about/')
def about():
    return render_template('about.html')

@app.route('/<some_file>')
def some_place_page(some_file):
    return(HTML_TEMPLATE.substitute(file_name=some_file))
    
def test_call(test_text):
    print("from actions.py got "+test_text)

'''    
def read_wv_payload(wv_payload_path):
    global wv_payload
    with open(wv_payload_path, 'rb') as handle:
        wv_payload = pickle.load(handle)
    return()
    '''

'''    
def load_wv_payload(input_wv_payload_list):
    # bring in payload list from actions.py
    global wv_payload
    wv_payload = input_wv_payload_list.copy()
    print("here is wv_payload from inside flask")
    for wv_payload_index in wv_payload:
        print("here is item "+str(wv_payload_index))
        print("display content is "+str(wv_payload[wv_payload_index].display_content))
        print("display type is "+str(wv_payload[wv_payload_index].display_type))
        print("return type is "+str(wv_payload[wv_payload_index].return_type))
        print("return payload is "+str(wv_payload[wv_payload_index].return_payload)) '''
        

'''
@app.route('/')
def index():
    return render_template('summary_template.html')
#    return 'Hello world'
'''

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
    #app.run(host='127.0.0.1', debug=True, ssl_context=context)
    # app.run(ssl_context='adhoc',debug=True, host='0.0.0.0')
    #context = ('C:\personal\chatbot_july_2019\ssl_experiment\server.crt', 'C:\personal\chatbot_july_2019\ssl_experiment\server.key')
    #app.run(ssl_context=context,debug=True, host='0.0.0.0')
