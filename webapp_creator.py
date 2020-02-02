import os
import base64
from optparse import OptionParser

CSS_CONTENT_ENCODED_B64=b''
JS_CONTENT_ENCODED_B64 = b'dmFyIG1haW49ZnVuY3Rpb24oKXtjb25zb2xlLmxvZygiTG9hZGVkIik7fQptYWluKCk='
HTML_CONTENT_ENCODED_B64 = b'PCFET0NUWVBFIGh0bWw+CjxodG1sPgoJPGhlYWQ+CgkJPHRpdGxlPldlYkFwcDwvdGl0bGU+CgkJPGxpbmsgcmVsPSJzdHlsZXNoZWV0IiBocmVmPSJ7eyB1cmxfZm9yKCdzdGF0aWMnLCBmaWxlbmFtZT0nY3NzL0FQUF9OQU1FLmNzcycpIH19Ij4KCTwvaGVhZD4KPGJvZHk+ICAgICAgICAgICAgICAgIAoJPGgxPldlbGNvbWUgb24gdGhlIG5ldyB3ZWItYXBwPC9oMT4KCTxzY3JpcHQgc3JjPSIge3sgdXJsX2Zvcignc3RhdGljJywgZmlsZW5hbWU9J2pzL0FQUF9OQU1FLmpzJykgfX0iPjwvc2NyaXB0PiAgICAgICAgICAgICAgICAKPC9ib2R5Pgo8L2h0bWw+'
FLASK_APP_CONTENT_ENCODED_B64=b'ZnJvbSBmbGFzayBpbXBvcnQgRmxhc2sscmVuZGVyX3RlbXBsYXRlCgphcHA9Rmxhc2soX19uYW1lX18pCgpAYXBwLnJvdXRlKCIvIikKZGVmIGluZGV4KCk6CglyZXR1cm4gcmVuZGVyX3RlbXBsYXRlKCJBUFBfTkFNRS5odG1sIikKCmlmIF9fbmFtZV9fPT0iX19tYWluX18iOgoJYXBwLnJ1bihkZWJ1Zz1UcnVlKQ=='

def p(a_str,level="info"):
    status="[+]"
    if(level=="error"):
        status="[!]"
    print("%s %s"%(status,a_str))

def decode_b64_content(encoded_string):
    return base64.b64decode(encoded_string).decode("utf8")

def encode_b64_content(content):
    return base64.b64encode(content.encode("utf8"))

def encode_b64_file(f_name):
    try:
        with open(f_name,'r') as f:
            data= f.read()
            print(encode_b64_content(data))
    except:
        print("Nothing to show")
    
class Webapp_creator:

    def __init__(self,name="sample_app"):
        # some basic cover on user input
        self.name = name.lower().replace(" ","").replace("\n","").replace("\t","").replace("../","")
        self.status = 0

    def check_for_existing_dir(self):
        r=True
        if os.path.exists(self.name):
            p("Can't create app named %s, file is existing"%self.name,level="error")
            self.status=1
            r=False
        return r


    def create_folders(self):
        p("Creation folders (templates,static,static/js,statics/css) in %s"%self.name)
        os.makedirs(self.name+"/templates")
        os.makedirs(self.name+"/static/js")
        os.makedirs(self.name+"/static/css")

    def create_file(self,path_and_name,content=""):
        try:
            p("Creation of %s"%path_and_name)
            with open(path_and_name,'w') as f:
                f.write(decode_b64_content(content).replace("APP_NAME",self.name))
        except Exception as e:
            self.status=1
            p("Error during creation of %s"%e,level="error")

    def create_static_css(self):
        path_and_name = self.name+"/static/css/"+self.name+".css"
        content =""
        self.create_file(path_and_name,content)

    def create_static_js(self):
        path_and_name = self.name+"/static/js/"+self.name+".js"
        content =JS_CONTENT_ENCODED_B64

        self.create_file(path_and_name,content)

    def create_html_template(self):
        path_and_name = self.name+"/templates/"+self.name+".html"
        content =HTML_CONTENT_ENCODED_B64

        self.create_file(path_and_name,content)  

    def create_flask_file(self):
        path_and_name = self.name+"/views.py"
        content =FLASK_APP_CONTENT_ENCODED_B64

        self.create_file(path_and_name,content)
 
    def create_files(self):
        self.create_static_js()
        self.create_static_css()
        self.create_html_template()
        self.create_flask_file()

    def main(self):
        if self.check_for_existing_dir():
            self.create_folders()
            self.create_files()


if __name__ =="__main__":
    APP_NAME ="sample_app"
    # options parsing
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option("-n", "--name",default=APP_NAME,dest="appname",help="Name of your app")

    (options, args) = parser.parse_args()
    APP_NAME = options.appname
    # end options parsing

    app=Webapp_creator(APP_NAME)
    app.main()
    print("[+] Done with status : %d"%app.status)
    exit(app.status)