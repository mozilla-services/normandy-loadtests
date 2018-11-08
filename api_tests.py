import os
from molotov import scenario


@scenario(weight=7)
async def recipe_endpoint_test(session):
    recipe_endpoint = os.environ["NORMANDY_DOMAIN"] + "/api/v1/recipe/?enabled=true/"
    async with session.get(recipe_endpoint) as resp:
        res = await resp.json()
        assert resp.status == 200
        assert len(res) > 0


@scenario(weight=7)
async def signed_recipe_endpoint_test(session):
    signed_recipe_endpoint = (
        os.environ["NORMANDY_DOMAIN"] + "/api/v1/recipe/signed/?enabled=true/"
    )
    async with session.get(signed_recipe_endpoint) as resp:
        res = await resp.json()
        assert resp.status == 200
        assert len(res) > 0


@scenario(weight=7)
async def heartbeat_test(session):
    heartbeat_endpoint = os.environ["NORMANDY_DOMAIN"] + "/__heartbeat__"
    async with session.get(heartbeat_endpoint) as resp:
        res = await resp.json()
        assert resp.status == 200
        assert "status" in res


@scenario(weight=50)
async def classify_client_test(session):
    classify_client_endpoint = (
        os.environ["NORMANDY_DOMAIN"] + "/api/v1/classify_client/"
    )
    async with session.get(classify_client_endpoint) as resp:
        res = await resp.json()
        assert resp.status == 200
        assert "country" in res
        assert "request_time" in res


@scenario(weight=7)
async def implementation_url_tests(session):
    signed_action_endpoint = os.environ["NORMANDY_DOMAIN"] + "/api/v1/action/signed/"
    async with session.get(signed_action_endpoint) as resp:
        res = await resp.json()
        assert resp.status == 200
        count = 0

        while count <= 4 and res[count]["action"]["implementation_url"] is not None:
            implementation_url = res[count]["action"]["implementation_url"]
            async with session.get(implementation_url) as iu_resp:
                iu_res = await iu_resp.text()
                assert iu_resp.status == 200
                assert len(iu_res) > 0
                count = count + 1
