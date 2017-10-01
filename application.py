from flask import render_template
from flask import url_for

#############
###NOTHING WORKS HERE
#############


url_for('static', filename='/static/index.html')
#url_for('static', filename='/static/assets/css/styles.min.css')
#url_for('static', filename='/static

@app.route('/')
def serve_index():
    return render_template('index.html')

