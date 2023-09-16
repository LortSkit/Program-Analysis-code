from tree_sitter import Language, Parser
import os
import re
import glob
import graphviz

FILE = "../languages.so" # the ./ is important
Language.build_library(FILE, ["tree-sitter-java"])

parser = Parser()
parser.set_language(Language(FILE, "java"))

os.chdir("course-02242-examples-main")
files = glob.glob("**/*.java", recursive=True)

exclude = set()
include = set()

def visualize(data): #(node,item) -> str
    '''
        data: key: node, item: list of dependencies of *node*

    '''
    dot = graphviz.Digraph(comment='Dependencies')
    for node, deps in data.items():
        for dep in deps:
            dot.node(str(dep,'utf-8'))
            dot.edge(node,str(dep,'utf-8'))
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

def getTree(filename):
   print(filename)
   with open(filename, "rb") as f:
      tree = parser.parse(f.read())
   global include, exclude
   include = set()
   exclude = set()
   return tree

class SyntaxFold:
   def visit(self, node):
      results = [ self.visit(n) for n in node.children ]
      if hasattr(self, node.type):
         return getattr(self, node.type)(node, results)
      else:
         return self.default(node, results)
         
      
# class Printer(SyntaxFold):
#    def default(self, node, results):
#       print(node)


class ContextSensitive (SyntaxFold) :     
   def type_identifier(self, node, results):
      def ret(ids):
         global include
         include = set().union(include,{node.text})
         if node.text in ids: return set()
         else: 
            return {node.text}
      return ret
   

   def method_invocation(self, node, results):
      def ret(ids):
         if node.text in ids: return set()
         else:
            for word in str(node.child_by_field_name('object').text,'utf-8').split('.'):
               if word[0].isupper():
                  return {bytes(word,'utf-8')}
            return set()
      return ret
   
   def type_parameter(self,node,results):
      def ret(ids):
         global exclude
         exclude = set().union(exclude,{node.text})
         return set()
      return ret

    
   def class_declaration(self, node, results):
      def ret(ids):
         global exclude
         exclude = set().union({node.child_by_field_name('name').text}, exclude)
         # print(exclude)
         return set().union(*[r(ids) for r in results]) 
      return ret
   
   def type_list(self, node, results):
      def ret(ids):
         global exclude
         for child in node.children:
            exclude = set().union({child.text.split(b'<')[0]},exclude)
         return set()
      return ret
   
   def default(self, node, results):
      def ret(ids):
         global exclude, include
         # print(include)
         return set().union(set().union(*[r(ids) for r in results]), include ) - exclude
      return ret


# print(os.listdir())
# tree = getTree()

# print(ContextSensitive().visit(tree.root_node)(set()) - exclude)

potentialClasses = []
for pF in files:
    file_path = pF.split('\\')
    file = (file_path[-1].split(".java")[0])
    potentialClasses.append(file)

dependencies = {}
for i,file in enumerate(files):
   file_path = file.split('\\')[-1]

   tree = getTree(file)
   dependencies[file_path.split('.java')[0]] = (set().union(ContextSensitive().visit(tree.root_node)(set()),include) - exclude)
   print(exclude)
    
   
print(dependencies)
visualize(dependencies)