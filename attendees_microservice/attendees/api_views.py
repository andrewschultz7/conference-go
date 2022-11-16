from django.http import JsonResponse
from common.json import ModelEncoder
from .models import Attendee, ConferenceVO
import json
from django.views.decorators.http import require_http_methods


class ConferenceVODetailEncoder(ModelEncoder):
    model = ConferenceVO
    properties = ["name", "import_href"]


class AttendeesListEncoder(ModelEncoder):
    model = Attendee
    properties = ["name"]


class AttendeeEncoder(ModelEncoder):
    model = Attendee
    properties = [
        "email",
        "name",
        "company_name",
        "created",
        "conference",
    ]
    encoders = {
        "conference": ConferenceVODetailEncoder(),
    }


@require_http_methods(["GET", "POST"])
def api_list_attendees(request, conference_vo_id=None):
    if request.method == "GET":
        attendees = Attendee.objects.filter(conference=conference_vo_id)
        return JsonResponse(
            {"attendees": attendees},
            encoder=AttendeesListEncoder,
        )
    else:
        content = json.loads(request.body)
        try:
            conference_href = f"/api/conferences/{conference_vo_id}/"
            conference = ConferenceVO.objects.get(import_href=conference_href)
            content["conference"] = conference
        except ConferenceVO.DoesNotExist:
            return JsonResponse(
                {"message": "Invalid conference id"},
                status=400,
            )

        attendee = Attendee.objects.create(**content)
        return JsonResponse(
            attendee,
            encoder=AttendeeEncoder,
            safe=False,
        )


@require_http_methods(["DELETE", "GET", "PUT"])
def api_show_attendee(request, id):
    if request.method == "GET":
        try:
            attendee = Attendee.objects.get(id=id)
        except Attendee.DoesNotExist:
            return JsonResponse(
                {"message": "Invalid attendee id"},
                status=400,
            )
        return JsonResponse(
            attendee,
            encoder=AttendeeEncoder,
            safe=False,
        )
    elif request.method == "DELETE":
        count, _ = Attendee.objects.filter(id=id).delete()
        return JsonResponse({"delete": count > 0})

    else:
        content = json.loads(request.body)
        Attendee.objects.filter(id=id).update(**content)
        attendee = Attendee.objects.get(id=id)
        return JsonResponse(
            attendee,
            encoder=AttendeeEncoder,
            safe=False,
        )
