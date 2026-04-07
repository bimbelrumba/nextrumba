import frappe


def get_context(context):
    context.no_cache = 1
    context.title = f"404 - {frappe._('Page Not Found')}"
    context.metatags = {
        "robots": "noindex, nofollow",
        "description": frappe._("The requested page could not be found."),
    }
    return context
