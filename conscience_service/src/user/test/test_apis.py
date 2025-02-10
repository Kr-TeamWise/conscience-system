from django.test import TestCase
from user.api import router
from ninja.testing import TestAsyncClient
from user.models import User
from mansung_settings.models import Region, District


class TestUser(TestCase):
    def setUp(self):
        self.client = TestAsyncClient(router)
        self.region = Region.objects.create(name="서울", is_active=True)
        self.district = District.objects.create(
            name="강남구", is_active=True, region=self.region
        )
        self.user = User.objects.create_user(
            username="test1",
            password="password1234!",
            status=User.UserStatusChoice.admin,
            terms_of_service=True,
            privacy_policy_agreement=True,
            company_name="test",
            region=self.region,
            district=self.district,
        )

    async def authenticate(self):
        data = {
            "username": self.user.username,
            "password": self.user.password,
        }
        response = await self.client.post("/login", json=data)
        data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertIn("access_token", response.json())
        self.assertIn("refresh_token", response.json())
        return {
            "Authorization": f"Bearer {data['access_token']}",
        }

    async def test_signup(self):
        data = {
            "username": "test2",
            "password": "password1234!",
            "password_confirm": "password1234!",
            "region_id": self.region.id,
            "district_id": self.district.id,
            "company_name": "company2",
            "terms_of_service": True,
            "privacy_policy_agreement": True,
        }
        response = await self.client.post("/signup", json=data)
        data = response.json()
        print(data)
        self.assertEqual(response.status_code, 200)

    async def test_signup_fail_duplicate(self):
        """회원가입 실패 테스트: 이미 등록된 아이디"""
        data = {
            "username": self.user.username,
            "password": "password1234!",
            "password_confirm": "password1234!",
            "region_id": self.region.id,
            "district_id": self.district.id,
            "company_name": "company3",
            "terms_of_service": True,
            "privacy_policy_agreement": True,
        }
        response = await self.client.post("/signup", json=data)
        self.assertEqual(response.status_code, 420)

    async def test_login_success(self):
        data = {
            "username": self.user.username,
            "password": self.user.password,
        }
        response = await self.client.post("/login", json=data)
        data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertIn("access_token", response.json())
        self.assertIn("refresh_token", response.json())

    async def test_get_me(self):
        headers = await self.authenticate()
        response = await self.client.get("/me", headers=headers)
        data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["username"], self.user.username)
        self.assertEqual(data["status"], self.user.status)
        self.assertEqual(data["region"]["id"], self.region.id)
        self.assertEqual(data["district"]["id"], self.district.id)
        self.assertEqual(data["company_name"], self.user.company_name)

    async def test_update_me(self):
        headers = await self.authenticate()
        data = {
            "real_name": "realname",
            "phone": "01012345678",
            "memo": "testmemo",
        }
        response = await self.client.patch(
            f"/{self.user.id}", json=data, headers=headers
        )
        data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["real_name"], "realname")
        self.assertEqual(data["phone"], "01012345678")
        self.assertEqual(data["memo"], "testmemo")
