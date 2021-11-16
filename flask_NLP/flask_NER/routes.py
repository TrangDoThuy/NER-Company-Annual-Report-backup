from flask import render_template, request, url_for, jsonify,flash
from flask_NER import app,db
from flask_NER.models import Company, Report,Exchange,JSON_file,JSON_type
import codecs
import json
import re
from boilerpy3 import extractors
import spacy
from random import random
from random import seed
nlp = spacy.load("en_core_web_sm")
seed(1)
import ahocorasick
from bs4 import BeautifulSoup
A = ahocorasick.Automaton()

@app.route("/")
@app.route("/home")
def home():
    page = request.args.get('page',1,type=int)
    companies = Company.query.order_by(Company.id).paginate(page = page, per_page = 20)
    exchanges = Exchange.query.order_by(Exchange.exchange_name)
    return render_template('home.html',companies = companies, exchanges = exchanges,currentExchangeId=0)

@app.route("/exchange/<int:exchangeId>")
def exchange(exchangeId):
    page = request.args.get('page',1,type=int)
    if(exchangeId == 0):
        companies = Company.query.order_by(Company.id).paginate(page = page, per_page = 20)
    else:
        companies = Company.query.filter_by(exchangeId=exchangeId).order_by(Company.id).paginate(page = page, per_page = 20)
    exchanges = Exchange.query.order_by(Exchange.exchange_name)
    return render_template('home.html',companies = companies, exchanges = exchanges,currentExchangeId= exchangeId)   

@app.route("/company/<int:company_id>")
def company_reports(company_id):
    page = request.args.get('page',1,type=int)
    company = Company.query.filter_by(id=company_id).first_or_404()
    reports = Report.query.filter_by(companyId=company_id).paginate(page = page,per_page=20)

    return render_template('company_reports.html',reports=reports,company=company)

@app.route("/annual-report/new.html")
def hihi():
    return render_template('new.html')
    
@app.route("/annotate", methods=['GET'])
def annotate():
    # render some data to frontend
    
    data = """<p>On January 6, a mob attacked the US Capitol with shouts of "Hang Mike Pence." Then-President Donald Trump had told his faithful vice president, according to a new book, "I don't want to be your friend anymore" because Pence said he wouldn't overturn the will of the people who chose Joe Biden to be president, and keep Trump in office.</p>
        <p>Michael D&#39;Antonio</p>
        <p>Michael D'Antonio</p>
        <p>But now, eight months later, Pence is indignant about how much coverage media is giving the people who came for him at the Capitol and suggested that the goal of the coverage is to tarnish the reputations of the millions of people supporting Trump. As for the former President, adds Pence, "We parted amicably." In fact, he says they have spoken at least a dozen times since their administration ended with Biden's swearing-in on January 20.</p>
        <p>Pence is behaving like the middle school kid intimidated by a bully's lunch money protection racket. Fearful of fighting back, he instead brings a little extra money for the gang every day and says the head bully is really his good buddy.</p>
        <p>Pence offered his sunny view of Trump and his supporters in an interview with Sean Hannity of Fox News and on the "Ruthless" podcast. It was broadcast after Trump, who seems certain to seek a return to the Oval Office in 2024, was beginning to talk tough about potential primary opponents. In an interview with Yahoo News, he warned Florida Gov. Ron DeSantis about challenging him for the 2024 nomination. "If I faced him, I'd beat him like I would beat everyone else," said Trump.</p>
        <p>"Everyone else" seems to include Pence, who, as he travels from one primary state to another, shows every sign of making a serious bid for the presidency himself. He has a new political organization, aided by a panel of big-name advisers, and he recently convened a retreat for donors in Jackson Hole, Wyoming. According to Axios, he is aiming to raise $18 million by year's end. Add the work Pence is doing to help follow Republicans across the country and he's obviously trying to make his long-held dreams of the presidency come true.</p>
        """

    return render_template('annotate.html', data=data)

@app.route("/update", methods=['POST'])
def update():
    if request.method == 'POST':
        data = eval(request.form["data"])
    return jsonify({"status": True, "data":data })


@app.route("/confirm_extraction", methods=['POST'])
def confirm_extraction():
    if request.method == 'POST':
        data = eval(request.form["data"])
    return jsonify({"status": True, "data":data })

@app.route("/NER/<int:report_id>", methods=['GET' ])
def NER(report_id):
    report = Report.query.filter_by(id=report_id).first_or_404()
    original_file = 'flask_NER/static/'+report.file_directory

    soup = BeautifulSoup(open(original_file, 'r'), 'html.parser')
    body = soup.body
    body = soup.find('body')
    children_count = len(body.contents)

    while(children_count == 1):
        body = body.contents[0]
        children_count = len(body.contents)
    data = str(body)

    def paginate_document(document,children_count):

        if(document.find("pagination__item")== -1):
            # <title>a-20201031</title></head><body>
            start_body = document.find("<body")
            start_body_index = document.find(">",start_body)+1
            # </body></html>
            end_body_index = document.find("</body>",start_body_index )
            if(document.find("pagination__list")== -1):
                if(children_count>1):
                    # add whole div for pagination
                    whole_div = "<div id=\"pagination-1\" class=\"pagination__list\"><div class=\"pagination__item\">"
                    document = document[:start_body_index]+ whole_div +document[start_body_index:end_body_index]+"</div></div></body>"
                else:
                    sub_start = document.find(">",start_body_index)+1
                    whole_div = "<div id=\"pagination-1\" class=\"pagination__list\"><div class=\"pagination__item\">"
                    document = document[:sub_start]+ whole_div +document[sub_start:end_body_index]+"</div></div></body>"
            
            # replace horizontal line by page-break
            break_page = "<hr style=\"page-break-after: always\" />"
            break_page_2 = "<hr style=\"page-break-after:always\"/>"
            break_page_3 = "<hr style=\"page-break-after:always\"></hr>"
            replace_paginate = "</div><div class=\"pagination__item\">"

            document = document.replace(break_page,replace_paginate)
            document = document.replace(break_page_2,replace_paginate)
            document = document.replace(break_page_3,replace_paginate)
        return document
    
    data = paginate_document(data,children_count)

    return render_template('NER.html',report=report, original_file=original_file,data=data,type='NER')

@app.route("/confirm_NER",methods=['POST'])
def confirm_NER():
    if request.method == 'POST':
        data = eval(request.form["data"])
        # create json file
        original_file = data["original_file"]
        report_id = data["report_id"]
        folder_dir = original_file.split(".")[0]
        file_directory = folder_dir+"_latest_NER.json"
        json_object = json.dumps(data,indent=4)
        with open(file_directory,"w") as outfile:
            outfile.write(json_object)
        # store the file directory to database
        json_file_num = JSON_file.query.filter_by(original_fileID=report_id,category=2).count()
        if json_file_num == 0:
            json_file = JSON_file(original_fileID=report_id,file_directory=file_directory,category=2)
            db.session.add(json_file)
        else:
            json_file = JSON_file.query.filter_by(original_fileID=report_id,category=2).first_or_404()
            json_file.file_directory = file_directory
        db.session.commit()
    return jsonify({"status": True, "data":data })

@app.route("/get_latest_NER",methods=["POST"])
def get_latest_NER():
    if request.method == 'POST':
        data = eval(request.form['data'])
        report_id = data['report_id']
        # if doesnt have latest, return the original file 
        json_file_num = JSON_file.query.filter_by(original_fileID=report_id,category=2).count()
        if json_file_num != 0:
            json_file = JSON_file.query.filter_by(original_fileID=report_id,category=2).first_or_404()
            file_directory = json_file.file_directory
            f = open(file_directory)
            data = json.load(f)
            return jsonify({"status": True, "data":data })
    return jsonify({"status": False })

@app.route("/get_original_NER",methods=["POST"])
def get_original_NER():
   
    def condense_newline(text):
        return '\n'.join([p for p in re.split('\n|\r', text) if len(p) > 0])
    def parse_html(html_path):
        # Text extraction with boilerpy3
        html_extractor = extractors.ArticleExtractor()
        return condense_newline(html_extractor.get_content_from_file(html_path))
    # create random color
    def getRandomColor(): 
        letters = '0123456789ABCDEF'
        color = '#'
        for i in range(6):
            color += letters[int(random() * 16)]
        return color

    if request.method == 'POST':
        data = eval(request.form['data'])
        content_page = data['content']
        doc = nlp(content_page)

        ent_color_dict = dict()
        text_label_JSON = {}
        text_label_JSON["res"]=[]

        for ent in doc.ents:
            if(ent.text.isnumeric()):
                continue
            if((ent.label_ =="CARDINAL") or (ent.label_ == "ORDINAL") or(ent.label_=="NORP")):
                continue
            # text_item = " "+ent.text+" "
            text_item = ent.text
            if(ent.label_ not in ent_color_dict):
                ent_color_dict[ent.label_] = getRandomColor()
            json_object = {}
            json_object["content"] = text_item
            json_object["tag"] = ent.label_
            json_object["color"] = ent_color_dict[ent.label_]
            text_label_JSON["res"].append(json_object)

        data = text_label_JSON
        return jsonify({"status": True, "data":data })
    return jsonify({"status": False })   

@app.route("/info_extraction/<int:report_id>")
def info_extraction(report_id):
    report = Report.query.filter_by(id=report_id).first_or_404()
    original_file = 'flask_NER/static/'+report.file_directory
    f=codecs.open(original_file, 'r')
    data= f.read()
    return render_template('info_extraction.html',report=report, original_file=original_file,data=data,type='info_extraction')

@app.route("/confirm_info_extraction",methods=['POST'])
def confirm_info_extraction():
    if request.method == 'POST':
        data = eval(request.form["data"])
        # create json file
        original_file = data["original_file"]
        report_id = data["report_id"]
        folder_dir = original_file.split(".")[0]
        file_directory = folder_dir+"_latest_info_extraction.json"
        json_object = json.dumps(data,indent=4)
        with open(file_directory,"w") as outfile:
            outfile.write(json_object)
        # store the file directory to database
        json_file_num = JSON_file.query.filter_by(original_fileID=report_id,category=4).count()
        if json_file_num == 0:
            json_file = JSON_file(original_fileID=report_id,file_directory=file_directory,category=4)
            db.session.add(json_file)
        else:
            json_file = JSON_file.query.filter_by(original_fileID=report_id,category=4).first_or_404()
            json_file.file_directory = file_directory
        db.session.commit()
    return jsonify({"status": True, "data":data })

@app.route("/get_latest_info_extraction",methods=["POST"])
def get_latest_info_extraction():
    if request.method == 'POST':
        data = eval(request.form['data'])
        report_id = data['report_id']
        # if doesnt have latest, return the original file 
        json_file_num = JSON_file.query.filter_by(original_fileID=report_id,category=4).count()
        if json_file_num != 0:
            json_file = JSON_file.query.filter_by(original_fileID=report_id,category=4).first_or_404()
            file_directory = json_file.file_directory
            f = open(file_directory)
            data = json.load(f)
            return jsonify({"status": True, "data":data })
    return jsonify({"status": False })

@app.route("/get_original_info_extraction",methods=["POST"])
def get_original_info_extraction():
    if request.method == 'POST':
        data = eval(request.form['data'])
        return jsonify({"status": True, "data":data })
    return jsonify({"status": False })  
    
@app.route("/print_backend",methods=["POST"])
def print_backend():
    if request.method == 'POST':
        data = eval(request.form['data'])
        print(data)
    return jsonify({"status": False })



