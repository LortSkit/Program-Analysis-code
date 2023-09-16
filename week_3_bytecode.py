import json
import graphviz
import os
import re
import glob
import graphviz

#os.chdir("course-02242-examples-main")
files = glob.glob("**/*.json", recursive=True)


def get_class_name(obj):
    return '.'.join(obj["name"].split('/'))
 

def get_class_attributes(obj):
    atts = []
    deps = []
    for attribute in obj["fields"]:
        name = attribute["name"]
        access=""
        if "public" in attribute["access"]:
            access = "+"
        elif "private" in attribute["access"] or "public" in attribute['access']:
            access = '-'
        attribute_type = attribute["type"]["kind"]

        attribute_type_name = '.'.join(attribute["type"]["name"].split ("/"))
        if attribute_type == "class":
            deps.append(attribute_type_name)
        atts.append({
            "name" : name,
            "access" : access,
            "type_name": attribute_type_name
        })

    return atts,deps

      

def get_method(obj, name):
    '''
        name: str,
        arguments: [],
        returns: {},
        access: []
    '''
    r = {}
    m = None
    for method in obj['methods']:
        if name == method["name"]:
            if name == "<init>":
                r["name"] = "init"
            else:
                r["name"] = '.'.join(name.split('/'))
            m = method
            break
    
    deps = []
    if m is not None:
        args = []
        for arg in m["params"]:
            temp = arg["type"]
            while "type" in list(temp.keys()):
                temp = temp["type"]
            args.append('.'.join(temp["name"].split('/')))
        r["arguments"] = args
        #deps.append('.'.join(temp["name"].split('/')))

    try:
        r["returns"] = '.'.join(m["returns"]["type"]["name"].split('/'))
    except:
        r["returns"]  = "void"
    

    if "public" in m["access"]:
        r["access"] = "+"
    elif "private" in m["access"] or "public" in m['access']:
        r["access"] = '-'

    try:
        bytecode =  m["code"]["bytecode"]
    except: 
        bytecode = None




    for d in bytecode:
        if d["opr"] == "new":
            deps.append('.'.join(d['class'].split('/')))
        if d["opr"] == "invoke":
            deps.append('.'.join(d["method"]["ref"]["name"].split('/')))
    

    r["dependencies"] = deps
    # print(r)
    return r

# print(get_method(obj,'main'))

def get_class_interfaces(obj):
    interfaces = obj["interfaces"]
    names = []
    for interface in interfaces:
        names.append(get_class_name(interface))
    return names


def get_methods(obj):
    r = []
    for method in obj["methods"]:
        r.append(get_method(obj,method["name"]))
    return r
# print(get_methods(obj))

        
def class_box(obj):
    class_name = get_class_name(obj)
    fields, deps = get_class_attributes(obj)
    methods = get_methods(obj)

    # print(methods)
    dictionary = {"name": class_name, "methods":methods, "fields": fields, "deps": deps}
    return dictionary

def visualize(data): #(node,item) -> str
    '''
        data: list of dicts

    '''
    dot = graphviz.Digraph(comment='wtf')
    for classs in data:
        fields = []
        methods = []
        dependencies = set(list(classs["deps"]))
        #fields
    
        #methods
        for method in classs["methods"]:
            methods.append((method["access"],method["name"],method["returns"]))
            dependencies = set().union(dependencies,method["dependencies"])
        for field in classs["fields"]:
            fields.append((field["name"], field["access"], field["type_name"]))

        # print(fields)
        #make fieldstuff
        fieldstuff = ""
        if len(fields)>0:
            for name, access, type_name in fields:
                fieldstuff += f"{access} {name} : {type_name}\l"

        #make methods
        methodstuff = ""
        if len(methods) > 0:
            for access,name,type in methods:
                methodstuff+=f"{access} {name}() : {type}\l"

        dot.node(classs["name"],shape="record",label="{"+f"{classs['name']}|{fieldstuff}|{methodstuff}"+"}")
        
        print(list())
        dependencies -= {classs["name"]}
        for dep in list(dependencies):
            dot.edge(classs["name"],dep)
    dot.render('Graph')
    print(dependencies)

    return

classes=[]


for file in files:
    f = open(file,'r')
    obj = json.load(f)
    classes.append(class_box(obj))
    # break
visualize(classes)

# # print(get_method(obj,'main').values())

# # print(get_method_arguments(obj, get_method(obj,'main')))

