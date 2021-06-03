import tkinter as tk
from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter import font as tkfont
from tkinter.ttk import *
from tkinter import messagebox
from lxml import etree
import xml.etree.ElementTree as ET
import rdflib
from rdflib import *
from rdflib import Namespace



class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("RDF app")
        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, Depart_data, Triples,  Choose, Prof, St, Dept, Lec):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage") #indicates which is the 1st page

    def show_frame(self, page_name):
        #Show a frame for the given page name
        frame = self.frames[page_name]
        frame.tkraise()


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(background='white')
        helv36 = tkfont.Font(family='Helvetica', size=13)
        global n
        #the namespace we use on our default file(erwthma3.rdf)
        n = Namespace("http://www.mydomain.org/uni-ns/")



        label = tk.Label(self, text="Welcome!",
                         font=controller.title_font, background='white')
        label.pack(side="top", fill="x", pady=10)
        opt1 = tk.Button(self, text="Show Department data", font=helv36, background='white', command=lambda: controller.show_frame("Depart_data"))
        opt1.pack(pady=35, padx=35)

        opt2 = tk.Button(self, text="Add new data", font=helv36, background='white', command=lambda: controller.show_frame("Choose"))
        opt2.pack(padx=200, pady=40)


        opt3 = tk.Button(self, text="Show triples", font=helv36,background='white', command=lambda: controller.show_frame("Triples"))
        opt3.pack(pady=30, padx=15)


class Triples(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(background='white')
        helv36 = tkfont.Font(family='Helvetica', size=13)
        label = tk.Label(self, text="Insert URI:",
                         font=controller.title_font, background='white')
        label.pack(side="top", fill="x", pady=10)
        eee = StringVar()
        E1 = Entry(self, textvariable=eee)
        E1.place(x=200, y=70)

        def show_triples(x):
            #x being the URI given by user
            #def is in comments, error occurs on Resource validation. That's PyCharm's problem NOT THE CODE'S ITSELF
            #presumably, this code prints on the console all the triples in the graph that inclde the URI given by the user

            '''
            g = rdflib.Graph()

            g.parse("erwthma3.rdf")

            k = Resource(g, URIRef(x.get()))

            for s, p in k.subject_predicates():
                print(s.value(RDF.type).qname())
                print(p.qname())
                for s, o in p.subject_objects():
                    print(s.value(RDF.type).qname())
                    print(o.value(RDF.type).qname())


'''

        b1=tk.Button(self, text="show", font=helv36, background='white', command=lambda: show_triples(eee))
        b1.place(x=200,y=150)

class Depart_data(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(background='white')
        helv36 = tkfont.Font(family='Helvetica', size=13)
        label = tk.Label(self, text="Choose department:",
                         font=controller.title_font, background='white')
        label.pack(side="top", fill="x", pady=10)
        #load rdf file
        g = rdflib.Graph()
        g.parse("erwthma3.rdf")
        #SPARQL query that takes all department names
        qres = g.query(
            """PREFIX uni: <http://www.mydomain.org/uni-ns/>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        SELECT ?depart 
        WHERE {?Department uni:dep_name ?depart
        }

        """)
        options = []
        #store all department names found from SPARQL query in options array
        for r in qres:
            options.append(r)
        chosenData = StringVar(self)
        chosenData.set(options[0])  # default value
        dropdown = OptionMenu(self, chosenData, *options)  # creates a dropdown list with all the departments
        dropdown.place(x=200, y=70)

        def show_data(x):
            #x is the given department from the user
            s=str(x.get())
            #strip the string from unnessesary punctuation created by SPARQL query
            #we dont strip the commas, cuz we need them for our string to be in SPARQL syntax
            s = s.replace(',','')
            s = s.replace('(', '')
            s = s.replace(')','')
            #create the required SPARQL query
            qres1 = g.query(
                """PREFIX uni: <http://www.mydomain.org/uni-ns/>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            SELECT $name ?age ?phone
            WHERE {?Person uni:has_name ?name.
            ?Person uni:has_age ?age.
            ?Person uni:has_phone ?phone.
            ?Person uni:member_of ?depart.
            FILTER(?depart=""" +s+ """)
            }
            """)

            print("Ονοματεπώνυμο | Ηλικια | Τηλέφωνο")

            #Print the data from the query
            for row in qres1:
                print("%s   %s  %s" % row)



        b1 = tk.Button(self, text="Show data", font=helv36, background='white', command=lambda: show_data(chosenData))
        b1.place(x=200, y=150)

class Choose(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(background='white')
        helv36 = tkfont.Font(family='Helvetica', size=13)
        label = tk.Label(self, text="Choose type of data you want to add:",
                         font=controller.title_font, background='white')
        label.place(x=30, y=10)
        options = ["Professor", "Student", "Department", "Lecture"]
        chosenData = StringVar(self)
        chosenData.set(options[0])  # default value
        dropdown = OptionMenu(self, chosenData, *options)  # creates a dropdown list with all the data
        dropdown.place(x=200, y=70)
        #redirects you to the corresponding window to insert the data, based on what you chose from the dropdown list
        def move_to(x):
            if(str(x.get()) == "Professor"):
                controller.show_frame("Prof")
            if (str(x.get()) == "Student"):
                controller.show_frame("St")
            if (str(x.get()) == "Department"):
                controller.show_frame("Dept")
            if (str(x.get()) == "Lecture"):
                controller.show_frame("Lec")
        b1 = tk.Button(self, text="Next", font=helv36,background='white',command=lambda:move_to(chosenData))
        b1.place(x=215, y=150)





class Prof(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(background='white')
        helv36 = tkfont.Font(family='Helvetica', size=13)
        label = tk.Label(self, text="Professor:",
                         font=controller.title_font, background='white')
        label.place(x=200, y=10)
        label = tk.Label(self, text="ID(for RDF initialization):",
                         font=controller.title_font, background='white')
        label.place(x=30, y=50)
        profID = StringVar()
        E1 = Entry(self, textvariable=profID).place(x=320, y=60)
        label = tk.Label(self, text="Name:",
                         font=controller.title_font, background='white')
        label.place(x=30, y=100)
        profName = StringVar()
        E2 = Entry(self, textvariable=profName).place(x=195, y=110)
        label = tk.Label(self, text="Phone:",
                         font=controller.title_font, background='white')
        label.place(x=30, y=150)
        profPhone = StringVar()
        E3 = Entry(self, textvariable=profPhone).place(x=195, y=160)
        label = tk.Label(self, text="Age:",
                         font=controller.title_font, background='white')
        label.place(x=30, y=200)
        profAge = StringVar()
        E4 = Entry(self, textvariable=profAge).place(x=195, y=210)
        label = tk.Label(self, text="Member_of(department):",
                         font=controller.title_font, background='white')
        label.place(x=30, y=250)
        profDep = StringVar()
        E5 = Entry(self, textvariable=profDep).place(x=320, y=260)
        label = tk.Label(self, text="teaches(lecture):",
                         font=controller.title_font, background='white')
        label.place(x=30, y=300)
        profLec = StringVar()
        E6 = Entry(self, textvariable=profLec).place(x=320, y=310)

        def insert_data(x,y,z,w,q,v):
            #x is ID, y is name, z is phone, w is age, q is dep, v is lecture
            currID = x.get()
            currname = y.get()
            currphone = z.get()
            currage = w.get()
            currdep = q.get()
            currclassroom = v.get()
            temp = open("erwthma3.rdf")
            #registering the prefix and namespaces to avoid the default namespace prefixes(like ns0 ns1 etc.)
            ET.register_namespace('rdf', 'http://www.w3.org/1999/02/22-rdf-syntax-ns#')
            ET.register_namespace('rdfs', 'http://www.w3.org/2000/01/rdf-schema#')
            ET.register_namespace('uni', 'http://www.mydomain.org/uni-ns/')
            tree = ET.parse(temp)
            root = tree.getroot()
            description_elem = ET.Element("rdf:Description", {"rdf:about": n + currID})
            type_elem = ET.Element("rdf:type", {"rdf:resource": n + "Professor"})
            name_elem = ET.Element("uni:has_name")
            name_elem.text = currname
            phone_elem = ET.Element("uni:has_phone")
            phone_elem.text = currphone
            age_elem = ET.Element("uni:has_age")
            age_elem.text = currage
            dept_elem = ET.Element("uni:member_of")
            dept_elem.text = currdep
            lec_elem = ET.Element("uni:teaches")
            lec_elem.text = currclassroom
            description_elem.append(type_elem) #append data to the parent
            description_elem.append(name_elem)
            description_elem.append(phone_elem)
            description_elem.append(age_elem)
            description_elem.append(dept_elem)
            description_elem.append(lec_elem)
            root.append(description_elem) #append to root node
            temp.close()
            tree.write("erwthma3.rdf") #write new data at the end of the file


        submit = tk.Button(self, text="Submit data", font=helv36, background='white',
                           command=lambda: insert_data(profID,profName,profPhone,profAge, profDep,profLec))
        submit.place(x=200,y=340)





class St(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(background='white')
        helv36 = tkfont.Font(family='Helvetica', size=13)
        label = tk.Label(self, text="Student:",
                         font=controller.title_font, background='white')
        label.place(x=200, y=10)

        label = tk.Label(self, text="ID(for RDF initialization):",
                         font=controller.title_font, background='white')
        label.place(x=30, y=50)
        profID = StringVar()
        E1 = Entry(self, textvariable=profID).place(x=320, y=60)
        label = tk.Label(self, text="Name:",
                         font=controller.title_font, background='white')
        label.place(x=30, y=100)
        profName = StringVar()
        E2 = Entry(self, textvariable=profName).place(x=195, y=110)
        label = tk.Label(self, text="Phone:",
                         font=controller.title_font, background='white')
        label.place(x=30, y=150)
        profPhone = StringVar()
        E3 = Entry(self, textvariable=profPhone).place(x=195, y=160)
        label = tk.Label(self, text="Age:",
                         font=controller.title_font, background='white')
        label.place(x=30, y=200)
        profAge = StringVar()
        E4 = Entry(self, textvariable=profAge).place(x=195, y=210)
        label = tk.Label(self, text="Member_of(department):",
                         font=controller.title_font, background='white')
        label.place(x=30, y=250)
        profDep = StringVar()
        E5 = Entry(self, textvariable=profDep).place(x=320, y=260)


        def insert_data(x, y, z, w, q):
            # x is ID, y is name, z is phone, w is age, q is dep
            currID = x.get()
            currname = y.get()
            currphone = z.get()
            currage = w.get()
            currdep = q.get()

            temp = open("erwthma3.rdf")
            ET.register_namespace('rdf', 'http://www.w3.org/1999/02/22-rdf-syntax-ns#')
            ET.register_namespace('rdfs', 'http://www.w3.org/2000/01/rdf-schema#')
            ET.register_namespace('uni', 'http://www.mydomain.org/uni-ns/')
            tree = ET.parse(temp)
            root = tree.getroot()
            description_elem = ET.Element("rdf:Description", {"rdf:about": n + currID})
            type_elem = ET.Element("rdf:type", {"rdf:resource": n + "Student"})
            name_elem = ET.Element("uni:has_name")
            name_elem.text = currname
            phone_elem = ET.Element("uni:has_phone")
            phone_elem.text = currphone
            age_elem = ET.Element("uni:has_age")
            age_elem.text = currage
            dept_elem = ET.Element("uni:member_of")
            dept_elem.text = currdep
            description_elem.append(type_elem)
            description_elem.append(name_elem)
            description_elem.append(phone_elem)
            description_elem.append(age_elem)
            description_elem.append(dept_elem)
            root.append(description_elem)
            temp.close()
            tree.write("erwthma3.rdf")

        submit = tk.Button(self, text="Submit data", font=helv36, background='white',
                           command=lambda: insert_data(profID, profName, profPhone, profAge, profDep))
        submit.place(x=200, y=300)



class Dept(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(background='white')
        helv36 = tkfont.Font(family='Helvetica', size=13)
        label = tk.Label(self, text="Department:",
                         font=controller.title_font, background='white')
        label.place(x=200, y=10)

        label = tk.Label(self, text="ID(for RDF initialization):",
                         font=controller.title_font, background='white')
        label.place(x=30, y=50)
        profID = StringVar()
        E1 = Entry(self, textvariable=profID).place(x=320, y=60)
        label = tk.Label(self, text="Name:",
                         font=controller.title_font, background='white')
        label.place(x=30, y=100)
        profName = StringVar()
        E2 = Entry(self, textvariable=profName).place(x=195, y=110)
        label = tk.Label(self, text="City:",
                         font=controller.title_font, background='white')
        label.place(x=30, y=150)
        profPhone = StringVar()
        E3 = Entry(self, textvariable=profPhone).place(x=195, y=160)


        def insert_data(x, y, z):
            # x is ID, y is name, z is city
            currID = x.get()
            currname = y.get()
            currphone = z.get()


            temp = open("erwthma3.rdf")
            ET.register_namespace('rdf', 'http://www.w3.org/1999/02/22-rdf-syntax-ns#')
            ET.register_namespace('rdfs', 'http://www.w3.org/2000/01/rdf-schema#')
            ET.register_namespace('uni', 'http://www.mydomain.org/uni-ns/')
            tree = ET.parse(temp)
            root = tree.getroot()
            description_elem = ET.Element("rdf:Description", {"rdf:about": n + currID})
            type_elem = ET.Element("rdf:type", {"rdf:resource": n + "Department"})
            name_elem = ET.Element("uni:dep_name")
            name_elem.text = currname
            phone_elem = ET.Element("uni:dep_city")
            phone_elem.text = currphone
            description_elem.append(type_elem)
            description_elem.append(name_elem)
            description_elem.append(phone_elem)
            root.append(description_elem)
            temp.close()
            tree.write("erwthma3.rdf")

        submit = tk.Button(self, text="Submit data", font=helv36, background='white',
                           command=lambda: insert_data(profID, profName, profPhone))
        submit.place(x=200, y=300)

class Lec(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(background='white')
        helv36 = tkfont.Font(family='Helvetica', size=13)
        label = tk.Label(self, text="Lecture:",
                         font=controller.title_font, background='white')
        label.place(x=200, y=10)

        label = tk.Label(self, text="ID(for RDF initialization):",
                         font=controller.title_font, background='white')
        label.place(x=30, y=50)
        profID = StringVar()
        E1 = Entry(self, textvariable=profID).place(x=320, y=60)
        label = tk.Label(self, text="Name:",
                         font=controller.title_font, background='white')
        label.place(x=30, y=100)
        profName = StringVar()
        E2 = Entry(self, textvariable=profName).place(x=195, y=110)
        label = tk.Label(self, text="taught by:",
                         font=controller.title_font, background='white')
        label.place(x=30, y=150)
        profPhone = StringVar()
        E3 = Entry(self, textvariable=profPhone).place(x=195, y=160)

        def insert_data(x, y, z):
            # x is ID, y is name, z is teacher
            currID = x.get()
            currname = y.get()
            currphone = z.get()

            temp = open("erwthma3.rdf")
            ET.register_namespace('rdf', 'http://www.w3.org/1999/02/22-rdf-syntax-ns#')
            ET.register_namespace('rdfs', 'http://www.w3.org/2000/01/rdf-schema#')
            ET.register_namespace('uni', 'http://www.mydomain.org/uni-ns/')
            tree = ET.parse(temp)
            root = tree.getroot()
            description_elem = ET.Element("rdf:Description", {"rdf:about": n + currID})
            name_elem = ET.Element("uni:les_name")
            name_elem.text = currname
            phone_elem = ET.Element("uni:taught_by")
            phone_elem.text = currphone
            description_elem.append(name_elem)
            description_elem.append(phone_elem)
            root.append(description_elem)
            temp.close()
            tree.write("erwthma3.rdf")

        submit = tk.Button(self, text="Submit data", font=helv36, background='white',
                           command=lambda: insert_data(profID, profName, profPhone))
        submit.place(x=200, y=300)



if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()