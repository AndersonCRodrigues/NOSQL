from fastapi.testclient import TestClient
from fastapi import status
import main 

client = TestClient(main.app)

def test_create_task_success():
    payload = {"title": "Estudar Pytest", "description": "Ler documentação", "completed": False}
    response = client.post("/tasks", json=payload)
    
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["id"] == 1
    assert data["title"] == payload["title"]
    assert data["description"] == payload["description"]
    assert data["completed"] is False

def test_create_task_missing_description():
    payload = {"title": "Apenas título"}
    response = client.post("/tasks", json=payload)
    
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["description"] is None
    assert data["completed"] is False


def test_get_all_tasks_empty():
    response = client.get("/tasks")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []

def test_get_all_tasks_with_items():
    client.post("/tasks", json={"title": "Tarefa 1"})
    client.post("/tasks", json={"title": "Tarefa 2"})
    
    response = client.get("/tasks")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 2
    assert data[0]["title"] == "Tarefa 1"
    assert data[1]["title"] == "Tarefa 2"

def test_get_task_by_id_success():
    client.post("/tasks", json={"title": "Tarefa Alvo"})
    
    response = client.get("/tasks/1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["title"] == "Tarefa Alvo"

def test_get_task_by_id_not_found():
    response = client.get("/tasks/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Tarefa não encontrada"


def test_update_task_success():
    client.post("/tasks", json={"title": "Antigo Título", "description": "Antiga Descrição"})
    
    payload = {"title": "Novo Título", "description": "Nova Descrição", "completed": True}
    response = client.put("/tasks/1", json=payload)
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == 1
    assert data["title"] == "Novo Título"
    assert data["description"] == "Nova Descrição"
    assert data["completed"] is True

def test_update_task_not_found():
    payload = {"title": "Qualquer uma", "completed": False}
    response = client.put("/tasks/999", json=payload)
    
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Tarefa não encontrada"


def test_delete_task_success():
    client.post("/tasks", json={"title": "Deletar-me"})
    
    response = client.delete("/tasks/1")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert response.text == ""
    
    get_response = client.get("/tasks")
    assert len(get_response.json()) == 0

def test_delete_task_not_found():
    response = client.delete("/tasks/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Tarefa não encontrada"