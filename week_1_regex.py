import glob
import os
import re
import graphviz

os.chdir("course-02242-examples-main")


def visualize(data): #(node,item) -> str
    '''
        data: key: node, item: list of dependencies of *node*

    '''
    dot = graphviz.Digraph(comment='Dependencies')
    for node,deps in data.items():
        for dep in deps:
            dot.node(dep)
            dot.edge(node,dep)
    print(dot.source)
    dot.render('Graph')
    return

#Golden standard -> glob.glob("**/*.txt", recursive=True)

def filter(code):
    '''
        code: string that is Java like code
        returns a string that contains the code but without multiline comments or inline comments
    '''
    temp = re.sub('/\*([^*]|[\r\n]|(\*+([^*/]|[\r\n])))*\*+/','', code)
    return re.sub('//.*','', temp)

files = glob.glob("**/*.java", recursive=True)
print(files)


#read the names of all classes 
folders_classes_dict={}
potentialClasses = []
for pF in files:
    file_path = pF.split('\\')
    file = (file_path[-1].split(".java")[0])
    potentialClasses.append(file)
    try:
        folder = file_path[-2]
    except:
        folder = "course-02242-examples-main"

    if folders_classes_dict.get(folder) is None:
        folders_classes_dict[folder] = [file]
    else:
        folders_classes_dict[folder].append(file)
    



# we are going through files to find imports and than checking if it is used
#this takes the clean code and return the list of dependenices
def imports(cleancode):
    dependencies_list = []
    matches = re.finditer('import( )+(\w.*);',cleancode)
    for match in matches:
        if not match is None:
            dep = match.group(2).split(".")
            if dep[-1] == "*":
                #find all dependencies_list from dep - 2
                folder_name = dep[-2]
                foler_classes = folders_classes_dict [folder_name]
                for file in foler_classes:
                    dependencies_list.append(file)
            else:
                dependencies_list.append(dep[-1])
    return dependencies_list

def get_dependencies_2(file):
    code = open(file).read()
    deps = []
    clean_code = filter(code)
    matches = re.findall('( |\(|\.)([A-Z_]([A-Z_]|[\w_])*)', clean_code)
    for _,m,_ in matches:
        if m != file.split('\\')[-1].split('.java')[0]:
            deps.append(m)

    return list(set(deps))



#https://www.geeksforgeeks.org/python-intersection-two-lists/
def intersection(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return lst3

# visualize(folders_classes_dict)

dependencies = {}
for i,file in enumerate(files):
    foler_of_a_file = file.split('\\')[-2]
    dependencies[potentialClasses[i]] = imports(filter(open(file).read()))
    #we add files in the same folder as dependencies as well
    for file_in_current_folder in folders_classes_dict[foler_of_a_file]:
        if potentialClasses[i] != file_in_current_folder:
            dependencies[potentialClasses[i]].append(file_in_current_folder)
    #we call the finction that givs us the list of all used Class names in the file
    get_dependencies_2_list = get_dependencies_2(file)
    # visualize(get_dependencies_2_list)


    # print(file)
    # print(get_dependencies_2_list)
    # dep_of_file = intersection(get_dependencies_2_list, dependencies[potentialClasses[i]])
    # dependencies[potentialClasses[i]] = dep_of_file
    dependencies[potentialClasses[i]] = get_dependencies_2_list
    
    



visualize(dependencies)


# print(potentialClasses)

# def ttt(cleancode):
#     matches = re.findall('([a-z][a-z_0-9]*\.)*[A-Z_]($[A-Z_]|[\w_])*', cleancode)
#     return matches

#  random : ([a-z][a-z_0-9]*\.)*[A-Z_]($[A-Z_]|[\w_])*  (all classes kinda)