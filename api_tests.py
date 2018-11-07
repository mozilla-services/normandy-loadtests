import os
from molotov import scenario


@scenario(weight=8)
async def api_endpoint_test(session):
    async with session.get(os.environ["NORMANDY_API_ENDPOINT"]) as resp:
        res = await resp.json()
        assert resp.status == 200
        assert "action-list" in res
        assert "action-signed" in res
        assert "recipe-list" in res
        assert "recipe-signed" in res
        assert "reciperevision-list" in res
        assert "approvalrequest-list" in res
        assert "classify-client" in res


@scenario(weight=7)
async def recipe_endpoint_test(session):
    recipe_endpoint = os.environ["NORMANDY_API_ENDPOINT"] + "recipe/?enabled=true"
    fields = [
        "id",
        "last_updated",
        "name",
        "enabled",
        "is_approved",
        "revision_id",
        "action",
        "arguments",
        "extra_filter_expression",
        "filter_expression",
        "latest_revision_id",
        "approved_revision_id",
        "approval_request",
        "identicon_seed",
    ]
    async with session.get(recipe_endpoint) as resp:
        res = await resp.json()
        assert resp.status == 200
        assert len(res) > 0
        for field in fields:
            assert field in res[0]


@scenario(weight=7)
async def signed_recipe_endpoint_test(session):
    recipe_endpoint = (
        os.environ["NORMANDY_API_ENDPOINT"] + "recipe/signed/?enabled=true"
    )
    signature_fields = ["timestamp", "signature", "x5u", "public_key"]
    recipe_fields = [
        "id",
        "name",
        "revision_id",
        "action",
        "arguments",
        "filter_expression",
    ]
    async with session.get(recipe_endpoint) as resp:
        res = await resp.json()
        assert resp.status == 200
        assert len(res) > 0
        assert "signature" in res[0]
        assert "recipe" in res[0]

        for field in signature_fields:
            assert field in res[0]["signature"]

        for field in recipe_fields:
            assert field in res[0]["recipe"]


@scenario(weight=7)
async def signed_action_endpoint_test(session):
    action_endpoint = os.environ["NORMANDY_API_ENDPOINT"] + "action/signed"
    signature_fields = ["timestamp", "signature", "x5u", "public_key"]
    action_fields = ["name", "implementation_url", "arguments_schema"]
    async with session.get(action_endpoint) as resp:
        res = await resp.json()
        assert resp.status == 200
        assert len(res) > 0
        assert "signature" in res[0]
        assert "action" in res[0]

        for field in signature_fields:
            assert field in res[0]["signature"]

        for field in action_fields:
            assert field in res[0]["action"]


@scenario(weight=7)
async def action_endpoint_test(session):
    action_endpoint = os.environ["NORMANDY_API_ENDPOINT"] + "action"
    arguments_schema_fields = ["$schema", "title", "type", "required", "properties"]
    async with session.get(action_endpoint) as resp:
        res = await resp.json()
        assert resp.status == 200
        assert len(res) > 0
        assert "name" in res[0]
        assert "implementation_url" in res[0]
        assert "arguments_schema" in res[0]

        for field in arguments_schema_fields:
            assert field in res[0]["arguments_schema"]


@scenario(weight=7)
async def recipe_revision_test(session):
    endpoint = os.environ["NORMANDY_API_ENDPOINT"] + "recipe_revision"
    fields = ["id", "date_created", "recipe", "comment", "approval_request"]
    async with session.get(endpoint) as resp:
        res = await resp.json()
        assert resp.status == 200
        assert len(res) > 0

        for field in fields:
            assert field in res[0]


@scenario(weight=7)
async def approval_request_test(session):
    endpoint = os.environ["NORMANDY_API_ENDPOINT"] + "approval_request"
    fields = ["id", "created", "approved", "approver", "comment"]
    async with session.get(endpoint) as resp:
        res = await resp.json()
        assert resp.status == 200
        assert len(res) > 0

        for field in fields:
            assert field in res[0]


@scenario(weight=50)
async def classify_client_test(session):
    classify_client_endpoint = os.environ["NORMANDY_API_ENDPOINT"] + "classify_client"
    async with session.get(classify_client_endpoint) as resp:
        res = await resp.json()
        assert resp.status == 200
        assert "country" in res
        assert "request_time" in res
