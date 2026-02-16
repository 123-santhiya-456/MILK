import os

# Define folder structure
structure = {
    "backend": {
        "app": {
            "api": ["__init__.py", "routes.py", "chat.py"],
            "db": ["__init__.py", "database.py", "crud.py", "init_db.py"],
            "models": ["__init__.py", "milk_model.py", "sensor_data.py"],
            "schemas": ["__init__.py", "milk_schema.py"],
            "services": [
                "__init__.py",
                "quality_score.py",
                "risk_level.py",
                "pricing.py",
                "prediction_service.py",
            ],
            "utils": ["__init__.py", "helpers.py"],
            "": ["main.py", "config.py", "__init__.py"],
        },
        "": [".env", "requirements.txt", "test_db.py", "README.md"],
    },
    "frontend": {},
    "": [".gitignore"],
}


def create_structure(base_path, structure_dict):
    for folder, contents in structure_dict.items():
        if folder != "":
            folder_path = os.path.join(base_path, folder)
            os.makedirs(folder_path, exist_ok=True)
        else:
            folder_path = base_path

        if isinstance(contents, dict):
            create_structure(folder_path, contents)
        elif isinstance(contents, list):
            for file_name in contents:
                file_path = os.path.join(folder_path, file_name)
                with open(file_path, "w") as f:
                    f.write("")  # Create empty file


if __name__ == "__main__":
    create_structure(".", structure)
    print("✅ Project structure created successfully!")
