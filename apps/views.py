# views.py
import datetime
import json
import logging

import telebot
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from .filter import get_hikvision, get_employees, get_departments, get_terminal

logger = logging.getLogger(__name__)
TOKEN = ""
bot = telebot.TeleBot(TOKEN)


class HikEventView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [AllowAny]

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
        branch_id = get_hikvision(device_id)
        if not branch_id:
            logger.warning(f"Unknown device ID: {device_id}")
            return Response({"error": "Unknown device"}, status=status.HTTP_403_FORBIDDEN)

        access_event = event_data.get("AccessControllerEvent", {})
        full_name = access_event.get("name", "Unknown")
        attendance_status = access_event.get("attendanceStatus", "UNKNOWN")
        date_time = event_data.get("dateTime", "")
        image = event_data.get("image", "")
        try:
            dt = datetime.datetime.fromisoformat(date_time)
        except ValueError:
            dt = datetime.datetime.strptime(date_time, "%Y-%m-%dT%H:%M:%S%z")

        date = dt.date()
        time = dt.time()
        if full_name:
            department = get_employees(full_name, branch_id=branch_id)
            telegram_id = get_departments(department)
            status_device = get_terminal(device_id)
            if attendance_status == "checkOut" or status_device == "onlyCheckOut":
                txt = (
                    f"🔑 Qurilma: {device_id}\n"
                    f"👤 Xodim: {full_name}\n"
                    f"📌 Status: CHIQISH\n"
                    f"📅 Sana: {date}\n"
                    f"   Vaqt: {time}\n"
                )
            else:
                txt = (
                    f"🔑 Qurilma: {device_id}\n"
                    f"👤 Xodim: {full_name}\n"
                    f"📌 Status: KIRISH\n"
                    f"📅 Sana: {date}\n"
                    f"   Vaqt: {time}\n"
                )
            telegram_id = telegram_id
            print(telegram_id)
            try:
                if telegram_id and image:
                    bot.send_photo(int(telegram_id), photo=image, caption=txt)
                elif telegram_id and not image:
                    bot.send_message(int(telegram_id), text=txt)
                else:
                    print("")
            except Exception as e:
                logger.error(f"Telegramga yuborishda xato: {e}")
                return Response({"error": "Telegram error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return Response({"status": "ok"}, status=status.HTTP_200_OK)
