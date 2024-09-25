from django.contrib import admin
from .models import Customer,AdminUser,Ticket,Categories,feedback,lostandfound,TicketInfo_telegram,LostAndFound_telegram,ReportFound_telegram,Feedback_telegram

admin.site.register(Customer)
admin.site.register(AdminUser)
admin.site.register(Ticket)
admin.site.register(Categories)
admin.site.register(feedback)
admin.site.register(lostandfound)
admin.site.register(TicketInfo_telegram)
admin.site.register(LostAndFound_telegram)
admin.site.register(ReportFound_telegram)
admin.site.register(Feedback_telegram)