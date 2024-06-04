from django.shortcuts import render, redirect
from django.http import HttpResponse
from . import util
from markdown2 import Markdown
from random import randint


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    entry = util.get_entry(title)
    if entry != None:
        markdowner = Markdown()
        out_entry = markdowner.convert(f"{entry}")
        return render(request, "encyclopedia/entry.html", {
            "entry": out_entry,
            "title": title,
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "entry": f"{title} Page not found",
            "title": "404 Error"
        })

def search(request):
    if request.method == "POST":
        query = request.POST.get('q').strip()
        all_entries = util.list_entries()
        matching_entries = [
            entry for entry in all_entries if query.lower() in entry.lower()]

        if query in [entry for entry in matching_entries]:
            # Exact match found, redirect to entry page
            return redirect('encyclopedia:entry', title=query)
        else:
            # No exact match, show search results
            return render(request, "encyclopedia/search.html", {
                "query": query,
                "results": matching_entries
            })
def new_page(request):
    if request.method=="POST":
        title = request.POST.get('title')
        content = request.POST.get('content')
        if not title or not content:
            return render(request, "encyclopedia/new_page.html", {
                "error": "Title and content must not be empty.",
                "title": title,
                "content": content
            })
        if util.get_entry(title):
            return render(request, "encyclopedia/new_page.html",{
                "error": "An entry with this title alredy exists.",
                "title": "",
                "content": content
            })
        util.save_entry(title, content)
        return redirect('encyclopedia:entry', title=title)
    return render(request, "encyclopedia/new_page.html")

def edit(request, title):
    content = util.get_entry(title.strip())
    if content is None:
        return render(request,"encyclopedia/edit.html",{
            "error":"404 Not Found!"
        })
    if request.method == "POST":
        content = request.POST.get("content").strip()
        if content == "":
            return render(request, "encyclopedia/edit.html", {
               "message":"Can not save with empty field content!",
                "title":title,
                "content":content
            })
        util.save_entry(title, content)
        return redirect('encyclopedia:entry', title=title)
    return render(request, "encyclopedia/edit.html", {
        "content": content,
        "title": title})

def random(request):
    entries = util.list_entries()
    random_title = entries[randint(0, len(entries)-1)]
    return redirect("encyclopedia:entry", title=random_title)

