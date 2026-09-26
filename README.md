# 🏥 MVP2 — Patient Backend

Backend REST responsável pelo **cadastro, consulta, atualização e remoção de pacientes** do sistema de gestão de saúde.

Este serviço faz parte de uma arquitetura composta por:

* [**Frontend** — interface web (docker-composer)](https://github.com/maloisio/mvp2-healthcare-frontend)
* [**BFF (Backend for Frontend)** — API GraphQL que centraliza as requisições do frontend](https://github.com/maloisio/mvp2-bff)
* [**Patient Backend** — gerenciamento de pacientes](https://github.com/maloisio/mvp2-patient-backend)
* [**Scheduling Backend** — gerenciamento de consultas](https://github.com/maloisio/mvp2-scheduling-backend)

---

## 📌 Responsabilidade

O Patient Backend é responsável pelos dados dos pacientes.

Entre suas principais funcionalidades estão:

* Cadastrar pacientes
* Consultar um paciente
* Listar pacientes
* Atualizar pacientes
* Remover pacientes
* Integrar com o Scheduling Backend para remover as consultas relacionadas a um paciente antes de sua exclusão





# ️ 🚀 Como executar

### As instruções de como executar estão no diretório do projeto mvp2-healthcare-frontend
# 🏗️ Arquitetura

```text
┌─────────────────────┐
│      Frontend       │
│   HTML / CSS / JS   │
└──────────┬──────────┘
           │
           │ GraphQL
           ▼
┌─────────────────────┐ REST  ┌─────────┐    
│         BFF         │◄─────►│  ViaCEP │ 
│ Flask + Ariadne     │       │         │ 
└──────────┬──────────┘       └─────────┘
           │
           ├──────────────────────────┐
           │                          │
           │ REST                     │ REST
           ▼                          ▼
┌─────────────────────┐      ┌─────────────────────┐
│   Patient Backend   │◄────►│ Scheduling Backend  │
│      Flask          │      │       Flask         │
└─────────────────────┘      └─────────────────────┘
           │                          │
           ▼                          ▼

```

O frontend **não acessa diretamente os backends REST**.

A comunicação principal da aplicação ocorre da seguinte maneira:

```text
Frontend
   │
   │ GraphQL
   ▼
 BFF
   │
   ├── REST ──► Patient Backend
   │
   └── REST ──► Scheduling Backend
```

Além disso, os dois backends possuem comunicação interna por meio de seus respectivos **clients**.

---

# 🔄 Comunicação com o BFF

O BFF funciona como intermediário entre o frontend e os serviços REST.

Por exemplo, quando o frontend solicita a lista de pacientes:

```text
Frontend
   │
   │ Query GraphQL
   ▼
BFF
   │
   │ GET /patients
   ▼
Patient Backend
```

O BFF possui um `patient_service.py` responsável por realizar essas chamadas.

Exemplo:

```python
response = requests.get(
    f"{PATIENT_BACKEND_URL}/patients",
    timeout=5
)
```



---

# 🔗 Comunicação com Scheduling Backend

Além do BFF, existe uma comunicação direta entre os dois backends.

Essa comunicação acontece por meio de **clients**.

A ideia é evitar que um backend conheça diretamente a implementação interna do outro.

Por exemplo:

```text
Patient Backend
      │
      │ scheduling_client.py
      │
      │ HTTP REST
      ▼
Scheduling Backend
```

E no sentido contrário:

```text
Scheduling Backend
      │
      │ patient_client.py
      │
      │ HTTP REST
      ▼
Patient Backend
```



---

# 🐳 Execução com Docker

A aplicação também possui um `Dockerfile`.

A imagem pode ser construída com:

```bash
docker build -t patient-backend .
```

##  Entretanto, no ambiente completo do projeto, o serviço é executado pelo `docker-compose.yml` localizado no repositório principal do [frontend](https://github.com/maloisio/mvp2-healthcare-frontend).




# 📖 OpenAPI

A API possui documentação automática através do Flask-OpenAPI3.

Com o serviço local:

```text
http://localhost:5000/openapi
```

A documentação permite testar os endpoints diretamente pelo navegador.
# 🛠️ Tecnologias

* Python
* Flask
* Flask-OpenAPI3
* Pydantic
* Requests
* SQLAlchemy
* Docker

---



