import pkg_resources as pkg
import graphviz as gr
from importlib.metadata import requires
import sys
import pip
import locale
def build_edges(graph, path="", parent_package=None):
    assert isinstance(pkg.working_set.by_key, object)
    f = open(path + ".git/logs/HEAD", encoding='utf-8', mode= 'r')
    history = f.readlines()
    branches = ["master"]
    current_branch = 0
    graph.node(branches[0])
    for str in history:
        commit = str.split()
        if parent_package is None:
            commit[1] +='\n' + ' '.join(commit[commit.index("(initial):")+1:])
        elif "checkout:" in commit:
            for tmp in graph.body:
                if commit[0] in tmp:
                    commit[0] = tmp[2:-2]
                    break
        else:
            commit[1] +='\n' + ' '.join(commit[commit.index("commit:")+1:])
            for tmp in graph.body:
                if commit[0] in tmp:
                    commit[0] = tmp[2:-2]
                    break
        if parent_package is None and commit[0]!=commit[1]:
            graph.node(commit[0])
            graph.node(commit[1])
            graph.edge(commit[0], commit[1])
            graph.edge(branches[current_branch], commit[1])
            parent_package = commit[1]
        elif "checkout:" in commit:
            if commit[-1] in branches:
                current_branch = branches.index(commit[-1])
            else:
                branches.append(commit[-1])
                current_branch = len(branches)-1
                graph.node(branches[current_branch])
                graph.edge(branches[current_branch], commit[0])
        else:
            graph.node(commit[1])
            graph.edge(commit[0], commit[1])
            try:
                graph.body.remove("\t"+branches[current_branch]+" -> \"" + commit[0] +"\"\n")
            except ValueError:
                try:
                    graph.body.remove("\t" + branches[current_branch] + " -> " + commit[0] + "\n")
                except ValueError:
                    None
            graph.edge(branches[current_branch], commit[1])
    graph.node("HEAD")
    graph.edge("HEAD",branches[current_branch])
    f.close()

def dmain(path=""):
    dot = gr.Digraph(comment="git graph " + path, format = "png")
    build_edges(dot)
    dot.render("graph/localgit")
locale.setlocale(locale.LC_ALL, 'ru')
dmain()
