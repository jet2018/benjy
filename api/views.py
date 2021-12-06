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
        fb = []
        wp = []
        tw = []
        sn = []
        inst = []
        reddit = []
        for a in data:
            all_data = data[a]

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
            eachUser.append(
                {"name": all_data["fullname"], "username": all_data["username"], "fb": sum(fb), "wp": sum(wp), "tw": sum(tw), "reddit": sum(reddit), "inst": sum(inst), 'sn': sum(sn)})

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

        context['usages'] = usage
        context['Students'] = eachUser
        return context


@api_view(['GET'])
def data_to_json(request):
    get_data = requests.get(
        'https://devicemonitor-2e4ba-default-rtdb.firebaseio.com/users.json')
    data = get_data.json()
    fb = []
    wp = []
    tw = []
    sn = []
    inst = []
    reddit = []
    for a in data:
        all_data = data[a]

        for b in all_data["usagedata"]:
            if b["faceboook"] and b["faceboook"] != "0":
                fb.append(round(int(b["faceboook"])/60000))
            if b["whatsapp"] and b["whatsapp"] != "0":
                wp.append(round(int(b["whatsapp"])/60000))
            if b["twitter"] and b["twitter"] != "0":
                tw.append(round(int(b["twitter"])/60000))
            if b["snapchat"] and b["snapchat"] != "0":
                sn.append(round(int(b["snapchat"])/60000))
            if b["instagram"] and b["instagram"] != "0":
                inst.append(round(int(b["instagram"])/60000))
            if b['reddit'] and b['reddit'] != "0":
                reddit.append(round(int(b['reddit'])/60000))
    fb_sum = sum(fb)
    wp_sum = sum(wp)
    tw_sum = sum(tw)
    sn_sum = sum(sn)
    inst_sum = sum(inst)
    reddit_sum = sum(reddit)
    usage = []
    usage.append({"facebook": fb_sum, "whatsapp": wp_sum, "twitter": tw_sum,
                  "instagram": inst_sum, "reddit": reddit_sum, "snapchat": sn_sum})
    return JsonResponse(usage, safe=False)


@api_view(['GET'])
def data_to_json_by_user(request, username):
    get_data = requests.get(
        'https://devicemonitor-2e4ba-default-rtdb.firebaseio.com/users.json')
    data = get_data.json()
    user_data = data['{}'.format(username)]
    fb = []
    wp = []
    tw = []
    sn = []
    inst = []
    dat = []
    reddit = []

    for dt in user_data['usagedata']:
        if dt['day']:
            dat.append(int(dt['day']))
        if dt['faceboook']:
            fb.append(round(int(dt["faceboook"])/60000))
        if dt['whatsapp']:
            wp.append(round(int(dt["whatsapp"])/60000))
        if dt['twitter']:
            tw.append(round(int(dt["twitter"])/60000))
        if dt['snapchat']:
            sn.append(round(int(dt["snapchat"])/60000))
        if dt['instagram']:
            inst.append(round(int(dt["instagram"])/60000))
        if dt['reddit']:
            reddit.append(round(int(dt["reddit"])/60000))
    fb_sum = sum(fb)
    wp_sum = sum(wp)
    tw_sum = sum(tw)
    sn_sum = sum(sn)
    inst_sum = sum(inst)
    reddit_sum = sum(reddit)
    usage = []
    usage.append({"facebook": fb_sum, "whatsapp": wp_sum, "twitter": tw_sum,
                  "instagram": inst_sum, "reddit": reddit_sum, "snapchat": sn_sum})
    all_usages = {"usages": usage, "facebook": fb, "whatsapp": wp,
                  "twitter": tw, "instagram": inst, "reddit": reddit, "snapchat": sn, "days": dat}
    return JsonResponse(all_usages, safe=False)


class SingleUserView(TemplateView):
    template_name = "single.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        username = self.kwargs['username']
        get_data = requests.get(
            'https://devicemonitor-2e4ba-default-rtdb.firebaseio.com/users.json')
        data = get_data.json()
        user_data = data['{}'.format(username)]
        context['user_data'] = user_data
        context['daily_usage'] = user_data['usagedata']
        return context
