from django.shortcuts import render
import markdown
import random

from . import util

def md_to_html(title):
    content = util.get_entry(title)
    mark_downer = markdown.Markdown()
    if content == None:
        return None
    else:
        return mark_downer.convert(content)
    
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    html_content = md_to_html(title)
    if html_content == None:
        return render(request, "encyclopedia/error.html",{
            "message": "this entry does not exist"
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": html_content
        })

def search(request):
    if request.method == "POST":
        entry_search = request.POST['q']
        html_content = md_to_html(entry_search)
        if html_content is not None:
            return render(request, "encyclopedia/entry.html", {
                "title": entry_search,
                "content": html_content
            })
        else:
            all_entries = util.list_entries()
            recommendations=[]
            for entry in all_entries:
                if entry_search.lower() in entry.lower():
                    recommendations.append(entry)
            return render(request, "encyclopedia/search.html", {
                "recommendations": recommendations
            })
                    
def new_page(request):
    if request.method == "GET":
        return render(request, "encyclopedia/new.html")
    else:
        title = request.POST["title"]
        content = request.POST["content"]
        title_exist = util.get_entry(title)
        if title_exist is not None:
            return render(request, "encyclopedia/error.html", {
                "message": "page already exist"
            })
        else:
            util.save_entry(title, content)
            html_content = md_to_html(title)
            return render(request, "encyclopedia/entry.html", {
                "title": title,
                "content": html_content
            })
        
def edit(request):
    if request.method == "POST":
        title = request.POST["entry_title"]
        content = util.get_entry(title)
        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "content": content
        })

def saved_edit(request):
    if request.method == "POST":
        title = request.POST["edit_title"]
        content = request.POST["content"]
        util.save_entry(title, content)
        html_content = md_to_html(title)
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": html_content
        })

def rand(request):
    all_entries = util.list_entries()
    random_entry = random.choice(all_entries)
    html_content = md_to_html(random_entry)
    return render(request, "encyclopedia/entry.html", {
        "title": random_entry,
        "content": html_content
    })



        

