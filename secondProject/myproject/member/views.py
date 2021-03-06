import json
from json.decoder import JSONDecodeError

from django.http import JsonResponse
from django.views.generic import View

from .models import Member


class MemberView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            name = data['name']
            age = data['age']
            if Member.objects.filter(name=name).exists():
                return JsonResponse({'message': '이미 해당 이메일의 회원이 있습니다'}, status=409)

            Member(name=name, age=age).save()

            return JsonResponse({'message': '회원 생성 성공'}, status=200)

        except JSONDecodeError:
            return JsonResponse({'message': 'JSON_DECODE_ERROR'}, status=400)
        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)


class ListMemberView(View):
    def get(self, request):
        if request.method == 'GET':
            members = Member.objects.all()

            result = [{
                'id': member.pk,
                'name': member.name,
                'age': member.age
            } for member in members]

            return JsonResponse({'data': result}, status=200)


class DetailMemberView(View):
    def get(self, request, member_id):
        try:
            member = Member.objects.get(pk=member_id)

            result = {'id': member.pk, 'name': member.name, 'age': member.age}

            return JsonResponse({'data': result}, status=200)
        except Member.DoesNotExist:
            return JsonResponse({'message': '해당 아이디의 회원이 없습니다'}, status=404)

    def patch(self, request, member_id):
        try:
            member = Member.objects.get(pk=member_id)

            data = json.loads(request.body)
            name = data['name']
            age = data['age']

            if Member.objects.filter(name=name).exists():
                return JsonResponse({'message': '이미 해당 이메일의 회원이 있습니다'}, status=409)

            member.name = name
            member.age = age
            member.save()

            return JsonResponse({'message': '회원 업데이트 성공'}, status=200)

        except Member.DoesNotExist:
            return JsonResponse({'message': '해당 아이디의 회원이 없습니다'}, status=404)
        except JSONDecodeError:
            return JsonResponse({'message': 'JSON_DECODE_ERROR'}, status=400)
        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)

    def delete(self, request, member_id):
        try:
            member = Member.objects.get(pk=member_id)
            member.delete()
            return JsonResponse({'message': '회원 삭제 완료'}, status=200)
        except Member.DoesNotExist:
            return JsonResponse({'message': '해당 아이디의 회원이 없습니다'}, status=404)
