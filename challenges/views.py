from django.shortcuts import render, resolve_url
from django.http import Http404, HttpResponseNotFound, HttpResponseRedirect
# allows to build paths, by extracting the path by name and injecting arguments
from django.urls import reverse

error_codes = {
    "invalid_argument": "<h1>Invalid month</h1>",
    "not_supported": "<h1>This month is not supported</h1>"
}

monthly_challanges = {
    "january": "This is January",
    "february": "This is February",
    "march": "This is Merch",
    "april": "This is April",
    "may": "This is May",
    "june": "This is June",
    "july": None
}


def index(request):
    list_items = ""
    months = list(monthly_challanges.keys())

    return render(request, "challenges/index.html", {
        "months": months
    })

    # the old way:
    for month in months:
        capitalized_month = month.capitalize()
        month_path = reverse("month-challange", args=[month])
        list_items += f"<li><a href=\"{month_path}\">{capitalized_month}</a></li>"

    response_data = f"<ul>{list_items}</ul>"
    return HttpResponse(response_data)


def monthly_challenge_by_number(request, month):
    months = list(monthly_challanges.keys())
    if month < 1 or month > len(months):
        return HttpResponseNotFound(error_codes["invalid_argument"])

    redirect_month = months[month-1]
    redirect_path = reverse("month-challange", args=[redirect_month])
    return HttpResponseRedirect(redirect_path)


def monthly_challenge(request, month):
    try:
        challange_text = monthly_challanges[month]
        # response_data = render_to_string("challenges/challenge.html")
        # return HttpResponse(response_data)
        # or just:
        return render(request, "challenges/challenge.html", {
            "month_name": month,
            # this allows to inject the new contentn to the html in the template
            "challenge_text": challange_text
        })
    except:
        # by using Http404, it will automatically look for 404.html template file
        # however, it will not work proparly if there is "DEBUG = True" set in the setting.py
        raise Http404() 
