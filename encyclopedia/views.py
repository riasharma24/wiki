from django.shortcuts import render
from django.http import HttpResponse
from . import util
import markdown
import random


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def convert_md_to_html(entry):
    content = util.get_entry(entry)
    markdowner = markdown.Markdown()
    if content == None:
        return None
    else:
        return markdowner.convert(content)




def display(request, entry):
    md_content=util.get_entry(entry)
    if md_content is None:
        return render(request, 'encyclopedia/invalid.html',{
            'entry':entry
        })
    else:
        html_content=convert_md_to_html(entry)
        return render(request, 'encyclopedia/display.html',{
            'content': html_content,
            'entry':entry
        })



def random_page(request):
    random_entry=random.choice(util.list_entries())
    return render(request, 'encyclopedia/display.html',{
        'entry':random_entry,
        'content': convert_md_to_html(random_entry)
    })



def search(request):
    if request.method=='POST':
        entry=request.POST['q']
        html_content=convert_md_to_html(entry)
        if html_content is not None:
            return render(request, 'encyclopedia/display.html',{
                'content': html_content,
                'entry':entry
            })
        else:
            total = util.list_entries()
            matched=[]
            for total_entry in total:
                if entry.lower() in total_entry.lower():
                    matched.append(total_entry)
            return render(request, 'encyclopedia/search.html',{
                'entry_list':matched
            })


def new(request):
    if request.method=='GET':
        return render(request, 'encyclopedia/new.html')
    
    if request.method=='POST':
        entry_name=request.POST['new_entry']
        md_content=request.POST['content']
        if util.get_entry(entry_name) is not None:
            return render(request, 'encyclopedia/exists.html',{
                'entry':entry_name
            })
        else:
            util.save_entry(entry_name,md_content)
            return render(request, 'encyclopedia/display.html',{
                'entry':entry_name,
                'content':convert_md_to_html(entry_name)
            })
        

def edit(request):
    if request.method=='POST':
        entry=request.POST['entry']
        md_content=util.get_entry(entry)
        if md_content is not None:
            return render(request, 'encyclopedia/edit.html',{
                'entry':entry,
                'content':md_content
            })
        

def save_changes(request):
    if request.method=='POST':
        entry=request.POST['entry']
        content=request.POST['content']
        util.save_entry(entry,content)
        html_content=convert_md_to_html(entry)
        return render(request, 'encyclopedia/display.html',{
            'entry':entry,
            'content':html_content
        })