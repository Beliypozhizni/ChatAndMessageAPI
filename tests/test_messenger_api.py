import pytest


@pytest.mark.anyio
async def test_create_chat(client):
    response = await client.post("/api/v1/chats/", json={"title": "Test chat"})
    assert response.status_code == 201, response.text

    data = response.json()
    assert data["id"] > 0
    assert data["title"] == "Test chat"
    assert "created_at" in data


@pytest.mark.anyio
async def test_create_message_and_get_chat_with_limit(client):
    response = await client.post("/api/v1/chats/", json={"title": "Chat with messages"})
    chat_id = response.json()["id"]

    for i in range(3):
        resp = await client.post(
            f"/api/v1/chats/{chat_id}/messages/",
            json={"text": f"m{i}"},
        )
        assert resp.status_code == 201, resp.text

    response = await client.get(
        f"/api/v1/chats/{chat_id}",
        params={"limit": 2},
    )
    assert response.status_code == 200, response.text

    data = response.json()
    assert data["id"] == chat_id
    assert len(data["messages"]) == 2

    created_at_values = [m["created_at"] for m in data["messages"]]
    assert created_at_values == sorted(created_at_values)

    texts = [m["text"] for m in data["messages"]]
    assert texts == ["m1", "m2"]


@pytest.mark.anyio
async def test_limit_constraints(client):
    response = await client.post("/api/v1/chats/", json={"title": "Limit chat"})
    chat_id = response.json()["id"]

    response = await client.get(
        f"/api/v1/chats/{chat_id}",
        params={"limit": 101},
    )
    assert response.status_code == 422


@pytest.mark.anyio
async def test_create_message_for_missing_chat_returns_404(client):
    response = await client.post(
        "/api/v1/chats/999999/messages/",
        json={"text": "hi"},
    )
    assert response.status_code == 404


@pytest.mark.anyio
async def test_delete_chat_cascades_messages(client):
    response = await client.post("/api/v1/chats/", json={"title": "To delete"})
    chat_id = response.json()["id"]

    for i in range(2):
        resp = await client.post(
            f"/api/v1/chats/{chat_id}/messages/",
            json={"text": f"x{i}"},
        )
        assert resp.status_code == 201

    response = await client.delete(f"/api/v1/chats/{chat_id}")
    assert response.status_code == 204, response.text

    response = await client.get(
        f"/api/v1/chats/{chat_id}",
        params={"limit": 20},
    )
    assert response.status_code == 404

    response = await client.post(
        f"/api/v1/chats/{chat_id}/messages/",
        json={"text": "should fail"},
    )
    assert response.status_code == 404
