from django.conf import settings
from django.core.paginator import InvalidPage, Paginator
from django.http import Http404
from django.template.response import TemplateResponse
from django.utils.translation import gettext as _


def paginate(
    request,
    queryset,
    page_size=settings.DEFAULT_PAGE_SIZE,
    param="page",
    allow_empty=True,
    orphans=0,
):

    paginator = Paginator(
        queryset, page_size, allow_empty_first_page=allow_empty, orphans=orphans
    )
    try:
        return paginator.page(int(request.GET.get(param, 1)))
    except (ValueError, InvalidPage):
        raise Http404(_("Invalid page"))


def render_paginated_response(
    request,
    queryset,
    template_name,
    pagination_template_name,
    extra_context=None,
    **pagination_kwargs,
):
    page_obj = paginate(request, queryset, **pagination_kwargs)
    context = {
        "page_obj": page_obj,
        "pagination_template": pagination_template_name,
        **(extra_context or {}),
    }
    if request.htmx and request.htmx.target == f"page-{page_obj.number}":
        template_name = pagination_template_name
        context["is_paginated"] = True

    return TemplateResponse(request, template_name, context)
