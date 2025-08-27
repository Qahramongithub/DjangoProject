# views.py
import json
import logging

import telebot
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Hikvision

logger = logging.getLogger(__name__)
TOKEN = ""
bot = telebot.TeleBot(TOKEN)


class HikEventView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, format=None):
        json_string = None
        for k, v in request.data.items():
            if k != "Picture" and "eventType" in str(v):
                json_string = v
                break

        if not json_string:
            return Response(
                {"error": "No valid event JSON found."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            event_data = json.loads(json_string)
        except Exception as e:
            return Response({"error": f"Invalid JSON: {e}"}, status=status.HTTP_400_BAD_REQUEST)

        device_id = event_data.get("deviceID")
        logger.info(f"Device ID: {device_id}")

        # Qurilma DBdan topiladi
        hikvision_device = Hikvision.objects.filter(devise_id=device_id).first()
        if not hikvision_device:
            logger.warning(f"Unknown device ID: {device_id}")
            return Response({"error": "Unknown device"}, status=status.HTTP_403_FORBIDDEN)

        # Qurilmaga tegishli company
        company = hikvision_device.company
        if not company.telegram_id:
            logger.error(f"Company {company} uchun telegram_id mavjud emas")
            return Response({"error": "No Telegram ID for company"}, status=status.HTTP_400_BAD_REQUEST)

        access_event = event_data.get("AccessControllerEvent", {})
        full_name = access_event.get("name", "Unknown")
        attendance_status = access_event.get("attendanceStatus", "UNKNOWN")
        time = event_data.get("dateTime", "")
        image = event_data.get("image", "")
        txt = (
            f"🏢 Kompaniya: {company.name}\n"
            f"🔑 Qurilma: {device_id}\n"
            f"👤 Xodim: {full_name}\n"
            f"📌 Status: {attendance_status}\n"
            f"📅 Sana: {time}\n"
        )

        try:
            bot.send_photo(int(company.telegram_id), image,txt)
        except Exception as e:
            logger.error(f"Telegramga yuborishda xato: {e}")
            return Response({"error": "Telegram error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({"status": "ok"}, status=status.HTTP_200_OK)
