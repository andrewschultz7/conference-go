from django.http import JsonResponse
from common.json import ModelEncoder
import json
from .models import Presentation
from events.models import Conference
from django.views.decorators.http import require_http_methods


class ListPresentationsEncoder(ModelEncoder):
    model = Presentation
    properties = ["title"]

    def get_extra_data(self, o):
        return {"status": o.status.name}


@require_http_methods(["GET", "POST"])
def api_list_presentations(request, conference_id):
    if request.method == "GET":
        presentations = Presentation.objects.filter(conference=conference_id)
        return JsonResponse(
            {"presentations": presentations},
            encoder=ListPresentationsEncoder,
        )
    else:
        content = json.loads(request.body)
        try:
            conference = Conference.objects.get(id=conference_id)
            content["conference"] = conference
        except Conference.DoesNotExist:
            return JsonResponse(
                {"message": "Invalid conference id"},
                status=400,
            )
        presentation = Presentation.create(**content)
        return JsonResponse(
            presentation,
            encoder=PresentationDetailEncoder,
            safe=False,
        )


class PresentationDetailEncoder(ModelEncoder):
    model = Presentation
    properties = [
        "presenter_name",
        "company_name",
        "presenter_email",
        "title",
        "synopsis",
        "created",
    ]


@require_http_methods(["DELETE", "GET", "PUT"])
def api_show_presentation(request, id):
    if request.method == "GET":
        try:
            presentation = Presentation.objects.get(id=id)
            return JsonResponse(
                presentation, encoder=PresentationDetailEncoder, safe=False
            )
        except Presentation.DoesNotExist:
            return JsonResponse(
                {"message": "Invalid presentation id"},
                status=400,
            )
    elif request.method == "DELETE":
        count, _ = Presentation.objects.filter(id=id).delete()
        return JsonResponse({"deleted": count > 0})
    else:
        content = json.loads(request.body)
        try:
            presentation = Presentation.objects.get(id=content["presentation"])
            content["presentation"] = presentation
        except Presentation.DoesNotExist:
            return JsonResponse(
                {"message": "Invalid presentation id"},
                status=400,
            )
        Presentation.objects.filter(id=id).update(**content)
        presentation = Presentation.objects.get(id=id)
        return JsonResponse(
            presentation,
            encoder=PresentationDetailEncoder,
            safe=False,
        )
