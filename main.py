from flask import Flask, request
import json

app = Flask(__name__)

def readDataFile() -> list:
  with open("data.json", "r", encoding="utf-8") as file:
    data = json.load(file)
  return data 


def updateDataFile(data: list) -> None:
  with open("data.json", "w", encoding="utf-8") as file:
    json.dump(data, file)


@app.route("/")
def start():
  try:
    return {
      "message": "Server running."
    }
  except Exception as e:
    return {
      "message": f"Error trying to start the server.",
      "error": f"{e}"
    }


@app.route("/alunos", methods=["GET"])
def readStudents():
  try:
    return readDataFile()
  except Exception as e:
    return {
      "message": f"Error trying to fetch the data.",
      "error": f"{e}"
    }


@app.route("/alunos/<int:id>", methods=["GET"])
def readStudentById(id):
  try:
    data = readDataFile()

    for aluno in data:
      if aluno["id"] == id:
        return aluno
    
    return {
      "message": f"Nenhum aluno com o ID {id} foi encontrado."
    }
  except Exception as e:
    return {
      "message": f"Error trying to fetch the data.",
      "error": f"{e}"
    }


@app.route("/alunos", methods=["POST"])
def createStudent():
  try:
    body = request.get_json()
    database = readDataFile()

    database.append(body)
    updateDataFile(database)

    return database
  except Exception as e:
    return {
      "message": f"Error trying to create new data.",
      "error": f"{e}"
    }


@app.route("/alunos/<int:id>", methods=["PUT"])
def updateStudentById(id):
  try:
    body = request.get_json()
    data = readDataFile()

    for aluno in data:
      if aluno["id"] == id:
        aluno.update(body)
        updateDataFile(data)

        return aluno

    return {
      "message": f"Nenhum aluno com o ID {id} foi encontrado."
    }
  except Exception as e:
    return {
      "message": f"Error trying to update the data.",
      "error": f"{e}"
    }


@app.route("/alunos/<int:id>", methods=["DELETE"])
def deleteStudentById(id):
  try:
    data = readDataFile()
    newData = []

    for aluno in data:
      if aluno["id"] != id:
        newData.append(aluno)

    updateDataFile(newData)
    
    return {
      "message": f"Aluno com ID {id} deletado com sucesso."
    }
  except Exception as e:
    return {
      "message": f"Error trying to delete the data.",
      "error": f"{e}"
    }

if __name__ == "__main__":
  app.run(debug=True)