from django.contrib.auth.models import User, auth
from django.shortcuts import render
from api.serializers import UsageDataSerializer
from rest_framework.decorators import api_view
from rest_framework import generics
from django.http.response import JsonResponse
import requests
from django.views.generic import TemplateView
# Create your views here.
from django.contrib.auth.mixins import LoginRequiredMixin


# from .models import UsageData


class HomePageView(LoginRequiredMixin, TemplateView):
    login_url = '/login/'
    template_name = 'home.html'
    redirect_field_name = 'redirect_to'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        get_data = requests.get(
            'https://devicemonitor-2e4ba-default-rtdb.firebaseio.com/users.json')
        data = get_data.json()
        eachUser = []
        for a in data:
            all_data = data[a]
            fb = []
            wp = []
            tw = []
            sn = []
            inst = []
            reddit = []
            for b in all_data["usagedata"]:
                if b["faceboook"]:
                    fb.append(round(int(b["faceboook"])/60000))
                if b["whatsapp"]:
                    wp.append(round(int(b["whatsapp"])/60000))
                if b["twitter"]:
                    tw.append(round(int(b["twitter"])/60000))
                if b["snapchat"]:
                    sn.append(round(int(b["snapchat"])/60000))
                if b["instagram"]:
                    inst.append(round(int(b["instagram"])/60000))
                if b['reddit']:
                    reddit.append(round(int(b['reddit'])/60000))

            # getting sums
            fb_sum = sum(fb)
            wp_sum = sum(wp)
            tw_sum = sum(tw)
            sn_sum = sum(sn)
            inst_sum = sum(inst)
            reddit_sum = sum(reddit)
            usage = []
            # getting the highest usage
            if fb_sum > wp_sum and fb_sum > tw_sum and fb_sum > sn_sum and fb_sum > inst_sum and fb_sum > reddit_sum:
                usage.append({"usage": fb_sum, "device": "facebook"})
            elif wp_sum > fb_sum and wp_sum > tw_sum and wp_sum > sn_sum and wp_sum > inst_sum and wp_sum > reddit_sum:
                usage.append({"usage": wp_sum, "device": "whatsapp"})
            elif tw_sum > fb_sum and tw_sum > wp_sum and tw_sum > sn_sum and tw_sum > inst_sum and tw_sum > reddit_sum:
                usage.append({"usage": tw_sum, "device": "twitter"})
            elif sn_sum > fb_sum and sn_sum > wp_sum and sn_sum > tw_sum and sn_sum > inst_sum and sn_sum > reddit_sum:
                usage.append({"usage": sn_sum, "device": "snapchat"})
            elif inst_sum > fb_sum and inst_sum > wp_sum and inst_sum > tw_sum and inst_sum > sn_sum and inst_sum > reddit_sum:
                usage.append({"usage": inst_sum, "device": "instagram"})
            elif reddit_sum > fb_sum and reddit_sum > wp_sum and reddit_sum > tw_sum and reddit_sum > sn_sum and reddit_sum > inst_sum:
                usage.append({"usage": reddit_sum, "device": "reddit"})

            eachUser.append(
                {"name": all_data["fullname"], "username": all_data["username"], "fb": sum(fb), "wp": sum(wp), "tw": sum(tw), "reddit": sum(reddit), "inst": sum(inst), 'sn': sum(sn)})

        context['usages'] = usage
        context['Students'] = eachUser
        return context
